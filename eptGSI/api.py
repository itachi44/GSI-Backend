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



class PlanningViewSet(ModelViewSet):
    serializer_class= PlanningSerializer
    #permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        queryset= Planning.objects.all()
    
        planning_id = self.request.GET.get('id_planning')
        if planning_id is not None:
            queryset = queryset.filter(id=planning_id)
        return queryset

    
class ProjetViewSet(ModelViewSet):
    serializer_class= ProjetSerializer
    #permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        queryset= Projet.objects.all()
    
        projet_id = self.request.GET.get('id_projet')
        if projet_id is not None:
            queryset = queryset.filter(id=projet_id)
        return queryset


class TacheViewSet(ModelViewSet):
    serializer_class= TacheSerializer
    #permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        queryset= Tache.objects.all()
    
        tache_id = self.request.GET.get('id_tache')
        if tache_id is not None:
            queryset = queryset.filter(id=tache_id)
        return queryset


    def destroy(self, request, *args, **kwargs):
        tache=self.get_object()
        SousTache.objects.filter(id=tache.id).delete()
        tache.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SousTacheViewSet(ModelViewSet):
    serializer_class= SousTacheSerializer
    #permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        queryset= SousTache.objects.all()
    
        sous_tache_id = self.request.GET.get('id_sous_tache')
        if sous_tache_id is not None:
            queryset = queryset.filter(id=sous_tache_id)
        return queryset


class DestinataireViewSet(ModelViewSet):
    serializer_class= DestinataireSerializer
    #permission_classes=(IsAuthenticated,)
    filter_fields=["label"]

    def get_queryset(self):
        queryset= Destinataire.objects.all()
    
        destinataire_id = self.request.GET.get('id_desinataire')
        if destinataire_id is not None:
            queryset = queryset.filter(id=destinataire_id)
        return queryset
    

class MembreDeptViewSet(ModelViewSet):
    serializer_class= MembreDeptSerializer
    #permission_classes=(IsAuthenticated,)
    filter_fields=["membre"]

    def get_queryset(self):
        queryset= MembreDept.objects.all()
    
        membreDept_id = self.request.GET.get('id_membreDept')
        if membreDept_id is not None:
            queryset = queryset.filter(id=membreDept_id)
        return queryset


    def destroy(self, request, *args, **kwargs):
        membreDept=self.get_object()
        Membre.objects.filter(email=membreDept.membre.email).delete()
        Compte.objects.filter(identifiant=membreDept.membre.compte.identifiant).delete()
        membreDept.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



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
    filter_fields=["membre"]

    def get_queryset(self):
        queryset= MaitreStage.objects.all()
    
        maitreStage_id = self.request.GET.get('id_maitreStage')
        if maitreStage_id is not None:
            queryset = queryset.filter(id=maitreStage_id)
        return queryset


    def destroy(self, request, *args, **kwargs):
        maitreStage=self.get_object()
        Membre.objects.filter(email=maitreStage.membre.email).delete()
        Compte.objects.filter(identifiant=maitreStage.membre.compte.identifiant).delete()
        maitreStage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class RespEntrepriseViewSet(ModelViewSet):
    serializer_class= RespEntrepriseSerializer
    #permission_classes=(IsAuthenticated,)
    filter_fields=["membre"]

    def get_queryset(self):
        queryset= RespEntreprise.objects.all()
    
        respEntreprise_id = self.request.GET.get('id_respEntreprise')
        if respEntreprise_id is not None:
            queryset = queryset.filter(id=respEntreprise_id)
        return queryset


    def destroy(self, request, *args, **kwargs):
        respEntreprise=self.get_object()
        Membre.objects.filter(email=respEntreprise.membre.email).delete()
        Compte.objects.filter(identifiant=respEntreprise.membre.compte.identifiant).delete()
        respEntreprise.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class ChefDeptViewSet(ModelViewSet):
    serializer_class= ChefDeptSerializer
    #permission_classes=(IsAuthenticated,)
    filter_fields=["membre"]

    def get_queryset(self):
        queryset= ChefDept.objects.all()
    
        chefDept_id = self.request.GET.get('id_chefDept')
        if chefDept_id is not None:
            queryset = queryset.filter(id=chefDept_id)
        return queryset


    def destroy(self, request, *args, **kwargs):
        chefDept=self.get_object()
        Membre.objects.filter(email=chefDept.membre.email).delete()
        Compte.objects.filter(identifiant=chefDept.membre.compte.identifiant).delete()
        chefDept.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageViewSet(ModelViewSet):
    serializer_class= MessageSerializer
    #permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        queryset= Message.objects.all()
    
        message_id = self.request.GET.get('id_message')
        if message_id is not None:
            queryset = queryset.filter(id=message_id)
        return queryset


    def destroy(self, request, *args, **kwargs):
        message=self.get_object()
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class EvaluationViewSet(ModelViewSet):
    serializer_class= EvaluationSerializer
    #permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        queryset= Evaluation.objects.all()
    
        evaluation_id = self.request.GET.get('id_evaluation')
        if evaluation_id is not None:
            queryset = queryset.filter(id=evaluation_id)
        return queryset


    def destroy(self, request, *args, **kwargs):
        evaluation=self.get_object()
        evaluation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class EvenementViewSet(ModelViewSet):
    serializer_class= EvenementSerializer
    #permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        queryset= Evenement.objects.all()
    
        evenement_id = self.request.GET.get('id_evenement')
        if evenement_id is not None:
            queryset = queryset.filter(id=evenement_id)
        return queryset
    
    
    def destroy(self, request, *args, **kwargs):
        evenement=self.get_object()
        evenement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PieceJointeViewSet(ModelViewSet):
    serializer_class= PieceJointeSerializer
    #permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        queryset= PieceJointe.objects.all()
    
        pieceJointe_id = self.request.GET.get('id_pieceJointe')
        if pieceJointe_id is not None:
            queryset = queryset.filter(id=pieceJointe_id)
        return queryset


    def destroy(self, request, *args, **kwargs):
        pieceJointe=self.get_object()
        pieceJointe.fichier.delete()
        pieceJointe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)