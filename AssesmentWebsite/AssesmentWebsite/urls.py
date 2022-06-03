from django.contrib import admin
from django.urls import path, include
import api
from api import views
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from AssesmentWebsite import settings
# Creating Router Object
# router = DefaultRouter()

# Register StudentViewSet with Router
# router.register('demographic', views.DemographicModelViewSet, basename='demographic')
# router.register('expertise', views.ExpertiseModelViewSet, basename='expertise')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)