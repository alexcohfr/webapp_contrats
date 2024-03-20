import requests
from bs4 import BeautifulSoup
import logging

# Logging
# Create a custom logger
logger = logging.getLogger(__name__)
# Create handlers
f_handler = logging.FileHandler('get_smic.log')
f_handler.setLevel(logging.ERROR)



# URL de la page web
url = "https://www.service-public.fr/particuliers/vosdroits/F2300"

# Envoie une requête GET pour récupérer le contenu HTML de la page
def get_smic():
    """_summary_

    Returns:
        _type_: _description_
    """
    try:
        # Envoie une requête GET pour récupérer le contenu HTML de la page
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        f_handler.error("ERROR: Failed to get URL:", e)
        smic="ERROR"
        # Gérer l'erreur ici, par exemple en affichant un message à l'utilisateur
        # ou en utilisant une valeur par défaut pour le SMIC
    else:
        html_content = response.content

        # Crée un objet BeautifulSoup à partir du contenu HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Recherche le tableau contenant les montants du Smic
        table = soup.find_all('span', class_='sp-prix')

        try:
            smic_tmp=table[1].get_text().strip().replace(" ","").replace("€","").replace(",",".")   
        except IndexError:
            f_handler.error("ERROR: Failed to get URL:", e)
            smic="ERROR"
        else: 

            smic = float(smic_tmp)

            if smic < 10 or smic > 20:
                f_handler.error("ERROR: smic value too high or too low", e)
                smic="ERROR"
    return smic
