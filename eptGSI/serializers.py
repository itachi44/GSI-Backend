from rest_framework import serializers 
from .models import Etudiant, Membre, Compte


class CompteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Compte
        fields='__all__'


class MembreSerializer(serializers.ModelSerializer):
    compte = CompteSerializer()

    class Meta:
        model=Membre
        fields='__all__'


class EtudiantSerializer(serializers.ModelSerializer):
    membre = MembreSerializer()

    class Meta:
        model=Etudiant
        fields=["niveau_etude","adresse","cv","membre"]
