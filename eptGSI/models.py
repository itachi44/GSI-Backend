from djongo import models
from djongo.storage import GridFSStorage
from django.conf import settings


grid_fs_storage = GridFSStorage(collection='cvs', base_url=''.join([settings.BASE_URL, 'cvs/']))

# Create your models here.



class Compte(models.Model):
    identifiant = models.CharField(max_length=100)
    mot_de_passe = models.CharField(max_length=100)

class Membre(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telephone = models.CharField(max_length=20)
    compte = models.ForeignKey(Compte,related_name="Compte",blank=True,
        null=True, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.prenom + ' '+ self.nom )




class Etudiant(models.Model):
    niveau_etude = models.CharField(max_length = 100)
    adresse = models.CharField(max_length=100)
    cv = models.FileField(upload_to='cvs', storage=grid_fs_storage)
    membre = models.ForeignKey(Membre,related_name="Membre",blank=True,
        null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.membre.prenom + ' '+ self.membre.nom )




# class SousTache(models.Model):
#     _id = models.ObjectIdField()
#     nom_tache = models.CharField(max_length=100)
#     echeance = models.DateField()
#     date_debut = models.DateField()
#     date_fin = models.DateField()
#     descriptif = models.TextField()
#     commentaire = models.TextField()
#     etat = models.BooleanField(default = False)


# class Tache(models.Model):
#     _id = models.ObjectIdField()
#     intitule = models.CharField(max_length=100)
#     sous_taches= models.ArrayField(
#         model_container = SousTache
#                 )

# class Projet(models.Model):
#     _id = models.ObjectIdField()
#     nom_projet = models.CharField(max_length=100)
#     descriptif_projet = models.TextField()
#     taches = models.ArrayField(
#         model_container = Tache
#                 )

# class Planning(models.Model):
#     _id = models.ObjectIdField()
#     projets = models.ArrayField(
#         model_container = Projet
#             )

# class MaitreStage(models.Model):
#     _id = models.ObjectIdField()
#     membre = models.EmbeddedField(
#         model_container = Membre
#     )
#     planning = models.ForeignKey(Planning, on_delete=models.PROTECT)

