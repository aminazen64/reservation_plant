# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class VBureau(models.Model):
    code_bureau = models.IntegerField(primary_key=True)
    nom_bureau = models.CharField(max_length=100)
    code_agence = models.CharField(max_length=10)

    class Meta:
        managed = True
        db_table = 'V_BUREAUX'
        ordering = ['nom_bureau']
    def __str__(self):
        return self.nom_bureau

class VCommune(models.Model):
    id_commune_n = models.CharField(max_length=100,primary_key=True)
    communespesi = models.CharField(max_length=100)

    def __str__(self):
        return self.communespesi

    class Meta:
        managed = True
        db_table = 'V_COMMUNES'
        ordering = ['communespesi']


class VPepiniere(models.Model):
    code_pepiniere = models.CharField(max_length=20, primary_key=True)
    nom_pepiniere = models.CharField(max_length=150)

    def __str__(self):
        return self.nom_pepiniere

    class Meta:
        managed = True
        db_table = 'V_PEPINIERES'


class VSociete(models.Model):
    soc_code_n = models.IntegerField(primary_key=True)
    societe = models.CharField(max_length=100)

    def __str__(self):
        return self.societe

    class Meta:
        managed = True
        db_table = 'V_SOCIETES'


class V_TYPEChantier(models.Model):
    code_chantier = models.CharField(max_length=50, primary_key=True)
    chantier_detail = models.CharField(max_length=255)

    def __str__(self):
        return self.chantier_detail

    class Meta:
        managed = True
        db_table = 'V_CHANTIER' 


class VNiv3TRAV(models.Model):
    nv3_codnv3_n = models.IntegerField(primary_key=True)
    nv3_lib_a = models.CharField(max_length=100)

    def __str__(self):
        return self.nv3_lib_a

    class Meta:
        managed = True
        db_table = 'V_NIV3_TRAVAUX'  


class VNiV4TRAV(models.Model):
    nv4_codnv4_n = models.IntegerField(primary_key=True)
    nv4_lib_a = models.CharField(max_length=100)
    nv4_codnv3_n = models.ForeignKey(
        VNiv3TRAV,
        on_delete=models.DO_NOTHING,
        db_column='nv4_codnv3_n'
    )

    def __str__(self):
        return self.nv4_lib_a

    class Meta:
        managed = True
        db_table = 'V_NIV4_TRAVAUX'



class VNIV5TRAV(models.Model):
    nv5_codnv5_n = models.IntegerField(primary_key=True)
    nv5_lib_a = models.CharField(max_length=100)
    nv5_codnv4_n = models.ForeignKey(
        VNiV4TRAV,
        on_delete=models.DO_NOTHING,
        db_column='nv5_codnv4_n'
    )

    def __str__(self):
        return self.nv5_lib_a

    class Meta:
        managed = True
        db_table = 'V_NIV5_TRAVAUX'



class VTypeOperation(models.Model):
    typ_codope_n = models.IntegerField(primary_key=True)
    typ_libope_a = models.CharField(max_length=100)
    typ_codnv5_n = models.ForeignKey(
        VNIV5TRAV,
        on_delete=models.DO_NOTHING,
        db_column='typ_codnv5_n'
    )

    def __str__(self):
        return self.typ_libope_a

    class Meta:
        managed = True
        db_table = 'V_TYPEOPE_TRAVAUX'
        

class VSousTraitant(models.Model):
    code_statut = models.CharField(max_length=20, primary_key=True)
    sous_traitants = models.CharField(max_length=255)

    def __str__(self):
        return self.sous_traitants

    class Meta:
        managed = True
        db_table = 'V_SOUS_TRAITANTS'


class VChantier(models.Model):
    code_chantier = models.CharField(primary_key=True, max_length=255)
    subvention = models.CharField(max_length=10, blank=True, null=True)
    agence = models.CharField(max_length=50, blank=True, null=True)
    bureau = models.CharField(max_length=50, blank=True, null=True)
    secteur = models.CharField(max_length=50, blank=True, null=True)
    surface = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    insee_commune = models.CharField(max_length=10, blank=True, null=True)
    proprietaire = models.CharField(max_length=255, blank=True, null=True)
    Cloture = models.IntegerField(blank=True, null=True)
    chantier_detail_complet = models.CharField(max_length=255, blank=True, null=True)

    
    class Meta:
        indexes = [models.Index(fields=['code_chantier'])]
        managed = True  
        db_table = 'v_CHANTIERS_RECUPERATION_DATA'
    def __str__(self):
        return self.chantier_detail_complet
         
class VSecteur(models.Model):
    code_secteur = models.CharField(max_length=10, primary_key=True)  
    libelle_secteur = models.CharField(max_length=255)
    code_bureau = models.CharField(max_length=10)  

    def __str__(self):
        return self.libelle_secteur

    class Meta:
        managed = True  
        db_table = 'V_SECTEURS'
        
class VAgence(models.Model):
    agence = models.CharField(max_length=10, primary_key=True)

    def __str__(self):
        return self.agence

    class Meta:
        managed = True
        db_table = 'V_AGENCES'  
        


class VEssence(models.Model):
    cod_nv1 = models.IntegerField(db_column='nv4_codnv1_n') 
    cod_nv4 = models.IntegerField(primary_key=True, db_column='code_essence')  
    libelle_essence = models.CharField(max_length=100, db_column='nv4_lib_a')  
    type_foret = models.CharField(max_length=50, db_column='nv2_lib_a')  

    def __str__(self):
        return self.libelle_essence

    class Meta:
        managed = True  
        db_table = 'V_ESSENCES'
        ordering = ['libelle_essence'] 

class VUnite (models.Model):
    nv3_codnv3_n = models.IntegerField(primary_key=True)
    nv3_lib_a = models.CharField(max_length=50)
    def __str__(self):
        return self.nv3_lib_a
    class Meta:
        managed = True  
        db_table = 'V_Unite'




class VNiv3SOIN(models.Model):
    nv3_codnv3_n = models.IntegerField(primary_key=True)
    nv3_lib_a = models.CharField(max_length=100)

    def __str__(self):
        return self.nv3_lib_a

    class Meta:
        managed = True
        db_table = 'V_NIV3_SOINS'  


class VNiV4SOIN(models.Model):
    nv4_codnv4_n = models.IntegerField(primary_key=True)
    nv4_lib_a = models.CharField(max_length=100)
    nv4_codnv3_n = models.ForeignKey(
        VNiv3SOIN,
        on_delete=models.DO_NOTHING,
        db_column='nv4_codnv3_n'
    )

    def __str__(self):
        return self.nv4_lib_a

    class Meta:
        managed = True
        db_table = 'V_NIV4_SOINS'



class VNIV5SOIN(models.Model):
    nv5_codnv5_n = models.IntegerField(primary_key=True)
    nv5_lib_a = models.CharField(max_length=100)
    nv5_codnv4_n = models.ForeignKey(
        VNiV4SOIN,
        on_delete=models.DO_NOTHING,
        db_column='nv5_codnv4_n'
    )

    def __str__(self):
        return self.nv5_lib_a

    class Meta:
        managed = True
        db_table = 'V_NIV5_SOINS'



class VTypeSOINS(models.Model):
    typ_codope_n = models.IntegerField(primary_key=True)
    typ_libope_a = models.CharField(max_length=100)
    typ_codnv5_n = models.ForeignKey(
        VNIV5SOIN,
        on_delete=models.DO_NOTHING,
        db_column='typ_codnv5_n'
    )

    def __str__(self):
        return self.typ_libope_a

    class Meta:
        managed = True
        db_table = 'V_TYPEOPE_SOINS'



class TbAgeDetaille(models.Model):
    agd_id_n = models.AutoField(primary_key=True)
    agd_lib_a = models.CharField(max_length=30, db_collation='French_CI_AS', blank=True, null=True)
    agd_ordre_n = models.IntegerField(blank=True, null=True)
    agd_abr_a = models.CharField(max_length=5, db_collation='French_CI_AS', blank=True, null=True)
    agd_actif_inactif_a = models.CharField(max_length=1, db_collation='French_CI_AS', blank=True, null=True)
    ags_id_n = models.ForeignKey('TbAgeSimple', models.DO_NOTHING, db_column='ags_id_n')

    class Meta:
        managed = False
        db_table = 'TB_Age_detaille'


class TbAgeSimple(models.Model):
    ags_id_n = models.AutoField(primary_key=True)
    ags_lib_a = models.CharField(max_length=5, db_collation='French_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TB_Age_simple'


class TbChantierSylviculture(models.Model):
    cs_id_n = models.AutoField(db_column= 'cs_id_n',primary_key=True)
    id_societe_n = models.ForeignKey(VSociete, on_delete=models.DO_NOTHING, db_column='id_societe_n', blank=True, null=True)
    id_typechantier_a = models.ForeignKey(VChantier, on_delete=models.DO_NOTHING, db_column='id_typeChantier_a', blank=True, null=True)  # Field name made lowercase.
    cs_important_b = models.BooleanField(blank=True, null=True)
    cs_subvention_a = models.CharField(max_length=1, choices=[('O', 'Oui'), ('N', 'Non')])
    nomproprietaire_a = models.CharField(db_column='nomProprietaire_a', max_length=100, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cs_agence_a = models.ForeignKey(VAgence, on_delete=models.DO_NOTHING, db_column='cs_agence_a', blank=True, null=True)
    id_bureau_n = models.ForeignKey(VBureau, on_delete=models.DO_NOTHING, db_column='id_bureau_n', blank=True, null=True)
    id_secteur_n = models.ForeignKey(VSecteur, on_delete=models.DO_NOTHING, db_column='id_secteur_n', blank=True, null=True)
    cs_surface_indicative_n = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    id_insee_n = models.ForeignKey(VCommune , on_delete=models.DO_NOTHING, db_column='id_insee_n', blank=True, null=True)
    id_pepiniere_a = models.ForeignKey(VPepiniere, on_delete=models.DO_NOTHING, db_column='id_pepiniere_a', blank=True, null=True)
    cs_bloc_notes_a = models.CharField(max_length=255, db_collation='French_CI_AS', blank=True, null=True)
    cs_date_creation_d = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    etat_id_n = models.ForeignKey('TbEtat', models.DO_NOTHING, db_column='etat_id_n')
    u_id_n = models.ForeignKey('TbUtilisateur', models.DO_NOTHING, db_column='u_id_n')

    class Meta:
        managed = False
        db_table = 'TB_Chantier_Sylviculture'


class TbConditionnement(models.Model):
    con_id_n = models.AutoField(primary_key=True)
    con_libelle_a = models.CharField(max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    con_abreviation_a = models.CharField(max_length=3, db_collation='French_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TB_Conditionnement'


class TbConditionnementPrecis(models.Model):
    cop_id_n = models.AutoField(primary_key=True)
    cop_libelle_a = models.CharField(max_length=10, db_collation='French_CI_AS', blank=True, null=True)
    con_id_n = models.ForeignKey(TbConditionnement, models.DO_NOTHING, db_column='con_id_n')

    class Meta:
        managed = False
        db_table = 'TB_Conditionnement_precis'


class TbDepot(models.Model):
    dep_id_n = models.AutoField(primary_key=True)
    dep_libelle_depot_a = models.CharField(max_length=50, db_collation='French_CI_AS', blank=True, null=True)
    dep_actif_inactif_a = models.CharField(max_length=1, db_collation='French_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TB_Depot'


class TbEtat(models.Model):
    Id_etat_n = models.AutoField(primary_key=True)
    type_a = models.CharField(max_length=10, db_collation='French_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TB_Etat'
        
    def __str__(self):
        return self.type_a


class TbEtiquette(models.Model):
    eti_id_n = models.AutoField(primary_key=True)
    eti_materiel_a = models.CharField(max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    eti_couleur_a = models.CharField(max_length=10, db_collation='French_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TB_Etiquette'


class TbIlots(models.Model):
    ilo_id_n = models.AutoField(primary_key=True)
    ilo_surface_n = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    ilo_prc_nonplantable_n = models.IntegerField(blank=True, null=True)
    ilo_espace_entreligne_n = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    ilo_espace_surligne_n = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    ilo_date_creation_d = models.DateTimeField(blank=True, null=True)
    ilo_bloc_notes_a = models.CharField(max_length=255, db_collation='French_CI_AS', blank=True, null=True)
    etat_id_n = models.ForeignKey(TbEtat, models.DO_NOTHING, db_column='etat_id_n')
    u_id_n = models.ForeignKey('TbUtilisateur', models.DO_NOTHING, db_column='u_id_n')
    cs_id_n = models.ForeignKey(TbChantierSylviculture, models.DO_NOTHING, db_column='cs_id_n')

    class Meta:
        managed = False
        db_table = 'TB_Ilots'


class TbOctrois(models.Model):
    oct_id_n = models.AutoField(primary_key=True)
    oct_nbr_plants_n = models.IntegerField(blank=True, null=True)
    oct_bloc_notes_a = models.CharField(max_length=255, db_collation='French_CI_AS', blank=True, null=True)
    oct_date_creation_d = models.DateTimeField(blank=True, null=True)
    id_essence_n = models.IntegerField(blank=True, null=True)
    id_pep_a = models.CharField(db_column='id_Pep_a', max_length=8, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    u_id_n = models.ForeignKey('TbUtilisateur', models.DO_NOTHING, db_column='u_id_n')
    agd_id_n = models.ForeignKey(TbAgeDetaille, models.DO_NOTHING, db_column='agd_id_n')
    ags_id_n = models.ForeignKey(TbAgeSimple, models.DO_NOTHING, db_column='ags_id_n')
    cop_id_n = models.ForeignKey(TbConditionnementPrecis, models.DO_NOTHING, db_column='cop_id_n')
    ta_id_n = models.ForeignKey('TbTaille', models.DO_NOTHING, db_column='ta_id_n')
    dep_id_n = models.ForeignKey(TbDepot, models.DO_NOTHING, db_column='dep_id_n')
    eta_id_n = models.ForeignKey(TbEtat, models.DO_NOTHING, db_column='eta_id_n')
    prv_id_n = models.ForeignKey('TbProvenance', models.DO_NOTHING, db_column='prv_id_n')
    ps_id_n = models.ForeignKey('TbPlantsSouhaites', models.DO_NOTHING, db_column='ps_id_n')
    con_id_n = models.ForeignKey(TbConditionnement, models.DO_NOTHING, db_column='con_id_n')

    class Meta:
        managed = False
        db_table = 'TB_Octrois'


class TbPlantsNonPlantes(models.Model):
    pnp_id_n = models.AutoField(primary_key=True)
    pnp_nbrplants_n = models.IntegerField(blank=True, null=True)
    dep_id_n = models.ForeignKey(TbDepot, models.DO_NOTHING, db_column='dep_id_n')
    oct_id_n = models.ForeignKey(TbOctrois, models.DO_NOTHING, db_column='oct_id_n')

    class Meta:
        managed = False
        db_table = 'TB_Plants_non_plantes'


class TbPlantsSouhaites(models.Model):
    ps_id_n = models.AutoField(primary_key=True)
    ps_provenances_substitution_a = models.CharField(max_length=255, db_collation='French_CI_AS', blank=True, null=True)
    ps_prc_essence_n = models.IntegerField(blank=True, null=True)
    ps_campagne_n = models.IntegerField(blank=True, null=True)
    ps_regarnis_b = models.BooleanField(blank=True, null=True)
    ps_nbr_plants_souhaites_n = models.IntegerField(blank=True, null=True)
    ps_bloc_notes_a = models.CharField(max_length=255, db_collation='French_CI_AS', blank=True, null=True)
    ps_date_creation_d = models.DateTimeField(blank=True, null=True)
    id_essence_n = models.IntegerField(blank=True, null=True)
    soi_id_n = models.ForeignKey('TbSoinsPlants', models.DO_NOTHING, db_column='soi_id_n')
    ilo_id_n = models.ForeignKey(TbIlots, models.DO_NOTHING, db_column='ilo_id_n')
    ta_id_n = models.ForeignKey('TbTaille', models.DO_NOTHING, db_column='ta_id_n')
    cop_id_n = models.ForeignKey(TbConditionnementPrecis, models.DO_NOTHING, db_column='cop_id_n')
    con_id_n = models.ForeignKey(TbConditionnement, models.DO_NOTHING, db_column='con_id_n')
    ags_id_n = models.ForeignKey(TbAgeSimple, models.DO_NOTHING, db_column='ags_id_n')
    agd_id_n = models.ForeignKey(TbAgeDetaille, models.DO_NOTHING, db_column='agd_id_n', blank=True, null=True)
    u_id_n = models.ForeignKey('TbUtilisateur', models.DO_NOTHING, db_column='u_id_n')
    sts_id_n = models.ForeignKey('TbStadeSouhaite', models.DO_NOTHING, db_column='sts_id_n')
    sai_id_n = models.ForeignKey('TbSaison', models.DO_NOTHING, db_column='sai_id_n')
    prv_id_n = models.ForeignKey('TbProvenance', models.DO_NOTHING, db_column='prv_id_n')

    class Meta:
        managed = False
        db_table = 'TB_Plants_souhaites'


class TbProvenance(models.Model):
    prv_id_n = models.AutoField(primary_key=True)
    prv_code_a = models.CharField(max_length=30, db_collation='French_CI_AS', blank=True, null=True)
    prv_lib_a = models.CharField(max_length=50, db_collation='French_CI_AS', blank=True, null=True)
    prv_actif_inactif_b = models.BooleanField(blank=True, null=True)
    eti_id_n = models.ForeignKey(TbEtiquette, models.DO_NOTHING, db_column='eti_id_n')
    ess_id_n = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'TB_Provenance'


class TbRegul(models.Model):
    reg_id_n = models.AutoField(primary_key=True)
    reg_date_d = models.DateTimeField(blank=True, null=True)
    reg_signe_b = models.BooleanField(blank=True, null=True)
    reg_nbr_plants_regul_n = models.IntegerField(blank=True, null=True)
    reg_source_regul_b = models.BooleanField(blank=True, null=True)
    reg_motif_a = models.CharField(max_length=100, db_collation='French_CI_AS', blank=True, null=True)
    u_id_n = models.ForeignKey('TbUtilisateur', models.DO_NOTHING, db_column='u_id_n')
    ps_id_n = models.ForeignKey(TbPlantsSouhaites, models.DO_NOTHING, db_column='ps_id_n')

    class Meta:
        managed = False
        db_table = 'TB_Regul'


class TbSaison(models.Model):
    sai_id_n = models.AutoField(primary_key=True)
    sai_lib_a = models.CharField(max_length=10, db_collation='French_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TB_Saison'


class TbSoinLieu(models.Model):
    sol_id_n = models.AutoField(primary_key=True)
    sol_lib_a = models.CharField(max_length=50, db_collation='French_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TB_Soin_Lieu'


class TbSoinsPlants(models.Model):
    soi_id_n = models.AutoField(primary_key=True)
    soi_quantite_n = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    id_unite_n = models.IntegerField(blank=True, null=True)
    id_typeope_n = models.IntegerField(blank=True, null=True)
    sol_id_n = models.ForeignKey(TbSoinLieu, models.DO_NOTHING, db_column='sol_id_n')

    class Meta:
        managed = False
        db_table = 'TB_Soins_plants'


class TbStadeSouhaite(models.Model):
    sts_id_n = models.AutoField(primary_key=True)
    sts_libelle_a = models.CharField(max_length=20, db_collation='French_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TB_Stade_Souhaite'


class TbStadeTravaux(models.Model):
    stt_id_n = models.AutoField(primary_key=True)
    stt_libelle_a = models.CharField(max_length=20, db_collation='French_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TB_Stade_travaux'


class TbTaille(models.Model):
    ta_id_n = models.AutoField(primary_key=True)
    ta_libelle_a = models.CharField(max_length=10, db_collation='French_CI_AS', blank=True, null=True)
    ta_actif_inactif_a = models.CharField(max_length=50, db_collation='French_CI_AS', blank=True, null=True)
    con_id_n = models.ForeignKey(TbConditionnement, models.DO_NOTHING, db_column='con_id_n')

    class Meta:
        managed = False
        db_table = 'TB_Taille'


class TbTravauxChantier(models.Model):
    tc_id_n = models.AutoField(primary_key=True)
    tc_annee_n = models.IntegerField(blank=True, null=True)
    tc_numero_semaine_n = models.IntegerField(blank=True, null=True)
    tc_quantite_n = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    id_sous_traitant_a = models.CharField(max_length=8, db_collation='French_CI_AS', blank=True, null=True)
    id_unite_n = models.IntegerField(blank=True, null=True)
    id_niv3_n = models.IntegerField(blank=True, null=True)
    id_niv4_n = models.IntegerField(blank=True, null=True)
    id_niv5_n = models.IntegerField(blank=True, null=True)
    id_typeope_n = models.IntegerField(blank=True, null=True)
    cs_id_n = models.ForeignKey(TbChantierSylviculture, models.DO_NOTHING, db_column='cs_id_n')
    stt_id_n = models.ForeignKey(TbStadeTravaux, models.DO_NOTHING, db_column='stt_id_n')

    class Meta:
        managed = False
        db_table = 'TB_Travaux_chantier'


class TbTravauxIlots(models.Model):
    til_id_n = models.AutoField(primary_key=True)
    til_annee_n = models.IntegerField(blank=True, null=True)
    til_numero_semaine_n = models.IntegerField(blank=True, null=True)
    til_quantite_n = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    id_sous_traitant_a = models.CharField(max_length=8, db_collation='French_CI_AS', blank=True, null=True)
    id_unite_n = models.IntegerField(blank=True, null=True)
    id_niv3_n = models.IntegerField(blank=True, null=True)
    id_niv4_n = models.IntegerField(blank=True, null=True)
    id_niv5_n = models.IntegerField(blank=True, null=True)
    id_typeope_n = models.IntegerField(blank=True, null=True)
    stt_id_n = models.ForeignKey(TbStadeTravaux, models.DO_NOTHING, db_column='stt_id_n')
    ilo_id_n = models.ForeignKey(TbIlots, models.DO_NOTHING, db_column='ilo_id_n')

    class Meta:
        managed = False
        db_table = 'TB_Travaux_ilots'


class TbUtilisateur(models.Model):
    u_id_n = models.AutoField(primary_key=True)
    u_username_a = models.CharField(max_length=50, db_collation='French_CI_AS', blank=True, null=True)
    role = models.CharField(max_length=50, db_collation='French_CI_AS', blank=True, null=True)
    id_util_n = models.CharField(max_length=50, db_collation='French_CI_AS', blank=True, null=True)
    user_djan = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TB_Utilisateur'
    def __str__(self):
        return self.u_username_a 
