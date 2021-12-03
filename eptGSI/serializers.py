from rest_framework import serializers 
from .models import Etudiant, Membre, Compte, Entreprise


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


