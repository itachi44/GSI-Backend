from django.conf.urls import url
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path, include
from . import views
from .api import EtudiantViewSet,MembreViewSet,CompteViewSet


#API ROUTER FOR ENDPOINTS
router = SimpleRouter()
router.register(r'etudiant', EtudiantViewSet, basename='Etudiant')
router.register(r'membre', MembreViewSet, basename='Membre')
router.register(r'compte', CompteViewSet, basename='Compte')


urlpatterns = [
    url(r'api/', include(router.urls)),
    url(r'^$', views.index, name='index')
]
