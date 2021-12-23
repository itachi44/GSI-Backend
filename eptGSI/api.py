from rest_framework.viewsets import ModelViewSet
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import *
import django_filters.rest_framework
from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework.decorators import action
from django.http import Http404
from rest_framework import status
from .permissions import IsStudentAuthenticated
from django.contrib.auth import authenticate
from .authentication import *
from django.contrib.auth import logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str,force_bytes, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
import os
import time


#les vues de l'API
class StagiairePedagogiqueViewSet(ModelViewSet):
    serializer_class= StagiairePedagogiqueSerializer
    #permission_classes=(IsStudentAuthenticated,)
    filter_fields=["niveau_etude","membre"]


    def get_queryset(self):
        queryset= StagiairePedagogique.objects.all()
        email = self.request.GET.get('email')
        if email is not None:
            queryset = queryset.filter(membre__email=email)
        return queryset


    def destroy(self, request, *args, **kwargs):
        stagiaire_pedagogique=self.get_object()
        Membre.objects.filter(email=stagiaire_pedagogique.membre.email).delete()
        Compte.objects.filter(identifiant=stagiaire_pedagogique.membre.compte.identifiant).delete()
        User.objects.filter(email=stagiaire_pedagogique.membre.email).delete()
        if(stagiaire_pedagogique.cv):
            extension=stagiaire_pedagogique.cv.name.split(".")[1]
            image_id=stagiaire_pedagogique.cv.url.split('/')[5]
            path=os.getcwd()+"/media/cvs"+'/'+image_id+"."+extension
            if os.path.isfile(path):
                os.remove(path)
            stagiaire_pedagogique.cv.delete()
        stagiaire_pedagogique.delete()
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
    
    def destroy(self, request, *args, **kwargs):
        programme=self.get_object()
        programme.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActiviteViewSet(ModelViewSet):
    serializer_class= ActiviteSerializer
    #permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        queryset= Activite.objects.all()
    
        activite_id = self.request.GET.get('id_activite')
        if activite_id is not None:
            queryset = queryset.filter(id=activite_id)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        activite=self.get_object()
        activite.delete()
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


class AlternanceViewSet(ModelViewSet):
    serializer_class= AlternanceSerializer
    #permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        queryset= Alternance.objects.all()
    
        alternance_id = self.request.GET.get('id_alternance')
        if alternance_id is not None:
            queryset = queryset.filter(id=alternance_id)
        return queryset
    

    def destroy(self, request, *args, **kwargs):
        alternance=self.get_object()
        Planning.objects.filter(id=alternance.planning._id).delete()
        if(alternance.convention):
            extension=alternance.convention.name.split(".")[1]
            image_id=alternance.convention.url.split('/')[5]
            path=os.getcwd()+"/media/conventions"+'/'+image_id+"."+extension
            if os.path.isfile(path):
                os.remove(path)
            alternance.convention.delete()
        alternance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

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
        if (immersion.rapport_stage):
            extension=immersion.rapport_stage.name.split(".")[1]
            image_id=immersion.rapport_stage.url.split('/')[5]
            path=os.getcwd()+"/media/rapports"+'/'+image_id+"."+extension
            if os.path.isfile(path):
                os.remove(path)
            immersion.rapport_stage.delete()
        immersion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MaitreStageViewSet(ModelViewSet):
    serializer_class= MaitreStageSerializer
    #permission_classes=(IsMaitreStageAuthenticated,)
    filter_fields=["membre"]

    def get_queryset(self):
        queryset= MaitreStage.objects.all()
    
        maitre_stage_id = self.request.GET.get('id_maitre_stage')
        if maitre_stage_id is not None:
            queryset = queryset.filter(id=maitre_stage_id)
        return queryset


    def destroy(self, request, *args, **kwargs):
        maitre_stage=self.get_object()
        Membre.objects.filter(email=maitre_stage.membre.email).delete()
        Compte.objects.filter(identifiant=maitre_stage.membre.compte.identifiant).delete()
        User.objects.filter(email=maitre_stage.membre.email).delete()
        maitre_stage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjetViewSet(ModelViewSet):
    serializer_class= ProjetSerializer
    #permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        queryset= Projet.objects.all()
    
        projet_id = self.request.GET.get('id_projet')
        if projet_id is not None:
            queryset = queryset.filter(id=projet_id)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        projet=self.get_object()
        projet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        piece_jointe=self.get_object()
        if(piece_jointe.fichier):
            extension=piece_jointe.fichier.name.split(".")[1]
            image_id=piece_jointe.fichier.url.split('/')[5]
            path=os.getcwd()+"/media/pjs"+'/'+image_id+"."+extension
            if os.path.isfile(path):
                os.remove(path)
            piece_jointe.fichier.delete()
        piece_jointe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FormateurViewSet(ModelViewSet):
    serializer_class= FormateurSerializer
    #permission_classes=(IsFormateurAuthenticated,)
    filter_fields=["membre"]

    def get_queryset(self):
        queryset= Formateur.objects.all()
    
        formateur_id = self.request.GET.get('id_formateur')
        if formateur_id is not None:
            queryset = queryset.filter(id=formateur_id)
        return queryset


    def destroy(self, request, *args, **kwargs):
        formateur=self.get_object()
        Membre.objects.filter(email=formateur.membre.email).delete()
        Compte.objects.filter(identifiant=formateur.membre.compte.identifiant).delete()
        User.objects.filter(email=formateur.membre.email).delete()
        formateur.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ManagerViewSet(ModelViewSet):
    serializer_class= ManagerSerializer
    #permission_classes=(IsManagerAuthenticated,)
    filter_fields=["maitre_stage"]

    def get_queryset(self):
        queryset= Manager.objects.all()
    
        manager_id = self.request.GET.get('id_manager')
        if manager_id is not None:
            queryset = queryset.filter(id=manager_id)
        return queryset


    def destroy(self, request, *args, **kwargs):
        manager=self.get_object()
        MaitreStage.objects.filter(id=manager.maitre_stage.id).delete()
        Membre.objects.filter(email=manager.maitre_stage.membre.email).delete()
        Compte.objects.filter(identifiant=manager.maitre_stage.membre.compte.identifiant).delete()
        User.objects.filter(email=manager.maitre_stage.membre.email).delete()
        manager.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   


class ResponsableImmersionViewSet(ModelViewSet):
    serializer_class= ResponsableImmersionSerializer
    #permission_classes=(IsResponsableImmersionAuthenticated,)
    filter_fields=["formateur"]

    def get_queryset(self):
        queryset= ResponsableImmersion.objects.all()
        responsable_immersion_id = self.request.GET.get('id_responsable_immersion')
        if responsable_immersion_id is not None:
            queryset = queryset.filter(id=responsable_immersion_id)
        return queryset


    def destroy(self, request, *args, **kwargs):
        responsable_immersion=self.get_object()
        Formateur.objects.filter(id=responsable_immersion.formateur.id).delete()
        Membre.objects.filter(email=responsable_immersion.formateur.membre.email).delete()
        Compte.objects.filter(identifiant=responsable_immersion.formateur.membre.compte.identifiant).delete()
        User.objects.filter(email=responsable_immersion.formateur.membre.email).delete()
        responsable_immersion.delete()
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
    
    
class GrilleEvaluationViewSet(ModelViewSet):
    serializer_class= GrilleEvaluationSerializer
    #permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        queryset= GrilleEvaluation.objects.all()
        grille_id = self.request.GET.get('id_grille')
        if grille_id is not None:
            queryset = queryset.filter(id=grille_id)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        grille=self.get_object()
        Critere.objects.filter(grille_id=grille.id).delete()
        grille.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
     

class CritereViewSet(ModelViewSet):
    serializer_class= CritereSerializer
    #permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        queryset= Critere.objects.all()
        critere_id = self.request.GET.get('id_critere')
        if critere_id is not None:
            queryset = queryset.filter(id=critere_id)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        critere=self.get_object()
        critere.delete()
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
    
    
class EvaluationPartielleViewSet(ModelViewSet):
    serializer_class= EvaluationPartielleSerializer
    #permission_classes=(IsAuthenticated,)
    filter_fields=["evaluation"]

    def get_queryset(self):
        queryset= EvaluationPartielle.objects.all()
        evaluation_partielle_id = self.request.GET.get('id_evaluation_partielle')
        if evaluation_partielle_id is not None:
            queryset = queryset.filter(id=evaluation_partielle_id)
        return queryset


    def destroy(self, request, *args, **kwargs):
        evaluation_partielle=self.get_object()
        Evaluation.objects.filter(id=evaluation_partielle.evaluation.id).delete()
        evaluation_partielle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
     
    
class EvaluationFinaleViewSet(ModelViewSet):
    serializer_class= EvaluationFinaleSerializer
    #permission_classes=(IsAuthenticated,)
    filter_fields=["evaluation"]

    def get_queryset(self):
        queryset= EvaluationFinale.objects.all()
        evaluation_finale_id = self.request.GET.get('id_evaluation_finale')
        if evaluation_finale_id is not None:
            queryset = queryset.filter(id=evaluation_finale_id)
        return queryset


    def destroy(self, request, *args, **kwargs):
        evaluation_finale=self.get_object()
        Evaluation.objects.filter(id=evaluation_finale.evaluation.id).delete()
        evaluation_finale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
      
class EvaluationApprentissageViewSet(ModelViewSet):
    serializer_class= EvaluationApprentissageSerializer
    #permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        queryset= EvaluationApprentissage.objects.all()
        evaluation_apprentissage_id = self.request.GET.get('id_evaluation_apprentissage')
        if evaluation_apprentissage_id is not None:
            queryset = queryset.filter(id=evaluation_apprentissage_id)
        return queryset
    
    
    def destroy(self, request, *args, **kwargs):
        evaluation_apprentissage=self.get_object()
        evaluation_apprentissage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
    
class CongeViewSet(ModelViewSet):
    serializer_class= CongeSerializer
    #permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        queryset= Conge.objects.all()
        conge_id = self.request.GET.get('id_conge')
        if conge_id is not None:
            queryset = queryset.filter(id=conge_id)
        return queryset
    
    
    def destroy(self, request, *args, **kwargs):
        conge=self.get_object()
        conge.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


class GetTokenViewSet(ModelViewSet):
    serializer_class= CompteSerializer
    http_method_names = ["post","head"]


    def create(self, request, *args, **kwargs):
        compte_serializer=CompteSerializer(data=request.data)
        if not compte_serializer.is_valid():
            return Response({'detail': 'Données invalides'}, status = status.HTTP_400_BAD_REQUEST)

        user= authenticate(
            username = compte_serializer.data['identifiant'],
            password = compte_serializer.data['mot_de_passe'] 
        )
        if not user:
            return Response({'detail': 'informations de connexion invalides.'}, status=status.HTTP_404_NOT_FOUND)
            
        #TOKEN STUFF
        token, _ = Token.objects.get_or_create(user = user)
        #token_expire_handler will check, if the token is expired it will generate new one
        is_expired, token = token_expire_handler(token)    
        user_serialized = UserSerializer(user)
        permission=list(user.get_all_permissions())[0]

        return Response({
        'user': user_serialized.data, 
        'expires_in': expires_in(token),
        'created_at': token.created,
        'token': token.key,
        'userType':permission.split(".")[1]
            }, status=status.HTTP_200_OK)


class VerifyToken(ModelViewSet):
    http_method_names = ["post","head"]


    def create(self, request, *args, **kwargs):
        token=request.data["token"]
        token=Token.objects.get(key = token)
        if(token):
            if not is_token_expired(token):
                return Response({'info':'token valide'},status=status.HTTP_200_OK)
            else:
                return Response({'info':'token invalide'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'info':'token invalide'},status=status.HTTP_401_UNAUTHORIZED)


class LogOut(ModelViewSet):
    http_method_names = ["post","head"]


    def create(self, request, *args, **kwargs):
        #request.user.auth_token.delete()
        logout(request)

        return Response({'info':'utilisateur deconnecté'},status=status.HTTP_200_OK)


class ResetPassword(ModelViewSet):
    http_method_names = ["post","head"]
    serializer_class=ResetPasswordSerializer


    def create(self, request, *args, **kwargs):
        serializer=ResetPasswordSerializer(data=request.data)
        email=request.data["email"]
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uidb64=urlsafe_base64_encode(force_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            absurl = request.META['HTTP_ORIGIN']+"/reset_password/"+"?uidb="+uidb64+"&key="+token
            email_body = 'Bonjour '+user.username + \
                    'Utilisez ce lien pour reinitialiser votre mot de passe \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                        'email_subject': 'Reinitialiser mot de passe.'}
            PasswordReset.objects.create(uidb=uidb64,key=token)

            Util.send_email(data)
        return Response({'info':'Le lien pour réinitialiser votre mot de passe a été envoyé dans votre boite mail.'},status=status.HTTP_200_OK)


class PasswordTokenCheck(ModelViewSet):
    http_method_names = ["post","head"]


    def create(self, request, *args, **kwargs):
        token=request.data["token"]
        uidb=request.data["uidb"]
        id = smart_str(urlsafe_base64_decode(uidb))
        user = User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({'info':'token invalide'},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'info':'token valide'},status=status.HTTP_200_OK)


class SetNewPassword(ModelViewSet):
    http_method_names = ["patch","head"]
    serializer_class = SetNewPasswordSerializer


    def patch(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            token = serializer.validated_data['token']
            uidb64 =serializer.validated_data['uidb64']
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            compte=Compte.objects.filter(identifiant=user.email)[0]
            compte.mot_de_passe=password
            user.set_password(password)
            user.save()
            compte.save()
            return Response({'success': True, 'message': 'le mot de passe a été réinitialisé avec succès.'}, status=status.HTTP_200_OK)