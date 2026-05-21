import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_FILE = 'crm_database.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Update table to include HW3 fields
    c.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT,
            validation_status TEXT,
            validation_errors TEXT,
            intent TEXT,
            urgency TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/api/leads', methods=['POST'])
def create_lead():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
        
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO leads (name, email, message, validation_status, validation_errors, intent, urgency)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('name'),
        data.get('email'),
        data.get('message'),
        data.get('validation_status'),
        data.get('validation_errors'),
        data.get('intent'),
        data.get('urgency')
    ))
    lead_id = c.lastrowid
    conn.commit()
    conn.close()
    
    print(f"[CRM API] NEW LEAD RECORDED -> ID: {lead_id}, Status: {data.get('validation_status')}")
    return jsonify({'status': 'success', 'lead_id': lead_id}), 201

@app.route('/api/leads', methods=['GET'])
def get_leads():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, name, email, message, validation_status, validation_errors, intent, urgency, created_at FROM leads ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    
    leads = []
    for r in rows:
        leads.append({
            'id': r[0],
            'name': r[1],
            'email': r[2],
            'message': r[3],
            'validation_status': r[4],
            'validation_errors': r[5],
            'intent': r[6],
            'urgency': r[7],
            'created_at': r[8]
        })
    return jsonify(leads), 200

if __name__ == '__main__':
    init_db()
    print("Mock CRM API 5001 portunda baslatiliyor...")
    app.run(port=5001, debug=True, use_reloader=False)
