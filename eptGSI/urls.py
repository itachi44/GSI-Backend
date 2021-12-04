from django.conf.urls import url
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path, include
from . import views
from .api import *


#API ROUTER FOR ENDPOINTS
router = SimpleRouter()
router.register(r'etudiant', EtudiantViewSet, basename='Etudiant')
router.register(r'membre', MembreViewSet, basename='Membre')
router.register(r'compte', CompteViewSet, basename='Compte')
router.register(r'immersion', ImmersionViewSet, basename='Immersion')
router.register(r'entreprise', EntrepriseViewSet, basename='Entreprise')
router.register(r'programme', ProgrammeViewSet, basename='Programme')
router.register(r'stage', StageViewSet, basename='Stage')
router.register(r'maitre_stage', MaitreStageViewSet, basename='MaitreStage')
router.register(r'planning', PlanningViewSet, basename='Planning')






urlpatterns = [

    url(r'api/', include(router.urls)),
    url(r'^$', views.index, name='index')
]
