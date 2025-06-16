import json
from pyexpat.errors import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import TbChantierSylvicultureForm, TbPlantsSouhaitesForm, TbSoinPlantsForm, TbTravauxChantierForm
from .models import VNIV5SOIN, TbAgeDetaille, TbChantierSylviculture, TbConditionnementPrecis, TbEtat, TbIlots,TbProvenance, TbSoinsPlants, V_TYPEChantier, VNiV4SOIN, VNiV4TRAV, VNIV5TRAV, VTypeOperation, VNiv3TRAV, VChantier,TbTravauxChantier ,TbPlantsSouhaites, TbRegul, VTypeSOINS
from django.db import connection
from django.utils.timezone import now
from django.db.models import Sum, Case, When, IntegerField
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
import time


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
        chantier = TbChantierSylviculture.objects.get(id_chantier_sylviculture_n=chantier_id)
    except TbChantierSylviculture.DoesNotExist:
        return HttpResponse("Chantier non trouvé", status=404)

    return render(request, 'liste_ilots.html', {
        'ilots_avec_calcul': ilots_avec_calcul,  # Passer la liste au template
        'chantier': chantier,
    })



def get_chantier_details(request):
    code_chantier = request.GET.get("code_chantier", "").strip()
    try:
        chantier = VChantier.objects.filter(code_chantier=code_chantier).first()

        # Tu dois ici mapper le `chantier.code_chantier` à un V_TYPEChantier, si possible
   
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
    travaux = TbTravauxChantier.objects.filter(id_cs=chantier)
    return render(request, 'voir_travaux_chantier.html', {'chantier': chantier, 'travaux': travaux})



def ajouter_chantier(request):
    start_time = time.time()
    
    if request.method == 'POST':
        t1 = time.time()
        chantier_form = TbChantierSylvicultureForm(request.POST)
        t2 = time.time()
        print(f"Temps création du formulaire : {t2 - t1:.3f}s")

        if chantier_form.is_valid():
            t3 = time.time()
            chantier = chantier_form.save()
            t4 = time.time()
            print(f"Temps validation + sauvegarde : {t4 - t3:.3f}s")

      

            print(f"⏱ Temps total traitement POST : {time.time() - start_time:.3f}s")
            return redirect('liste_chantiers')
        else:
            print("Formulaire invalide :")
            print(chantier_form.errors)

            # Afficher les requêtes même si formulaire invalide

            print(f"⏱ Temps total traitement POST avec erreurs : {time.time() - start_time:.3f}s")
    
    else:
        t5 = time.time()
        chantier_form = TbChantierSylvicultureForm()
        t6 = time.time()
        print(f"Temps création du formulaire (GET) : {t6 - t5:.3f}s")


    context = {
        'chantier_form': chantier_form,
    }

    total_time = time.time() - start_time
    print(f"⏱ Temps total fonction ajouter_chantier : {total_time:.3f}s")

    return render(request, 'ajouter_reb.html', context)



def ajouter_travaux_chantier(request, chantier_id):
    chantier = get_object_or_404(TbChantierSylviculture, pk=chantier_id)

    if request.method == 'POST':
        travaux_form = TbTravauxChantierForm(request.POST)
        if travaux_form.is_valid():
            travaux = travaux_form.save(commit=False)
            travaux.id_cs = chantier  # lie le travaux au chantier existant
            travaux.save()
            return redirect('liste_chantiers')
    else:
        travaux_form = TbTravauxChantierForm()

    context = {
        'chantier': chantier,
        'travaux_form': travaux_form,
    }
    return render(request, 'ajouter_travaux.html', context)


def liste_chantiers(request):
    chantiers = TbChantierSylviculture.objects.all().select_related(
        'id_insee', 'societe',
    )

    return render(request, 'list_reb.html', {
        'chantiers': chantiers
    })
    
    
    
def modifier_chantier(request, chantier_id):
    chantier = get_object_or_404(TbChantierSylviculture, id_chantier_sylviculture_n=chantier_id)
    if request.method == 'POST':
        form = TbChantierSylvicultureForm(request.POST, instance=chantier)
        if form.is_valid():
            form.save()
            return redirect('liste_chantiers')  # ou autre nom de vue pour retourner à la liste
    else:
        form = TbChantierSylvicultureForm(instance=chantier)
    return render(request, 'modifier_chantier.html', {'form': form, 'chantier': chantier})



@require_POST
@csrf_protect
def annuler_reboisement(request, chantier_id):
    chantier = get_object_or_404(TbChantierSylviculture, id_chantier_sylviculture_n=chantier_id)

    # Cherche les îlots liés
    ilots = TbIlots.objects.filter(cs_id_n=chantier)

    # S'il y a des îlots, vérifier les plants souhaités bloquants
    if ilots.exists():
        bloquant = TbPlantsSouhaites.objects.filter(
            ilo_id_n__in=ilots,
            sts_id_n__in=[2, 7]  # 2 = réservé, 7 = commandé
        ).exists()

        if bloquant:
            return JsonResponse({"status": "blocked"})

        # Annuler aussi les îlots
        etat_annule = TbEtat.objects.get(id_etat_n=4)
        ilots.update(eta_id_n=etat_annule)
    else:
        etat_annule = TbEtat.objects.get(id_etat_n=4)

    # Mise à jour de l’état du chantier
    chantier.etat_id_n = etat_annule
    chantier.save()

    return JsonResponse({"status": "ok", "redirect_url": "/chantiers/"})


def ajouter_plant_souhaite(request, ilot_id):
    ilot = get_object_or_404(TbIlots, pk=ilot_id)

    if request.method == 'POST':
        form = TbPlantsSouhaitesForm(request.POST)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.ilo_id_n = ilot  
            plant.save()
            return redirect('liste_plants_pour_ilot', ilot_id=ilot.ilo_id_n)  # Correction : ilot.ilo_id_n au lieu de ilot.id_ilot_n
    else:
        form = TbPlantsSouhaitesForm()  # Définit form dans le cas GET

    return render(request, 'ajouter_plantes.html', {
        'form': form,
        'ilot': ilot,
    })



def liste_plants(request, ilot_id):
    ilot = get_object_or_404(TbIlots, pk=ilot_id)
    plants = TbPlantsSouhaites.objects.filter(ilo_id_n=ilot_id)
    chantier = ilot.cs_id_n  # objet TbChantierSylviculture

    plants_with_totals = []
    for plant in plants:
        souhaites = plant.ps_nbr_plants_souhaites_n or 0
        if plant.ps_campagne_n is None:
            plant.ps_campagne_n = 0
        else:
            plant.ps_campagne_n = f" { plant.ps_campagne_n} - {plant.ps_campagne_n+ 1}"
        # Calcul des régulations pour chaque plant
        # Total des régulations pour le plant
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
            'total_regule': total_regule
        })

    return render(request, 'liste_plants.html', {
        'plants_with_totals': plants_with_totals,
        'chantier': chantier,
        'ilot': ilot,
        'plants': plants,
    })


def choix_annuler_reporter(request, ps_id):
    plant = get_object_or_404(TbPlantsSouhaites, ps_id_n=ps_id)

    STADE_ENVISAGE = 1
    STADE_ANNULE = 4  # À créer si pas encore dans la table
    STADE_COMMANDE_TERMINEE = 5  # Exemple

    if plant.sts_id_n_id == STADE_COMMANDE_TERMINEE (plant):
        messages.error(request, "Andouille, tu as déjà effectué des demandes de livraison !")
        return redirect('liste_plants', ilot_id=plant.ilo_id_n_id)

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

        if choix == "annuler":
            if total_regule > 0:
                TbRegul.objects.create(
                    ps_id_n=plant,
                    quantite=-total_regule,
                    motif="Annulation"
                )
            plant.sts_id_n_id = STADE_ANNULE
            plant.save()
            return redirect('liste_plants', ilot_id=plant.ilo_id_n_id)

        elif choix == "reporter":
            # Dupliquer la fiche
            new_plant = TbPlantsSouhaites.objects.get(pk=plant.pk)
            new_plant.pk = None
            new_plant.ps_campagne_n += 1
            new_plant.sts_id_n_id = STADE_ENVISAGE
            new_plant.save()

            # Copier les réguls
            for reg in plant.regul_set.all():
                TbRegul.objects.create(
                    ps_id_n=new_plant,
                    quantite=reg.quantite,
                    motif=f"Reporté depuis {plant.ps_id_n}"
                )

            # Marquer ancienne comme annulée
            plant.sts_id_n_id = STADE_ANNULE
            plant.save()

            return redirect('liste_plants', ilot_id=plant.ilo_id_n_id)

    return render(request, "choix_annuler_reporter.html", {"plant": plant})

def get_chantier_from_ilot(ilot):
    try:
        return TbChantierSylviculture.objects.get(id_chantier_sylviculture_n=ilot.cs_id_n)
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
    # Récupère le plant ou renvoie 404 si inexistant
    plant = get_object_or_404(TbPlantsSouhaites, pk=plant_id)

    # Récupère la liste des soins liés à ce plant
    soins = TbSoinsPlants.objects.filter(ps_id_n=plant).order_by('soi_id_n')

    context = {
        'plant': plant,
        'soins': soins,
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