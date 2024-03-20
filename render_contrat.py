from docxtpl import DocxTemplate
from config import NBRE_JOUR_TRAVAILLE, NBRE_SEMAINE_TRAVAILLE
from datetime import datetime
from get_smic import get_smic
import sqlite3

smic=get_smic()


def format_date(date):
    """Formate une date de la forme 2002-01-28 en 28 janvier 2002
    
    Args:
        date (str): date à formater
    
    Returns:
        str: date formater
    """
    # Conversion de la chaîne de caractères en objet datetime
    date_obj = datetime.strptime(date, "%Y-%m-%d")

    # Formatage de l'objet datetime en nouvelle chaîne de caractères sous la forme "28/01/2002"
    formatted_date = date_obj.strftime("%d/%m/%Y")

    return formatted_date


def format_sexe(sexe):
    """Formate le sexe du salarié pour l'adapter à la phrase
    
    Args:
        sexe (str): sexe du salarié
    
    Returns:
        tuple str: accords des différents mots utilisés dans le contrat
    """

    ###   FORMATAGE DES DONNEES POUR ACCORDER LES VARIABLES AVEC LE SEXE DU SALARIE   ###
    if sexe == "Homme":
        salariee = "Le salarié"
        monsieurmadame = "Monsieur"
        # job = "Hôte-standardiste"
        hotesse = "hôte"
        embauchee = "embauché"
        informee = "informé"
        interessee = "intéressé"
        sexe_naissance = "né"
        coiffee_apprette = "coiffé et apprêté"
        affiliee = "affilié"
        mensualisee = "mensualisé"
        il_elle = 'il'
        affectee = "affecté"
        tenue = "tenu"
    else:
        salariee = "La salariée"
        monsieurmadame = "Madame"
        # job = "Hôtesse-standardiste"
        hotesse = "hôtesse"
        embauchee = "embauchée"
        informee = "informée"
        interessee = "intéressée"
        sexe_naissance = "née"
        coiffee_apprette = "coiffée et apprêtée"
        affiliee = "affiliée"
        mensualisee = "mensualisée"
        il_elle = 'elle'
        affectee = "affectée"
        tenue = "tenue"
    
    return salariee, monsieurmadame, hotesse, embauchee, informee, interessee, sexe_naissance, coiffee_apprette, affiliee, mensualisee, il_elle, affectee, tenue
    

    


def get_ctxt(data):
    """formatage des données pour envoyer les données à render_contrat sous la bonne forme
    
    Returns:
        dict : contexte utile à docxtpl
    """


    # Data est de la forme suivante:
    # {'nom': 'test', 'prénom': 'test', 'date-naissance': '2021-01-01', 'sexe': 'Homme', 
    # 'nationalité': 'test', 'etranger': 'on', 'numéro-rue': '1', 'cp-adresse': '1', 
    # 'ville-adresse': 'test', 'ville-naissance': 'test', 'dep-naissance': 'test', 
    # 'sécu-sociale': '1', 'type-contrat': 'CDD', 'poste': 'test', 'période-essai': 'oui', 
    # 'durée-période-essai': '1', 'rémunération-type': 'Mensuel', 'salaire': '1', 'smic': '1', 
    # 'date-embauche': '2021-01-01', 'nbre_jours_formations': '1', 'date-fin-cdd': '2021-01-01', 
    # 'nbre-heure': '1', 'formation1': 'test', 'formation2': 'test', 'formation3': 'test', 'echelon': 
    # '1', 'coefficient': '1'}

    # On formate les données pour les envoyer à render_contrat

    # On commence par formater les dates
    
    date_naissance = format_date(data['date-naissance'])
    date_embauche = format_date(data['date-embauche'])
    if data['type-contrat'] == "CDD":
        date_fin_embauche = format_date(data['date-fin-cdd'])

    # Un peu moche mais voilà
    sexe = data['sexe']
    salariee, monsieurmadame, hotesse, embauchee, informee, interessee, sexe_naissance, coiffee_apprette, affiliee, mensualisee, il_elle, affectee, tenue = format_sexe(sexe)

    if sexe == "Homme":
        if data['poste'] == "Hôtesse volante multisites":
            job = "Hôte volant multisites"
        else:
            job = "Hôte-standardiste"
    else:
        if data['poste'] == "Hôtesse volante multisites":
            job = "Hôtesse volante multisites"
        else:
            job = "Hôtesse-standardiste"


    nom_contrat = f"{monsieurmadame} {data['prénom'].strip()[0].upper()}{data['prénom'].strip()[1:]} {data['nom'].strip()}" # Monsieur Alexandre COHEN
    
    renouvelable = "renouvelable" if data['période-essai'] == "ren" else "non renouvelable" #OK

    type_contrat = "CDI" if data['type-contrat'] == "CDI" else "CDD" # OK

    lieu_naissance = f"à {data['ville-naissance']} ({data['dep-naissance']})"

    try:
        stranger = data['etranger']
        nationalite = "française" if data['etranger'] != "on" else data['nationalité']
    except:
        nationalite = "française"
    
    adresse = f"{data['numéro-rue']} {data['cp-adresse']} {data['ville-adresse']}" # 15 rue Clément Bayard 92300 Levallois-Perret
    
    num_secu = data['sécu-sociale']

    heure_semaine = float(data['nbre-heure'])

    if heure_semaine >= 35:
        plein_partiel = "PLEIN"
    else:
        plein_partiel = "PARTIEL"

    heure_jour = round(heure_semaine/NBRE_JOUR_TRAVAILLE, 2)

    heure_annuelle = round(heure_jour*NBRE_JOUR_TRAVAILLE*NBRE_SEMAINE_TRAVAILLE,0)

    heure_mois = round(heure_semaine*NBRE_SEMAINE_TRAVAILLE/12,2)
    if type_contrat == "CDI":
        nbre_jours_formations = int(data['nbre_jours_formations'])
    
    

    try:
        if data['smic'] == "on":
            taux_horaire = smic
    except:
        taux_horaire = float(data['salaire'])

    if data['rémunération-type'] == "Heure":
        remuneration_mois = round(heure_semaine*NBRE_SEMAINE_TRAVAILLE/12*taux_horaire,2)
        if type_contrat == "CDI":
            if nbre_jours_formations == 0:
                remuneration_formations = 0
            else:
                remuneration_formations =round(nbre_jours_formations*taux_horaire*heure_jour,2)

    elif data['rémunération-type'] == "Jour":
        remuneration_heure = round(taux_horaire/heure_jour,2)
        remuneration_mois = round(heure_semaine*NBRE_SEMAINE_TRAVAILLE/12*remuneration_heure,2)
        if type_contrat == "CDI":
            if nbre_jours_formations == 0:
                remuneration_formations = 0
            else:
                remuneration_formations = round(nbre_jours_formations*remuneration_heure*heure_jour,2)
        
    elif data['rémunération-type'] == "Cadre":
        remuneration_mois = taux_horaire    
        remuneration_formations = 0   # On part du principe que les formations sont directement inclus dans le salaire mensuel
    if type_contrat == "CDI":
        if nbre_jours_formations == 0:
            date_formated = "aucun"
        elif nbre_jours_formations == 1:
            date_formation1 = format_date(data['formation1'])
            date_formated = f"{date_formation1}"
        elif nbre_jours_formations == 2:
            date_formation1 = format_date(data['formation1'])
            date_formation2 = format_date(data['formation2'])
            date_formated = f"{date_formation1} et {date_formation2}"
        elif nbre_jours_formations == 3:
            date_formation1 = format_date(data['formation1'])
            date_formation2 = format_date(data['formation2'])
            date_formation3 = format_date(data['formation3'])
            date_formated = f"{date_formation1}, {date_formation2} et {date_formation3}"

    temps_essai = f"{data['tps_periode_essai']} {data['durée-période-essai']}"
    

    if type_contrat == "CDI":

        context = { 
                        'SALAIRE_FORMATION' : f'{remuneration_formations}'.replace(".",","),
                        'HEURE_SEMAINE' : f'{heure_semaine}'.replace(".",","),
                        'HEURE_JOUR' : f'{heure_jour}'.replace(".",","),
                        'DATE_EMBAUCHE' : f'{date_embauche}',
                        'SALAIRE' : f'{remuneration_mois}'.replace(".",","),
                        'NOM_CONTRAT' : f'{nom_contrat}',
                        'DATE_FORMATION' : f'{date_formated}',
                        'DATE_NAISSANCE' : f'{date_naissance}',
                        'NUMERO_SECU' : f'{num_secu}',
                        'ADRESSE' : f'{adresse}',
                        'PLEIN_PARTIEL' : f'{plein_partiel}',
                        'DUREE_ANNUELLE' : f'{heure_annuelle}'.replace(".",","),
                        'NATIONALITE' : f'{nationalite}',
                        'RENOUVELABLE' : f'{renouvelable}',
                        'TEMPS_ESSAI' : f'{temps_essai}',
                        'LIEU_NAISSANCE' : f'{lieu_naissance}',
                        'ECHELON' : f'{data["echelon"]}',
                        'COEFFICIENT' : f'{data["coefficient"]}',                        
                        #Variables d'accords
                        'JOB': f'{job}',
                        'HOTESSE': f'{hotesse}',
                        'EMBAUCHEE': f'{embauchee}',
                        'INFORMEE': f'{informee}',
                        'INTERESSEE': f'{interessee}',
                        'SEXE_NAISSANCE': f'{sexe_naissance}',
                        'SALARIEE' : f'{salariee}',
                        'AFFILIEE': f'{affiliee}',
                        'COIFFEE_APPRETTE' : f'{coiffee_apprette}',
                        'MENSUALISEE' : f'{mensualisee}',
                        'TENUE' : f'{tenue}',
                        'AFFECTEE' : f'{affectee}',
                        'ELLE' : f'{il_elle}'
                        }
        verif_ctxt = {
                "vie": {
                        'Nom / Prénom' : nom_contrat,
                        'Sexe' : data['sexe'],
                        'Date de Naissance' : date_naissance,
                        'Lieu de Naissance' : f'{lieu_naissance}',
                        'Numéro de Sécurité Sociale' : num_secu,
                        'Adresse' : adresse,
                        'Nationalité' : nationalite
                },
                "contrat": {
                        'Type de Contrat' : type_contrat,
                        'Salaire mensuel' : remuneration_mois,
                        "Nombre d'heures par semaine" : heure_semaine,
                        "Date d'embauche" : date_embauche,
                        "Echelon et coefficient" : f"{data['echelon']} / {data['coefficient']}",
                        "Periode d'essai" : f'{temps_essai} {renouvelable}',
                        "Jours de formation" : date_formated,
                        "Salaire formations" : "compté dans le salaire mensuel" if data['rémunération-type'] == "Cadre" else remuneration_formations
                        }
        }



        
    elif type_contrat == "CDD":
        context = { 
                    'HEURE_SEMAINE' : f'{heure_semaine}'.replace(".",","),
                    'HEURE_JOUR' : f'{heure_jour}'.replace(".",","),
                    'DATE_EMBAUCHE' : f'{date_embauche}',
                    'SALAIRE' : f'{remuneration_mois}'.replace(".",","),
                    'NOM_CONTRAT' : f'{nom_contrat}',
                    'DATE_NAISSANCE' : f'{date_naissance}',
                    'NUMERO_SECU' : f'{num_secu}',
                    'ADRESSE' : f'{adresse}',
                    'PLEIN_PARTIEL' : f'{plein_partiel}',
                    'DUREE_ANNUELLE' : f'{heure_annuelle}'.replace(".",","),
                    'RENOUVELABLE' : f'{renouvelable}',
                    'TEMPS_ESSAI' : f'{temps_essai}',
                    'LIEU_NAISSANCE' : f'{lieu_naissance}',
                    'ECHELON' : f'{data["echelon"]}',
                    'COEFFICIENT' : f'{data["coefficient"]}',
                    'DATE_FIN_EMBAUCHE' : f'{date_fin_embauche}',
                    'HEURE_MOIS' : f'{heure_mois}'.replace(".",","),
                    'NATIONALITE' : f'{nationalite}',
                    #Variables d'accords
                    'JOB': f'{job}',
                    'HOTESSE': f'{hotesse}',
                    'EMBAUCHEE': f'{embauchee}',
                    'INFORMEE': f'{informee}',
                    'INTERESSEE': f'{interessee}',
                    'SEXE_NAISSANCE': f'{sexe_naissance}',
                    'SALARIEE' : f'{salariee}',
                    'COIFFEE_APPRETTE' : f'{coiffee_apprette}' ,
                    'AFFILIEE': f'{affiliee}',
                    'ELLE' : f'{il_elle}',
                    'TENUE' : f'{tenue}',
                    'AFFECTEE' : f'{affectee}',
                    'MENSUALISEE' : f'{mensualisee}'
                    
                    }
        verif_ctxt = {
                "vie": {
                        'Nom / Prénom' : nom_contrat,
                        'Sexe' : data['sexe'],
                        'Date de Naissance' : date_naissance,
                        'Lieu de Naissance' : f'{lieu_naissance}',
                        'Numéro de Sécurité Sociale' : num_secu,
                        'Adresse' : adresse,
                        'Nationalité' : nationalite
                },
                "contrat": {
                        'Type de Contrat' : type_contrat,
                        'Salaire mensuel' : remuneration_mois,
                        "Nombre d'heures par semaine" : heure_semaine,
                        "Date d'embauche" : date_embauche,
                        "Date de fin de contrat" : date_fin_embauche,
                        "Echelon et coefficient" : f"{data['echelon']} / {data['coefficient']}",
                        "Periode d'essai" : temps_essai,
                        }
        }
    else:
        raise ValueError("Type de contrat inconnu")
    
    return context, verif_ctxt

def render_contrat(data):
    """Rendu du contrat en fonction des données du formulaire

    Args:
        data (dict): Dictionnaire contenant les données du formulaire

    Returns:
        None
    """
    if data['type-contrat'] == "CDI":
        if data['poste'] == "Hôtesse volante multisites":
            doc = DocxTemplate(r"public/assets/Contrat_CDD_TEMPLATE.docx")
        else:
            doc = DocxTemplate(r"public/assets/Contrat_CDD_TEMPLATE.docx")
    else:
        doc = DocxTemplate(r"public/assets/Contrat_CDD_TEMPLATE.docx")
    context,verif_ctxt = get_ctxt(data)
    doc.render(context)

    date = datetime.now().strftime("%Y%m%d%H%M%S")
    doc.save(f"public/cache/contrat_{date}.docx")
    return f"public/cache/contrat_{date}.docx", verif_ctxt


if __name__ == "__main__":
    data = {'nom': 'test', 'prénom': 'test', 'date-naissance': '2021-01-01', 'sexe': 'Homme', 
    'nationalité': 'test', 'etranger': 'on', 'numéro-rue': '1', 'cp-adresse': '1',
    'ville-adresse': 'test', 'ville-naissance': 'test', 'dep-naissance': 'test',
    'sécu-sociale': '1', 'type-contrat': 'CDD', 'poste': 'test', 'période-essai': 'oui',
    'durée-période-essai': '1', 'rémunération-type': 'Cadre', 'salaire': '1', 'smic': '1',
    'date-embauche': '2021-01-01', 'nbre_jours_formations': '1', 'date-fin-cdd': '2021-01-01',
    'nbre-heure': '1', 'formation1': '2021-01-01', 'formation2': '2021-01-01', 'formation3': '2021-01-01', 'echelon': '1', 'coefficient': '1', 'tps_periode_essai': '3'}
    render_contrat(data)
