from django.urls import path,include

# urls.py
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter


from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from .views import *

from project_app.views  import *

schema_view = get_schema_view(
   openapi.Info(
      title="App API",
      default_version='v1',
      description="API documentation for your project",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# Define the router and register the viewset
router = DefaultRouter()




urlpatterns = [
   path('', include(router.urls)),

   
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]