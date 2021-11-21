from django.conf.urls import url
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path, include
from . import views
from .api import etudiantViewSet


#API ROUTER FOR ENDPOINTS
router = SimpleRouter()
router.register(r'etudiant', etudiantViewSet, basename='Etudiant')

urlpatterns = [
    url(r'api/', include(router.urls)),
    url(r'^$', views.index, name='index')
]
