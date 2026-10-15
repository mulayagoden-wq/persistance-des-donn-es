from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)


@app.route("/api/v1/stats/produits", methods=["GET"])
def analyser_produits():
    # 1. Récupérer les données depuis Internet
    url = "https://dummyjson.com/products"
    donnees = pd.read_json(url)

    # 2. Transformer les produits en tableau
    df = pd.DataFrame(list(donnees["products"]))

    # 3. Sélectionner la colonne des prix
    series_prix = df["price"]

    # 4. Calculer les statistiques
    stats = series_prix.describe().to_dict()

    # 5. Renvoyer les résultats en JSON
    return jsonify({
        "total_produits": int(stats["count"]),
        "prix_moyen": round(stats["mean"], 2),
        "prix_min": stats["min"],
        "prix_max": stats["max"],
        "apercu_colonnes": list(df.columns)
    }), 200


if __name__ == "__main__":
    app.run(debug=True)