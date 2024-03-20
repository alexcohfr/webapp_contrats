import re
import os
from config import CHAMP_FORMULAIRE, CHAMP_FORMULAIRE_INDISPENSABLE
import logging




def verification_client_input(dict_input)-> tuple[bool,dict]:
    """
    This function will verify the inputs transmitted by the user to the server.
    """

    # Check if the input is a dictionary
    if not isinstance(dict_input, dict):
        return False,{"type d'erreur": "Mauvais type d'entrée des donnés."}

    # Check if the input contains the right keys
    dic_reponse = {"type d'erreur": "Champs manquants ou mal remplis."}
    status = True
    type_contrat = dict_input["type-contrat"]
    for key, value in dict_input.items():
        try:
            CHAMP_FORMULAIRE_INDISPENSABLE.remove(key)
        except:
            pass
        if key not in CHAMP_FORMULAIRE:
            return False,{"type d'erreur": "Des champs non compris dans le formulaire ont été envoyés."}
        else:
            # Vérification de tous les champs du formulaire pour les valider côté serveur.
            # Les champs qu'on ne vérifie pas sont les suivants: "numéro-rue" -> on a pas de pattern a exclure donc ça sert à rien
            if key == "nom":
                pattern = re.compile(r'[0-9]')
                # Match all digits in the string and replace them with an empty string
                new_value = re.sub(pattern, '', value )
                if value == "" or new_value != value:
                    
                    dic_reponse[key] = value
                    status = False

            if key ==  "prénom":
                pattern = re.compile(r'[0-9]')
                new_value = re.sub(pattern, '', value )
                if value == "" or new_value != value:
                    
                    dic_reponse[key] = value
                    status = False

            if key ==  "date-naissance":
                pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
                try:
                    new_value = pattern.findall(value)[0]
                except:
                    new_value = None
                if value == "" or new_value != value:
                    
                    dic_reponse[key] = value
                    status = False

            if key ==  "sexe":
                pattern = re.compile(r'^(Homme|Femme)$')
                try:
                    new_value = pattern.findall(value)[0]
                except:
                    new_value = None
                if value == "" or new_value != value:
                    
                    dic_reponse[key] = value
                    status = False

            if key ==  "nationalité":
                pattern = re.compile(r'[0-9]')
                try:
                    new_value = re.sub(pattern, '', value )
                except:
                    new_value = None
                if value == "" or new_value != value:
                    
                    dic_reponse[key] = value
                    status = False

            if key ==  "etranger":
                if value != "on":
                    
                    dic_reponse[key] = value
                    status = False

            if key ==  "cp-adresse":
                pattern = re.compile(r'\d{5}')
                new_value = pattern.findall(value)[0]
                if value == "" or new_value != value:
                    
                    dic_reponse[key] = value
                    status = False

            if key ==  "ville-adresse":
                pattern = re.compile(r'[0-9]')
                new_value = re.sub(pattern, '', value )
                if value == "" or new_value != value:
                    
                    dic_reponse[key] = value
                    status = False

            if key ==  "ville-naissance":
                pattern = re.compile(r'[0-9]')
                new_value = re.sub(pattern, '', value )
                if value == "" or new_value != value:
                    
                    dic_reponse[key] = value
                    status = False

            if key ==  "dep-naissance":
                pattern = re.compile(r'\d{2}')
                try:
                    new_value = pattern.findall(value)[0]
                except:
                    new_value = None
                if value == "" or new_value != value:
                    
                    dic_reponse[key] = value
                    status = False

            if key ==  "sécu-sociale":
                pattern = re.compile(r'\d{15}')
                try:
                    new_value = pattern.findall(value)[0]
                except:
                    new_value = None
                if value == "" or new_value != value:
                    
                    dic_reponse[key] = value
                    status = False

            if key ==  "type-contrat":
                if value not in ["CDI", "CDD"]:
                    
                    dic_reponse[key] = value
                    status = False

            if key ==  "poste":
                if value not in ["hotesse","coord_site","concierge","autre"]:
                    
                    dic_reponse[key] = value
                    status = False

            if key ==  "période-essai":
                if value not in ["ren","non_ren"]:
                    
                    dic_reponse[key] = value
                    status = False

            if key ==  "durée-période-essai":
                if value not in ["Mois","Jours"]:
                    
                    dic_reponse[key] = value
                    status = False

            if key ==  "rémunération-type":
                if value not in ["Heure","Jour","Cadre"]:
                    
                    dic_reponse[key] = value
                    status = False

            if key ==  "salaire":
                if not value.isdigit():
                    
                    dic_reponse[key] = value
                    status = False

            if key ==  "smic":
                if value != "on":
                    
                    dic_reponse[key] = value
                    status = False

            if key ==  "date-embauche":
                pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
                try:
                    new_value = pattern.findall(value)[0]
                except:
                    new_value = None
                if value == "" or new_value != value:
                    
                    dic_reponse[key] = value
                    status = False

            if key ==  "nbre_jours_formations":
                nbre_jours_formations = None
                if value not in ["0","1","2","3"]:
                    
                    dic_reponse[key] = value
                    status = False

                else:
                    nbre_jours_formations = value
                
            if key ==  "date-fin-cdd":
                if dict_input["type-contrat"] == "CDI":
                    pass
                else:
                    pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
                    try:
                        new_value = pattern.findall(value)[0]
                    except:
                        new_value = None
                    if value == "" or new_value != value:
                        
                        dic_reponse[key] = value
                        status = False

            if key ==  "nbre-heure":
                if not value.isdigit():
                    
                    dic_reponse[key] = value
                    status = False

            if key ==  "formation1":
                if type_contrat == "CDI":
                    if nbre_jours_formations not in ["1","2","3"]:
                        pass
                    elif nbre_jours_formations > "0":
                        pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
                        try:
                            new_value = pattern.findall(value)[0]
                        except:
                            new_value = None
                        if value == "" or new_value != value:
                            
                            dic_reponse[key] = value
                            status = False

            if key ==  "formation2":
                if type_contrat == "CDI":
                    if nbre_jours_formations not in ["2","3"]:
                        pass
                    elif nbre_jours_formations > "1":
                        pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
                        try:
                            new_value = pattern.findall(value)[0]
                        except:
                            new_value = None
                        if value == "" or new_value != value:
                            
                            dic_reponse[key] = value
                            status = False

            if key ==  "formation3":
                if type_contrat == "CDI":
                    if nbre_jours_formations != "3":
                        pass
                    elif nbre_jours_formations > "2":
                        pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
                        try:
                            new_value = pattern.findall(value)[0]
                        except:
                            new_value = None
                        if value == "" or new_value != value:
                            
                            dic_reponse[key] = value
                            status = False

            if key ==  "tps_periode_essai":
                if not value.isdigit():
                    
                    dic_reponse[key] = value
                    status = False
    
    if len(CHAMP_FORMULAIRE_INDISPENSABLE) > 0:
        return False,{"type d'erreur": "Des champs indispensables n'ont pas été remplis."}
    
    
    return status, dic_reponse


if __name__ ==  "__main__":
    pass
