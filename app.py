from flask import Flask, render_template, request, json 
from verif import verification_client_input 
from get_smic import get_smic
from render_contrat import render_contrat
import logging
import datetime
from get_latest_contract import remove_cache, move_file_to_archive, get_latest_contrat
import requests



app = Flask(__name__, static_folder='public', static_url_path='/public')

# Logging
app.logger.setLevel(logging.ERROR)  # Set log level to INFO
handler = logging.FileHandler('app.log')  # Log to a file
app.logger.addHandler(handler)


@app.route('/') # En faire une page de login.
def index():
    """Page d'acceuil du site (directement le formulaire)

    Returns:
        template : index.html
    """
    maintenant = datetime.datetime.now()
    if request.headers.getlist("X-Forwarded-For"):
        client_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        client_ip = request.remote_addr
    print(f"HEURE :{maintenant.strftime('%m-%d %H:%M:%S')} CONNEXION : index, IP :{client_ip}")
    app.logger.info(f"INFO : {datetime.datetime.now()}: Accès à la page d''acceuil du site")
    return "<h1> Hello World </h1>"

@app.route('/demeter')
def demeter():
    """Page d'acceuil du site (directement le formulaire)

    Returns:
        template : index.html
    """
    try:
        url = 'http://freegeoip.net/json/{}'.format(request.remote_addr)
        r = requests.get(url)
        j = json.loads(r.text)
        city = j['city']
        print(city)
    except:
        pass
    maintenant = datetime.datetime.now()
    if request.headers.getlist("X-Forwarded-For"):
        client_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        client_ip = request.remote_addr
    print(f"HEURE :{maintenant.strftime('%m-%d %H:%M:%S')} CONNEXION : Demeter, IP :{client_ip}")
    app.logger.info(f"INFO : {datetime.datetime.now()}: Accès au formulaire")
    return render_template('index.html', smic = get_smic()) # Le smic est défini celui dans get_smic.py

@app.route('/download', methods=['POST','GET'])
def download():
    """Gestion de l'envoi du formulaire par l'utilisateur.

    Returns:
        template : download.html ou error.html si il y a une erreur
    """
    remove_cache()
    app.logger.info(f"INFO : {datetime.datetime.now()}: Envoi du formulaire")
    reponses_formulaire = request.form.to_dict()

    reponses_formulaire_vide = {}
    for key, value in reponses_formulaire.items():
        if value == "":
            reponses_formulaire_vide[key] = "vide"
    

    if verification_client_input(reponses_formulaire):
        nom_contrat,ctxt_verif = render_contrat(reponses_formulaire)
        return render_template('download.html', filename = nom_contrat, data = ctxt_verif)
    else:
        app.logger.error(f"ERROR : {datetime.datetime.now()}: Erreur envoi du formulaire, problème côté client ou code")
        return render_template('error.html', data = reponses_formulaire_vide)


# Page en plus de "fin de contrat" pour dire que le contrat a bien été envoyé 
# et en même temps gérer l'historique et le cache des contrats
@app.route('/end', methods=['GET'])
def finished():
    """Page de fin de contrat

    Returns:
        template : finished.html
    """
    app.logger.info(f"INFO : {datetime.datetime.now()}: Accès à la page de fin de contrat")
    if move_file_to_archive():
        app.logger.info(f" : {datetime.datetime.now()}: Le contrat a bien été envoyé")
    else:
        app.logger.error(f"ERROR : {datetime.datetime.now()}: Erreur envoi du contrat, problème côté code")
    return render_template('end.html')


### EN CHANTIER ###

# Page pour gérer l'historique des contrats
# Page de login / logout etc.



@app.errorhandler(500)
def internal_error(error):

    app.logger.error(f"ERROR : {datetime.datetime.now()}: Erreur 500, problème côté code !!")
    return render_template('error500.html'), 500

@app.errorhandler(401)
def unauthorized(error):

    app.logger.error(f"ERROR : {datetime.datetime.now()}: Erreur 401, problème côté client !!")
    return render_template('error401.html'), 401