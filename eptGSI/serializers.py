from rest_framework import serializers 
from .models import Etudiant, Membre, Compte


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


    # def validate_email(self, value):
    #     if Membre.objects.filter(email=value).exists():
    #         raise serializers.ValidationError('Membre already exists')
    #     return value


class EtudiantSerializer(serializers.ModelSerializer):
    membre = MembreSerializer()

    class Meta:
        model=Etudiant
        fields=["niveau_etude","adresse","cv","membre"]

    def create(self, validated_data):
        print(validated_data)
        membre = validated_data.pop('membre')
        print(membre)
        # etudiant = Etudiant.objects.create(**validated_data)
        # for track_data in tracks_data:
        #     Track.objects.create(album=album, **track_data)
        # return album
    def update(self, instance, validated_data):
        print(validated_data)