# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, abort
from flask.shelve import get_shelve, init_app
import datetime as dt

app = Flask(__name__)
# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, abort
from flask.shelve import get_shelve, init_app
import datetime as dt
 
app = Flask(__name__)
app.config['SHELVE_FILENAME'] = 'shelve.db'
init_app(app)

@app.route('/')
def index():
    db = get_shelve('c')
    reserves = db.get('reserves', [])
    return render_template('index.html', reserves = reserves)
 
 
@app.route('/dia/<index>')
def day(index):
    db = get_shelve('c')
    reserves = db.get('reserves', [])
    try:
        dia = reserves[int(index)]
        activitats = dia['activitats']
        for j, activitat in enumerate(activitats):
            ocupades = sum(1 for p in activitat['places'] if p)
            activitats[j]['disponibles'] = (
                len(activitat['places']) - ocupades
            )
    except:
        #abort(404)
        raise
    return render_template('dia.html', dia = dia)
 
 
@app.route('/admin', methods=["GET", "POST"])
def admin():
    db = get_shelve('c')
    reserves = db.get('reserves', [
      {
        'nom': u"Dissabte Matí",
        'activitats': [
           {'nom': u'Receptari Literari - 11:00', 'places': [False] * 15},
           {'nom': u'Llums i ombres - 11:30', 'places': [False] * 15},
           {'nom': u'El Lleó i jo - 11:45', 'places': [False] * 15},
           {'nom': u'Paraules que alimenten - 11:45', 'places': [False] * 15},        
           {'nom': u'Receptari Literari - 12:45', 'places': [False] * 15},
           {'nom': u'Paraules que alimenten - 13:00', 'places': [False] * 15},
           {'nom': u'Llums i ombres - 13:00', 'places': [False] * 15},
        ]
      }, {
        'nom': u"Dissabte Tarda",
        'activitats': [
           {'nom': u'Paraules que alimenten - 16:00', 'places': [False] * 15},
           {'nom': u'Receptari Literari - 16:30', 'places': [False] * 15},
           {'nom': u'Llums i ombres - 16:45', 'places': [False] * 15},
        ]
      }, {
        'nom': u"Diumenge Matí",
        'activitats': [
           {'nom': u'Llums i ombres - 11:00', 'places': [False] * 15},
           {'nom': u'El Lleó i jo - 11:15', 'places': [False] * 15},
           {'nom': u'Paraules que Alimenten - 11:45', 'places': [False] * 15},
           {'nom': u'Llums i ombres - 12:45', 'places': [False] * 15},
           {'nom': u'Receptari literari - 12:30', 'places': [False] * 15},
           {'nom': u'Receptari literari - 13:00', 'places': [False] * 15},
        ]
      }, {
        'nom': u"Diumenge Tarda",
        'activitats': [
           {'nom': u'Receptari literari - 16:00', 'places': [False] * 15},
           {'nom': u'Paraules que Alimenten - 17:00', 'places': [False] * 15},
        ]
      }
    ])
    if request.method == 'POST':
        for i, dia in enumerate(reserves):
            for j, activitat in enumerate(dia['activitats']):
                for k, value in enumerate(activitat['places']):
                    key = "{}_{}_{}".format(i, j, k)
                    reserves[i]['activitats'][j]['places'][k] = key in request.form
        import json
        print(json.dumps(reserves))
        db['reserves'] = reserves
    return render_template('admin.html', reserves=reserves)
 
 
if __name__ == '__main__':
    app.run(debug=True)
