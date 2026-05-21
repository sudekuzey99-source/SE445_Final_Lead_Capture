from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

CRM_API_URL = "http://localhost:5001/api/leads"

def antigravity_crm_connector(lead_data):
    """
    Antigravity Connector: Verilen veriyi hedef CRM API'sine iletir.
    """
    print(f"[WORKFLOW] Antigravity Connector calisiyor. CRM'e gonderiliyor: {lead_data['email']}")
    try:
        response = requests.post(CRM_API_URL, json=lead_data)
        if response.status_code == 201:
            print("[WORKFLOW] CRM kaydi basarili!")
            return response.json()
        else:
            print(f"[WORKFLOW] CRM kaydi basarisiz! Hata Kodu: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        print("[WORKFLOW] HATA: CRM API'sine baglanilamadi. Lutfen mock_crm_api.py'nin calistigindan emin olun.")
        return None

@app.route('/webhook', methods=['POST'])
def capture_lead():
    # 1. Gelen HTTP POST istegini al
    payload = request.json
    print(f"\n[WORKFLOW] Yeni webhook tetiklendi! Gelen payload: {payload}")

    # 2. Payload icinden ilgili alanlari ayikla
    name = payload.get('name')
    email = payload.get('email')
    message = payload.get('message')

    if not name or not email or not message:
        return jsonify({"error": "Lutfen name, email ve message alanlarinin eksiksiz oldugundan emin olun."}), 400

    lead_data = {
        "name": name,
        "email": email,
        "message": message
    }

    # 3. Veriyi CRM'e gonder (Antigravity Connector vasitasiyla)
    crm_result = antigravity_crm_connector(lead_data)

    if crm_result:
        return jsonify({
            "status": "success",
            "message": "Lead basariyla islendi ve CRM'e aktarildi.",
            "crm_response": crm_result
        }), 200
    else:
        return jsonify({"error": "Lead CRM'e kaydedilemedi."}), 500

if __name__ == '__main__':
    print("HW2 Workflow Endpoint (Webhook) 5000 portunda baslatiliyor...")
    print("Gonderilecek Endpoint: http://localhost:5000/webhook")
    app.run(port=5000, debug=True, use_reloader=False)
