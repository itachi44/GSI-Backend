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


#Vues API

class EtudiantViewSet(ModelViewSet):
    serializer_class= EtudiantSerializer
    permission_classes=(IsStudentAuthenticated,)
    filter_fields=["niveau_etude","membre"]

    def get_queryset(self):
        queryset= Etudiant.objects.all()

    
        email = self.request.GET.get('email')
        if email is not None:
            queryset = queryset.filter(membre__email=email)
        return queryset


    def destroy(self, request, *args, **kwargs):
        etudiant=self.get_object()
        Membre.objects.filter(email=etudiant.membre.email).delete()
        Compte.objects.filter(identifiant=etudiant.membre.compte.identifiant).delete()
        User.objects.filter(email=etudiant.membre.email).delete()
        extension=etudiant.cv.name.split(".")[1]
        image_id=etudiant.cv.url.split('/')[5]
        path=os.getcwd()+"/media/cvs"+'/'+image_id+"."+extension
        if os.path.isfile(path):
            os.remove(path)
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


#get Token view


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


#verifier le token
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




#logout user

class LogOut(ModelViewSet):
    http_method_names = ["post","head"]

    def create(self, request, *args, **kwargs):
        #request.user.auth_token.delete()
        logout(request)

        return Response({'info':'utilisateur deconnecté'},status=status.HTTP_200_OK)


#password reset

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
            print(absurl)
            #TODO save the token in the database
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