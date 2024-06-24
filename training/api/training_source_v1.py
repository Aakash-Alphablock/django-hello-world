
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from common.authentications import ClerkJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from common.decorators import validate_request_data
from training.api import serializers
from training.private import  SitemapLoader
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import permission_classes, authentication_classes

from common.resource import BaseAPIResource

class TrainingSourceAPIV1(BaseAPIResource):
    # authentication_classes = [ClerkJWTAuthentication]
    # permission_classes = [IsAuthenticated] #This is to apply authentication to all the methods in the class
    
    @action(detail=False, methods=['post'], url_path='get-sitemaps')
    @validate_request_data(serializer=serializers.SitemapSerializer)
    def delete_source(self, request, *args, **kwargs):
        try:
            data = kwargs.get('validated_data')
            sitemap_loader = SitemapLoader()
            sitemap_urls = sitemap_loader.sitemap_urls(data['urls'])
            return self.create_success_response(data=sitemap_urls)
        except Exception as e:
            return self.create_error_response(data=f"Error: {str(e)}")      