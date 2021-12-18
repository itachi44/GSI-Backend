# Generated by Django 2.2.8 on 2021-12-18 14:20

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import djongo.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Compte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifiant', models.CharField(max_length=100)),
                ('mot_de_passe', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Destinataire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Entreprise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_entreprise', models.CharField(max_length=100)),
                ('localisation', models.CharField(max_length=100)),
                ('domaine_expertise', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Etudiant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('niveau_etude', models.CharField(max_length=100)),
                ('adresse', models.CharField(max_length=100)),
                ('cv', models.FileField(blank=True, null=True, storage=djongo.storage.GridFSStorage(base_url='http://127.0.0.1:8000/media/cvs/', collection='media/cvs'), upload_to='media/cvs')),
            ],
        ),
        migrations.CreateModel(
            name='Evenement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.TextField()),
                ('intitule', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('destinataires', models.ManyToManyField(to='eptGSI.Destinataire')),
            ],
        ),
        migrations.CreateModel(
            name='Immersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('entreprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Immersion', to='eptGSI.Entreprise')),
            ],
        ),
        migrations.CreateModel(
            name='MaitreStage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Membre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('telephone', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='le numero de telephone est invalide!', regex='^(\\+221)?[- ]?(77|70|76|78)[- ]?([0-9]{3})[- ]?([0-9]{2}[- ]?){2}$')])),
                ('compte', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Membre', to='eptGSI.Compte')),
            ],
        ),
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=200)),
                ('uidb', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Projet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_projet', models.CharField(max_length=100)),
                ('descriptif_projet', models.TextField(blank=True, null=True)),
                ('etat', models.CharField(blank=True, max_length=100, null=True)),
                ('programme', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Projet', to='eptGSI.Programme')),
            ],
        ),
        migrations.CreateModel(
            name='Tache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intitule', models.CharField(max_length=100)),
                ('projet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Tache', to='eptGSI.Projet')),
            ],
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annee', models.DateField(max_length=100)),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('rapport_stage', models.FileField(blank=True, null=True, storage=djongo.storage.GridFSStorage(base_url='http://127.0.0.1:8000/rapports/', collection='media/rapports'), upload_to='rapports')),
                ('etudiant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Stage', to='eptGSI.Etudiant')),
                ('immersion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Stage', to='eptGSI.Immersion')),
            ],
        ),
        migrations.CreateModel(
            name='SousTache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_tache', models.CharField(max_length=100)),
                ('echeance', models.DateField(blank=True, null=True)),
                ('date_debut', models.DateField(blank=True, null=True)),
                ('date_fin', models.DateField(blank=True, null=True)),
                ('descriptif', models.TextField(blank=True, null=True)),
                ('commentaire', models.TextField(blank=True, null=True)),
                ('etat', models.BooleanField(default=False)),
                ('tache', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='SousTache', to='eptGSI.Tache')),
            ],
        ),
        migrations.CreateModel(
            name='RespEntreprise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RespEntreprise', to='eptGSI.Membre')),
            ],
        ),
        migrations.CreateModel(
            name='Planning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annee', models.DateField()),
                ('etudiant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Planning', to='eptGSI.Etudiant')),
                ('maitreStage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Planning', to='eptGSI.MaitreStage')),
                ('projets', models.ManyToManyField(to='eptGSI.Projet')),
            ],
        ),
        migrations.CreateModel(
            name='PieceJointe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fichier', models.FileField(storage=djongo.storage.GridFSStorage(base_url='http://127.0.0.1:8000/pjs/', collection='media/pjs'), upload_to='pjs')),
                ('evenement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='PieceJointe', to='eptGSI.Evenement')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intitule', models.CharField(max_length=100)),
                ('contenu', models.TextField()),
                ('date_envoi', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('etudiant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Message', to='eptGSI.Etudiant')),
            ],
        ),
        migrations.CreateModel(
            name='MembreDept',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MembreDept', to='eptGSI.Membre')),
            ],
        ),
        migrations.AddField(
            model_name='maitrestage',
            name='membre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MaitreStage', to='eptGSI.Membre'),
        ),
        migrations.AddField(
            model_name='immersion',
            name='programme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Immersion', to='eptGSI.Programme'),
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note_evaluation', models.FloatField()),
                ('appreciation', models.TextField()),
                ('etudiant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Evaluation', to='eptGSI.Etudiant')),
                ('maitre_de_stage', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Evaluation', to='eptGSI.MaitreStage')),
            ],
        ),
        migrations.AddField(
            model_name='etudiant',
            name='membre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Etudiant', to='eptGSI.Membre'),
        ),
        migrations.CreateModel(
            name='ChefDept',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ChefDept', to='eptGSI.Membre')),
            ],
        ),
    ]
