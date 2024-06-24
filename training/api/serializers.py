# serializers.py
from rest_framework import serializers
from training.models import DataSource

class SetSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = '__all__'
        
class GetSourceSerializer(serializers.Serializer):
    assistant_id = serializers.IntegerField(required=True)
    fileType = serializers.CharField(required=True)
    page = serializers.IntegerField(required=False)
    
class UpdateSourceSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=100)
    version = serializers.IntegerField()
    source_id = serializers.IntegerField()
    
class DeleteSourceSerializer(serializers.Serializer):
    source_id = serializers.IntegerField()
    assistant_id = serializers.IntegerField()
    fileType = serializers.CharField(max_length=255) # url , pdf , csv , notionPages
    version = serializers.IntegerField()
    
class  SitemapSerializer(serializers.Serializer):
    urls = serializers.JSONField(default=[])

# class DataSourceLogsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DataSourceLogs
#         fields = '__all__'
