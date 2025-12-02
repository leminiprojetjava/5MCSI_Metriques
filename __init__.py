from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")
    
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Convert Kelvin -> °C
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route('/commits-data/')
def commits_data():
    # Appel à l'API GitHub pour récupérer la liste des commits
    response = urlopen('https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))

    # Dictionnaire minute -> nombre de commits
    commits_by_minute = {}

    for commit in json_content:
        # On récupère la date du commit : commit -> author -> date
        date_str = commit.get('commit', {}).get('author', {}).get('date')
        if date_str:
            # Exemple de date : "2024-02-11T11:57:27Z"
            date_object = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minute = date_object.minute  # minute = 0 à 59
            commits_by_minute[minute] = commits_by_minute.get(minute, 0) + 1

    # Transformation en liste pour l'envoyer au front
    results = []
    for minute in sorted(commits_by_minute.keys()):
        results.append({'minute': minute, 'count': commits_by_minute[minute]})

    return jsonify(results=results)
    
@app.route("/commits/")
def commits_graph():
    return render_template("commits.html")

if __name__ == "__main__":
    app.run(debug=True)
