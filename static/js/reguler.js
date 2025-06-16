document.addEventListener("DOMContentLoaded", function() {
    console.log("JS chargé !");
    document.querySelector("form").addEventListener("submit", function(event) {
        const input = document.getElementById("nombre");
        const signe = document.getElementById("signe").value;
        const valeur = parseInt(input.value, 10);
        const totalReserves = parseInt(input.dataset.nbrReserves || "0", 10);
        console.log("Total réservés :", totalReserves);
        console.log("Valeur entrée :", valeur);
        console.log("Signe :", signe);

        if (signe === "-" || signe === "+" && totalReserves > 0 && valeur > totalReserves * 0.5) {
            const confirmer = confirm(
                "⚠️ La régulation demandée dépasse 50% des plants réservés (" + totalReserves + ").\n" +
                "Êtes-vous sûr de vouloir continuer ?"
            );
            if (!confirmer) {
                event.preventDefault();
            }
        }
    });
});