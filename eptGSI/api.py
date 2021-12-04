from rest_framework.viewsets import ModelViewSet
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Etudiant, Membre, Compte
import django_filters.rest_framework
from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework.decorators import action
from django.http import Http404
from rest_framework import status

#Vues API

class EtudiantViewSet(ModelViewSet):
    serializer_class= EtudiantSerializer
    #permission_classes=(IsAuthenticated,)
    filter_fields=["niveau_etude","membre"]

    def get_queryset(self):
        queryset= Etudiant.objects.all()
    
        etudiant_id = self.request.GET.get('id_etudiant')
        if etudiant_id is not None:
            queryset = queryset.filter(id=etudiant_id)
        return queryset


    def destroy(self, request, *args, **kwargs):
        etudiant=self.get_object()
        Membre.objects.filter(email=etudiant.membre.email).delete()
        Compte.objects.filter(identifiant=etudiant.membre.compte.identifiant).delete()
        etudiant.cv.delete()
        etudiant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



        
class MembreViewSet(ModelViewSet):
    serializer_class= MembreSerializer
    #permission_classes=(IsAuthenticated,)
    filter_fields=["nom","prenom"]

    def get_queryset(self):
        queryset= Membre.objects.all()
    
        membre_id = self.request.GET.get('id_membre')
        if membre_id is not None:
            queryset = queryset.filter(id=membre_id)
        return queryset
    

    def destroy(self, request, *args, **kwargs):
        membre=self.get_object()
        print(membre)
        Compte.objects.filter(identifiant=membre.compte.identifiant).delete()
        membre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CompteViewSet(ModelViewSet):
    serializer_class= CompteSerializer
    #permission_classes=(IsAuthenticated,)
    filter_fields=["identifiant"]

    def get_queryset(self):
        queryset= Compte.objects.all()
    
        compte_id = self.request.GET.get('id_compte')
        if compte_id is not None:
            queryset = queryset.filter(id=compte_id)
        return queryset



class ImmersionViewSet(ModelViewSet):
    serializer_class= ImmersionSerializer
    #permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        queryset= Immersion.objects.all()
    
        immersion_id = self.request.GET.get('id_immersion')
        if immersion_id is not None:
            queryset = queryset.filter(id=immersion_id)
        return queryset
    

    def destroy(self, request, *args, **kwargs):
        immersion=self.get_object()
        Programme.objects.filter(id=immersion.programme.id).delete()
        immersion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class EntrepriseViewSet(ModelViewSet):
    serializer_class= EntrepriseSerializer
    #permission_classes=(IsAuthenticated,)
    filter_fields=["nom_entreprise"]

    def get_queryset(self):
        queryset= Entreprise.objects.all()
    
        entreprise_id = self.request.GET.get('id_entreprise')
        if entreprise_id is not None:
            queryset = queryset.filter(id=entreprise_id)
        return queryset


class ProgrammeViewSet(ModelViewSet):
    serializer_class= ProgrammeSerializer
    #permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        queryset= Programme.objects.all()
    
        programme_id = self.request.GET.get('id_programme')
        if programme_id is not None:
            queryset = queryset.filter(id=programme_id)
        return queryset


class StageViewSet(ModelViewSet):
    serializer_class= StageSerializer
    #permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        queryset= Stage.objects.all()
    
        stage_id = self.request.GET.get('id_stage')
        if stage_id is not None:
            queryset = queryset.filter(id=stage_id)
        return queryset


    def destroy(self, request, *args, **kwargs):
        stage=self.get_object()
        stage.rapport_stage.delete()
        stage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class MaitreStageViewSet(ModelViewSet):
    serializer_class= MaitreStageSerializer
    #permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        queryset= MaitreStage.objects.all()
    
        maitre_stage_id = self.request.GET.get('id_maitre_stage')
        if maitre_stage_id is not None:
            queryset = queryset.filter(id=maitre_stage_id)
        return queryset


class PlanningViewSet(ModelViewSet):
    serializer_class= PlanningSerializer
    #permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        queryset= Planning.objects.all()
    
        planning_id = self.request.GET.get('id_planning')
        if planning_id is not None:
            queryset = queryset.filter(id=planning_id)
        return queryset