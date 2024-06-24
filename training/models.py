from common.models import BaseModel
from django.db import models

class DataSource(BaseModel):
    assistant_id = models.PositiveBigIntegerField()
    name = models.CharField(max_length=255, )
    source_url = models.CharField(max_length=255,)  # path of source / url,pdf s3 
    category = models.CharField(max_length=255,) #Todo: Change to enum , type filetype url , csv, etc
    provider_type = models.CharField(max_length=255,) #Todo: Change to enum file type url , csv etc
    extra_info = models.JSONField(default={})
    description = models.TextField(help_text='Description of the data source if required')
    version = models.IntegerField(default=1)
    status = models.CharField(max_length=155) # status type [procesing, failed, trained]

    def __str__(self):
        return self.name
    
    def to_dict(self):
        return {
            'id': self.id,
            'assistant_id': self.assistant_id,
            'name': self.name,
            'source_url': self.source_url,
            'category': self.category,
            'provider_type': self.provider_type,
            'extra_info': self.extra_info,
            'description': self.description,
            'version': self.version,
            'status': self.status,
            'updated_at': self.updated_at,
            'created_at': self.created_at,
        }
    
class DataSourceLogs(BaseModel):
    data_source_id = models.PositiveBigIntegerField()
    assistant_id = models.PositiveBigIntegerField()
    name = models.CharField(max_length=255, )
    data_type = models.CharField(max_length=255, default='') # ToDo: Change to enum
    source_url = models.CharField(max_length=255, default='')
    category = models.CharField(max_length=255, default='') #Todo: Change to enum
    provider_type = models.CharField(max_length=255, default='') #Todo: Change to enum
    extra_info = models.JSONField(default={})
    description = models.TextField(default='', help_text='Description of the data source if required')
    status = models.CharField(max_length=255)