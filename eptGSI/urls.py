from django.conf.urls import url
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path, include
from . import views
from .api import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='GESTION ET SUIVI DES IMMERSIONS : API')
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas

#Les endpoints pour toutes les fonctionnalités
router = SimpleRouter()
router.register(r'stagiaire_pedagogique', StagiairePedagogiqueViewSet, basename='StagiairePedagogique')
router.register(r'membre', MembreViewSet, basename='Membre')
router.register(r'compte', CompteViewSet, basename='Compte')
router.register(r'alternance', AlternanceViewSet, basename='Alternance')
router.register(r'entreprise', EntrepriseViewSet, basename='Entreprise')
router.register(r'planning', PlanningViewSet, basename='Planning')
router.register(r'immersion', ImmersionViewSet, basename='Immersion')
router.register(r'maitre_stage', MaitreStageViewSet, basename='MaitreStage')
router.register(r'projet', ProjetViewSet, basename='Projet')
router.register(r'programme', ProgrammeViewSet, basename='Programme')
router.register(r'activite', ActiviteViewSet, basename='Activite')
router.register(r'tache', TacheViewSet, basename='Tache')
router.register(r'sous_tache', SousTacheViewSet, basename='SousTache')
router.register(r'destinataire', DestinataireViewSet, basename='Destinataire')
router.register(r'evenement', EvenementViewSet, basename='Evenement')
router.register(r'piece_jointe', PieceJointeViewSet, basename='PieceJointe')
router.register(r'formateur', FormateurViewSet, basename='Formateur')
router.register(r'manager', ManagerViewSet, basename='Manager')
router.register(r'responsable_immersion', ResponsableImmersionViewSet, basename='ResponsableImmersion')
router.register(r'message', MessageViewSet, basename='Message')
router.register(r'evaluation', EvaluationViewSet, basename='Evaluation')
router.register(r'grille_evaluation', GrilleEvaluationViewSet, basename='GrilleEvaluation')
router.register(r'critere', CritereViewSet, basename='Critere')
router.register(r'evaluation_partielle', EvaluationPartielleViewSet, basename='EvaluationPartielle')
router.register(r'evaluation_finale', EvaluationFinaleViewSet, basename='EvaluationFinale')
router.register(r'evaluation_apprentissage', EvaluationApprentissageViewSet, basename='EvaluationApprentissage')
router.register(r'conge', CongeViewSet, basename='Conge')


#URIs pour l'Authentification 
router.register(r'login', GetTokenViewSet, basename='Obtain_token')
router.register(r'logout', LogOut, basename='LogOut')
router.register(r'verify_token', VerifyToken, basename='verify_token')


#URIs pour reinitialiser son mot de passe
router.register(r'reset_password', ResetPassword, basename='reset_password')
router.register(r'password_reset_check', PasswordTokenCheck, basename='password_reset_confirm')
router.register(r'password_reset_complete', SetNewPassword, basename='password_reset_complete')


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='GESTION ET SUIVI DES IMMERSIONS : API')
    return response.Response(generator.get_schema(request=request))


urlpatterns = [
    url(r'api/', include(router.urls)),
    url(r'^$', schema_view, name='documentation'), 
]