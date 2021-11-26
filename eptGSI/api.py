from rest_framework.viewsets import ModelViewSet
from .serializers import EtudiantSerializer
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







#return Response(data)
#Tutorial.objects.get(pk=pk) 


#Vues API

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


    def destroy(self, request, *args, **kwargs):
        etudiant=self.get_object()
        Membre.objects.filter(email=etudiant.membre.email).delete()
        Compte.objects.filter(identifiant=etudiant.membre.compte.identifiant).delete()
        etudiant.cv.delete()
        etudiant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



        

    # #mixin pour modifier les informations personnelles de l'étudiant
    # # => detail =True
    # @transaction.atomic
    # @action(detail=True, methods=['put','patch'])
    # def updatePersonalInfos(self, request, pk):
    #     # une transaction atomique car plusieurs requêtes vont être exécutées
    #     # en cas d'erreur, nous retrouverions alors l'état précédent

    #     # récupérons l'étudiant 
    #     etudiant = self.get_object()
    #     # récupération des données 
    #     serializer = EtudiantSerializer(data=request.data)
    #     #validation test
    #     if serializer.is_valid():
    #         data=request.data
    #         print(data)
    #         if data[""]:
    #             etudiant.niveau_etude=data[""]
    #         if data[""]:
    #             etudiant.adresse=data[""]
    #         if data[""]


    #         etudiant.save()
    #         return Response({'status': 'updated'})
    #     else:
    #         return Response(serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)


    #     # Retournons enfin une réponse (status_code=200 par défaut) pour indiquer le succès de l'action
    #     return Response()
