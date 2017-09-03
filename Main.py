'''
Equipe Meca Solutions - Hackathon Celesc 2017
Rodolfo Cavour Moretti Schiavi - rodolfocmschiavi@gmail.com
================================================

Esse código realiza a função de um Web Service com Flask, realizando a comunicação entre o banco de dados e os terminais web
e implementando um mapa com simulações de uma situação de avalização de fiscalização
'''

from flask import Flask, send_file, render_template
import json
import sqlite3
from flask_googlemaps import GoogleMaps, Map, icons

# Configurações do Flask
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__, template_folder="web", static_folder="web/tmp")
app.config['GOOGLEMAPS_KEY'] = "AIzaSyDJBPpeHwqiVegrupbUWieBsbrET8CeIwI"
GoogleMaps(app)

# Inicialização do DB
conn = sqlite3.connect('possiveis_fraudes.db')

# Instancia as páginas no servidor
@app.route('/')
def index():
    return send_file('web/index.html')
@app.route('/req')
def req():
    return send_file('web/req.html')
@app.route("/web/tablestyles.css")
def table_styles():
    return send_file('web/tablestyles.css')
@app.route('/tmp/marca_celesc.jpeg')
def pic():
    return send_file('web/tmp/marca_celesc.jpeg')

# Realiza a inserção do Maps no terminal
@app.route("/maps")
def mapview():
    trdmap = Map(
        style="height:100%;width:100%;margin:0;",
        identifier="trdmap",
        lat=-27.595303,
        lng= -48.544976,
        markers=[
            {
                'icon': icons.alpha.B,
                'lat':  -27.595343,
                'lng':  -48.544978,
                'infobox': "Grande risco de gato!"
            },
            {
                'icon': icons.dots.blue,
                'lat':  -27.590843,
                'lng':  -48.549478,
                'infobox': "Parece estar tudo OK!"
            },
            {
                'icon': icons.dots.yellow,
                'lat': -27.596117,
                'lng': -48.552894,
                'infobox': (
                    "Há indicioes de fraude!"
                )
            }
        ]
    )
    return render_template('mapa.html', trdmap=trdmap)

# Fornece os dados para a atualização das informações no terminal
@app.route("/update")
def update():
    cur = conn.cursor()
    cur.execute(
'''
SELECT * FROM Suspeitos
 ORDER BY Suspeitos.probabilidade DESC
'''
                )
    data = [list(tup) for tup in cur.fetchall()]
    print(data)

    cur.close()

    return json.dumps(data)

app.run()