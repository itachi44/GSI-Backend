from django.db import models
from djongo.storage import GridFSStorage
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator
from django.utils.timezone import now
import os


cv_grid_fs_storage = GridFSStorage(collection='cvs', base_url=''.join([settings.BASE_URL, 'cvs/']))
rapport_grid_fs_storage = GridFSStorage(collection='rapports', base_url=''.join([settings.BASE_URL, 'rapports/']))
pj_grid_fs_storage = GridFSStorage(collection='pjs', base_url=''.join([settings.BASE_URL, 'pjs/']))



class Compte(models.Model):
    identifiant = models.CharField(max_length=100)
    mot_de_passe = models.CharField(max_length=100)


class Membre(models.Model):
    phone_regex=RegexValidator(regex=r'^(\+221)?[- ]?(77|70|76|78)[- ]?([0-9]{3})[- ]?([0-9]{2}[- ]?){2}$', message="le numero de telephone est invalide!") #phone number validator

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telephone = models.CharField(validators=[phone_regex],max_length=20)
    compte = models.ForeignKey(Compte,related_name="Membre",blank=True,
        null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.prenom + ' '+ self.nom )
    
    __repr__=__str__


class Etudiant(models.Model):
    niveau_etude = models.CharField(max_length = 100)
    adresse = models.CharField(max_length=100)
    cv = models.FileField(upload_to='cvs', storage=cv_grid_fs_storage,blank=True,
        null=True)
    membre = models.ForeignKey(Membre,related_name="Etudiant", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.membre.prenom + ' '+ self.membre.nom )

    __repr__=__str__
    
    #methode pour récupérer le cv
    def get_cv(self):
        cv=self.cv
        cv_data=cv.read()
        url=cv.url
        extension=cv.name.split(".")[1]
        image_id=url.split('/')[4]
        #1-verifier si le répertoire existe sinon le créer
        directory="cvs"
        parent_dir=os.getcwd()
        path = os.path.join(parent_dir, directory)
        if not os.path.isdir(os.getcwd()+"/cvs"):
            os.mkdir(path, mode = 0o777)
        #vérifier que le fichier n'existe pas encore 
        image_path=path+'/'+image_id+"."+extension
        if os.path.isfile(image_path):
            print("le fichier existe déja")
        else:
        #créer le fichier
            with open(image_path, "wb+") as file:
                file.write(cv_data)
        #sauvegarder dans un repertoire avec l'id



class Entreprise(models.Model):
    nom_entreprise = models.CharField(max_length=100)
    localisation = models.CharField(max_length=100)
    domaine_expertise = models.CharField(max_length=100,blank=True,
        null=True)

    def __str__(self):
        return str(self.nom_entreprise)

    __repr__=__str__


class Programme(models.Model):
    
    def __str__(self):
        return str('Programme '+ str(self.id))

    __repr__=__str__


class Immersion(models.Model):
    description = models.TextField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    entreprise= models.ForeignKey(Entreprise, related_name="Immersion", on_delete=models.CASCADE)
    programme = models.ForeignKey(Programme, related_name="Immersion", on_delete=models.CASCADE)

    def __str__(self):
        return str('Immersion '+ self.entreprise.nom_entreprise+' '+ str(self.id))
    
    __repr__=__str__
 
class Stage(models.Model):
    annee = models.DateField(max_length=100)
    date_debut = models.DateField()
    date_fin = models.DateField()
    rapport_stage = models.FileField(upload_to='rapports', storage=rapport_grid_fs_storage,blank= True,
        null=True)
    etudiant = models.ForeignKey(Etudiant, related_name="Stage", on_delete=models.CASCADE)
    immersion = models.ForeignKey(Immersion, related_name="Stage", on_delete=models.CASCADE)

    def __str__(self):
        return str('Stage '+ self.etudiant.membre.prenom+' '+ self.etudiant.membre.nom+' '+ self.annee )

    __repr__=__str__

class MaitreStage(models.Model):
    membre = models.ForeignKey(Membre, related_name = "MaitreStage", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.membre.prenom+' '+ self.membre.nom)

    __repr__=__str__


class Projet(models.Model):
    nom_projet = models.CharField(max_length=100)
    descriptif_projet = models.TextField(blank=True,
        null=True)
    etat = models.CharField(max_length=100,blank=True,
        null=True)
    programme = models.ForeignKey(Programme, related_name = "Projet", on_delete=models.PROTECT)

    def __str__(self):
        return str(self.nom_projet)

    __repr__=__str__


class Planning(models.Model):
    annee = models.DateField()
    etudiant = models.ForeignKey(Etudiant, related_name="Planning", on_delete=models.CASCADE)
    maitreStage = models.ForeignKey(MaitreStage, related_name="Planning", on_delete=models.CASCADE)
    projets = models.ManyToManyField(Projet)
    
    def __str__(self):
        return str('Planning '+ self.etudiant.membre.prenom+' '+ self.etudiant.membre.nom+ ' '+ self.annee )
    
    __repr__=__str__

class Tache(models.Model):
    intitule = models.CharField(max_length=100)
    projet = models.ForeignKey(Projet, related_name = "Tache",on_delete=models.PROTECT)

    def __str__(self):
        return str(self.intitule)
    
    __repr__=__str__


class SousTache(models.Model):
    nom_tache = models.CharField(max_length=100)
    echeance = models.DateField(blank=True,null=True)
    date_debut = models.DateField(blank=True,null=True)
    date_fin = models.DateField(blank=True,null=True)
    descriptif = models.TextField(blank=True,null=True)
    commentaire = models.TextField(blank=True,null=True)
    etat = models.BooleanField(default = False)
    tache = models.ForeignKey(Tache, related_name = "SousTache",blank=True,null=True, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.nom_tache)

    __repr__=__str__


class Destinataire(models.Model):
    label=models.CharField(max_length=100)

    def __str__(self):
        return str(self.label)

    __repr__=__str__


class Evenement(models.Model):
    details = models.TextField()
    intitule = models.CharField(max_length=100)
    date = models.DateField()
    destinataires = models.ManyToManyField(Destinataire)

    def __str__(self):
        return str(self.intitule)

    __repr__=__str__


class PieceJointe(models.Model):
    fichier = models.FileField(upload_to='pjs', storage=pj_grid_fs_storage)
    evenement = models.ForeignKey(Evenement, related_name="PieceJointe", on_delete = models.CASCADE)

    def __str__(self):
        return str('Piece Jointe '+ self.evenement.intitule)

    __repr__=__str__

class MembreDept(models.Model):
    membre = models.ForeignKey(Membre, related_name = "MembreDept", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.membre.prenom + ' '+ self.membre.nom)

    __repr__=__str__

class RespEntreprise(models.Model): 
    membre = models.ForeignKey(Membre, related_name = "RespEntreprise",on_delete=models.CASCADE)

    def __str__(self):
        return str(self.membre.prenom + ' '+ self.membre.nom)

    __repr__=__str__


class ChefDept(models.Model):
    membre = models.ForeignKey(Membre, related_name = "ChefDept", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.membre.prenom + ' '+ self.membre.nom)

    __repr__=__str__


class Message(models.Model):
    intitule = models.CharField(max_length=100)
    contenu = models.TextField()
    etudiant = models.ForeignKey(Etudiant, related_name = "Message", on_delete=models.PROTECT)
    date_envoi = models.DateTimeField(default=now, editable=False)  #auto_now_add = True

    def __str__(self):
        return str(self.intitule)

    __repr__=__str__


class Evaluation(models.Model):
    note_evaluation = models.FloatField()
    appreciation = models.TextField()
    etudiant = models.ForeignKey(Etudiant, related_name = "Evaluation", on_delete=models.PROTECT)
    maitre_de_stage = models.ForeignKey(MaitreStage, related_name = "Evaluation", on_delete = models.PROTECT)

    def __str__(self):
        return str('Evaluation '+ self.etudiant.membre.prenom + ' '+ self.etudiant.membre.nom)

    __repr__=__str__

