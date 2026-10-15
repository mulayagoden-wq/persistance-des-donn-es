import os

import pandas as pd
import requests
from flask import Flask, jsonify

app = Flask(__name__)

DOSSIER = os.path.dirname(os.path.abspath(__file__))
FICHIER_LOCAL = os.path.join(DOSSIER, "data_local.json")
URL_DISTANTE = "https://dummyjson.com/products"



def resumer_prix(serie):
    desc = serie.describe().to_dict()
    return {
        "total_produits": int(desc["count"]),
        "prix_moyen": round(desc["mean"], 2),
        "prix_min": desc["min"],
        "prix_max": desc["max"],
    }


# ------------------------------------------------------------
# Accueil : liste des routes
# ------------------------------------------------------------
@app.route("/", methods=["GET"])
def accueil():
    return jsonify({
        "projet": "Mini-démo Flask + Pandas",
        "routes": ["/api/v1/stats/local", "/api/v1/stats/produits"],
    }), 200


# ------------------------------------------------------------
# Source A : fichier local
# ------------------------------------------------------------
@app.route("/api/v1/stats/local", methods=["GET"])
def stats_local():
    tableau = pd.read_json(FICHIER_LOCAL)        # DataFrame
    prix = tableau["prix"]                       # Series

    reponse = {"source": "data_local.json"}
    reponse.update(resumer_prix(prix))
    reponse["stock_total"] = int(tableau["stock"].sum())
    reponse["apercu_colonnes"] = list(tableau.columns)
    return jsonify(reponse), 200


# ------------------------------------------------------------
# Source B : Internet avec requests (HTTPS)
# ------------------------------------------------------------
@app.route("/api/v1/stats/produits", methods=["GET"])
def stats_distant():
    try:
        retour = requests.get(URL_DISTANTE, timeout=10)
        retour.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({
            "erreur": "Impossible de joindre la source distante",
            "detail": str(e),
        }), 502

    liste_produits = retour.json()["products"]
    tableau = pd.DataFrame(liste_produits)       # DataFrame
    prix = tableau["price"]                      # Series

    reponse = {"source": URL_DISTANTE}
    reponse.update(resumer_prix(prix))
    reponse["apercu_colonnes"] = list(tableau.columns)
    return jsonify(reponse), 200


if __name__ == "__main__":
    app.run(debug=True, port=3000)