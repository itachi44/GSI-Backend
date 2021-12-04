from django.contrib import admin
from .models import *


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
class EntrepriseAdmin(admin.ModelAdmin):
    pass

@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    pass

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    pass

@admin.register(MaitreStage)
class MaitreStageAdmin(admin.ModelAdmin):
    pass

