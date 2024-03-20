const form = document.querySelector("form"),
        nextBtn = form.querySelector(".nextBtn"),
        backBtn = form.querySelector(".backBtn"),
        allInputfirst = form.querySelectorAll(".first input");
        allInputsecond = form.querySelectorAll(".second input");
        allSelectsecond = form.querySelectorAll(".second select");
        allInput = form.querySelectorAll("input");
 


const secusociale = document.getElementById('num-sécu');
const date_naissance = document.getElementById('date-naissance');
const checkboxsecu = document.getElementById('checkbox-sécu');
var checkboxEtranger = document.getElementById('checkbox-etranger');

// On veut remplir les premiers caractères du numéro de sécurité sociale avec le sexe (1 si homme, 2 si femme)
// On veut que les caractères 2 et 3 correspondent aux 2 derniers chiffres de l'année de naissance
// On veut que les caractères 4 et 5 correspondent au mois de naissance
// On veut que les caractères 6 et 7 correspondent au département de naissance



/*  ### Remplissage sécurité sociale ### */
form.addEventListener('input', function(e) {
    if (checkboxsecu.checked) {
    }
    else {
        if (e.target.id === 'sexe' || e.target.id === 'date-naissance' || e.target.id === 'num-sécu' || e.target.id === 'dep-naissance' ) {
            if (secusociale.value != "A venir") {
            let sexe = document.getElementById('sexe').value;
            if (sexe === 'Homme') {
                sexe = '1';
            } else if (sexe === 'Femme') {
                sexe = '2';
            }
            if (checkboxEtranger.checked) {
                cpNaissance = "99";
            }
            else {
                cpNaissance = document.getElementById('dep-naissance').value;
            }
            let dateNaissance = document.getElementById('date-naissance').value;
            let numSecu = sexe + dateNaissance.substring(2, 4) + dateNaissance.substring(5, 7) + cpNaissance + secusociale.value.substring(7 , 15);  
            secusociale.value = numSecu;
        }
        }
    } // Fonction assez claire 
});

// Si on coche "A venir", on désactive l'input et on le remplace par "A venir"
checkboxsecu.addEventListener('change', function(e) {
    if (checkboxsecu.checked) {
        secusociale.required = false;
        secusociale.type = "text";
        secusociale.value = "A venir";
    } else {
        secusociale.value = "";
        secusociale.required = true;
        secusociale.type = "number";
    }
});



// Fonction qui se charge de vérifier que tous les champs sont remplis avant de passer à la page suivante
nextBtn.addEventListener("click", ()=> {
    let status = true;
    allInputfirst.forEach(input => {
        if(input.id === 'num-sécu' && !(checkboxsecu.checked) && input.value.length !== 15){
            input.required = true;
            input.minLength = 15;
            status = false;
            alert("Le numéro de sécurité sociale doit contenir 15 chiffres");
        }
        if(input.value.trim() === ""){
            if (input.id !== 'checkbox-etranger') {
                input.required = true;
                status = false;
            }
        }
        else{
            input.required = false;
        }
    })
    if(status){
        form.classList.add('secActive');
    }
})

backBtn.addEventListener("click", () => form.classList.remove('secActive')); // On retire la classe secActive pour revenir à la page précédente


// Gestion de l'auto complétion de l'adresse
document.getElementById('adresse-input').addEventListener('input', function(e) {
    let adresse = e.target.value;

    if (adresse.length > 2) { // Pour éviter des requêtes trop fréquentes, on attend au moins 3 caractères.
        fetch(`https://api-adresse.data.gouv.fr/search/?q=${encodeURIComponent(adresse)}&limit=5`)
            .then(response => response.json())
            .then(data => {
                afficherResultats(data.features);
            })
            .catch(error => console.error('Erreur lors de la récupération des adresses:', error));
    } else {
        document.getElementById('resultats').innerHTML = ''; // Nettoyer les résultats précédents
    }
});

function afficherResultats(adresses) {
    let ul = document.getElementById('resultats');
    ul.innerHTML = ''; // Nettoyer les résultats précédents

    adresses.forEach(adresse => {
        let li = document.createElement('li');
        li.textContent = adresse.properties.label;
        li.addEventListener('click', function() {
            document.getElementById('adresse-input').value = adresse.properties.name;
            document.getElementById('cp').value = adresse.properties.postcode; // pour le code postal
            document.getElementById('ville').value = adresse.properties.city; // pour la ville
            ul.innerHTML = ''; // Nettoyer les résultats après sélection
        });
        ul.appendChild(li);
    });
}


// Récupérez l'élément input et la liste de résultats
var inputAdresse = document.getElementById('adresse-input');
var resultList = document.getElementById('resultats');

// Ajoutez un gestionnaire d'événements 'blur' à votre champ d'entrée
inputAdresse.addEventListener('blur', function(e) {
    // Utilisez une petite astuce avec setTimeout pour donner le temps à la liste d'attraper le clic sur une suggestion
    setTimeout(function() {
        // Cachez la liste de suggestions
        resultList.style.display = 'none';
    }, 100); // Un délai de 100ms est généralement suffisant
});

// Assurez-vous que la liste réapparaisse si l'utilisateur revient à l'input
inputAdresse.addEventListener('focus', function(e) {
    resultList.style.display = 'block'; // ou 'flex', 'grid', etc., selon votre mise en page
});

// Assurez-vous que la liste ne se cache pas si l'utilisateur clique sur une suggestion
resultList.addEventListener('mousedown', function(e) {
    e.preventDefault(); // Empêche le 'blur' lorsqu'on clique sur la liste
});



/*
Gestion de la checkbox "Né à l'étranger" et du changements des inputs en conséquence
*/
var inputNationalite = document.getElementById('nationalite');
var inputDepartementNaissance = document.getElementById('dep-naissance');
var inputDepartementNaissanceLabel = document.getElementById('dep-naissance-label');

checkboxEtranger.addEventListener('change', function(e) {
    if (checkboxEtranger.checked) {
        inputNationalite.disabled = false;
        inputNationalite.value = "";
        inputDepartementNaissanceLabel.innerHTML = "Pays";
        inputDepartementNaissance.placeholder = "Pays de naissance";
        inputDepartementNaissance.type = "text";
    } else {
        inputNationalite.disabled = true;
        inputNationalite.value = "Française";
        inputDepartementNaissanceLabel.innerHTML = "Département";
        inputDepartementNaissance.placeholder = "Département de naissance";
        inputDepartementNaissance.type = "number";
    }
});


// Autocomplétion pour la ville de naissance
document.getElementById('ville-naissance').addEventListener('input', function(e) {
    
    if (checkboxEtranger.checked) {
    }// Si l'utilisateur a coché la case "Etranger", on ne fait pas d'autocomplétion
    
    else{
        let adresse = e.target.value;
        if (adresse.length > 2) { // Pour éviter des requêtes trop fréquentes, on attend au moins 3 caractères.
            fetch(`https://api-adresse.data.gouv.fr/search/?q=${encodeURIComponent(adresse)}&limit=5`)
                .then(response => response.json())
                .then(data => {
                    afficherResultatsNaissance(data.features);
                })
                .catch(error => console.error('Erreur lors de la récupération des adresses:', error));
        } else {
            document.getElementById('resultats').innerHTML = ''; // Nettoyer les résultats précédents
        }
    }
});

// Fonction claire
function afficherResultatsNaissance(adresses) {
    let ul = document.getElementById('resultats-naissance');
    ul.innerHTML = ''; // Nettoyer les résultats précédents

    adresses.forEach(adresse => {
        let li = document.createElement('li');
        li.textContent = adresse.properties.city;
        li.addEventListener('click', function() {
            document.getElementById('ville-naissance').value = adresse.properties.city;
            // On ne choisit que les 2 premiers chiffres du code postal
            document.getElementById('dep-naissance').value = adresse.properties.postcode.substring(0, 2);
            ul.innerHTML = ''; // Nettoyer les résultats après sélection
            if (checkboxsecu.checked) {}
            else {
            secusociale.value = secusociale.value.substring(0, 5) + adresse.properties.postcode.substring(0, 2) + secusociale.value.substring(7, 15);
            }
        });
        ul.appendChild(li);
    });
}

var inputAdresseNaissance = document.getElementById('ville-naissance');
var resultListNaissance = document.getElementById('resultats-naissance');

// Ajoutez un gestionnaire d'événements 'blur' à votre champ d'entrée
inputAdresseNaissance.addEventListener('blur', function(e) {
    // Utilisez une petite astuce avec setTimeout pour donner le temps à la liste d'attraper le clic sur une suggestion
    setTimeout(function() {
        // Cachez la liste de suggestions
        resultListNaissance.style.display = 'none';
    }, 100); // Un délai de 100ms est généralement suffisant
});

// Assurez-vous que la liste réapparaisse si l'utilisateur revient à l'input
inputAdresseNaissance.addEventListener('focus', function(e) {
    resultListNaissance.style.display = 'block'; // ou 'flex', 'grid', etc., selon votre mise en page
});

// Assurez-vous que la liste ne se cache pas si l'utilisateur clique sur une suggestion
resultListNaissance.addEventListener('mousedown', function(e) {
    e.preventDefault(); // Empêche le 'blur' lorsqu'on clique sur la liste
});


const JoursFomations = document.getElementById('nbreformation');
const dateFormation = document.getElementById('formation1');
const dateFormationDiv = document.getElementById('formation1-div');
const dateFormation2 = document.getElementById('formation2');
const dateFormationDiv2 = document.getElementById('formation2-div');
const dateFormation3 = document.getElementById('formation3');
const dateFormationDiv3 = document.getElementById('formation3-div');
const divformation = document.getElementById('divformation');


// Gestion des jours de formation en fonction du nombre de jours de formation
JoursFomations.addEventListener('input', function(e) {
    let nbreFormation = e.target.value;
    if (nbreFormation == 1) {
        dateFormation.required = true;
        dateFormation.disabled = false;
        dateFormationDiv.style.display = 'flex';
        dateFormation2.required = false;
        dateFormationDiv2.disabled = true;
        dateFormationDiv2.style.display = 'none';
        dateFormation3.required = false;
        dateFormationDiv3.disabled = true;
        dateFormationDiv3.style.display = 'none';
        divformation.style.display = 'flex';
    }
    else if (nbreFormation == 2) {
        dateFormation.disabled = false;
        dateFormation.required = true;
        dateFormationDiv.style.display = 'flex';
        dateFormation2.disabled = false;
        dateFormation2.required = true;
        dateFormationDiv2.style.display = 'flex';
        dateFormation3.required = false;
        dateFormation3.disabled = true;
        dateFormationDiv3.style.display = 'none';
        divformation.style.display = 'flex';
    }
    else if (nbreFormation == 3) {
        dateFormation.disabled = false;
        dateFormation.required = true;
        dateFormationDiv.style.display = 'flex';
        dateFormation2.disabled = false;
        dateFormation2.required = true;
        dateFormationDiv2.style.display = 'flex';
        dateFormation3.disabled = false;
        dateFormation3.required = true;
        dateFormationDiv3.style.display = 'flex';
        divformation.style.display = 'flex';
    }
    else {
        dateFormation.required = false;
        dateFormation.disabled = true;
        dateFormationDiv.style.display = 'none';
        dateFormation2.required = false;
        dateFormation2.disabled = true;
        dateFormationDiv2.style.display = 'none';
        dateFormation3.required = false;
        dateFormation3.disabled = true;
        dateFormationDiv3.style.display = 'none';
        divformation.style.display = 'none';
    }
});


const typeContrat = document.getElementById('type-contrat');
const dateFin = document.getElementById('date-fin-cdd');
const dateFinInput = document.getElementById('date-fin-input');
const divNbreFormation = document.getElementById('jours-formation');
const labelformation = document.getElementById('label-formation');

typeContrat.addEventListener('input', function(e) {
    if (typeContrat.value === "CDD") {
        dateFinInput.required = true;
        divNbreFormation.style.display = 'none';
        dateFin.style.display = 'flex';
        divformation.style.display = 'none';
        labelformation.style.display = 'none';
    }
    else if (typeContrat.value === "CDI") {
        dateFin.required = false;
        dateFin.style.display = 'none';
        divformation.style.display = 'flex';
        divNbreFormation.style.display = 'flex';
        JoursFomations.required = true;
        labelformation.style.display = 'flex';
    }
});

/* Mode de rémunération */

const modeRemuneration = document.getElementById('rémunération-input');
const mondeRemunerationDiv = document.getElementById('rémunération-div');
const salaire = document.getElementById('salaire');
const salairelabel = document.getElementById('salaire-label');
const smic = document.getElementById('smic-checbox');
const smiclabel = document.getElementById('smic-checbox-label');


modeRemuneration.addEventListener('input', function(e) {
    if (modeRemuneration.value === "Heure") {
        salaire.required = true;
        salaire.placeholder = "Taux horaire";
        salairelabel.innerHTML = "Taux horaire";
        smic.style.display = 'flex';
        smiclabel.style.display = 'flex';

    }
    else if (modeRemuneration.value === "Jour") {
        salaire.required = true;
        salaire.placeholder = "Salaire journalier";
        salairelabel.innerHTML = "Salaire journalier";
        smic.style.display = 'none';
        smiclabel.style.display = 'none';
    }
    else if (modeRemuneration.value === "Cadre") {
        salaire.required = true;
        salaire.placeholder = "Salaire mensuel";
        salairelabel.innerHTML = "Salaire mensuel";
        smic.style.display = 'none';
    }
    else {
        salaire.required = false;
    }
});


smic.addEventListener('change', function(e) {
    if (smic.checked) {
        salaire.disabled = true;
        salaire.value = "";
        salaire.required = false;
    }
    else {
        salaire.disabled = false;
        salaire.required = true;
    }
});

/* On code le bouton submit de la 2e page*/

const buttonSubmit = document.getElementById('submit_button');

// On va vérifier que tous les inputs ne sont pas vides et, si certains ont un ID on leur appliquera un filtre différent
function checkallinputs() {
    let allInputsValid = true;
    allSelectsecond.forEach(select => {
        if (select.value === "default") {
            if (select.id === 'nbreformation') {
                if (typeContrat.value === "CDD") {
                    select.required = false;
                } else {
                    select.required = true;
                    console.log("nbre_formation", select);
                    allInputsValid = false;
                }
            } else {
                select.required = true;
                select.classList.add('error');
                console.log("select", select);
                allInputsValid = false;
            }
        } else {
            select.classList.remove('error');
            select.required = false;
        }
    });

    allInput.forEach(input => {
        if (input.value.trim() === "") {
            if (input.id === "date-fin-input" && typeContrat.value === "CDI") {
                input.required = false;
            } 
            else if (input.id === "salaire") {
                if (smic.checked === true) {
                    input.required = false;
                    console.log("salaire1",input);
                } else {
                    input.required = true;
                    console.log("salaire2",input);
                    allInputsValid = false;
                }
            } else if (input.id === 'formation1') {
                if (typeContrat.value === "CDI" && JoursFomations.value >= 1) {
                    input.required = true;
                    console.log("formation",input);
                    allInputsValid = false;
                }
            } 
            else if (input.id === 'formation2') {
                if (typeContrat.value === "CDI" && JoursFomations.value >= 2) {
                    input.required = true;
                    console.log("formation",input);
                    allInputsValid = false;
                }
            }
            else if (input.id === 'formation3') {
                if (typeContrat.value === "CDI" && JoursFomations.value === 3) {
                    input.required = true;
                    console.log("formation",input);
                    allInputsValid = false;
                }
            }
            else {
                input.required = true;
                console.log("input", input.value);
                allInputsValid = false;
                        }
        } else {
            input.required = false;
        }
    });

    return allInputsValid;
}

buttonSubmit.addEventListener('click', function(e) {
    e.preventDefault();
    if (checkallinputs()) {
        form.submit();
    }
    else{
        alert("Veuillez remplir tous les champs obligatoires");
    }
});


// On ajoute un envent listener pour tous les inputs qui va changer dynamiquement leur title en fonction de ce qu'on a entré
// On actualise tous les titles à chaque fois qu'on change la valeur d'un input pour avoir ceux qui sont autocomplétés

allInput.forEach(input => {
    let intervalId = null; // Identifiant pour l'intervalle, utilisé pour le démarrer et l'arrêter

    // Fonction pour vérifier la valeur de l'input et mettre à jour le titre
    const checkValueAndUpdateTitle = () => {
        if (input.title !== input.value) {
            input.title = input.value; // Mettre à jour le titre si la valeur de l'input a changé
        }
    };

    // Écouter l'événement 'focus' pour démarrer la vérification périodique
    input.addEventListener('focus', function() {
        intervalId = setInterval(checkValueAndUpdateTitle, 200); // Vérifier toutes les 200 millisecondes
    });

    // Écouter l'événement 'blur' pour arrêter la vérification périodique
    input.addEventListener('blur', function() {
        clearInterval(intervalId); // Arrêter la vérification périodique
    });
});

