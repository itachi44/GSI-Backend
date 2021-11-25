from django.db import models
from djongo.storage import GridFSStorage
from django.conf import settings
from djangotoolbox.fields import ListField



cv_grid_fs_storage = GridFSStorage(collection='cvs', base_url=''.join([settings.BASE_URL, 'cvs/']))
rapport_grid_fs_storage = GridFSStorage(collection='rapports', base_url=''.join([settings.BASE_URL, 'rapports/']))

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


class Programme(models.Model):
    pass

class Planning(models.Model):
    pass


class Projet(models.Model):
    nom_projet = models.CharField(max_length=100)
    descriptif_projet = models.TextField()
    programme = models.ForeignKey(Programme, related_name = "Programme", on_delete=models.PROTECT)
    planning = models.ForeignKey(Planning, related_name = "Planning", on_delete=models.PROTECT)


class Tache(models.Model):
    intitule = models.CharField(max_length=100)
    projet = models.ForeignKey(Projet, related_name = "Projet", on_delete=models.PROTECT)


class SousTache(models.Model):
    nom_tache = models.CharField(max_length=100)
    echeance = models.DateField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    descriptif = models.TextField()
    commentaire = models.TextField()
    etat = models.BooleanField(default = False)
    tache = models.ForeignKey(Tache, related_name = "Tache", on_delete=models.PROTECT)

class Immersion(models.Model):
    description = models.TextField()
    annee = models.CharField(max_length=100)
    date_debut = models.DateField()
    date_fin = models.DateField()
    programme = models.ForeignKey(Programme, related_name = "Immersion", blank = True, null = True, on_delete=models.CASCADE)


class Etudiant(models.Model):
    niveau_etude = models.CharField(max_length = 100)
    adresse = models.CharField(max_length=100)
    cv = models.FileField(upload_to='cvs', storage=cv_grid_fs_storage)
    membre = models.ForeignKey(Membre,related_name="Membre",blank=True,
        null=True, on_delete=models.CASCADE)
    planning = models.ForeignKey(Planning, related_name="planning", blank = True, null = True, on_delete=models.CASCADE)
    immersion = models.ForeignKey(Immersion, related_name = "Immersion", on_delete=models.PROTECT)
    rapport_stage = models.FileField(upload_to='rapports', storage=rapport_grid_fs_storage, null=True,blank = True)

    def __str__(self):
        return str(self.membre.prenom + ' '+ self.membre.nom )


class Entreprise(models.Model):
    nom_entreprise = models.CharField(max_length=100)
    localisation = models.CharField(max_length=100)
    domaine_expertise = models.CharField(max_length=100)


class Evenement(models.Model):
    details = models.TextField()
    intitule = models.CharField(max_length=100)
    date = models.DateField()
    destinataires = models.ListField()


class MembreDept(models.Model):
    membre = models.ForeignKey(Membre, related_name = "MembreDept" , on_delete=models.CASCADE)


class MaitreStage(models.Model):
    membre = models.ForeignKey(Membre, related_name = "MaitreStage", on_delete=models.CASCADE)
    planning = models.ForeignKey(Planning, related_name = "MaitreStage", blank = True, null = True, on_delete=models.PROTECT)


class RespEntreprise(models.Model): 
    membre = models.ForeignKey(Membre, related_name = "RespEntreprise", on_delete=models.CASCADE)


class ChefDept(models.Model):
    membre = models.ForeignKey(Membre, related_name = "ChefDept", on_delete=models.CASCADE)

class Message(models.Model):
    intitule = models.CharField(max_length=100)
    contenu = models.TextField()
    etudiant = models.ForeignKey(Etudiant, related_name = "Message", on_delete=models.PROTECT)


class Evaluation(models.Model):
    note_evaluation = models.FloatField()
    appreciation = models.TextField()
    etudiant = models.ForeignKey(Etudiant, related_name = "Evaluation", on_delete=models.PROTECT)
    maitre_de_stage = models.ForeignKey(MaitreStage, related_name = "Evaluation", on_delete = models.PROTECT)

