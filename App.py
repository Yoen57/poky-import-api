from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/import", methods=["POST"])
def import_products():
    data = request.get_json() or {}

    shop = data.get("shop")
    # 👉 hier kun je later je echte Poky-logica zetten
    print(f"Received import request for shop: {shop}")

    return jsonify({
        "ok": True,
        "shop": shop,
        "message": "Poky importer received the request successfully."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
