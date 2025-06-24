from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns = [
    path('', lambda request: redirect('chantiers/')), 
    path('ajouter/', views.ajouter_chantier, name='ajouter_chantier'),
    path('get-chantier-details/', views.get_chantier_details, name='get_chantier_details'),
    path('chantiers/', views.liste_chantiers, name='liste_chantiers'),
    path('ajax/get_bureaux_by_agence/', views.get_bureaux_by_agence, name='get_bureaux_by_agence'),  
    path('ajax/get_secteurs_by_bureau/', views.get_secteurs_by_bureau, name='get_secteurs_by_bureau'),
    path('ajax/get_communes_by_filters/', views.get_communes_by_filters, name='get_communes_by_filters'),
    path('chantier/<int:chantier_id>/essences/', views.afficher_essences_chantier, name='afficher_essences_chantier'),
    path('chantier/<int:chantier_id>/ilots/', views.liste_ilots_chantiers, name='liste_ilots_chantier'),
    path('chantier/ajouter_ilot/<int:chantier_id>/', views.ajouter_ilot, name='ajouter_ilot'),
    path('plant/<int:plant_id>/octrois/', views.liste_octrois_pour_plant, name='liste_octrois_pour_plant'),
    path('octrois/<int:plant_id>/', views.octrois_form, name='octrois_form'),
    path('travaux/ajouter/<int:ilot_id_n>/', views.ajouter_travaux_ilot, name='ajouter_travaux_ilot'),
    path('ilot/<int:ilot_id_n>/travaux/', views.liste_travaux_ilot, name='liste_travaux_ilot'),
    path('ilots/<int:ilot_id>/modifier/', views.modifier_ilot, name='modifier_ilot'),
    path('remplir/', views.remplissage_Utilisateur, name='remplir'),
    path('chantiers/<int:id>/voir-travaux/', views.voir_travaux_chantier, name='voir_travaux_chantier'),
    path('ajax/get-niv4/', views.get_niv4_by_niv3, name='get_niv4_by_niv3'),
    path('ajax/get-niv5/', views.get_niv5_by_niv4, name='get_niv5_by_niv4'),
    path('ajax/get-ops/', views.get_ops_by_niv5, name='get_ops_by_niv5'),
    path('chantier/modifier/<int:chantier_id>/', views.modifier_chantier, name='modifier_chantier'),
    path('chantier/annuler/<int:chantier_id>/', views.annuler_reboisement, name='annuler_reboisement'),
    path('plants/<int:plant_id>/soins/', views.liste_soins_plants, name='liste_soins_plants'),
    path('plants/<int:ps_id>/reguls/', views.voir_regul, name='voir_regul'),
    path('ilot/<int:ilot_id>/plants/<int:ps_id>/ajouter-soin/', views.ajouter_soin_pour_plant, name='ajouter_soin_plant'),
    path('ilot/<int:ilot_id>/plants/<int:ps_id>/reguler/', views.reguler_plant, name='reguler_plant'),
    path('get-niv4-by-niv3/', views.get_niv4_by_niv3_soins, name='get_niv4_by_niv3_soins'),
    path('get-niv5-by-niv4/', views.get_niv5_by_niv4_soins, name='get_niv5_by_niv4_soins'),
    path('get-ops-by-niv5/', views.get_ops_by_niv5_soins, name='get_ops_by_niv5_soins'),
    path('ilot/<int:ilot_id>/plants/ajouter/', views.ajouter_plant_souhaite, name='ajouter_plante'),
    path('ilot/<int:ilot_id>/plants/', views.liste_plants, name='liste_plants_pour_ilot'),
    path('ajax/get_provenances/', views.get_provenances_by_essence, name='get_provenances_by_essence'),
    path('ajax/get_agedetaille/', views.get_agedetaille_by_agesimple, name='get_agedetaille_by_agesimple'),
    path('ajax/get_cond_precis/', views.get_cond_precis_by_cond, name='get_cond_precis_by_cond'),
    path('plants/<int:ps_id>/reguls/', views.voir_regul, name='voir_regul'),
    path('choix-annuler-reporter/<int:ilot_id>/<int:ps_id>/', views.choix_annuler_reporter, name='choix_annuler_reporter'),
    path('travaux_chantiers/ajouter/<int:chantier_id>/', views.ajouter_travaux_chantier, name='ajouter_travaux_chantier'),




]


