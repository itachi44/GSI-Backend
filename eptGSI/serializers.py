from rest_framework import serializers 
from .models import *
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import AuthenticationFailed
import os


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


class StagiairePedagogiqueSerializer(serializers.ModelSerializer):
    membre = MembreSerializer()

    class Meta:
        model=StagiairePedagogique
        fields=["niveau_etude","adresse","cv","membre","get_cv"]

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
        stagiaire_pedagogique= StagiairePedagogique.objects.create(membre=membre,**validated_data)
        user=User.objects.create_user(username=identifiant, email=email,password=mot_de_passe)
        content_type = ContentType.objects.get_for_model(StagiairePedagogique)
        permission = Permission.objects.filter(codename='is_student').first()
        if permission:
            user.user_permissions.add(permission)
        else:
            created = Permission.objects.create(codename='is_student', name='is student', content_type=content_type)
            user.user_permissions.add(created)
        return stagiaire_pedagogique


    def update(self, instance, validated_data,*args, **kwargs):  
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
                extension=instance.cv.name.split(".")[1]
                image_id=instance.cv.url.split('/')[5]
                path=os.getcwd()+"/media/cvs"+'/'+image_id+"."+extension
                if os.path.isfile(path):
                    os.remove(path)
                instance.cv.delete()
            instance.cv = validated_data.get('cv', instance.cv)
        instance.save()
        return instance


class EntrepriseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Entreprise
        fields="__all__"


class PlanningSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Planning
        fields="__all__"


class AlternanceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Alternance
        fields="__all__"


    def create(self, validated_data):
        entreprise = validated_data.pop('entreprise')
        planning= validated_data.pop('planning')
        date_debut=validated_data.get('date_debut')
        
        if (Alternance.objects.filter(entreprise=entreprise).exists() and Alternance.objects.filter(date_debut=date_debut).exists()):
            raise serializers.ValidationError('Cette alternance existe déjà')
        
        alternance= Alternance.objects.create(entreprise=entreprise,planning=planning,**validated_data)

        return alternance

    def update(self, instance, validated_data,*args, **kwargs):  
        if 'description' in validated_data.keys():   
            instance.description = validated_data.get('description', instance.description)
        if 'date_debut' in validated_data.keys():   
            instance.date_debut = validated_data.get('date_debut', instance.date_debut)
        if 'date_fin' in validated_data.keys():   
            instance.date_fin = validated_data.get('date_fin', instance.date_fin)
        if 'convention' in validated_data.keys():
            if (instance.convention):
                extension=instance.convention.name.split(".")[1]
                image_id=instance.convention.url.split('/')[5]
                path=os.getcwd()+"/media/conventions"+'/'+image_id+"."+extension
                if os.path.isfile(path):
                    os.remove(path)
                instance.convention.delete()
            instance.convention = validated_data.get('convention', instance.convention)
        if 'entreprise' in validated_data.keys():   
            instance.entreprise = validated_data.get('entreprise', instance.entreprise)
        if 'planning' in validated_data.keys():   
            instance.planning = validated_data.get('planning', instance.planning)
        
        instance.save()
        return instance
    

class ImmersionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Immersion
        fields="__all__"


    def create(self, validated_data):
        stagiaire_pedagogique = validated_data.pop('stagiaire_pedagogique')
        alternance= validated_data.pop('alternance')
        
        if Immersion.objects.filter(stagiaire_pedagogique=stagiaire_pedagogique, annee=validated_data["annee"], alternance=alternance).exists() :
            raise serializers.ValidationError('Cette immersion existe déja')
        
        immersion = Immersion.objects.create(stagiaire_pedagogique=stagiaire_pedagogique,alternance=alternance,**validated_data)

        return immersion

    def update(self, instance, validated_data,*args, **kwargs):  
        print(validated_data)
        if 'stagiaire_pedagogique' in validated_data.keys():   
            instance.stagiaire_pedagogique = validated_data.get('stagiaire_pedagogique', instance.stagiaire_pedagogique)
        if 'alternance' in validated_data.keys():   
            instance.alternance = validated_data.get('alternance', instance.alternance)
        if 'annee' in validated_data.keys():   
            instance.annee = validated_data.get('annee', instance.annee)
        if 'date_debut' in validated_data.keys():   
            instance.date_debut = validated_data.get('date_debut', instance.date_debut)
        if 'date_fin' in validated_data.keys():   
            instance.date_fin = validated_data.get('date_fin', instance.date_fin)
        if 'rapport_stage' in validated_data.keys():
            if (instance.rapport_stage):
                extension=instance.rapport_stage.name.split(".")[1]
                image_id=instance.rapport_stage.url.split('/')[5]
                path=os.getcwd()+"/media/rapports"+'/'+image_id+"."+extension
                if os.path.isfile(path):
                    os.remove(path)
                instance.rapport_stage.delete()
            instance.rapport_stage = validated_data.get('rapport_stage', instance.rapport_stage)
        instance.save()
        return instance


class MaitreStageSerializer(serializers.ModelSerializer):
    membre = MembreSerializer()

    class Meta:
        model=MaitreStage
        fields=["membre", "entreprise"]
   
    def create(self, validated_data):
        membre = validated_data.pop('membre')
        compte= membre.pop('compte')
        entreprise = validated_data.pop('entreprise')
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
        maitre_stage= MaitreStage.objects.create(membre=membre, entreprise=entreprise, **validated_data)
        user=User.objects.create_user(username=identifiant, email=email,password=mot_de_passe)
        content_type = ContentType.objects.get_for_model(MaitreStage)
        permission = Permission.objects.filter(codename='is_maitre_stage').first()
        if permission:
            user.user_permissions.add(permission)
        else:
            created = Permission.objects.create(codename='is_maitre_stage', name='is maitre_stage', content_type=content_type)
            user.user_permissions.add(created)
        return maitre_stage


    def update(self, instance, validated_data,*args, **kwargs):  
        if 'membre' in validated_data.keys():   
            membre_data = validated_data.pop('membre')
            membre_serializer = MembreSerializer(data = membre_data,partial=True) 
            if membre_serializer.is_valid():
                membre = membre_serializer.update(instance=instance.membre, validated_data=membre_serializer.validated_data)
                
        instance.save()
        return instance


class ProgrammeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Programme
        fields="__all__"


    def create(self, validated_data):
        stagiaire_pedagogique = validated_data.pop('stagiaire_pedagogique')
        maitre_stage= validated_data.pop('maitre_stage')
        projets = validated_data.pop('projets')
        if Programme.objects.filter(stagiaire_pedagogique=stagiaire_pedagogique, annee=validated_data["annee"], maitre_stage=maitre_stage).exists() :
            raise serializers.ValidationError('Ce Programme existe déja')
            return validated_data
        programme = Programme.objects.create(stagiaire_pedagogique=stagiaire_pedagogique,maitre_stage=maitre_stage,**validated_data)
        if(projets):
            for projet in projets:
                programme.projets.add(projet)
            programme.save()
            
        return programme


    def update(self, instance, validated_data,*args, **kwargs):  
        if 'projets' in validated_data.keys(): 
            projets = validated_data.pop('projets')   
        if (projets):
            Programme.projets.through.objects.filter(programme_id=instance.id).delete()
            for projet in projets :
                instance.projets.add(projet)
                
        if 'annee' in validated_data.keys():           
            instance.annee = validated_data.get('annee', instance.annee)
        if 'stagiaire_pedagogique' in validated_data.keys():
            instance.stagiaire_pedagogique= validated_data.get('stagiaire_pedagogique', instance.stagiaire_pedagogique)
        if 'maitre_stage' in validated_data.keys():
            instance.maitre_stage= validated_data.get('maitre_stage', instance.maitre_stage)

        instance.save()
        return instance


class ProjetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Projet
        fields="__all__"


    def create(self, validated_data):
        planning= validated_data.pop('planning')
        responsables_projet = validated_data.pop('responsables_projet')
        
        if Projet.objects.filter(nom_projet=validated_data["nom_projet"], descriptif_projet=validated_data["descriptif_projet"]).exists() :
            raise serializers.ValidationError('Ce Projet existe déja')
            return validated_data
        projet = Projet.objects.create(planning=planning,**validated_data)
        
        for responsable_projet in responsables_projet:
            projet.responsables_projet.add(responsable_projet)
        projet.save()
        
        return projet

    def update(self, instance, validated_data,*args, **kwargs):    
        if 'responsables_projet' in validated_data.keys():   
            responsables_projet= validated_data.pop('responsables_projet')   
        if 'nom_projet' in validated_data.keys():     
            instance.nom_projet = validated_data.get('nom_projet', instance.nom_projet)
        if 'descriptif_projet' in validated_data.keys(): 
            instance.descriptif_projet= validated_data.get('descriptif_projet', instance.descriptif_projet)
        if 'etat' in validated_data.keys(): 
            instance.etat= validated_data.get('etat', instance.etat)
        if 'budget' in validated_data.keys(): 
            instance.budget = validated_data.get('budget', instance.budget)
        if 'duree' in validated_data.keys(): 
            instance.duree = validated_data.get('duree', instance.duree)
        if 'planning' in validated_data.keys(): 
            instance.planning= validated_data.get('planning', instance.planning)
        if(responsables_projet):
            Projet.responsables_projet.through.objects.filter(projet_id=instance.id).delete()
            for responsable_projet in responsables_projet:
                instance.responsables_projet.add(responsable_projet)
                  
        instance.save()

        return instance


class ActiviteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Activite
        fields="__all__"


    def create(self, validated_data):
        if 'projet' in validated_data.keys():
            projet = validated_data.pop('projet')
        if Activite.objects.filter(nom_activite=validated_data["nom_activite"],projet=projet).exists() :
            raise serializers.ValidationError('Cette activité existe déja')
            return validated_data
        activite = Activite.objects.create(projet=projet,**validated_data)

        return activite


    def update(self, instance, validated_data,*args, **kwargs):     
        if 'nom_activite' in validated_data.keys():   
            instance.nom_activite = validated_data.get('nom_activite', instance.nom_activite)
        if 'date_debut' in validated_data.keys():   
            instance.date_debut = validated_data.get('date_debut', instance.date_debut)
        if 'date_fin' in validated_data.keys():   
            instance.date_fin = validated_data.get('date_fin', instance.date_fin)
        if 'cadre' in validated_data.keys():   
            instance.cadre = validated_data.get('cadre', instance.cadre)
        if 'description' in validated_data.keys():   
            instance.description = validated_data.get('description', instance.description)
        if 'cout' in validated_data.keys():   
            instance.cout = validated_data.get('cout', instance.cout)
        if 'ressources' in validated_data.keys():   
            instance.ressources = validated_data.get('ressources', instance.ressources)
        if 'projet' in validated_data.keys():   
            instance.projet = validated_data.get('projet', instance.projet)
            
        instance.save()
        return instance


class TacheSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Tache
        fields="__all__"


    def create(self, validated_data):
        if 'activite' in validated_data.keys():
            activite = validated_data.pop('activite')
        if 'stagiaire_pedagogique' in validated_data.keys():
            stagiaire_pedagogique = validated_data.pop('stagiaire_pedagogique')
            
        if Tache.objects.filter(intitule=validated_data["intitule"],activite=activite,stagiaire_pedagogique=stagiaire_pedagogique).exists() :
            raise serializers.ValidationError('Cette tache existe déja')
            return validated_data
        tache = Tache.objects.create(activite=activite,stagiaire_pedagogique=stagiaire_pedagogique,**validated_data)

        return tache


    def update(self, instance, validated_data,*args, **kwargs):
        if 'intitule' in validated_data.keys():               
            instance.intitule = validated_data.get('intitule', instance.intitule)
        if 'projet' in validated_data.keys():               
            instance.projet = validated_data.get('projet', instance.projet)
        if 'stagiaire_pedagogique' in validated_data.keys():               
            instance.stagiaire_pedagogique = validated_data.get('stagiaire_pedagogique', instance.stagiaire_pedagogique)
        instance.save()
        return instance


class SousTacheSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=SousTache
        fields="__all__"


    def create(self, validated_data):
        if 'tache' in validated_data.keys():
            tache = validated_data.pop('tache')
        if SousTache.objects.filter(nom_tache=validated_data["nom_tache"],tache=tache).exists() :
            raise serializers.ValidationError('Cette sous-tache existe déjà')
            return validated_data
        sous_tache = SousTache.objects.create(tache=tache,**validated_data)

        return sous_tache

    def update(self, instance, validated_data,*args, **kwargs): 
        if 'nom_tache' in validated_data.keys():       
            instance.nom_tache = validated_data.get('nom_tache', instance.nom_tache)
        if 'echeance' in validated_data.keys():
            instance.echeance= validated_data.get('echeance', instance.echeance)
        if 'date_debut' in validated_data.keys():
            instance.date_debut = validated_data.get('date_debut', instance.date_debut)
        if 'date_fin' in validated_data.keys():
            instance.date_fin= validated_data.get('date_fin', instance.date_fin)
        if 'descriptif' in validated_data.keys():
            instance.descriptif = validated_data.get('descriptif', instance.descriptif)
        if 'commentaire' in validated_data.keys():
            instance.commentaire= validated_data.get('commentaire', instance.commentaire)
        if 'etat' in validated_data.keys():
            instance.etat = validated_data.get('etat', instance.etat)
        if 'tache' in validated_data.keys():
            instance.tache= validated_data.get('tache', instance.tache)
        if 'technologies' in validated_data.keys():
            instance.technologies= validated_data.get('technologies', instance.technologies)
        if 'langages' in validated_data.keys():
            instance.langages= validated_data.get('langages', instance.langages)
        instance.save()
        return instance


class DestinataireSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Destinataire
        fields="__all__"
        

class EvenementSerializer(serializers.ModelSerializer):
    class Meta:
        model=Evenement
        fields="__all__"


    def create(self, validated_data):
        if 'destinataires' in validated_data.keys():
            destinataires = validated_data.pop("destinataires")
        evenement = Evenement.objects.create(**validated_data)
        if(destinataires) :
            for destinataire in destinataires:
                evenement.destinataires.add(destinataire)
        evenement.save()
        return evenement


    def update(self, instance, validated_data,*args, **kwargs): 
        if 'details' in validated_data.keys():       
            instance.details = validated_data.get('details', instance.details)
        if 'intitule' in validated_data.keys():
            instance.intitule= validated_data.get('intitule', instance.intitule)
        if 'date' in validated_data.keys():    
            instance.date= validated_data.get('date', instance.date)
        if 'type' in validated_data.keys():    
            instance.type= validated_data.get('type', instance.type)
        if 'destinataires' in validated_data.keys():    
            destinataires = validated_data.pop('destinataires')   
        if (destinataires):
            Evenement.destinataires.through.objects.filter(evenement_id=instance.id).delete()
            for destinataire in destinataires :
                instance.destinataires.add(destinataire)
        instance.save()
        return instance


class PieceJointeSerializer(serializers.ModelSerializer):
    class Meta:
        model=PieceJointe
        fields="__all__"


    def create(self, validated_data):
        if 'evenement' in validated_data.keys():
            evenement = validated_data.pop('evenement')
        pieceJointe = PieceJointe.objects.create(evenement=evenement, **validated_data)
        
        return pieceJointe


    def update(self, instance, validated_data,*args, **kwargs): 
        if 'evenement' in validated_data.keys():
            instance.evenement = validated_data.get('evenement', instance.evenement)       
        if 'fichier' in validated_data.keys():
            if instance.fichier:
                extension=instance.fichier.name.split(".")[1]
                image_id=instance.fichier.url.split('/')[5]
                path=os.getcwd()+"/media/pjs"+'/'+image_id+"."+extension
                if os.path.isfile(path):
                    os.remove(path)
                instance.fichier.delete()
            instance.fichier = validated_data.get('fichier', instance.fichier)
        instance.save()
        return instance


class FormateurSerializer(serializers.ModelSerializer):
    membre = MembreSerializer()

    class Meta:
        model=Formateur
        fields=["membre"]


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
        formateur= Formateur.objects.create(membre=membre,**validated_data)
        user=User.objects.create_user(username=identifiant, email=email,password=mot_de_passe)
        content_type = ContentType.objects.get_for_model(Formateur)
        permission = Permission.objects.filter(codename='is_formateur').first()
        if permission:
            user.user_permissions.add(permission)
        else:
            created = Permission.objects.create(codename='is_formateur', name='is formateur', content_type=content_type)
            user.user_permissions.add(created)

        return formateur

    def update(self, instance, validated_data,*args, **kwargs):    
        membre_data = validated_data.pop('membre')
        membre_serializer = MembreSerializer(data = membre_data,partial=True)
             
        if membre_serializer.is_valid():
            membre = membre_serializer.update(instance=instance.membre, validated_data=membre_serializer.validated_data)
        
        instance.save()
        
        return instance



class ManagerSerializer(serializers.ModelSerializer):
    maitre_stage = MaitreStageSerializer()

    class Meta:
        model=Manager
        fields=["maitre_stage"]


    def create(self, validated_data):
        maitre_stage = validated_data.pop('maitre_stage')
        membre = maitre_stage.pop('membre')
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
        maitre_stage= MaitreStage.objects.create(membre=membre, **maitre_stage)
        manager= Manager.objects.create(maitre_stage=maitre_stage,**validated_data)
        user=User.objects.create_user(username=identifiant, email=email,password=mot_de_passe)
        content_type = ContentType.objects.get_for_model(Manager)
        permission = Permission.objects.filter(codename='is_manager').first()
        if permission:
            user.user_permissions.add(permission)
        else:
            created = Permission.objects.create(codename='is_manager', name='is manager', content_type=content_type)
            user.user_permissions.add(created)
        return manager


    def update(self, instance, validated_data,*args, **kwargs):    
        maitre_stage = validated_data.pop('maitre_stage')
        membre = maitre_stage.pop('membre')
        membre_serializer = MembreSerializer(data = membre,partial=True)
             
        if membre_serializer.is_valid():
            membre = membre_serializer.update(instance=instance.maitre_stage.membre, validated_data=membre_serializer.validated_data)
        instance.save()
        return instance
    
    
class ResponsableImmersionSerializer(serializers.ModelSerializer):
    formateur = FormateurSerializer()

    class Meta:
        model=ResponsableImmersion
        fields=["formateur"]


    def create(self, validated_data):
        formateur = validated_data.pop('formateur')
        membre = formateur.pop('membre')
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
        formateur= Formateur.objects.create(membre=membre, **formateur)
        responsable_immersion= ResponsableImmersion.objects.create(formateur=formateur,**validated_data)
        user=User.objects.create_user(username=identifiant, email=email,password=mot_de_passe)
        content_type = ContentType.objects.get_for_model(ResponsableImmersion)
        permission = Permission.objects.filter(codename='is_responsable_immersion').first()
        if permission:
            user.user_permissions.add(permission)
        else:
            created = Permission.objects.create(codename='is_responsable_immersion', name='is responsable_immersion', content_type=content_type)
            user.user_permissions.add(created)
        return responsable_immersion


    def update(self, instance, validated_data,*args, **kwargs):    
        formateur = validated_data.pop('formateur')
        membre = formateur.pop('membre')
        membre_serializer = MembreSerializer(data = membre,partial=True) 
        if membre_serializer.is_valid():
            membre = membre_serializer.update(instance=instance.formateur.membre, validated_data=membre_serializer.validated_data)
        instance.save()
        return instance
    
    
class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Message
        fields="__all__"


    def create(self, validated_data):
        if 'stagiaire_pedagogique' in validated_data.keys():
            stagiaire_pedagogique = validated_data.pop('stagiaire_pedagogique')
        message = Message.objects.create(stagiaire_pedagogique=stagiaire_pedagogique,**validated_data)
        return message


    def update(self, instance, validated_data,*args, **kwargs):  
        if 'intitule' in validated_data.keys():      
            instance.intitule = validated_data.get('intitule', instance.intitule)
        if 'contenu' in validated_data.keys():
            instance.contenu= validated_data.get('contenu', instance.contenu)
        if 'stagiaire_pedagogique' in validated_data.keys():
            instance.stagiaire_pedagogique= validated_data.get('stagiaire_pedagogique', instance.stagiaire_pedagogique)
        instance.save()
        return instance
    

class GrilleEvaluationSerializer(serializers.ModelSerializer):
        
    class Meta:
        model=GrilleEvaluation
        fields="__all__"


class CritereSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Critere
        fields="__all__"


    def create(self, validated_data):
        if 'grille' in validated_data.keys():
            grille = validated_data.pop('grille')
        critere = Critere.objects.create(grille=grille,**validated_data)
        return critere


    def update(self, instance, validated_data,*args, **kwargs):  
        if 'label_critere' in validated_data.keys():      
            instance.label_critere = validated_data.get('label_critere', instance.label_critere)
        if 'pourcentage' in validated_data.keys():
            instance.pourcentage= validated_data.get('pourcentage', instance.pourcentage)
        if 'grille' in validated_data.keys():
            instance.grille= validated_data.get('grille', instance.grille)

        instance.save()
        return instance
    

class EvaluationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Evaluation
        fields="__all__"


    def create(self, validated_data):
        if 'grille' in validated_data.keys():
            grille = validated_data.pop('grille')
        if 'maitre_stage' in validated_data.keys():
            maitres_stage = validated_data.pop("maitre_stage")
        evaluation = Evaluation.objects.create(grille=grille, **validated_data)
        if(maitres_stage) :
            for maitre_stage in maitres_stage:
                evaluation.maitre_stage.add(maitre_stage)
        evaluation.save()
        return evaluation


    def update(self, instance, validated_data,*args, **kwargs): 
        if 'note_evaluation' in validated_data.keys():       
            instance.note_evaluation = validated_data.get('note_evaluation', instance.note_evaluation)
        if 'appreciation' in validated_data.keys():
            instance.appreciation= validated_data.get('appreciation', instance.appreciation)
        if 'date' in validated_data.keys():    
            instance.date= validated_data.get('date', instance.date)
        if 'grille' in validated_data.keys():    
            instance.grille= validated_data.get('grille', instance.grille)
        if 'maitre_stage' in validated_data.keys():    
            maitres_stage = validated_data.pop('maitre_stage')   
        if (maitres_stage):
            Evaluation.maitre_stage.through.objects.filter(evaluation_id=instance.id).delete()
            for maitre_stage in maitres_stage :
                instance.maitre_stage.add(maitre_stage)
        instance.save()
        return instance
  
    
class EvaluationPartielleSerializer(serializers.ModelSerializer):
    evaluation = EvaluationSerializer()

    class Meta:
        model=EvaluationPartielle
        fields="__all__"


    def create(self, validated_data):
        if 'stagiaire_pedagogique' in validated_data.keys():
            stagiaire_pedagogique = validated_data.pop('stagiaire_pedagogique')
        if 'projet' in validated_data.keys():
            projet = validated_data.pop('projet')
        if EvaluationPartielle.objects.filter(projet=projet, stagiaire_pedagogique=stagiaire_pedagogique).exists():
            raise serializers.ValidationError('Cette évaluation a déjà été faite')
            return projet
        evaluation_data = validated_data.pop('evaluation')
        maitres_stage = evaluation_data.pop('maitre_stage')
        evaluation = Evaluation.objects.create(**evaluation_data)
        if(maitres_stage):
            for maitre_stage in maitres_stage:
                evaluation.maitre_stage.add(maitre_stage)
        evaluation.save()
        evaluation_partielle= EvaluationPartielle.objects.create(projet=projet, stagiaire_pedagogique=stagiaire_pedagogique, evaluation=evaluation,**validated_data)
        return evaluation_partielle


    def update(self, instance, validated_data,*args, **kwargs):    
        if 'projet' in validated_data.keys():
            instance.projet= validated_data.get('projet', instance.projet)
        if 'stagiaire_pedagogique' in validated_data.keys():
            instance.stagiaire_pedagogique= validated_data.get('stagiaire_pedagogique', instance.stagiaire_pedagogique)
        if 'evaluation' in validated_data.keys():  
            evaluation = validated_data.pop('evaluation')
        if 'maitre_stage' in evaluation:
            maitres_stage = evaluation.pop('maitre_stage')
        evaluation_serializer = EvaluationSerializer(data = evaluation,partial=True)
        if evaluation_serializer.is_valid():
            evaluation = evaluation_serializer.update(instance=instance.evaluation, validated_data=evaluation_serializer.validated_data)
        instance.save()
        return instance  
    

class EvaluationFinaleSerializer(serializers.ModelSerializer):
    evaluation = EvaluationSerializer()

    class Meta:
        model=EvaluationFinale
        fields="__all__"


    def create(self, validated_data):
        if 'immersion' in validated_data.keys():
            immersion = validated_data.pop('immersion')
        if EvaluationFinale.objects.filter(immersion=immersion).exists():
            raise serializers.ValidationError('Cette évaluation a déjà été faite')
            return projet
        evaluation_data = validated_data.pop('evaluation')
        maitres_stage = evaluation_data.pop('maitre_stage')
        evaluation = Evaluation.objects.create(**evaluation_data)
        if(maitres_stage):
            for maitre_stage in maitres_stage:
                evaluation.maitre_stage.add(maitre_stage)
        evaluation.save()
        evaluation_finale= EvaluationFinale.objects.create(immersion=immersion, evaluation=evaluation,**validated_data)
        return evaluation_finale


    def update(self, instance, validated_data,*args, **kwargs):    
        if 'immersion' in validated_data.keys():
            instance.immersion= validated_data.get('immersion', instance.immersion)
            evaluation = validated_data.pop('evaluation')
        if 'maitre_stage' in evaluation:
            maitres_stage = evaluation.pop('maitre_stage')
        evaluation_serializer = EvaluationSerializer(data = evaluation,partial=True)   
        if evaluation_serializer.is_valid():
            evaluation = evaluation_serializer.update(instance=instance.evaluation, validated_data=evaluation_serializer.validated_data)
        instance.save()
        return instance


class EvaluationApprentissageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=EvaluationApprentissage
        fields="__all__"


    def create(self, validated_data):
        if 'grille' in validated_data.keys():
            grille = validated_data.pop('grille')
        if 'stagiaire_pedagogique' in validated_data.keys():
            stagiaire_pedagogique = validated_data.pop("stagiaire_pedagogique")
        if 'immersion' in validated_data.keys():
            immersion = validated_data.pop("immersion")
        if EvaluationApprentissage.objects.filter(immersion=immersion, stagiaire_pedagogique=stagiaire_pedagogique, grille=grille).exists():
            raise serializers.ValidationError('Cette évaluation a déjà été faite')
        evaluation = EvaluationApprentissage.objects.create(grille=grille, stagiaire_pedagogique=stagiaire_pedagogique, immersion=immersion, **validated_data)
        return evaluation


    def update(self, instance, validated_data,*args, **kwargs): 
        if 'immersion' in validated_data.keys():       
            instance.immersion = validated_data.get('immersion', instance.immersion)
        if 'stagiaire_pedagogique' in validated_data.keys():
            instance.stagiaire_pedagogique= validated_data.get('stagiaire_pedagogique', instance.stagiaire_pedagogique)
        if 'grille' in validated_data.keys():    
            instance.grille= validated_data.get('grille', instance.grille)
        instance.save()
        return instance    
        

class CongeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Conge
        fields="__all__"


    def create(self, validated_data):
        if 'stagiaire_pedagogique' in validated_data.keys():
            stagiaire_pedagogique = validated_data.pop('stagiaire_pedagogique')
        date_debut = validated_data['date_debut']
        date_fin = validated_data['date_fin']
        if Conge.objects.filter(stagiaire_pedagogique=stagiaire_pedagogique, date_debut=date_debut, date_fin=date_fin).exists():
            raise serializers.ValidationError('Ce congé a déjà étét enregistré')    
        conge = Conge.objects.create(stagiaire_pedagogique=stagiaire_pedagogique, **validated_data)
        return conge


    def update(self, instance, validated_data,*args, **kwargs): 
        if 'date_debut' in validated_data.keys():       
            instance.date_debut = validated_data.get('date_debut', instance.date_debut)
        if 'date_fin' in validated_data.keys():
            instance.date_fin= validated_data.get('date_fin', instance.date_fin)
        if 'motif' in validated_data.keys():    
            instance.motif= validated_data.get('motif', instance.motif)
        if 'grille' in validated_data.keys():    
            instance.grille= validated_data.get('grille', instance.grille)
        if 'stagiaire_pedagogique' in validated_data.keys():    
            instance.stagiaire_pedagogique= validated_data.get('stagiaire_pedagogique', instance.stagiaire_pedagogique)
            
        instance.save()
        return instance 
    

#User serializer pour la classe User de django
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"


#reset password serializer
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=100)
    class Meta:
        fields = ['email']


#token serializer
class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(min_length=100)
    class Meta:
        fields = ['token']


class PasswordTokenCheckSerializer(serializers.Serializer):
    token = serializers.CharField(min_length=100)
    uidb =serializers.CharField(max_length=100)
    class Meta:
        fields = ['token','uidb']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']