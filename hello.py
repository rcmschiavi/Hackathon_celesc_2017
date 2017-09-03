from flask import Flask, send_file, send_from_directory, render_template
import json
import sqlite3
from flask_googlemaps import GoogleMaps, Map, icons

import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__, template_folder="web", static_folder="web/tmp")
# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "XXXXXXXXXX"

# Initialize the extension
GoogleMaps(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
conn = sqlite3.connect('possiveis_fraudes.db')

@app.route('/')
def hello_world():
    return send_file('web/index.html')

@app.route('/req')
def req():
    return send_file('web/req.html')

@app.route("/web/tablestyles.css")
def table_styles():
    return send_file('web/tablestyles.css')

@app.route('/tmp/marca_celesc.jpeg')
def foto():
    return send_file('web/tmp/marca_celesc.jpeg')

@app.route("/maps")
def mapview():
    trdmap = Map(
        identifier="trdmap",
        lat=37.4419,
        lng=-122.1419,
        markers=[
            {
                'icon': icons.alpha.B,
                'lat':  37.4419,
                'lng':  -122.1419,
                'infobox': "Hello I am < b style='color:green;'>B< / b >!"
            },
            {
                'icon': icons.dots.blue,
                'lat': 37.4300,
                'lng': -122.1400,
                'infobox': "Hello I am < b style='color:blue;'>BLUE< / b >!"
            },
            {
                'icon': icons.dots.yellow,
                'lat': 37.4500,
                'lng': -122.1350,
                'infobox': (
                    "Hello I am < b style='color:#ffcc00;'> YELLOW < / b >!"
                    "< h2 >It is HTML title< / h2 >"
                    "< img src=' //placehold.it/50' >"
                    "< br >Images allowed!"
                )
            }
        ]
    )
    return render_template('mapa.html', trdmap=trdmap)


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