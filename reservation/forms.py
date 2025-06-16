from django import forms
from .models import (
    VNIV5SOIN, V_TYPEChantier, VChantier,VNiV4SOIN,
    TbChantierSylviculture, 
    TbTravauxChantier, 
    TbEtat,TbPlantsSouhaites ,TbSoinsPlants, VNiv3SOIN
)
from reservation import models

# ==== FORMULAIRE TRAVAUX ====
class TbTravauxChantierForm(forms.ModelForm):
    # Formulaire pour les travaux de chantier
    # (Le champ à définir sera fait dans la vue ou via l'URL)
    class Meta:
        model = TbTravauxChantier
        exclude = ['id_cs'] 
        fields = '__all__'
        
        # Ou spécifie explicitement les champs dont tu as besoin

class TbChantierSylvicultureForm(forms.ModelForm):
    
    
    chantier_virtuel = forms.ModelChoiceField(
        queryset=VChantier.objects.all(),
        required=False,
        label="Sélection rapide chantier",
        widget=forms.Select(attrs={'id': 'id_chantier_virtuel'}),
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remplir la liste avec les chantiers disponibles (code + libellé)
        self.fields['chantier_virtuel'].choices = [
            ("", "---------"),
            *[(chantier.code_chantier, f"{chantier.chantier_detail_complet}")
              for chantier in VChantier.objects.all()]
        ]
    cs_subvention_a = forms.BooleanField(
        required=False,
        label="Subvention",
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = TbChantierSylviculture
        fields = [
            'chantier_virtuel',
            'cs_id_n',
            'id_typechantier_a',
            'cs_important_b',
            'cs_subvention_a',
            'id_societe_n',
            'nomproprietaire_a',
            'cs_agence_a',
            'id_bureau_n',
            'id_secteur_n',
            'cs_surface_indicative_n',
            'id_insee_n',
            'id_pepiniere_a',
            'cs_bloc_notes_a',
            'cs_date_creation_d',
            'etat_id_n',
            'u_id_n',
          
        ]
        widgets = {
            'id_typechantier_a': forms.Select(attrs={'id': 'id_type_chantier'}),
            'id_bureau_n': forms.Select(attrs={'id': 'id_bureau'}),
            'cs_agence_a': forms.Select(attrs={'id': 'id_agence'}),
            'nomproprietaire_a': forms.TextInput(attrs={'id': 'id_nom_propietaire'}),
            'id_secteur_n': forms.Select(attrs={'id': 'id_secteur'}),
            'cs_surface_indicative_n': forms.NumberInput(attrs={'id': 'id_surface'}),
            'cs_subvention_a': forms.CheckboxInput(attrs={'id': 'id_subvention'}),
            'id_insee_n': forms.Select(attrs={'id': 'id_insee_commune'}),
            'etat_id_n': forms.RadioSelect(),
            'u_id_n': forms.Select(attrs={'id': 'id_utilisateur'}),
        }


        exclude = ['cs_date_creation_d', 'cs_id_n']
        labels = {
            'id_typechantier_a': 'code chantier + type chantier ',
            'cs_important_b': 'particulièrement important ?',
            'cs_subvention_a': 'Subvention',
            'id_societe_n': 'Société',
            'id_bureau_n': 'Bureau',
            'cs_agence_a': 'Agence',
            'id_secteur_n': 'Secteur',
            'nomproprietaire_a': 'Nom Propietaire',
            'id_insee_n': 'Commune principale',
            'cs_surface_indicative_n': 'Surface indicative',       
            'u_id_n': 'Utilisateur',
            'etat_id_n': 'stade reboisement',
            'id_pepiniere_a': 'pépinière pressentie',
            'cs_bloc_notes_a': 'Bloc Notes',
            'u_id_n': 'Utilisateur',
            }
    def clean_cs_subvention_a(self):
        val = self.cleaned_data.get('cs_subvention_a')
        return 'O' if val else 'N'


class TbPlantsSouhaitesForm(forms.ModelForm):
    nbre_plants_calcule = forms.IntegerField(
        label="Nombre de plants calculé",
        required=False,
        widget=forms.NumberInput(attrs={'readonly': 'readonly', 'id': 'id_nbre_plants_calcule'})
    )
  
    class Meta:
        model = TbPlantsSouhaites
        fields = [
            'id_essence_n',
            'prv_id_n',
            'ps_provenances_substitution_a',
            'con_id_n',
            'cop_id_n',
            'ags_id_n',
            'agd_id_n',
            'ta_id_n',
            'ps_prc_essence_n',
            'ps_nbr_plants_souhaites_n',
            'nbre_plants_calcule',
            'ps_campagne_n',
            'sai_id_n',
            'ps_regarnis_b',
            'sts_id_n',
            'ps_bloc_notes_a',
        ]
        
        labels = {
            'id_essence_n' : 'essence',
            'ps_provenances_substitution_a': 'Provenance de Substitution',
            'ps_campagne_n': 'Campagne',
            'ps_regarnis_b': 'Regarnis',
            'ps_nbr_plants_souhaites_n': 'Nombre de plants souhaités',
            'nbre_plants_calcule': 'Nombre de plants calculé',
            'sai_id_n': 'Saison',
            'ps_prc_essence_n': '% Essence',
            'prv_id_n': 'Provenance souhaitée',
            'ps_bloc_notes_a': 'Bloc Notes',
            'ilo_id_n': 'Ilot',
            'ta_id_n': 'Taille',
            'con_id_n': 'Conditionnement',
            'cop_id_n': 'Conditionnement précis',
            'ags_id_n': 'Age Simple',
            'agd_id_n': 'Age Detaillé',
            'sts_id_n': 'Stade',   
        }
        widgets = {
            'ps_bloc_notes_a': forms.Textarea(attrs={'rows': 2}),
        }
        exclude = ['ps_date_creation_d','ilo_id_n']

class TbSoinPlantsForm(forms.ModelForm):

    class Meta:
        model = TbSoinsPlants
        exclude = ['ps_id_n'] 
        fields = [
            'soi_quantite_n',
            'id_typeope_n',          
            'id_unite_n',
            'id_typeope_n',
            'sol_id_n',
        ]
        labels = {

            'soi_quantite_n': 'Quantité',
            'id_typeope_n': 'Type soin',
            'id_unite_n': 'Unité',
            'sol_id_n': 'Lieu soin',
               
        }
    soins_niv3_n = forms.ModelChoiceField(
        queryset= VNiv3SOIN.objects.all(), required=False, label="Niveau 3"
    )
    soins_niv4_n = forms.ModelChoiceField(
        queryset=VNiV4SOIN.objects.all(), required=False, label="Niveau 4"
    )
    soins_niv5_n = forms.ModelChoiceField(
        queryset=VNIV5SOIN.objects.all(), required=False, label="Niveau 5"
    )