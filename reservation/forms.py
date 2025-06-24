from django import forms
from .models import (
    VNIV5SOIN, TbIlots, TbOctrois, TbTravauxIlots, V_TYPEChantier, VChantier,VNiV4SOIN,
    TbChantierSylviculture, 
    TbTravauxChantier, 
    TbEtat,TbPlantsSouhaites ,TbSoinsPlants, VNiv3SOIN
)
from reservation import models


class TbTravauxChantierForm(forms.ModelForm):
    class Meta:
        model = TbTravauxChantier
        exclude = ['cs_id_n', 'u_id_n', 'tc_id_n', 'tc_date_creation_d'] 
        fields =  'id_unite_n', 'id_niv3_n', 'id_niv4_n', 'id_niv5_n','id_typeope_n', 'id_sous_traitant_a', 'tc_annee_n', 'tc_numero_semaine_n', 'tc_quantite_n', 'stt_id_n'
        widgets = { 
            'id_typeope_n': forms.Select(attrs={'id': 'id_typeope'}),
            'id_unite_n': forms.Select(attrs={'id': 'id_unite'}),
            'id_niv3_n': forms.Select(attrs={'id': 'id_niv3'}),
            'id_niv4_n': forms.Select(attrs={'id': 'id_niv4'}),
            'id_niv5_n': forms.Select(attrs={'id': 'id_niv5'}),
            'id_sous_traitant_a': forms.Select(attrs={'id': 'id_sous_traitant'}),
            'tc_annee_n': forms.NumberInput(attrs={'id': 'id_annee'}),
            'tc_numero_semaine_n': forms.NumberInput(attrs={'id': 'id_numero_semaine'}),
            'tc_quantite_n': forms.NumberInput(attrs={'id': 'id_quantite'}),
        }
        labels = {
            'id_typeope_n': 'Type d\'opération',
            'id_unite_n': 'Unité',
            'id_niv3_n': 'Niveau 3',
            'id_niv4_n': 'Niveau 4',
            'id_niv5_n': 'Niveau 5',
            'id_sous_traitant_a': 'Sous-traitant',
            'tc_annee_n': 'Année',
            'tc_numero_semaine_n': 'Semaine',
            'tc_quantite_n': 'Quantité',
            'stt_id_n': 'Stade travaux',
        }
        
        

class TbChantierSylvicultureForm(forms.ModelForm):
    
    
    chantier_virtuel = forms.ModelChoiceField(
        queryset=VChantier.objects.all(),
        required=False,
        label="Sélection rapide chantier",
        widget=forms.Select(attrs={'id': 'id_chantier_virtuel'}),
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        }


        exclude = ['cs_date_creation_d', 'cs_id_n' ,'u_id_n']
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
            'etat_id_n': 'stade reboisement',
            'id_pepiniere_a': 'pépinière pressentie',
            'cs_bloc_notes_a': 'Bloc Notes',
            }
    def clean_cs_subvention_a(self):
        val = self.cleaned_data.get('cs_subvention_a')
        return 'O' if val else 'N'

class TBIlotsForm(forms.ModelForm):
    class Meta:
        model = TbIlots

        exclude = ['ilo_id_n', 'ilo_date_creation_d', 'u_id_n', 'cs_id_n']
        labels = {  
            'ilo_nom_a': 'Nom',  
            'ilo_surface_n': 'Surface',  
            'ilo_prc_nonplantable_n': 'Pourcentage Non plantable',  
            'ilo_espace_entreligne_n': 'Espace Entreligne',  
            'ilo_espace_surligne_n': 'Espace Surligne',  
            'ilo_bloc_notes_a': 'Bloc Notes',  
            'etat_id_n': 'Etat',  
        }


class TbOctroisForm(forms.ModelForm):  
    afficher_depot = forms.BooleanField(  
        required=False,  
        label="Afficher le dépôt",  
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_afficher_depot'})  
    )  

    class Meta:  
        model = TbOctrois  
        exclude = ['oct_id_n','ps_id_n','oct_date_creation_d','u_id_n']  
        labels = {  
            'oct_nbr_plants_n': 'Nombre Plants',  
            'oct_bloc_notes_a': 'Bloc Notes',  
            'id_essence_n': 'Essence',  
            'id_pep_a': 'Pepiniere ',  
            'agd_id_n': 'Age Detaillé',  
            'ags_id_n': 'Age Simple',  
            'cop_id_n': 'Conditionnement Precis',  
            'con_id_n': 'Conditionnement',  
            'ta_id_n': 'Taille',  
            'eta_id_n': 'Etat',  
            'dep_id_n':'Depot',  
            'prv_id_n':'Provenance'  
        }  
        widgets = {  
            'oct_nbr_plants_n': forms.NumberInput(attrs={'class': 'form-control'}),  
            'oct_bloc_notes_a': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),  
            'id_essence_n': forms.Select(attrs={'class': 'form-select select2'}),  
            'id_pep_a': forms.Select(attrs={'class': 'form-select select2'}),  
            'agd_id_n': forms.Select(attrs={'class': 'form-select select2'}),  
            'ags_id_n': forms.Select(attrs={'class': 'form-select select2'}),  
            'cop_id_n': forms.Select(attrs={'class': 'form-select select2'}),  
            'con_id_n': forms.Select(attrs={'class': 'form-select select2'}),  
            'ta_id_n': forms.Select(attrs={'class': 'form-select select2'}),  
            'eta_id_n': forms.Select(attrs={'class': 'form-select select2'}),  
            'dep_id_n': forms.Select(attrs={'class': 'form-select select2'}),  
            'prv_id_n': forms.Select(attrs={'class': 'form-select select2'}),  
        }
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        self.fields['id_essence_n'].disabled = True

class TbTravauxIlotForm(forms.ModelForm):   

    class Meta:
        model = TbTravauxIlots
        exclude = ['ilo_id_n']
        labels = {  
            'til_annee_n': 'Année',  
            'til_numero_semaine_n': 'Semaine',  
            'til_quantite_n': 'Quantité',  
            'id_sous_traitant_a': 'Sous-traitant ',  
            'stt_id_n': 'Stade souhaité',  
            'id_unite_n': 'Unité',  
            'id_niv3_n': 'Niveau 3',  
            'id_niv4_n': 'Niveau 4',  
            'id_niv5_n': 'Niveau 5',  
            'id_typeope_n': 'Type d\'opération' 
        }
          
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
        exclude = ['ps_date_creation_d','ilo_id_n','u_id_n','ps_id_n']

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