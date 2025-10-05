import os
import json
import requests
from openai import OpenAI

# ====== CONFIG ======
SHOPIFY_DOMAIN = os.getenv("SHOPIFY_DOMAIN")  # vb: vivaicona.myshopify.com
SHOPIFY_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# ====== FUNCTIE: titel + beschrijving herschrijven ======
def rewrite_product_text(title, description):
    prompt = f"""
    Rewrite the following product information in fluent Italian, optimized for Shopify SEO.
    Title: {title}
    Description: {description}
    Output: short JSON with keys 'title' and 'description'.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    data = json.loads(response.choices[0].message.content)
    return data["title"], data["description"]

# ====== FUNCTIE: product toevoegen aan Shopify ======
def create_product_on_shopify(title, body_html):
    url = f"https://{SHOPIFY_DOMAIN}/admin/api/2024-07/products.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": SHOPIFY_TOKEN
    }
    payload = {
        "product": {
            "title": title,
            "body_html": body_html,
            "status": "draft"
        }
    }
    r = requests.post(url, headers=headers, json=payload)
    return r.status_code, r.text

# ====== HOOFDFUNCTIE ======
def run_import():
    # voorbeeld: normaal komt dit uit Excel of Poky-scraper
    example_products = [
        {"title": "Blusa donna elegante", "description": "Camicia con bottoni e maniche lunghe"},
        {"title": "Pantaloni casual", "description": "Pantaloni comodi in cotone"}
    ]

    results = []
    for p in example_products:
        new_title, new_desc = rewrite_product_text(p["title"], p["description"])
        status, resp = create_product_on_shopify(new_title, new_desc)
        results.append({
            "original": p["title"],
            "new_title": new_title,
            "status": status
        })
    return results


if __name__ == "__main__":
    output = run_import()
    print(json.dumps(output, indent=2, ensure_ascii=False))
