from django.contrib import admin

# # Register your models here.

from .models import Etudiant, Membre, Compte,Entreprise, Programme


# ############################################# affichage indépendamment des relations ##################################################


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    pass

@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    pass

@admin.register(Compte)
class CompteAdmin(admin.ModelAdmin):
    pass

@admin.register(Entreprise)
class CompteAdmin(admin.ModelAdmin):
    pass

@admin.register(Programme)
class CompteAdmin(admin.ModelAdmin):
    pass



# @admin.register(Etudiant)
# class EtudiantAdmin(admin.ModelAdmin):
#     list_display = ('nom', 'prenom','email','date_naissance','lieu_naissance')
#     search_fields=['nom', 'prenom','email']
#     list_filter = ['lieu_naissance'] 
#     extra=5
#     readonly_fields = ["password", "email"] #champs autorisées en lecture seule, non modifiable par le superuser

# @admin.register(Matiere)
# class MatiereAdmin(admin.ModelAdmin):
#     list_display = ('nom_matiere', 'code_matiere','coef_matiere','credit_matiere','quota_horaire','desc_matiere')
#     search_fields=['nom_matiere', 'code_matiere']
#     list_filter = ['coef_matiere','credit_matiere','quota_horaire'] 
    



# ############################################# relations Many to Many ##################################################


# #une relation ManyTo Many suppose qu'il existe une table intermédiaire
# class ProfesseurDepartementInline(admin.TabularInline):
#     model = Professeur.departments.through # la requête passe par la table intermédiaire.
#     extra = 5 #nbre de lignes additionnelles
#     search_fields=['nom', 'nom_dept','prenom']
#     verbose_name = "Professeur"
#     verbose_name_plural = "Professeurs"


# #décorateur pour l'affichage
# @admin.register(Departement)
# class DepartementAdmin(admin.ModelAdmin):
#     list_display = ('nom_dept', 'email_dept','numero_dept','desc_dept')

#     inlines = [ProfesseurDepartementInline]



# class MatiereProfesseurInline(admin.TabularInline):
#     model = Matiere.professeurs.through 
#     extra = 5
#     search_fields=['nom_matiere', 'code_matiere','nom','prenom']
#     list_filter = ['coef_matiere','credit_matiere','quota_horaire'] 
#     verbose_name = "Matière"
#     verbose_name_plural = "Matières"

# @admin.register(Professeur)
# class DepartementAdmin(admin.ModelAdmin):
#     search_fields=['nom', 'prenom','email','contact_prof']
#     list_filter = ['date_adhesion'] 
#     list_display = ('nom', 'prenom','email','contact_prof','date_adhesion','chef_departement')
#     inlines = [MatiereProfesseurInline]


    



# ############################################# relations Foreign key ##################################################


# @admin.register(Classe)
# class AuthorAdmin(admin.ModelAdmin):
#     search_fields=['nom_classe', 'desc_classe']
#     list_filter = ['departement'] 
#     list_display = ('nom_classe', 'desc_classe','departement')
#     #limitation du nombre de classe à max 4
#     #on remplit les classes dans la BD puis on retire la permission d'ajouter des nouvelles classes
#     #permission
#     #def has_add_permission(self, request,obj=None):
#         #return False


# @admin.register(UE_matiere)
# class AuthorAdmin(admin.ModelAdmin):
#     search_fields=['nom_UE','classe','matiere']
#     list_filter = ['matiere','classe'] 
#     list_display = ('nom_UE', 'code_UE','classe','matiere')


# @admin.register(Inscription)
# class AuthorAdmin(admin.ModelAdmin):
#     search_fields=['annee_scolaire','etudiant','classe']
#     list_filter = ['annee_scolaire'] 
#     list_display = ('annee_scolaire','etudiant','classe')




