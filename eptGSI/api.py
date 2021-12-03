from rest_framework.viewsets import ModelViewSet
from .serializers import EtudiantSerializer, MembreSerializer, CompteSerializer, EntrepriseSerializer,ProgrammeSerializer
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
    filter_fields=["niveau_etude"]

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