import sqlite3
import os

DB_FILE = 'farmportal.db'

schemes_data = [
    {
        "title": "Kisan Credit Card (KCC)",
        "desc": "Access to affordable credit for cultivation and post-harvest expenses with insurance coverage. Flexible repayment options available.",
        "elig": "All farmers-individuals/Joint borrowers who are owner cultivators. Tenant farmers, Oral lessees and Share Croppers etc.",
        "ben": "Credit at a subsidized rate of interest (effectively 4% if repaid closely). ATM enabled RuPay Card. Insurance coverage for accidental death or permanent disability.",
        "apply": "Visit your nearest public sector bank branch or apply online through the bank's website.",
        "link": "https://agriwelfare.gov.in/en/Major/"
    },
    {
        "title": "Pradhan Mantri Fasal Bima Yojana",
        "desc": "Comprehensive crop insurance protecting farmers from yield losses due to non-preventable natural risks. Low premium rates.",
        "elig": "Farmers including sharecroppers and tenant farmers growing notified crops in notified areas are eligible for coverage.",
        "ben": "Provides insurance coverage and financial support to the farmers in the event of failure of any of the notified crop as a result of natural calamities, pests & diseases.",
        "apply": "Apply through the NCIP Portal (https://pmfby.gov.in/), Banks, or Common Service Centres (CSCs).",
        "link": "https://pmfby.gov.in/"
    }
    # ... more schemes can be added here
]

news_data = [
    {
        "title": "Rice Exports Expected to Hit Record Highs",
        "category": "Market",
        "date": "Feb 02, 2026",
        "content": "<p>The global demand for Basmati and non-Basmati rice has seen an unprecedented surge this quarter.</p>"
    },
    {
        "title": "New Solar Pump Subsidy Announced",
        "category": "Subsidies",
        "date": "Feb 01, 2026",
        "content": "<p>Government increases subsidy from 40% to 60% for PM-KUSUM scheme.</p>"
    }
]

def setup():
    if not os.path.exists(DB_FILE):
        print(f"Database {DB_FILE} not found. Please run app.py first.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create Admin User
    try:
        cursor.execute('''
            INSERT INTO users (full_name, email, username, password, role)
            VALUES (?, ?, ?, ?, ?)
        ''', ('Admin User', 'admin@farmportal.com', 'admin', 'admin123', 'admin'))
        print("Admin user created (admin / admin123)")
    except sqlite3.IntegrityError:
        print("Admin user already exists.")

    # Populate Schemes
    cursor.execute('DELETE FROM schemes')
    for s in schemes_data:
        cursor.execute('''
            INSERT INTO schemes (title, description, eligibility, benefits, how_to_apply, link)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (s['title'], s['desc'], s['elig'], s['ben'], s['apply'], s['link']))
    
    # Populate News
    cursor.execute('DELETE FROM news')
    for n in news_data:
        cursor.execute('''
            INSERT INTO news (title, category, date, content)
            VALUES (?, ?, ?, ?)
        ''', (n['title'], n['category'], n['date'], n['content']))

    conn.commit()
    print("Database populated with initial schemes and news.")
    conn.close()

if __name__ == '__main__':
    setup()
