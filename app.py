import traceback
from flask import Flask, jsonify
from poky_import_core import run_import

app = Flask(__name__)

@app.route("/import", methods=["POST"])
def import_products():
    try:
        result = run_import()
        return jsonify({"ok": True, "imported": result})
    except Exception as e:
        print("❌ Error in /import:", e)
        traceback.print_exc()
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
