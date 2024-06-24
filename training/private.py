# all methods/services defined in private are supposed to be used within the bot app/service only.
# never call any of the methods of public in private else later it will cause circular import issue.

from training import dal, constants
from typing import Optional
import requests
from xml.etree import ElementTree as ET
    
import os
from pinecone.grpc import PineconeGRPC as Pinecone
from supabase import create_client, Client

# all methods/services defined in private are supposed to be used within the bot app/service only.
# never call any of the methods of public in private else later it will cause circular import issue.


class DataSourceService():
    
    @staticmethod
    def get_trained_sources(payload):
        category = payload['fileType']
        if(payload['fileType'] == 'docs'):
          category = constants.FILES_AND_URL
        filter_by = {
            "assistant_id":payload['assistant_id'],
            "page": payload['page'] or 1,
            "category": category,
        }
        get_trained_sources =  dal.DataSource.get_trained_sources(filter_by)
        return get_trained_sources
    
    @staticmethod
    def set_source(args):
        trained_sources = dal.DataSource.is_source_trained(args)
        
        if trained_sources.exists():
            first_trained_source = trained_sources.first()
            
            if args['category'] == constants.DataSourceType.URL or constants.DataSourceType.NOTIONPAGES:
                update_url_status = dal.DataSource.update_status(first_trained_source.id, {'status': 'processing'})
                set_source = {**update_url_status.to_dict(), 'next_version': update_url_status.version + 1}
            else:
                new_entry = dal.DataSource.set_source(args)
                set_source = {**new_entry.to_dict(), 'next_version': new_entry.version}
        else:
            new_entry = dal.DataSource.set_source(args)
            set_source = {**new_entry.to_dict(), 'next_version': new_entry.version}

        return set_source
        
    def update_source(self, payload):
        if payload['status'] == constants.SourceStatus.TRAINED and int(payload['version']) != 1:
            trained_source = dal.DataSource.get_source(payload['source_id'])
            self.delete_from_pinecone(payload['source_id'], trained_source['assistant_id'], trained_source['category'], int(payload['version']) - 1)

        new_entry = dal.DataSource.update_status(payload['source_id'],{"status":payload['status'],'version':payload['version']})
        return  new_entry.to_dict(),
    
    def delete_source(self, source_id, assistant_id, fileType, version, supabase_path=""):
        results = [
            self.delete_from_pinecone(source_id, assistant_id, fileType, version),
            dal.DataSource.delete_source(source_id)
        ]

        if fileType in constants.ALLOWED_FILE_TYPES:
            results.append(self.delete_supabase_file(supabase_path))

        has_any_error = any(result is None for result in results)
        if has_any_error:
            error_reasons = [str(result) for result in results if result is None]
            print("error_reasons: {}", error_reasons)
            raise Exception("\n".join(error_reasons))

        return {
                'msg': 'source deleted successfully'
        }
    
    @staticmethod
    def delete_from_pinecone(source_id, namespace, file_type, version):
        try:
            print("delete form pinecone args >>>", source_id, namespace, file_type, version)
            pinecone_service = PineconeService()
            response = pinecone_service.delete_from_pinecone(source_id, f"{namespace}", file_type, version)
            return response
        except Exception as e:
            print(f"Error deleting from Pinecone: {str(e)}")
            raise Exception(f"Failed to delete from Pinecone: {str(e)}")
            
    @staticmethod
    def delete_supabase_file(supabase_path):
        supbase = SupabaseService()
        return supbase.Delete_from_supabase(supabase_path)
    
        
class SitemapLoader():
    def sitemap_urls(self, sitemap_urls):
        all_urls = []
        for sitemap_url in sitemap_urls:
            try:
                urls = self.get_urls_from_sitemap(sitemap_url)
                all_urls.extend(urls)
            except requests.HTTPError as http_err:
                print(f"HTTP error occurred while fetching sitemap {sitemap_url}: {http_err}")
                raise Exception(f"HTTP error occurred while fetching sitemap {sitemap_url}: {http_err}")
            except ConnectionError as conn_err:
                print(f"Connection error occurred while fetching sitemap {sitemap_url}: {conn_err}")
                raise Exception(f"Connection error occurred while fetching sitemap {sitemap_url}: {conn_err}")
            except Exception as e:
                print(f"An error occurred while fetching sitemap {sitemap_url}: {e}")
                raise Exception(f"An error occurred while fetching sitemap {sitemap_url}: {e}")
        return all_urls
    
    def get_urls_from_sitemap(self, url):
        response = requests.get(url)
        response.raise_for_status()
        sitemap_xml = response.text
        urls = self.parse_sitemap(sitemap_xml)
        return urls
    
    def parse_sitemap(self, sitemap_xml):
        urls = []
        root = ET.fromstring(sitemap_xml)
        for elem in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
            loc_elem = elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
            if loc_elem is not None:
                urls.append(loc_elem.text)
        return urls
    
    
class PineconeService:
    def __init__(self):
        self.pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

    def delete_from_pinecone(self, source_id, name_space, file_type, version):
        print("prefix to be deleted>>>>",f"{file_type}#{source_id}#v{version}")
        try:
            if not source_id or not name_space or not file_type or not version:
                raise ValueError(f"field required: nameSpace {name_space} filetype {file_type} sourceId {source_id} version {version}")

            index = self.pc.Index("default")
            def delete_all_pages(file_type, source_id, version, pagination_token=None):
                results = index.list_paginated(
                prefix=f"{file_type}#{source_id}#v{version}",
                   namespace=name_space,
                   pagination_token=pagination_token
                )
              
                print("vectors to be deleted: ", results.vectors)
                vector_ids = [vector.id for vector in results.vectors]
                if vector_ids:
                    index.delete(ids=vector_ids,namespace=name_space)
                if results.pagination and results.pagination.next:
                    delete_all_pages(file_type, source_id, version, results.pagination.next)
                else:
                    print("All pages deleted.")

            delete_all_pages(file_type, source_id, version)
            return {'success': True, 'msg' : 'All vectors deleted'}
        
        except Exception as e:
            print(f"Error: {str(e)}")
            raise ValueError(str(e))


class SupabaseService:
    def __init__(self):
        self.url: str = os.environ.get("SUPABASE_URL")
        self.key: str = os.environ.get("SUPABASE_KEY")
        self.supabase: Client = create_client(self.url, self.key)
        
    def Delete_from_supabase(self, supbase_file_path):
        res = self.supabase.storage.from_(os.environ.get("SUPABASE_BUCKET_NAME")).remove(supbase_file_path)
        return res

