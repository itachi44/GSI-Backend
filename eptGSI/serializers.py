from rest_framework import serializers 
from .models import *


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
            'telephone': {'validators': []}
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

        return etudiant

    def update(self, instance, validated_data,*args, **kwargs):        
        membre_data = validated_data.pop('membre')
        membre_serializer = MembreSerializer(data = membre_data,partial=True)        
        instance.niveau_etude = validated_data.get('niveau_etude', instance.niveau_etude)
        instance.adresse = validated_data.get('adresse', instance.adresse)
        if instance.cv:
            instance.cv.delete()
        instance.cv = validated_data.get('cv', instance.cv)
        instance.save()
        if membre_serializer.is_valid():
            membre = membre_serializer.update(instance=instance.membre, validated_data=membre_serializer.validated_data)

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
        compte = validated_data.pop('compte')
        email=validated_data.get("email")
        telephone=validated_data.get("telephone")
        identifiant=validated_data.get("identifiant")
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
        maitre_stage= MaitreStage.objects.create(membre=membre,**validated_data)


        return maitre_stage


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


class PlanningSerializer(serializers.ModelSerializer):

    class Meta:
        model=Planning
        fields=["annee","etudiant","maitreStage"]


    def create(self, validated_data):
        print(validated_data)
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
        if Projet.objects.filter(etudiant=programme, nom_projet=validated_data["nom_projet"],planning=planning).exists() :
            raise serializers.ValidationError('Ce Planning existe déja')
            return validated_data
        planning = Planning.objects.create(etudiant=etudiant,maitreStage=maitre_de_stage,**validated_data)

        return planning

    def update(self, instance, validated_data,*args, **kwargs):        
        instance.annee = validated_data.get('annee', instance.annee)
        instance.etudiant= validated_data.get('etudiant', instance.etudiant)
        instance.maitreStage= validated_data.get('maitreStage', instance.maitreStage)

        instance.save()
        return instance


