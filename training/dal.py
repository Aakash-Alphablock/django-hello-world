from django.db import IntegrityError
from training import models
from typing import Optional

class DataSource:
    
    @staticmethod
    def set_source(data) -> models.DataSource:
        """Create a new data source.
        
        Args:
            data (dict): Data containing the validated model fields.

        Returns:
            models.DataSource: DataSource model object.

        Raises:
            IntegrityError: If a data source with the same details already exists.
        """
        try:
            return models.DataSource.objects.create(
                assistant_id=data['assistant_id'],
                name=data['name'],
                source_url=data['source_url'],
                category=data['category'],
                provider_type=data['provider_type'],
                extra_info=data.get('extra_info', {}),
                description=data['description'],
                status = data['status']
            )
        except IntegrityError:
            raise IntegrityError("Data source already exists")

    @staticmethod
    def get_source(id: int) -> Optional[models.DataSource]:
        """Get data source details by ID.

        Args:
            bot_id (int): Data source ID.

        Returns:
            models.DataSource: DataSource model object or None if not found.
        """
        return models.DataSource.objects.filter(id=id).values('assistant_id','category','version').first()
    
    
    @staticmethod
    def get_trained_sources(payload):
        """Get trained data sources details by assistant_id, fileType(category).

        Args:
            bot_id (int): Data source ID.

        Returns:
            models.DataSource: DataSource model object or None if not found.
        """
        per_page = 3
        page = payload['page']
        category = payload['category']
        skip = (page - 1) * per_page
        where_condition = {'assistant_id': payload['assistant_id']}
        
        if isinstance(category, str):
            where_condition['category'] = category
        elif isinstance(category, list):
            where_condition['category__in'] = category
 
        total_count = models.DataSource.objects.filter(**where_condition).count()
        total_pages = (total_count + per_page - 1) // per_page 
        trained_sources = models.DataSource.objects.filter(**where_condition).order_by('-updated_at')[skip:skip + per_page]
  
        return {
            'data': list(trained_sources.values()),
            'totalPages': total_pages,
        }

    @staticmethod
    def update_status(source_id, payload):
        """Update the status of a data source.

        Args:
            source_id (int): Data source ID.
            payload (dict): Fields to update.

        Returns:
            models.DataSource: Updated DataSource model object.
        """
        models.DataSource.objects.filter(id=source_id).update(**payload)
        return models.DataSource.objects.get(id=source_id)

    @staticmethod
    def is_source_trained(args):
        """Check if a URL has already been trained.

        Args:
            args (dict): Arguments containing the source URL and bot ID.

        Returns:
            object:
        """        
            # Basic filter conditions
        filter_conditions = {
        'source_url': args['source_url'],
        'assistant_id': args['assistant_id'],
        'category': args['category']
    }
    
    # if page_id is provided in args (notion pages handled)
        if 'pageId' in args['extra_info']:
            filter_conditions['extra_info__pageId'] = args['extra_info']['pageId']
            
        isTrained = models.DataSource.objects.filter(**filter_conditions)
        return isTrained
    
    @staticmethod
    def delete_source(source_id):
        return models.DataSource.objects.filter(id=source_id).delete()

