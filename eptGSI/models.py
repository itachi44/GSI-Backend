from django.db import models
from djongo.storage import GridFSStorage
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator
from django.utils.timezone import now
import os


cv_grid_fs_storage = GridFSStorage(collection='media/cvs', base_url=''.join([settings.BASE_URL, 'media/cvs/']))
rapport_grid_fs_storage = GridFSStorage(collection='media/rapports', base_url=''.join([settings.BASE_URL, 'rapports/']))
pj_grid_fs_storage = GridFSStorage(collection='media/pjs', base_url=''.join([settings.BASE_URL, 'pjs/']))
convention_grid_fs_storage = GridFSStorage(collection='media/conventions', base_url=''.join([settings.BASE_URL, 'media/conventions/']))



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


class StagiairePedagogique(models.Model):
    niveau_etude = models.CharField(max_length = 100)
    adresse = models.CharField(max_length=100)
    cv = models.FileField(upload_to='media/cvs', storage=cv_grid_fs_storage,blank=True,null=True)
    membre = models.ForeignKey(Membre,related_name="StagiairePedagogique", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.membre.prenom + ' '+ self.membre.nom )

    __repr__=__str__
    
    #methode pour récupérer le cv
    def get_cv(self):
        if self.cv:
            cv=self.cv
            cv_data=cv.read()
            url=cv.url
            extension=cv.name.split(".")[1]
            image_id=url.split('/')[5]
            #1-verifier si le répertoire existe sinon le créer
            parent_dir=os.getcwd()
            if not os.path.isdir(os.getcwd()+"/media"):
                os.mkdir(os.path.join(parent_dir, "media"), mode = 0o777)
            if not os.path.isdir(os.getcwd()+"/media/cvs"):
                os.mkdir(os.getcwd()+"/media/cvs", mode = 0o777)
            #vérifier que le fichier n'existe pas encore 
            image_path=os.getcwd()+"/media/cvs"+'/'+image_id+"."+extension
            if os.path.isfile(image_path):
                print("le fichier existe déja")
            else:
            #créer le fichier
                with open(image_path, "wb+") as file:
                    file.write(cv_data)
            return cv.url+'.'+extension


class Entreprise(models.Model):
    nom_entreprise = models.CharField(max_length=100)
    localisation = models.CharField(max_length=100)
    domaine_expertise = models.CharField(max_length=100,blank=True,
        null=True)

    def __str__(self):
        return str(self.nom_entreprise)

    __repr__=__str__


class Planning(models.Model):
    date_creation = models.DateField()
    
    def __str__(self):
        return str('Planning '+ str(self.id))

    __repr__=__str__


class Alternance(models.Model):
    description = models.TextField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    convention = models.FileField(upload_to='media/conventions', storage=convention_grid_fs_storage,blank=True,
        null=True)
    entreprise= models.ForeignKey(Entreprise, related_name="Alternance", on_delete=models.PROTECT)
    planning = models.ForeignKey(Planning, related_name="Alternance",blank=True,
        null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str('Alternance '+ self.entreprise.nom_entreprise+' '+ str(self.date_debut))
    
    __repr__=__str__
    
    #methode pour récupérer la convention de stage
    def get_convention(self):
        if self.convention:
            convention=self.convention
            convention_data=convention.read()
            url=convention.url
            extension=convention.name.split(".")[1]
            image_id=url.split('/')[5]
            #1-verifier si le répertoire existe sinon le créer
            parent_dir=os.getcwd()
            if not os.path.isdir(os.getcwd()+"/media"):
                os.mkdir(os.path.join(parent_dir, "media"), mode = 0o777)
            if not os.path.isdir(os.getcwd()+"/media/conventions"):
                os.mkdir(os.getcwd()+"/media/conventions", mode = 0o777)
            #vérifier que le fichier n'existe pas encore 
            image_path=os.getcwd()+"/media/conventions"+'/'+image_id+"."+extension
            if os.path.isfile(image_path):
                print("le fichier existe déjà")
            else:
            #créer le fichier
                with open(image_path, "wb+") as file:
                    file.write(convention_data)
            return convention.url+'.'+extension

 
class Immersion(models.Model):
    annee = models.CharField(max_length=100)
    date_debut = models.DateField()
    date_fin = models.DateField()
    rapport_stage = models.FileField(upload_to='rapports', storage=rapport_grid_fs_storage,blank= True,
        null=True)
    stagiaire_pedagogique = models.ForeignKey(StagiairePedagogique, related_name="Immersion", on_delete=models.PROTECT)
    alternance = models.ForeignKey(Alternance, related_name="Immersion", on_delete=models.PROTECT)

    def __str__(self):
        return str('Immersion '+ self.stagiaire_pedagogique.membre.prenom+' '+ self.stagiaire_pedagogique.membre.nom+' '+ self.annee )

    __repr__=__str__
    
    #methode pour récupérer le rapport de stage
    def get_rapport(self):
        if self.rapport_stage:
            rapport_stage=self.rapport_stage
            rapport_data=rapport_stage.read()
            url=rapport_stage.url
            extension=rapport_stage.name.split(".")[1]
            image_id=url.split('/')[5]
            #1-verifier si le répertoire existe sinon le créer
            parent_dir=os.getcwd()
            if not os.path.isdir(os.getcwd()+"/media"):
                os.mkdir(os.path.join(parent_dir, "media"), mode = 0o777)
            if not os.path.isdir(os.getcwd()+"/media/rapports"):
                os.mkdir(os.getcwd()+"/media/rapports", mode = 0o777)
            #vérifier que le fichier n'existe pas encore 
            image_path=os.getcwd()+"/media/rapports"+'/'+image_id+"."+extension
            if os.path.isfile(image_path):
                print("le fichier existe déja")
            else:
            #créer le fichier
                with open(image_path, "wb+") as file:
                    file.write(rapport_data)
            return rapport_stage.url+'.'+extension


class MaitreStage(models.Model):
    membre = models.ForeignKey(Membre, related_name = "MaitreStage", on_delete=models.CASCADE)
    entreprise = models.ForeignKey(Entreprise, related_name="MaitreStage", on_delete=models.PROTECT)

    def __str__(self):
        return str(self.membre.prenom+' '+ self.membre.nom)

    __repr__=__str__


class Projet(models.Model):
    nom_projet = models.CharField(max_length=100)
    descriptif_projet = models.TextField(blank=True,null=True)
    etat = models.CharField(max_length=100,blank=True,null=True)
    budget = models.CharField(max_length=100, blank=True, null=True)
    duree = models.CharField(max_length=100, blank=True, null=True)
    planning = models.ForeignKey(Planning, related_name = "Projet", on_delete=models.PROTECT)
    responsables_projet = models.ManyToManyField(MaitreStage)

    def __str__(self):
        return str(self.nom_projet)

    __repr__=__str__


class Programme(models.Model):
    annee = models.CharField( max_length=100)
    stagiaire_pedagogique = models.ForeignKey(StagiairePedagogique, related_name="Programme", on_delete=models.PROTECT)
    maitre_stage = models.ForeignKey(MaitreStage, related_name="Programme", on_delete=models.PROTECT)
    projets = models.ManyToManyField(Projet)
    
    def __str__(self):
        return str('Programme '+ self.stagiaire_pedagogique.membre.prenom+' '+ self.stagiaire_pedagogique.membre.nom+ ' '+ self.annee )
    
    __repr__=__str__


class Activite(models.Model):
    nom_activite = models.CharField(max_length=100)
    date_debut = models.DateField()
    date_fin = models.DateField(blank=True, null=True)
    cadre = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    cout = models.CharField(max_length=100, blank=True, null=True)
    ressources = models.TextField(blank=True, null=True)
    projet = models.ForeignKey(Projet, related_name="Activite", on_delete=models.PROTECT)
    
    def __str__(self):
        return str(self.nom_activite)
    
    __repr__=__str__


class Tache(models.Model):
    intitule = models.CharField(max_length=100)
    activite = models.ForeignKey(Activite, related_name = "Tache",on_delete=models.PROTECT)
    stagiaire_pedagogique = models.ForeignKey(StagiairePedagogique, related_name="Tache", on_delete=models.PROTECT)

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
    technologies = models.TextField(blank=True,null=True)
    langages = models.TextField(blank=True,null=True)
    tache = models.ForeignKey(Tache, related_name = "SousTache",blank=True,null=True, on_delete=models.CASCADE)

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
    type = models.CharField(max_length=100)
    destinataires = models.ManyToManyField(Destinataire)

    def __str__(self):
        return str(self.intitule)

    __repr__=__str__


class PieceJointe(models.Model):
    fichier = models.FileField(upload_to='pjs', storage=pj_grid_fs_storage)
    evenement = models.ForeignKey(Evenement, related_name="PieceJointe", on_delete = models.PROTECT)

    def __str__(self):
        return str('Piece Jointe '+ self.evenement.intitule)

    __repr__=__str__
    
    #methode pour récupérer une pj
    def get_pj(self):
        if self.fichier:
            fichier=self.fichier
            pj_data=fichier.read()
            url=fichier.url
            extension=fichier.name.split(".")[1]
            image_id=url.split('/')[5]
            #1-verifier si le répertoire existe sinon le créer
            parent_dir=os.getcwd()
            if not os.path.isdir(os.getcwd()+"/media"):
                os.mkdir(os.path.join(parent_dir, "media"), mode = 0o777)
            if not os.path.isdir(os.getcwd()+"/media/pjs"):
                os.mkdir(os.getcwd()+"/media/pjs", mode = 0o777)
            #vérifier que le fichier n'existe pas encore 
            image_path=os.getcwd()+"/media/pjs"+'/'+image_id+"."+extension
            if os.path.isfile(image_path):
                print("le fichier existe déja")
            else:
            #créer le fichier
                with open(image_path, "wb+") as file:
                    file.write(pj_data)
            return fichier.url+'.'+extension


class Formateur(models.Model):
    membre = models.ForeignKey(Membre, related_name = "Formateur", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.membre.prenom + ' '+ self.membre.nom)

    __repr__=__str__


class Manager(models.Model): 
    maitre_stage = models.ForeignKey(MaitreStage, related_name = "Manager",on_delete=models.CASCADE)

    def __str__(self):
        return str(self.maitre_stage.membre.prenom + ' '+ self.maitre_stage.membre.nom)

    __repr__=__str__


class ResponsableImmersion(models.Model):
    formateur = models.ForeignKey(Formateur, related_name = "ResponsableImmersion", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.formateur.membre.prenom + ' '+ self.formateur.membre.nom)

    __repr__=__str__


class Message(models.Model):
    intitule = models.CharField(max_length=100)
    contenu = models.TextField()
    etudiant = models.ForeignKey(Etudiant, related_name = "Message", on_delete=models.PROTECT)
    date_envoi = models.DateTimeField(default=now, editable=False)  #auto_now_add = True

    def __str__(self):
        return str(self.intitule)

    __repr__=__str__


class GrilleEvaluation(models.Model):
    intitule = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.intitule)
    
    __repr__=__str__


class Critere(models.Model):
    label_critere = models.CharField(max_length=100)
    pourcentage = models.CharField(max_length=100)
    grille = models.ForeignKey(GrilleEvaluation, related_name='Critere', blank=True, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.label_critere)
    
    __repr__=__str__


class Evaluation(models.Model):
    note_evaluation = models.FloatField()
    appreciation = models.TextField()
    date = models.DateField(default=now)
    maitre_stage = models.ManyToManyField(MaitreStage)
    grille = models.ForeignKey(GrilleEvaluation, related_name='Evaluation', on_delete=models.PROTECT)

    def __str__(self):
        return str('Evaluation '+ str(self.id))

    __repr__=__str__


class EvaluationPartielle(models.Model):
    projet = models.ForeignKey(Projet, related_name='EvaluationPartielle', on_delete=models.PROTECT)
    stagiaire_pedagogique = models.ForeignKey(StagiairePedagogique, related_name='EvaluationPartielle', on_delete=models.PROTECT)
    evaluation = models.ForeignKey(Evaluation, related_name='EvaluationPartielle', on_delete=models.CASCADE)
    
    def __str__(self):
        return str('Evaluation Partielle '+ self.stagiaire_pedagogique.membre.prenom +' '+ self.stagiaire_pedagogique.membre.nom + ' '+ str(self.id))
    
    __repr__=__str__


class EvaluationFinale(models.Model):
    immersion = models.ForeignKey(Immersion, related_name='EvaluationFinale', on_delete=models.PROTECT)
    evaluation = models.ForeignKey(Evaluation, related_name='EvaluationFinale', on_delete = models.CASCADE)
    
    def __str__(self):
        return str('Evaluation Finale '+ self.immersion.stagiaire_pedagogique.membre.prenom + ' '+ self.immersion.stagiaire_pedagogique.membre.nom + ' '+ self.immersion.annee)
    
    __repr__=__str__


class EvaluationApprentissage(models.Model):
    grille = models.ForeignKey(GrilleEvaluation, related_name='EvaluationApprentissage', on_delete=models.PROTECT)
    stagiaire_pedagogique = models.ForeignKey(StagiairePedagogique, related_name='EvaluationApprentissage', on_delete=models.PROTECT)
    immersion = models.ForeignKey(Immersion, related_name='EvaluationApprentissage', on_delete=models.PROTECT)
    
    def __str__(self):
        return str('Evaluation Immersion ' + self.immersion.annee + ' ' + self.stagiaire_pedagogique.membre.prenom + ' '+ self.stagiaire_pedagogique.membre.nom)
    
    __repr__=__str__


class Conge(models.Model):
    date_debut = models.DateField()
    date_fin = models.DateField()
    motif = models.TextField()
    stagiaire_pedagogique = models.ForeignKey(StagiairePedagogique, related_name='Conge', on_delete = models.PROTECT)
    
    def __str__(self):
        return str('Conge '+ self.stagiaire_pedagogique.membre.prenom + ' '+  self.stagiaire_pedagogique.membre.nom + ' '+ str(self.id))    