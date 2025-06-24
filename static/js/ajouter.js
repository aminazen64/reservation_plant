$(document).ready(function () {


 
    // Activer Select2
    $('select').select2({ width: '100%' });

    // Niveau 3 → Niveau 4
    $('#id_niv3').on('change', function () {
        const niv3Id = $(this).val();
        if (!niv3Id) return;

        $.get(getNiv4Url, { niv3_id: niv3Id }, function (data) {
            $('#id_niv4').empty().append('<option value="">---------</option>');
            $('#id_niv5, #id_typeope').empty().append('<option value="">---------</option>');

            data.forEach(function (item) {
                $('#id_niv4').append(new Option(item.nv4_lib_a, item.nv4_codnv4_n));
            });

            $('#id_niv5').trigger('change');
        });
    });

    // Niveau 4 → Niveau 5
    $('#id_niv4').on('change', function () {
        const niv4Id = $(this).val();
        if (!niv4Id) return;

        $.get(getNiv5Url, { niv4_id: niv4Id }, function (data) {
            $('#id_niv5').empty().append('<option value="">---------</option>');
            $('#id_typeope').empty().append('<option value="">---------</option>');

            data.forEach(function (item) {
                $('#id_niv5').append(new Option(item.nv5_lib_a, item.nv5_codnv5_n));
            });

            $('#id_niv5').trigger('change');
        });
    });

    // Niveau 5 → Type opération
    $('#id_niv5').on('change', function () {
        const niv5Id = $(this).val();
        if (!niv5Id) return;

        $.get(getOpsUrl, { niv5_id: niv5Id }, function (data) {
            $('#id_typeope').empty().append('<option value="">---------</option>');
            data.forEach(function (item) {
                $('#id_typeope').append(new Option(item.typ_libope_a, item.typ_codope_n));
            });
        });
    });

    // Type de chantier → Remplir infos
    $('#id_chantier_virtuel').on('change', function () {
        const codeChantier = $(this).val();
        if (!codeChantier) return;

        $.get(getChantierDetailsUrl, { code_chantier: codeChantier }, function (data) {
            console.log(data);
            if (data.error) {
                console.warn("Erreur:", data.error);
                return;
            }

            if ($('#id_bureau').length) {
                $('#id_bureau').val(data.bureau).trigger('change.select2');
                $('#id_bureau').on('select2:opening select2:unselecting', function(e) {
                    e.preventDefault();
                });
            }
            if ($('#id_agence').length) {
                $('#id_agence').val(data.agence).trigger('change.select2');
                $('#id_agence').on('select2:opening select2:unselecting', function(e) {
                    e.preventDefault();
                });
            }
            if ($('#id_nom_propietaire').length) {
                $('#id_nom_propietaire').val(data.propietaire);
                $('#id_nom_propietaire').prop('readonly', true);
            }
            if ($('#id_secteur').length) {
                $('#id_secteur').val(data.secteur).trigger('change.select2');
                $('#id_secteur').on('select2:opening select2:unselecting', function(e) {
                    e.preventDefault();
                });
            }
            if ($('#id_surface').length) {
                $('#id_surface').val(data.surface).prop('readonly', true);
            }
          if    ($('#id_subvention').length) {
                $('#id_subvention').val(data.subvention);
                $('#id_subvention').prop('checked', data.subvention === 'O');
                $('#id_subvention').prop('readonly', true);
            }
            if ($('#id_insee_commune').length) {
                $('#id_insee_commune').val(data.insee_commune).trigger('change.select2');
                $('#id_insee_commune').on('select2:opening select2:unselecting', function(e) {
                    e.preventDefault();
                });
            }
                       // Type chantier : rempli aussi (mais on le rend modifiable après)
                        const $chantier = $('#id_type_chantier');
            if ($chantier.length && data.type_chantier) {
                if ($chantier.find(`option[value="${data.type_chantier}"]`).length === 0) {
                    // Injecte une option temporaire si elle n'existe pas
                    $chantier.append(new Option(data.type_chantier, data.type_chantier, true, true));
                }
                $chantier.val(data.type_chantier).trigger('change.select2');
            }

            $('#id_chantier_virtuel').val('').trigger('change.select2');
        });
    });



     $('#id_id_essence_n').change(function(){
            var essenceId = $(this).val();
            $.ajax({
                url: '/ajax/get_provenances/',
                data: {'essence_id': essenceId},
                success: function(data){
                    var $select = $('#id_prv_id_n');
                    $select.empty();
                    $select.append('<option value="">---------</option>');
                    data.forEach(function(item){
                        $select.append('<option value="'+item.prv_id_n+'">'+item.prv_lib_a+'</option>');
                    });
                }
            });
        });

        // Âge Détail par Âge Simple
        $('#id_ags_id_n').change(function(){
            var ageSimpleId = $(this).val();
            $.ajax({
                url: '/ajax/get_agedetaille/',
                data: {'age_simple_id': ageSimpleId},
                success: function(data){
                    var $select = $('#id_agd_id_n');
                    $select.empty();
                    $select.append('<option value="">---------</option>');
                    data.forEach(function(item){
                        $select.append('<option value="'+item.agd_id_n+'">'+item.agd_lib_a+'</option>');
                    });
                }
            });
        });

        // Conditionnement précis par Conditionnement
        $('#id_con_id_n').change(function(){
            var condId = $(this).val();
            $.ajax({
                url: '/ajax/get_cond_precis/',
                data: {'cond_id': condId},
                success: function(data){
                    var $select = $('#id_cop_id_n');
                    $select.empty();
                    $select.append('<option value="">---------</option>');
                    data.forEach(function(item){
                        $select.append('<option value="'+item.cop_id_n+'">'+item.cop_libelle_a+'</option>');
                    });
                }
            });
        });
        
    $('form').on('submit', function () {
        $("#loading-overlay").css("display", "flex");
    });

    // Niveau 3 → Niveau 4
$('#id_soins_niv3_n').on('change', function () {
    const niv3Id = $(this).val();
    if (!niv3Id) return;

    $.get(getNiv4SoinsUrl, { niv3_id: niv3Id }, function (data) {
        $('#id_soins_niv4_n').empty().append('<option value="">---------</option>');
        $('#id_soins_niv5_n, #id_id_typeope_n').empty().append('<option value="">---------</option>');

        data.forEach(function (item) {
            $('#id_soins_niv4_n').append(new Option(item.nv4_lib_a, item.nv4_codnv4_n));
        });

        $('#id_soins_niv4_n').trigger('change');
    });
});

// Niveau 4 → Niveau 5
$('#id_soins_niv4_n').on('change', function () {
    const niv4Id = $(this).val();
    if (!niv4Id) return;

    $.get(getNiv5SoinsUrl, { niv4_id: niv4Id }, function (data) {
        $('#id_soins_niv5_n').empty().append('<option value="">---------</option>');
        $('#id_id_typeope_n').empty().append('<option value="">---------</option>');

        data.forEach(function (item) {
            $('#id_soins_niv5_n').append(new Option(item.nv5_lib_a, item.nv5_codnv5_n));
        });

        $('#id_soins_niv5_n').trigger('change');
    });
});


// Niveau 5 → Type d'opération
$('#id_soins_niv5_n').on('change', function () {
    const niv5Id = $(this).val();
    if (!niv5Id) return;

    $.get(getOpsSoinsUrl, { niv5_id: niv5Id }, function (data) {
        $('#id_id_typeope_n').empty().append('<option value="">---------</option>');

        data.forEach(function (item) {
            $('#id_id_typeope_n').append(new Option(item.typ_libope_a, item.typ_codope_n));
        });
    });
});

if (document.querySelector('input[name="etat_id_n"]')) {
    document.querySelector('input[name="etat_id_n"][value="2"]').disabled = true;
    document.querySelector('input[name="etat_id_n"][value="4"]').disabled = true;
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Ce cookie commence par le nom qu’on cherche
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ✅ On définit bien la variable avant usage
const csrftoken = getCookie('csrftoken');

         $('#btn-annuler-reboisement').click(function() {
            if (confirm("Êtes-vous sûr de vouloir annuler ce reboisement ?")) {
                fetch(annulerReboisementUrl, {
                    method: "POST",
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({})
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "ok") {
                        // Redirection
                        window.location.href = data.redirect_url;
                    } else if (data.status === "blocked") {
                        alert("Impossible d'annuler : des plants sont encore en état 'réservé' ou 'commandé'.");
                    } else {
                        alert("Erreur lors de l’annulation.");
                    }
                })
                .catch(error => {
                    console.error("Erreur fetch :", error);
                    alert("Erreur réseau.");
                });



            }
        });



        
});
