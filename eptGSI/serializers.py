from rest_framework import serializers 
from .models import *
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType



class CompteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Compte
        fields='__all__'

        extra_kwargs = {
            'identifiant': {'validators': []}
        }


class MembreSerializer(serializers.ModelSerializer):
    compte = CompteSerializer()

    class Meta:
        model=Membre
        fields='__all__'

        extra_kwargs = {
            'email': {'validators': []},
            #'telephone': {'validators': []}
        }

    def create(self, validated_data):
        compte = validated_data.pop('compte')
        email=validated_data.get('email')
        telephone=validated_data.get('telephone')
        identifiant=validated_data.get('identifiant')
        if Membre.objects.filter(email=email).exists() :
            raise serializers.ValidationError('Ce membre existe déja')
            return email
        if Membre.objects.filter(telephone=telephone).exists():
            raise serializers.ValidationError('Ce membre existe déja')
            return telephone
        if Compte.objects.filter(identifiant=identifiant).exists():
            raise serializers.ValidationError('Ce compte existe déja')
            return identifiant
        compte=Compte.objects.create(**compte)
        membre=Membre.objects.create(compte=compte,**validated_data)

        return membre


    def update(self, instance, validated_data):
        compte_data = validated_data.pop('compte')
        compte = instance.compte         
        instance.nom = validated_data.get('nom', instance.nom)
        instance.prenom = validated_data.get('prenom', instance.prenom)
        instance.email = validated_data.get('email', instance.email)
        instance.telephone = validated_data.get('telephone', instance.telephone)
        instance.save()
        
        compte.identifiant = compte_data.get('identifiant', compte.identifiant)
        compte.mot_de_passe = compte_data.get('mot_de_passe', compte.mot_de_passe)
        compte.save()
        
        return instance


class EtudiantSerializer(serializers.ModelSerializer):
    membre = MembreSerializer()

    class Meta:
        model=Etudiant
        fields=["niveau_etude","adresse","cv","membre"]


    def create(self, validated_data):
        membre = validated_data.pop('membre')
        compte= membre.pop('compte')
        email=membre["email"]
        telephone=membre["telephone"]
        identifiant=compte["identifiant"]
        mot_de_passe=compte["mot_de_passe"]
        if Membre.objects.filter(email=email).exists() :
            raise serializers.ValidationError('Ce membre existe déja')
            return email
        if Membre.objects.filter(telephone=telephone).exists():
            raise serializers.ValidationError('Ce membre existe déja')
            return telephone
        if Compte.objects.filter(identifiant=identifiant).exists():
            raise serializers.ValidationError('Ce compte existe déja')
            return identifiant
        compte=Compte.objects.create(**compte)
        membre=Membre.objects.create(compte=compte,**membre)
        etudiant= Etudiant.objects.create(membre=membre,**validated_data)
        user=User.objects.create_user(username=email, email=identifiant,password=mot_de_passe)
        content_type = ContentType.objects.get_for_model(Etudiant)
        permission = Permission.objects.filter(codename='is_student').first()
        if permission:
            user.user_permissions.add(permission)
        else:
            created = Permission.objects.create(codename='is_student', name='is student', content_type=content_type)
            user.user_permissions.add(created)
        return etudiant


    def update(self, instance, validated_data,*args, **kwargs):  
        print(validated_data)
        if 'membre' in validated_data.keys():   
            membre_data = validated_data.pop('membre')
            membre_serializer = MembreSerializer(data = membre_data,partial=True) 
            if membre_serializer.is_valid():
                membre = membre_serializer.update(instance=instance.membre, validated_data=membre_serializer.validated_data)

        if 'niveau_etude' in validated_data.keys():   
            instance.niveau_etude = validated_data.get('niveau_etude', instance.niveau_etude)
        if 'adresse' in validated_data.keys():   
            instance.adresse = validated_data.get('adresse', instance.adresse)
        if 'cv' in validated_data.keys():
            if instance.cv:
                instance.cv.delete()
            instance.cv = validated_data.get('cv', instance.cv)
        instance.save()
        return instance


class EntrepriseSerializer(serializers.ModelSerializer):

    class Meta:
        model=Entreprise
        fields="__all__"


class ProgrammeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Programme
        fields="__all__"


class ImmersionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Immersion
        fields="__all__"


    def create(self, validated_data):
        entreprise = validated_data.pop('entreprise')
        programme= validated_data.pop('programme')
        immersion= Immersion.objects.create(entreprise=entreprise,programme=programme,**validated_data)

        return immersion

    def update(self, instance, validated_data,*args, **kwargs):       
              
        instance.description = validated_data.get('description', instance.description)
        instance.date_debut = validated_data.get('date_debut', instance.date_debut)
        instance.date_fin = validated_data.get('date_fin', instance.date_fin)
        instance.entreprise=validated_data.get('entreprise', instance.entreprise)
        instance.programme=validated_data.get('programme', instance.programme)
        instance.save()
        
        return instance
    


class StageSerializer(serializers.ModelSerializer):

    class Meta:
        model=Stage
        fields="__all__"


    def create(self, validated_data):
        etudiant = validated_data.pop('etudiant')
        immersion= validated_data.pop('immersion')
        if Stage.objects.filter(etudiant=etudiant, annee=validated_data["annee"]).exists() :
            raise serializers.ValidationError('Ce stage existe déja')
            return email
        stage = Stage.objects.create(etudiant=etudiant,immersion=immersion,**validated_data)

        return stage

    def update(self, instance, validated_data,*args, **kwargs):        
        instance.annee = validated_data.get('annee', instance.annee)
        instance.date_debut= validated_data.get('date_debut', instance.date_debut)
        instance.date_fin= validated_data.get('date_fin', instance.date_fin)
        instance.etudiant= validated_data.get('etudiant', instance.etudiant)
        instance.immersion= validated_data.get('immersion', instance.immersion)


        if instance.rapport_stage:
            instance.rapport_stage.delete()
        instance.rapport_stage = validated_data.get('rapport_stage', instance.rapport_stage)


        instance.save()
        return instance


class MaitreStageSerializer(serializers.ModelSerializer):
    membre = MembreSerializer()

    class Meta:
        model=MaitreStage
        fields=["membre"]


    def create(self, validated_data):
        membre = validated_data.pop('membre')
        compte= membre.pop('compte')
        email=membre["email"]
        telephone=membre["telephone"]
        identifiant=compte["identifiant"]
        if Membre.objects.filter(email=email).exists() :
            raise serializers.ValidationError('Ce membre existe déja')
            return email
        if Membre.objects.filter(telephone=telephone).exists():
            raise serializers.ValidationError('Ce membre existe déja')
            return telephone
        if Compte.objects.filter(identifiant=identifiant).exists():
            raise serializers.ValidationError('Ce compte existe déja')
            return identifiant
        compte=Compte.objects.create(**compte)
        membre=Membre.objects.create(compte=compte,**membre)
        maitreStage= MaitreStage.objects.create(membre=membre,**validated_data)

        return maitreStage

    def update(self, instance, validated_data,*args, **kwargs):        
        membre_data = validated_data.pop('membre')
        membre_serializer = MembreSerializer(data = membre_data,partial=True)
             
        if membre_serializer.is_valid():
            membre = membre_serializer.update(instance=instance.membre, validated_data=membre_serializer.validated_data)
        
           
        instance.save()
        
        return instance





class PlanningSerializer(serializers.ModelSerializer):

    class Meta:
        model=Planning
        fields=["annee","etudiant","maitreStage"]


    def create(self, validated_data):
        etudiant = validated_data.pop('etudiant')
        maitre_stage= validated_data.pop('maitreStage')
        if Planning.objects.filter(etudiant=etudiant, annee=validated_data["annee"], maitreStage=maitre_stage).exists() :
            raise serializers.ValidationError('Ce Planning existe déja')
            return validated_data
        planning = Planning.objects.create(etudiant=etudiant,maitreStage=maitre_stage,**validated_data)

        return planning

    def update(self, instance, validated_data,*args, **kwargs):        
        instance.annee = validated_data.get('annee', instance.annee)
        instance.etudiant= validated_data.get('etudiant', instance.etudiant)
        instance.maitreStage= validated_data.get('maitreStage', instance.maitreStage)

        instance.save()
        return instance


class ProjetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Projet
        fields="__all__"


    def create(self, validated_data):
        programme = validated_data.pop('programme')
        planning= validated_data.pop('planning')
        if Projet.objects.filter(nom_projet=validated_data["nom_projet"], descriptif_projet=validated_data["descriptif_projet"]).exists() :
            raise serializers.ValidationError('Ce Projet existe déja')
            return validated_data
        projet = Projet.objects.create(programme=programme,planning=planning,**validated_data)

        return planning

    def update(self, instance, validated_data,*args, **kwargs):        
        instance.nom_projet = validated_data.get('nom_projet', instance.nom_projet)
        instance.descriptif_projet= validated_data.get('descriptif_projet', instance.descriptif_projet)
        instance.etat= validated_data.get('etat', instance.etat)
        instance.programme = validated_data.get('programme', instance.programme)
        instance.planning= validated_data.get('planning', instance.planning)

        instance.save()
        return instance


class TacheSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Tache
        fields="__all__"


    def create(self, validated_data):
        projet = validated_data.pop('projet')
        if Tache.objects.filter(intitule=validated_data["intitule"],projet=projet).exists() :
            raise serializers.ValidationError('Cette tache existe déja')
            return validated_data
        tache = Tache.objects.create(projet=projet,**validated_data)

        return tache

    def update(self, instance, validated_data,*args, **kwargs):        
        instance.intitule = validated_data.get('intitule', instance.intitule)
        instance.projet= validated_data.get('projet', instance.projet)
        instance.save()
        return instance


class SousTacheSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=SousTache
        fields="__all__"


    def create(self, validated_data):
        tache = validated_data.pop('tache')
        if SousTache.objects.filter(nom_tache=validated_data["nom_tache"],tache=tache).exists() :
            raise serializers.ValidationError('Cette sous tache existe déja')
            return validated_data
        sous_tache = SousTache.objects.create(tache=tache,**validated_data)

        return sous_tache

    def update(self, instance, validated_data,*args, **kwargs):        
        instance.nom_tache = validated_data.get('nom_tache', instance.nom_tache)
        instance.echeance= validated_data.get('echeance', instance.echeance)
        instance.date_debut = validated_data.get('date_debut', instance.date_debut)
        instance.date_fin= validated_data.get('date_fin', instance.date_fin)
        instance.descriptif = validated_data.get('descriptif', instance.descriptif)
        instance.commentaire= validated_data.get('commentaire', instance.commentaire)
        instance.etat = validated_data.get('etat', instance.etat)
        instance.tache= validated_data.get('tache', instance.tache)
        instance.save()
        return instance


class MembreDeptSerializer(serializers.ModelSerializer):
    membre = MembreSerializer()

    class Meta:
        model=MembreDept
        fields=["membre"]


    def create(self, validated_data):
        membre = validated_data.pop('membre')
        compte= membre.pop('compte')
        email=membre["email"]
        telephone=membre["telephone"]
        identifiant=compte["identifiant"]
        if Membre.objects.filter(email=email).exists() :
            raise serializers.ValidationError('Ce membre existe déja')
            return email
        if Membre.objects.filter(telephone=telephone).exists():
            raise serializers.ValidationError('Ce membre existe déja')
            return telephone
        if Compte.objects.filter(identifiant=identifiant).exists():
            raise serializers.ValidationError('Ce compte existe déja')
            return identifiant
        compte=Compte.objects.create(**compte)
        membre=Membre.objects.create(compte=compte,**membre)
        membreDept= MembreDept.objects.create(membre=membre,**validated_data)

        return membreDept

    def update(self, instance, validated_data,*args, **kwargs):        
        membre_data = validated_data.pop('membre')
        membre_serializer = MembreSerializer(data = membre_data,partial=True)
             
        if membre_serializer.is_valid():
            membre = membre_serializer.update(instance=instance.membre, validated_data=membre_serializer.validated_data)
        
        instance.save()
        
        return instance
    
    
class DestinataireSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Destinataire
        fields="__all__"


class RespEntrepriseSerializer(serializers.ModelSerializer):
    membre = MembreSerializer()

    class Meta:
        model=RespEntreprise
        fields=["membre"]


    def create(self, validated_data):
        membre = validated_data.pop('membre')
        compte= membre.pop('compte')
        email=membre["email"]
        telephone=membre["telephone"]
        identifiant=compte["identifiant"]
        if Membre.objects.filter(email=email).exists() :
            raise serializers.ValidationError('Ce membre existe déja')
            return email
        if Membre.objects.filter(telephone=telephone).exists():
            raise serializers.ValidationError('Ce membre existe déja')
            return telephone
        if Compte.objects.filter(identifiant=identifiant).exists():
            raise serializers.ValidationError('Ce compte existe déja')
            return identifiant
        compte=Compte.objects.create(**compte)
        membre=Membre.objects.create(compte=compte,**membre)
        respEntreprise= RespEntreprise.objects.create(membre=membre,**validated_data)

        return respEntreprise

    def update(self, instance, validated_data,*args, **kwargs):        
        membre_data = validated_data.pop('membre')
        membre_serializer = MembreSerializer(data = membre_data,partial=True)   
             
        if membre_serializer.is_valid():
            membre = membre_serializer.update(instance=instance.membre, validated_data=membre_serializer.validated_data)
        
        instance.save()
        
        return instance
    
    
class ChefDeptSerializer(serializers.ModelSerializer):
    membre = MembreSerializer()

    class Meta:
        model=ChefDept
        fields=["membre"]


    def create(self, validated_data):
        membre = validated_data.pop('membre')
        compte= membre.pop('compte')
        email=membre["email"]
        telephone=membre["telephone"]
        identifiant=compte["identifiant"]
        if Membre.objects.filter(email=email).exists() :
            raise serializers.ValidationError('Ce membre existe déja')
            return email
        if Membre.objects.filter(telephone=telephone).exists():
            raise serializers.ValidationError('Ce membre existe déja')
            return telephone
        if Compte.objects.filter(identifiant=identifiant).exists():
            raise serializers.ValidationError('Ce compte existe déja')
            return identifiant
        compte=Compte.objects.create(**compte)
        membre=Membre.objects.create(compte=compte,**membre)
        chefDept= ChefDept.objects.create(membre=membre,**validated_data)

        return chefDept

    def update(self, instance, validated_data,*args, **kwargs):        
        membre_data = validated_data.pop('membre')
        membre_serializer = MembreSerializer(data = membre_data,partial=True)   
             
        if membre_serializer.is_valid():
            membre = membre_serializer.update(instance=instance.membre, validated_data=membre_serializer.validated_data)
        
        instance.save()
        
        return instance
    
    
class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Message
        fields="__all__"


    def create(self, validated_data):
        etudiant = validated_data.pop('etudiant')
        stage = Stage.objects.create(etudiant=etudiant,**validated_data)

        return stage

    def update(self, instance, validated_data,*args, **kwargs):        
        instance.intitule = validated_data.get('intitule', instance.intitule)
        instance.contenu= validated_data.get('contenu', instance.contenu)
        instance.etudiant= validated_data.get('etudiant', instance.etudiant)

        instance.save()
        return instance
    
    
class EvaluationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Evaluation
        fields="__all__"


    def create(self, validated_data):
        etudiant = validated_data.pop('etudiant')
        maitre_de_stage = validated_data.pop('maitre_de_stage')
        stage = Stage.objects.create(etudiant=etudiant, maitre_de_stage=maitre_de_stage, **validated_data)

        return stage

    def update(self, instance, validated_data,*args, **kwargs):        
        instance.note_evaluation = validated_data.get('note_evaluation', instance.note_evaluation)
        instance.appreciation= validated_data.get('appreciation', instance.appreciation)
        instance.etudiant= validated_data.get('etudiant', instance.etudiant)
        instance.maitre_de_stage= validated_data.get('maitre_de_stage', instance.maitre_de_stage)

        instance.save()
        return instance
    
    
class EvenementSerializer(serializers.ModelSerializer):
    class Meta:
        model=Evenement
        fields="__all__"


    def create(self, validated_data):
        destinataires = validated_data.pop("destinataires")
        evenement = Evenement.objects.create(**validated_data)
        for destinataire in destinataires:
            evenement.destinataires.add(destinataire)
        evenement.save()

        return evenement

    def update(self, instance, validated_data,*args, **kwargs):        
        instance.details = validated_data.get('details', instance.details)
        instance.intitule= validated_data.get('intitule', instance.intitule)
        instance.date= validated_data.get('date', instance.date)

        instance.save()
        return instance
    
    
class PieceJointeSerializer(serializers.ModelSerializer):
    class Meta:
        model=PieceJointe
        fields="__all__"


    def create(self, validated_data):
        evenement = validated_data.pop('evenement')
        pieceJointe = PieceJointe.objects.create(evenement=evenement, **validated_data)
        
        return pieceJointe

    def update(self, instance, validated_data,*args, **kwargs): 
        instance.evenement = validated_data.get('evenement', instance.evenement)       
        if instance.fichier:
            instance.fichier.delete()
        instance.fichier = validated_data.get('fichier', instance.fichier)

        instance.save()
        return instance



#User serializer pour la classe User de django

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"
