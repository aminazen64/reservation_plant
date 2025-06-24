import datetime
import json
import logging
from pyexpat.errors import messages
from sqlite3 import Cursor
import time
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import TBIlotsForm, TbChantierSylvicultureForm, TbOctroisForm, TbPlantsSouhaitesForm, TbSoinPlantsForm, TbTravauxChantierForm, TbTravauxIlotForm
from .models import VNIV5SOIN, AuthUser, TbAgeDetaille, TbChantierSylviculture, TbConditionnementPrecis, TbEtat, TbIlots, TbOctrois,TbProvenance, TbSoinsPlants, TbTravauxIlots, TbUtilisateur, V_TYPEChantier, VAgence, VBureau, VCommune, VEssence, VNiV4SOIN, VNiV4TRAV, VNIV5TRAV, VPepiniere, VSecteur, VTypeOperation, VNiv3TRAV, VChantier,TbTravauxChantier ,TbPlantsSouhaites, TbRegul, VTypeSOINS, VUtilisateur
from django.db import connection
from django.utils.timezone import now
from django.db.models import Sum, Case, When, IntegerField
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.models import User
import os
from django.contrib.auth import login as django_log


def liste_chantiers(request):  
    agence_id = request.GET.get('agence') or ''  
    bureau_id = request.GET.get('bureau') or ''  
    secteur_id = request.GET.get('secteur') or ''  
    commune_id = request.GET.get('commune') or ''  
    essence_id = request.GET.get('essence') or ''  
    travaux = request.GET.get('annee_travaux') or ''  
    campagne = request.GET.get('annee_campagne', '') or ''  
    selected_pepiniere = request.GET.get('pepiniere') or ''  
    cloture = request.GET.get('cloture', '0')  

    default_items_per_page = 10  

    items_per_page = request.GET.get('per_page', default_items_per_page)  
    try:  
        items_per_page = int(items_per_page)  
        if items_per_page not in [10, 25, 50, 100]:  
            items_per_page = default_items_per_page  
    except (ValueError, TypeError):  
        items_per_page = default_items_per_page  

    chantiers = TbChantierSylviculture.objects.all()  

    

    if agence_id:  
        chantiers = chantiers.filter(cs_agence_a=agence_id)  
    if bureau_id:  
        chantiers = chantiers.filter(id_bureau_n=bureau_id)  
    if secteur_id:  
        chantiers = chantiers.filter(id_secteur_n=secteur_id)  
    if commune_id:  
        chantiers = chantiers.filter(id_insee_n=commune_id)  
    if travaux:  
        try:  
            travaux = int(travaux)  
            chantiers = chantiers.filter(tbtravauxchantier__annee_n=travaux).distinct()  
        except ValueError:  
            pass  
    if cloture != '':  
        codes_chantiers = list(VChantier.objects.filter(Cloture=int(cloture)).values_list('code_chantier', flat=True))  
        chantiers = chantiers.filter(id_typechantier_a__code_chantier__in=codes_chantiers)  
    if campagne:  
        try:  
            campagne_int = int(campagne)  
            chantiers = chantiers.filter(  
                cs_id_n__in=TbIlots.objects.filter(  
                    tbplantssouhaites__ps_campagne_n=campagne_int  
                ).values_list('cs_id_n', flat=True)  
            )  
        except ValueError:  
            pass  
    if essence_id:  
        chantiers = chantiers.filter(  
            cs_id_n__in=TbIlots.objects.filter(  
                tbplantssouhaites__id_essence_n=essence_id  
            ).values_list('cs_id_n', flat=True)  
        )  
    if selected_pepiniere:  
        chantiers = chantiers.filter(id_pepiniere_a=selected_pepiniere)  

    paginator = Paginator(chantiers, items_per_page)  
    page = request.GET.get('page', 1)  

    try:  
        chantiers_page = paginator.page(page)  
    except PageNotAnInteger:  
        chantiers_page = paginator.page(1)  
    except EmptyPage:  
        chantiers_page = paginator.page(paginator.num_pages)  

    chantiers_avec_essences = []  
    for chantier in chantiers_page:  
        essences = VEssence.objects.filter(  
            cod_nv4__in=TbPlantsSouhaites.objects.filter(  
                ilo_id_n__in=TbIlots.objects.filter(  
                    cs_id_n=chantier.cs_id_n  
                ).values_list('ilo_id_n', flat=True)  
            ).values_list('id_essence_n', flat=True)  
        ).distinct()  

        total_plants = 0  
        ilots = TbIlots.objects.filter(cs_id_n=chantier.cs_id_n)  

        for ilot in ilots:  
            plants_souhaites = TbPlantsSouhaites.objects.filter(ilo_id_n=ilot.ilo_id_n)  

            for plant in plants_souhaites:  
                plant_count = plant.ps_nbr_plants_souhaites_n or 0  

                reguls = TbRegul.objects.filter(ps_id_n=plant.ps_id_n)  
                for regul in reguls:  
                    adjustment = regul.reg_nbr_plants_regul_n or 0  
                    if regul.reg_signe_b:  
                        plant_count += adjustment  
                    else:  
                        plant_count -= adjustment  

                total_plants += plant_count  

        chantiers_avec_essences.append({  
            'chantier': chantier,  
            'essences': essences,  
            'total_plants': total_plants  
        })  

    class PaginatedList:  
        def __init__(self, data, page_obj):  
            self.object_list = data  
            self.paginator = page_obj.paginator  
            self.number = page_obj.number  

        def __iter__(self):  
            return iter(self.object_list)  

        def __len__(self):  
            return len(self.object_list)  

        def has_other_pages(self):  
            return self.paginator.num_pages > 1  

        def has_previous(self):  
            return self.number > 1  

        def has_next(self):  
            return self.number < self.paginator.num_pages  

        def previous_page_number(self):  
            return self.number - 1 if self.has_previous() else None  

        def next_page_number(self):  
            return self.number + 1 if self.has_next() else None  

        def start_index(self):  
            return (self.number - 1) * self.paginator.per_page + 1  

        def end_index(self):  
            return min(self.number * self.paginator.per_page, self.paginator.count)  

    paginated_chantiers = PaginatedList(chantiers_avec_essences, chantiers_page)  

    agences = VAgence.objects.all().order_by('agence')  
    if agence_id:  
        bureaux = VBureau.objects.filter(code_agence=agence_id).order_by('nom_bureau')  
    else:  
        bureaux = VBureau.objects.all().order_by('nom_bureau')  
    if bureau_id:  
        secteurs = VSecteur.objects.filter(code_bureau=bureau_id).order_by('libelle_secteur')  
    else:  
        secteurs = VSecteur.objects.all().order_by('libelle_secteur')  

    communes = VCommune.objects.all().order_by('communespesi')  
    essences = VEssence.objects.all().order_by('libelle_essence')  
    pepinieres = VPepiniere.objects.all().order_by('nom_pepiniere')  

    return render(request, 'list_reb.html', {  
        'chantiers_avec_essences': paginated_chantiers,  
        'agences': agences,  
        'bureaux': bureaux,  
        'secteurs': secteurs,  
        'communes': communes,  
        'pepinieres': pepinieres,  
        'essences': essences,  
        'selected_agence': agence_id,  
        'selected_bureau': bureau_id,  
        'selected_secteur': secteur_id,  
        'selected_commune': commune_id,  
        'selected_annee_travaux': travaux,  
        'selected_annee_campagne': campagne,  
        'selected_pepiniere': selected_pepiniere,  
        'selected_essence': essence_id,  
        'selected_cloture': cloture,  
        'items_per_page': items_per_page,  
    }) 
def get_communes_by_filters(request):
    agence_id = request.GET.get('agence_id')
    bureau_id = request.GET.get('bureau_id')
    secteur_id = request.GET.get('secteur_id')

    chantiers = TbChantierSylviculture.objects.all()

    if agence_id and agence_id != '':
        chantiers = chantiers.filter(agence_id=agence_id)
    if bureau_id and bureau_id != '':
        chantiers = chantiers.filter(bureau_id=bureau_id)
    if secteur_id and secteur_id != '':
        chantiers = chantiers.filter(secteur_id=secteur_id)
    
    commune_ids = chantiers.exclude(id_insee=None).values_list('id_insee', flat=True).distinct()
    
    communes = VCommune.objects.filter(id_commune_n__in=commune_ids)
    
    data = [{'id': commune.id_commune_n, 'nom': commune.communespesi} for commune in communes]
    
    return JsonResponse(data, safe=False)
def get_bureaux_by_agence(request):
    agence_id = request.GET.get('agence_id')
    if agence_id:
        bureaux = VBureau.objects.filter(code_agence=agence_id)
    else:
        bureaux = VBureau.objects.all()
    data = [{'id': bureau.code_bureau, 'nom': bureau.nom_bureau} for bureau in bureaux]
    return JsonResponse(data, safe=False)

def get_secteurs_by_bureau(request):
    bureau_id = request.GET.get('bureau_id')
    if bureau_id:
        secteurs = VSecteur.objects.filter(code_bureau=bureau_id)
    else:
        secteurs = VSecteur.objects.all()
    data = [{'id': secteur.code_secteur, 'nom': secteur.libelle_secteur} for secteur in secteurs]
    return JsonResponse(data, safe=False)
 

def liste_ilots_chantiers(request, chantier_id):
 
    ilots = TbIlots.objects.filter(cs_id_n=chantier_id)

    ilots_avec_calcul = [] 

    for ilot in ilots:
        if ilot.ilo_surface_n is not None and ilot.ilo_prc_nonplantable_n is not None:
            calcul_non_plantable = ilot.ilo_surface_n * ilot.ilo_prc_nonplantable_n / 100
        else:
            calcul_non_plantable = None


        ilots_avec_calcul.append({
            'ilot': ilot,
            'calcul_non_plantable': calcul_non_plantable
        })


    try:
        chantier = TbChantierSylviculture.objects.get(cs_id_n=chantier_id)
    except TbChantierSylviculture.DoesNotExist:
        return HttpResponse("Chantier non trouvé", status=404)

    return render(request, 'liste_ilots.html', {
        'ilots_avec_calcul': ilots_avec_calcul,  
        'chantier': chantier,
    })



def get_chantier_details(request):
    code_chantier = request.GET.get("code_chantier", "").strip()
    try:
        chantier = VChantier.objects.filter(code_chantier=code_chantier).first()

        return JsonResponse({
            'agence': chantier.agence,
            'bureau': chantier.bureau,
            'propietaire': chantier.proprietaire,
            'secteur': chantier.secteur,
            'surface': chantier.surface,
            'subvention': chantier.subvention ,
            'insee_commune': chantier.insee_commune,
            "type_chantier": chantier.code_chantier,  
                     

        })
    except VChantier.DoesNotExist:
        return JsonResponse({'error': 'Chantier non trouvé'}, status=404)

def get_niv4_by_niv3(request):
    niv3_id = request.GET.get('niv3_id')
    niv4_options = VNiV4TRAV.objects.filter(nv4_codnv3_n=niv3_id).values('nv4_codnv4_n', 'nv4_lib_a')
    return JsonResponse(list(niv4_options), safe=False)


def get_niv5_by_niv4(request):
    niv4_id = request.GET.get('niv4_id')
    niv5_options = VNIV5TRAV.objects.filter(nv5_codnv4_n=niv4_id).values('nv5_codnv5_n', 'nv5_lib_a')
    return JsonResponse(list(niv5_options), safe=False)


def get_ops_by_niv5(request):
    niv5_id = request.GET.get('niv5_id')
    op_options = VTypeOperation.objects.filter(typ_codnv5_n=niv5_id).values('typ_codope_n', 'typ_libope_a')
    return JsonResponse(list(op_options), safe=False)




def voir_travaux_chantier(request, id):
    chantier = get_object_or_404(TbChantierSylviculture, pk=id)
    travaux = TbTravauxChantier.objects.filter(cs_id_n=chantier)
    return render(request, 'voir_travaux_chantier.html', {'chantier': chantier, 'travaux': travaux})



def ajouter_chantier(request):
    user = os.getenv("USERNAME")
    if request.method == 'POST':
        chantier_form = TbChantierSylvicultureForm(request.POST)
        if chantier_form.is_valid():
            chantier = chantier_form.save(commit=False)
            tb_user = TbUtilisateur.objects.get(username=user)
            chantier.u_id_n = tb_user
            chantier.save()
            return redirect('liste_chantiers')
        else:
            print(chantier_form.errors)    
    else:
        chantier_form = TbChantierSylvicultureForm()
 

    context = {
        'chantier_form': chantier_form,
    }
    return render(request, 'ajouter_reb.html', context)



def ajouter_travaux_chantier(request, chantier_id):
    chantier = get_object_or_404(TbChantierSylviculture, pk=chantier_id)

    if request.method == 'POST':
        travaux_form = TbTravauxChantierForm(request.POST)
        if travaux_form.is_valid():
            travaux = travaux_form.save(commit=False)
            travaux.cs_id_n = chantier
            travaux.save()
            return redirect('liste_chantiers')
    else:
        travaux_form = TbTravauxChantierForm()

    context = {
        'chantier': chantier,
        'travaux_form': travaux_form,
    }
    return render(request, 'ajouter_travaux.html', context)



    
    
    
def modifier_chantier(request, chantier_id):
    chantier = get_object_or_404(TbChantierSylviculture,cs_id_n=chantier_id)
    if request.method == 'POST':
        form = TbChantierSylvicultureForm(request.POST, instance=chantier)
        if form.is_valid():
            form.save()
            return redirect('liste_chantiers') 
    else:
        form = TbChantierSylvicultureForm(instance=chantier)
    return render(request, 'modifier_chantier.html', {'form': form, 'chantier': chantier})



@require_POST
@csrf_protect
def annuler_reboisement(request, chantier_id):
    chantier = get_object_or_404(TbChantierSylviculture, cs_id_n=chantier_id)


    ilots = TbIlots.objects.filter(cs_id_n=chantier)


    if ilots.exists():
        bloquant = TbPlantsSouhaites.objects.filter(
            ilo_id_n__in=ilots,
            sts_id_n__in=[2, 7] 
        ).exists()

        if bloquant:
            return JsonResponse({"status": "blocked"})

        etat_annule = TbEtat.objects.get(Id_etat_n=4)
        ilots.update(etat_id_n=etat_annule)
    else:
        etat_annule = TbEtat.objects.get(Id_etat_n=4)

    chantier.etat_id_n = etat_annule
    chantier.save()

    return JsonResponse({"status": "ok", "redirect_url": "/chantiers/"})


def ajouter_plant_souhaite(request, ilot_id):
    ilot = get_object_or_404(TbIlots, pk=ilot_id)
    if request.method == 'POST':
        form = TbPlantsSouhaitesForm(request.POST)
        user=os.getenv("USERNAME")
        if form.is_valid():
            plant = form.save(commit=False)
            tb_user = TbUtilisateur.objects.get(username=user)
            plant.ilo_id_n = ilot
            plant.u_id_n = tb_user
            plant.save()
            return redirect('liste_plants_pour_ilot', ilot_id=ilot.ilo_id_n) 
    else:
        form = TbPlantsSouhaitesForm() 

    return render(request, 'ajouter_plantes.html', {
        'form': form,
        'ilot': ilot,
    })



def liste_plants(request, ilot_id):
    ilot = get_object_or_404(TbIlots, pk=ilot_id)
    plants = TbPlantsSouhaites.objects.filter(ilo_id_n=ilot_id)
    chantier = ilot.cs_id_n  
    role = TbUtilisateur.objects.get(username=os.getenv("USERNAME")).role
    plants_with_totals = []
    for plant in plants:
        souhaites = plant.ps_nbr_plants_souhaites_n or 0
        if plant.ps_campagne_n is None:
            plant.ps_campagne_n = 0
        else:
            plant.ps_campagne_n = f" { plant.ps_campagne_n} - {plant.ps_campagne_n+ 1}"
        total_plus = TbRegul.objects.filter(ps_id_n=plant, reg_signe_b=True).aggregate(
            Sum('reg_nbr_plants_regul_n')
        )['reg_nbr_plants_regul_n__sum'] or 0

        total_moins = TbRegul.objects.filter(ps_id_n=plant, reg_signe_b=False).aggregate(
            Sum('reg_nbr_plants_regul_n')
        )['reg_nbr_plants_regul_n__sum'] or 0

        total_regule = souhaites + total_plus - total_moins
        
        if total_regule < 0:
            total_regule = 0

        plants_with_totals.append({
            'plant': plant,
            'total_regule': total_regule,
          
        })

    return render(request, 'liste_plants.html', {
        'plants_with_totals': plants_with_totals,
        'chantier': chantier,
        'ilot': ilot,
        'plants': plants,
        'role': role,
    })

def ajouter_ilot(request,chantier_id):
    types = TbEtat.objects.exclude(type_a__isnull=True).distinct()
    chantier = get_object_or_404(TbChantierSylviculture, cs_id_n=chantier_id)
    user = os.getenv("USERNAME")
    if request.method == 'POST':
        form = TBIlotsForm(request.POST)
        if form.is_valid():
            ilot = form.save(commit=False)
            tb_user = TbUtilisateur.objects.get(username=user)
            ilot.u_id_n = tb_user

            ilot.cs_id_n = chantier
            ilot.ilo_date_creation_d = timezone.now()       
            ilot.save()
            return redirect('liste_ilots_chantier')
    else:
        form = TBIlotsForm()

    return render(request, 'ajouter_ilot.html', {'form': form, 'types': types})

def liste_octrois_pour_plant(request, plant_id):  
    plant = get_object_or_404(TbPlantsSouhaites, pk=plant_id)  
    octrois = TbOctrois.objects.filter(ps_id_n=plant_id)  
    ilot = plant.ilo_id_n
    return render(request, 'liste_octrois.html', {  
        'plant': plant,  
        'octrois': octrois, 
        'ilot':ilot

    })

def octrois_form(request, plant_id):
    plant = get_object_or_404(TbPlantsSouhaites, ps_id_n=plant_id)
    pepiniere_id = None
   
    ilot = plant.ilo_id_n
  
    chantier_id = ilot.cs_id_n
    if chantier_id:
        try:
           
            chantier = TbChantierSylviculture.objects.get(pk=chantier_id)
            0
            pepiniere_id = chantier.id_pepiniere_id
        except TbChantierSylviculture.DoesNotExist:
            pepiniere_id = None

    if request.method == 'POST':
        form = TbOctroisForm(request.POST)
        if form.is_valid():
            afficher_depot = form.cleaned_data.get('afficher_depot', False)
            octrois = form.save(commit=False)
            octrois.u_id_n = get_object_or_404(Utilisateurprocofor, user_djan=366)
            octrois.ps_id_n = plant
            octrois.oct_date_creation_d = timezone.now()
            if not afficher_depot:
                octrois.dep_id_n = None
            from .models import VEssence
            octrois.id_essence_n = VEssence.objects.get(pk=plant.id_essence_n)
            octrois.save()
            return redirect('liste_octrois_pour_plant', plant_id=plant_id)
    else:
        form = TbOctroisForm(initial={
            'id_pep_a': pepiniere_id,
            'id_essence_n': plant.id_essence_n,
            'ta_id_n': plant.ta_id_n_id,  
            'con_id_n': plant.con_id_n,  
            'cop_id_n': plant.cop_id_n_id, 
            'ags_id_n': plant.ags_id_n_id,
            'agd_id_n': plant.agd_id_n_id,  
            'oct_nbr_plants_n': plant.ps_nbr_plants_souhaites_n, 
            'prv_id_n': plant.prv_id_n_id, 
        })
    return render(request, 'ajouter_octrois.html', {
        'form': form,
    })
  
def choix_annuler_reporter(request, ilot_id, ps_id):
    plant = get_object_or_404(TbPlantsSouhaites, ps_id_n=ps_id)

    STADE_ENVISAGE = 1
    STADE_ANNULE = 3  
    STADE_COMMANDE_TERMINEE = 7 

    if plant.sts_id_n == STADE_COMMANDE_TERMINEE:
        messages.error(request, "tu as déjà effectué des demandes de livraison !")
        return redirect('liste_plants', ilot_id=plant.ilo_id_n)

    if request.method == "POST":
        choix = request.POST.get("choix")

        total_regule = TbRegul.objects.filter(ps_id_n=plant).aggregate(
            total_plus=Sum(Case(
                When(reg_signe_b=True, then='reg_nbr_plants_regul_n'),
                default=0,
                output_field=IntegerField()
            )),
            total_moins=Sum(Case(
                When(reg_signe_b=False, then='reg_nbr_plants_regul_n'),
                default=0,
                output_field=IntegerField()
            ))
        )

        total_plus = total_regule['total_plus'] or 0
        total_moins = total_regule['total_moins'] or 0
        quantite_totale = total_plus - total_moins

        if choix == "annuler":
            if quantite_totale > 0:
                TbRegul.objects.create(
                    ps_id_n=plant,
                    reg_nbr_plants_regul_n= quantite_totale,
                    reg_date_d=now(),
                    u_id_n=1,  
                    reg_signe_b=False,
                    reg_motif_a="Régulation automatique",
                )
            plant.sts_id_n_id = STADE_ANNULE
            plant.save()
            return redirect('liste_plants_pour_ilot', ilot_id=ilot_id)


        elif choix == "reporter":
            # Dupliquer la fiche
            new_plant = TbPlantsSouhaites.objects.get(pk=plant.pk)
            new_plant.pk = None
            new_plant.ps_campagne_n += 1
            new_plant.sts_id_n_id = STADE_ENVISAGE
            new_plant.save()

            # Copier les réguls
            for reg in plant.reguls.all():
                TbRegul.objects.create(
                    ps_id_n=new_plant,
                    reg_nbr_plants_regul_n=reg.reg_nbr_plants_regul_n,
                    reg_signe_b=reg.reg_signe_b,
                    reg_date_d=reg.reg_date_d,
                    u_id_n=reg.u_id_n,
                    reg_motif_a=f"Reporté depuis {plant.ps_id_n}"
                )

            # Marquer ancienne comme annulée
            plant.sts_id_n_id = STADE_ANNULE
            plant.save()

            return redirect('liste_plants_pour_ilot', ilot_id=ilot_id)
    ilot = plant.ilo_id_n  # Objet TbIlots directement

    return render(request, "choix_annuler_reporter.html", {"plant": plant, 'ilot': ilot})

def get_chantier_from_ilot(ilot):
    try:
        return TbChantierSylviculture.objects.get(cs_id_n=ilot.cs_id_n)
    except TbChantierSylviculture.DoesNotExist:
        return None

def get_niv4_by_niv3_soins(request):
    niv3_id = request.GET.get('niv3_id')
    niv4_options = VNiV4SOIN.objects.filter(nv4_codnv3_n=niv3_id).values('nv4_codnv4_n', 'nv4_lib_a')
    return JsonResponse(list(niv4_options), safe=False)


def get_niv5_by_niv4_soins(request):
    niv4_id = request.GET.get('niv4_id')
    niv5_options = VNIV5SOIN.objects.filter(nv5_codnv4_n=niv4_id).values('nv5_codnv5_n', 'nv5_lib_a')
    return JsonResponse(list(niv5_options), safe=False)


def get_ops_by_niv5_soins(request):
    niv5_id = request.GET.get('niv5_id')
    op_options = VTypeSOINS.objects.filter(typ_codnv5_n=niv5_id).values('typ_codope_n', 'typ_libope_a')
    return JsonResponse(list(op_options), safe=False)


def ajouter_soin_pour_plant(request, ps_id,ilot_id):

    plant = get_object_or_404(TbPlantsSouhaites, pk=ps_id)

    if request.method == 'POST':
        form = TbSoinPlantsForm(request.POST)
        if form.is_valid():
            soin = form.save(commit=False)
            soin.ps_id_n = plant  
            soin.save()
            return redirect('liste_plants_pour_ilot', ilot_id= ilot_id) 
    else:
        form = TbSoinPlantsForm()

    context = {
        'form': form,
        'plant': plant,
        'ilot': plant.ilo_id_n,
    }
    return render(request, 'ajouter_soin.html', context)


def liste_soins_plants(request, plant_id):
    plant = get_object_or_404(TbPlantsSouhaites, pk=plant_id)

    soins = TbSoinsPlants.objects.filter(ps_id_n=plant).order_by('soi_id_n')

    context = {
        'plant': plant,
        'soins': soins,
        'ilot': plant.ilo_id_n,  # Utilisation de l'objet TbIlots directement
    }
    return render(request, 'voir_soins.html', context)

def reguler_plant(request, ps_id , ilot_id):
    plant = get_object_or_404(TbPlantsSouhaites, pk=ps_id)


    if request.method == 'POST':
        signe = request.POST['signe'] 
        nombre = int(request.POST['nombre'])


        TbRegul.objects.create(
            reg_date_d=now(),
            reg_signe_b=(signe == '+'),
            reg_nbr_plants_regul_n=nombre,
            reg_source_regul_b=True,
            reg_motif_a="Régulation manuelle",
            u_id_n=1,  
            ps_id_n=plant
        )

        return redirect('liste_plants_pour_ilot', ilot_id= ilot_id)  # Correction : ilot.ilo_id_n au lieu de ilot.id_ilot_n
    return render(request, 'reguler_plant.html', {
        'plant': plant, 
        'ilot': plant.ilo_id_n,
    })
    
def voir_regul(request, ps_id):
    plant = get_object_or_404(TbPlantsSouhaites, pk=ps_id)
    reguls = TbRegul.objects.filter(ps_id_n=plant).order_by('-reg_date_d')

    ilot = plant.ilo_id_n  # Objet TbIlots directement

    total_ajouts = reguls.filter(reg_signe_b=True).aggregate(
        total=Sum('reg_nbr_plants_regul_n')
    )['total'] or 0

    total_retraits = reguls.filter(reg_signe_b=False).aggregate(
        total=Sum('reg_nbr_plants_regul_n')
    )['total'] or 0

    # Correction ici :
    nouveau_total = (plant.ps_nbr_plants_souhaites_n or 0) + (total_ajouts - total_retraits)

    return render(request, 'voir_regul.html', {
        'plant': plant,
        'reguls': reguls,
        'nouveau_total': nouveau_total,
        'ilot': ilot,
    })

def get_provenances_by_essence(request):
    essence_id = request.GET.get('essence_id')
    provenances = TbProvenance.objects.filter(ess_id_n=essence_id).values('prv_id_n', 'prv_lib_a')
    return JsonResponse(list(provenances), safe=False)

def get_agedetaille_by_agesimple(request):
    age_simple_id = request.GET.get('age_simple_id')
    ages_detailles = TbAgeDetaille.objects.filter(ags_id_n=age_simple_id).values('agd_id_n', 'agd_lib_a')
    return JsonResponse(list(ages_detailles), safe=False)

def get_cond_precis_by_cond(request):
    cond_id = request.GET.get('cond_id')
    cond_precis = TbConditionnementPrecis.objects.filter(con_id_n=cond_id).values('cop_id_n', 'cop_libelle_a')
    return JsonResponse(list(cond_precis), safe=False)

def afficher_essences_chantier(request, chantier_id):  
    chantier = get_object_or_404(TbChantierSylviculture,cs_id_n=chantier_id)  

    essences = VEssence.objects.filter(  
        cod_nv4__in=TbPlantsSouhaites.objects.filter(  
            ilo_id_n__in=TbIlots.objects.filter(  
                cs_id_n=chantier.cs_id_n  
            ).values_list('ilo_id_n', flat=True)  
        ).values_list('id_essence_n', flat=True)  
    ).distinct()  

    context = {  
        'chantier': chantier,  
        'essences': essences  
    }  
    return render(request, 'afficher_essences_chantier.html', context)



logger = logging.getLogger(__name__)  
def user_login(request):
    username = os.getenv("USERNAME")
    try:
        user = User.objects.get(username=username)
        django_login(request, user)
        return redirect('ajouter_chantier')
    except User.DoesNotExist:
        return render(request, 'ajouter_reb.html', {
            'error': f"Utilisateur '{username}' non trouvé."
        })
    
def ajouter_travaux_ilot(request, ilot_id_n):
    ilot = get_object_or_404(TbIlots, pk=ilot_id_n)
    travaux = None

    if request.method == 'POST':
        travaux_form = TbTravauxIlotForm(request.POST) 
        if travaux_form.is_valid():
            travaux = travaux_form.save(commit=False)
            travaux.ilo_id_n = ilot  
            travaux.save()
            return redirect('liste_chantiers') 
    else:
        travaux_form = TbTravauxIlotForm() 

    context = {
        'ilot': ilot, 
        'travaux': travaux,
        'travaux_form': travaux_form,
    }
    return render(request, 'travaux_ilot.html', context)  

def liste_travaux_ilot(request, ilot_id_n):  
    ilot = get_object_or_404(TbIlots, pk=ilot_id_n)  
    travaux = TbTravauxIlots.objects.filter(ilo_id_n=ilot).select_related(  
        'ilo_id_n',  
        'id_sous_traitant_a',  
        'id_niv3_n',  
        'id_niv4_n',  
        'id_niv5_n',  
        'id_typeope_n'  
    ).order_by('-til_id_n')  
    chantier=ilot.cs_id_n
    return render(request, 'liste_travaux_ilot.html', {'travaux': travaux, 'ilot': ilot, 'chantier':chantier})

def modifier_ilot(request, ilot_id):
    ilot = get_object_or_404(TbIlots, pk=ilot_id)
    
    if request.method == 'POST':
        form = TBIlotsForm(request.POST, instance=ilot)
        if form.is_valid():
            if form.cleaned_data.get('eta_id_n') == 3:  
                plants = TbPlantsSouhaites.objects.filter(ilo_id_n=ilot_id)
                plants.update(sts_id_n=3) 
            form.save()
            return redirect('liste_ilots_chantier', ilot.cs_id_n)
    else:
        form = TBIlotsForm(instance=ilot)

    chantier=ilot.cs_id_n
    types = TbEtat.objects.all()
    return render(request, 'form_ilot.html', {'form': form, 'ilot': ilot, 'types': types,'chantier':chantier})

def remplissage_Utilisateur(request):
    v_users = VUtilisateur.objects.all()
    for v_user in v_users:
        user = AuthUser.objects.create_user(
            username=v_user.username
        )
        TbUtilisateur.objects.create(
            username=v_user.username,
            role=v_user.role,
            user_djan=user 
        )
    return render(request, 'remplissage.html', {'message': 'Remplissage terminé'})