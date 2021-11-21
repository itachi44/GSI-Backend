from rest_framework.viewsets import ModelViewSet
from .serializers import EtudiantSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Etudiant
import django_filters.rest_framework
from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated


#return Response(data)
#request.data : Handles arbitrary data.  Works for 'POST', 'PUT' and 'PATCH' methods.
#Tutorial.objects.get(pk=pk) 


#Vues API

#METHODE GET POUR TOUS LES ETUDIANTS 
class etudiantViewSet(ModelViewSet):
    serializer_class= EtudiantSerializer
    #permission_classes=(IsAuthenticated,)
    filter_fields=["niveau_etude"]
    def get_queryset(self):
        queryset= Etudiant.objects.all()
    
        etudiant_id = self.request.GET.get('id_etudiant')
        if etudiant_id is not None:
            queryset = queryset.filter(id=etudiant_id)
        return queryset
