from django.contrib import admin
from .models import *


@admin.register(StagiairePedagogique)
class StagiairePedagogiqueAdmin(admin.ModelAdmin):
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

@admin.register(Planning)
class PlanningAdmin(admin.ModelAdmin):
    pass

@admin.register(Alternance)
class AlternanceAdmin(admin.ModelAdmin):
    pass

@admin.register(Immersion)
class ImmersionAdmin(admin.ModelAdmin):
    pass

@admin.register(MaitreStage)
class MaitreStageAdmin(admin.ModelAdmin):
    pass

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    pass

# @admin.register(Programme)
# class ProgrammeAdmin(admin.ModelAdmin):
#     pass

# @admin.register(Activite)
# class ActiviteAdmin(admin.ModelAdmin):
#     pass

# @admin.register(Tache)
# class TacheAdmin(admin.ModelAdmin):
#     pass

# @admin.register(SousTache)
# class SousTacheAdmin(admin.ModelAdmin):
#     pass

# @admin.register(Destinataire)
# class DestinataireAdmin(admin.ModelAdmin):
#     pass

# @admin.register(Evenement)
# class EvenementAdmin(admin.ModelAdmin):
#     pass

# @admin.register(PieceJointe)
# class PieceJointeAdmin(admin.ModelAdmin):
#     pass

# @admin.register(Formateur)
# class FormateurAdmin(admin.ModelAdmin):
#     pass

# @admin.register(Manager)
# class ManagerAdmin(admin.ModelAdmin):
#     pass

# @admin.register(ResponsableImmersion)
# class ResponsableImmersionAdmin(admin.ModelAdmin):
#     pass

# @admin.register(Message)
# class MessageAdmin(admin.ModelAdmin):
#     pass

# @admin.register(GrilleEvaluation)
# class GrilleEvaluationAdmin(admin.ModelAdmin):
#     pass

# @admin.register(Critere)
# class CritereAdmin(admin.ModelAdmin):
#     pass

# @admin.register(Evaluation)
# class EvaluationAdmin(admin.ModelAdmin):
#     pass

# @admin.register(EvaluationPartielle)
# class EvaluationPartielleAdmin(admin.ModelAdmin):
#     pass

# @admin.register(EvaluationFinale)
# class EvaluationFinaleAdmin(admin.ModelAdmin):
#     pass

# @admin.register(EvaluationApprentissage)
# class EvaluationApprentissageAdmin(admin.ModelAdmin):
#     pass

# @admin.register(Conge)
# class CongeAdmin(admin.ModelAdmin):
#     pass