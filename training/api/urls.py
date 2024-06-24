
from django.urls import path, include
from assistant import views
from training.api.data_source_v1 import DataSourceAPIV1
from training.api.training_source_v1 import TrainingSourceAPIV1
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', DataSourceAPIV1, basename='data_source')
router.register(r'', TrainingSourceAPIV1, basename='training_source')


urlpatterns = [
    path('', include(router.urls))
]
