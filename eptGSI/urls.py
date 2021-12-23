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
router.register(r'tache', TacheViewSet, basename='Tache')
router.register(r'sous_tache', SousTacheViewSet, basename='SousTache')
router.register(r'destinataire', DestinataireViewSet, basename='Destinataire')
router.register(r'membreDept', MembreDeptViewSet, basename='MembreDept')
router.register(r'entreprise', EntrepriseViewSet, basename='Entreprise')
router.register(r'programme', ProgrammeViewSet, basename='Programme')
router.register(r'stage', StageViewSet, basename='Stage')
router.register(r'respEntreprise', RespEntrepriseViewSet, basename='RespEntreprise')
router.register(r'chefDept', ChefDeptViewSet, basename='ChefDept')
router.register(r'message', MessageViewSet, basename='Message')
router.register(r'evenement', EvenementViewSet, basename='Evenement')
router.register(r'pieceJointe', PieceJointeViewSet, basename='PieceJointe')


#URIs pour la connexion et la deconnexion 
router.register(r'login', GetTokenViewSet, basename='Obtain_token')
router.register(r'logout', LogOut, basename='LogOut')
router.register(r'verify_token', VerifyToken, basename='verify_token')

#reset password
router.register(r'reset_password', ResetPassword, basename='reset_password')
router.register(r'password_reset_check', PasswordTokenCheck, basename='password_reset_confirm')
router.register(r'password_reset_complete', SetNewPassword, basename='password_reset_complete')



urlpatterns = [

    url(r'api/', include(router.urls)),
    url(r'^$', views.index, name='index'),
]
