# from rest_framework.viewsets import ModelViewSet
# from .serializers import EtudiantSerializer
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from .models import Etudiant
# import django_filters.rest_framework
# from rest_framework.permissions import IsAuthenticated




# #Vues API

# #API GET POUR OBTENIR LES INFOS DE TOUS LES ETUDIANTS 

# class etudiantViewSet(ModelViewSet):
#     queryset=Etudiant.objects.all()
#     serializer_class= EtudiantSerializer
#     permission_classes=(IsAuthenticated,)
#     filter_fields=["date_naissance","lieu_naissance"]


# #API GET POUR OBTENIR LES INFOS DES ETUDIANTS D'UNE CLASSE

# class etudiantClasseViewSet(ModelViewSet):
#     serializer_class= EtudiantSerializer
#     permission_classes=(IsAuthenticated,)
#     filter_fields=["date_naissance","lieu_naissance"]


#     #on fait un override de la méthode get_queryset
#     def get_queryset(self, *args, **kwargs):
#         #par défaut on affiche tous les étudiants
#         queryset=Etudiant.objects.all()
#         classe = self.request.query_params.get("classe")
#         if classe!=None:
#             queryset =Inscription.objects.filter(classe__nom_classe=classe)
#             name_list=list()
#             for obj in queryset:
#                 name_list.append(obj.etudiant.nom)
#                 print(obj.etudiant.nom)
#             #on récupère les étudiants
#             etudiants = Etudiant.objects.filter(nom__in=name_list)

#             return etudiants
#         return queryset

