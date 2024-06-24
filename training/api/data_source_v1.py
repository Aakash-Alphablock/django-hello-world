
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from common.authentications import ClerkJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from common.decorators import validate_request_data
from training.api import serializers
from training.private import DataSourceService, SitemapLoader
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import permission_classes, authentication_classes

from common.resource import BaseAPIResource

class DataSourceAPIV1(BaseAPIResource):
    # authentication_classes = [ClerkJWTAuthentication]
    # permission_classes = [IsAuthenticated] #This is to apply authentication to all the methods in the class

    @action(detail=False, methods=['get'], url_path='get-sources')
    @validate_request_data(serializer=serializers.GetSourceSerializer)
    def get_trained_sources(self, request, *args, **kwargs):
        try:
            data = kwargs.get('validated_data')
            data_source_service = DataSourceService()
            get_trained_sources = data_source_service.get_trained_sources(data)
            return self.create_success_response(**get_trained_sources)
        except Exception as e:
            return self.create_error_response(data=f"Error: {str(e)}")

    @action(detail=False, methods=['post'], url_path='set-source')
    @validate_request_data(serializer=serializers.SetSourceSerializer)
    def set_source(self, request, *args, **kwargs):
        try:
            data = kwargs.get('validated_data')
            data_source_service = DataSourceService()
            set_source = data_source_service.set_source(data)
            return self.create_success_response(data=set_source)
        except Exception as e:
            return self.create_error_response(data=f"Error: {str(e)}")

    # @permission_classes([IsAuthenticated])
    # @authentication_classes([ClerkJWTAuthentication])
    @action(detail=False, methods=['post'], url_path='update-source')
    @validate_request_data(serializer=serializers.UpdateSourceSerializer)
    def update_source(self, request, *args, **kwargs):
        try:
            data = kwargs.get('validated_data')
            data_source_service = DataSourceService()
            update_source = data_source_service.update_source(data)
            return self.create_success_response(data=update_source)
        except Exception as e:
            return self.create_error_response(data=f"Error: {str(e)}")
    
    # @permission_classes([IsAuthenticated])
    # @authentication_classes([ClerkJWTAuthentication])
    @action(detail=False, methods=['post'], url_path='delete-source')
    @validate_request_data(serializer=serializers.DeleteSourceSerializer)
    def delete_source(self, request, *args, **kwargs):
        try:
            data = kwargs.get('validated_data')
            data_source_service = DataSourceService()
            delete_source = data_source_service.delete_source(**data)
            return self.create_success_response(data=delete_source)
        except Exception as e:
            return self.create_error_response(data=f"Error: {str(e)}")
    