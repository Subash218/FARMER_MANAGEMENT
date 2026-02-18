import sqlite3
import os

DB_FILE = 'farmportal.db'

# --- PRODUCTS (Existing) ---
products = [
    {"name": "Hybrid Wheat Seeds", "price": 450, "desc": "Premium quality hybrid seeds.", "image": "img/s1.png", "category": "seeds"},
    {"name": "Organic Tomato Seeds", "price": 120, "desc": "Certified organic tomato seeds.", "image": "img/s2.png", "category": "seeds"},
    {"name": "Golden Corn Seeds", "price": 300, "desc": "High-yield corn seeds.", "image": "img/s3.png", "category": "seeds"},
    {"name": "Sunflower Seeds", "price": 280, "desc": "Rich oil-content seeds.", "image": "img/a3.png", "category": "seeds"},
    {"name": "Heavy Duty Shovel", "price": 850, "desc": "Ergonomic shovel.", "image": "img/shovel.jpg", "category": "tools"},
    {"name": "Sprayer 5L", "price": 1200, "desc": "Manual pressure sprayer.", "image": "img/spray.jpeg", "category": "tools"},
    {"name": "Garden Trowel", "price": 450, "desc": "Stainless steel trowel.", "image": "img/f1.png", "category": "tools"},
    {"name": "Pruning Shears", "price": 650, "desc": "Sharp trimming shears.", "image": "img/f2.png", "category": "tools"},
    {"name": "NPK 19-19-19", "price": 2500, "desc": "Balanced fertilizer.", "image": "img/f3.png", "category": "fertilizers"},
    {"name": "Organic Vermicompost", "price": 350, "desc": "Nutrient-rich manure.", "image": "img/vermi.jpg", "category": "fertilizers"},
    {"name": "Neem Cake", "price": 550, "desc": "Organic pest repellent.", "image": "img/f4.png", "category": "fertilizers"},
    {"name": "Bio-Potash", "price": 400, "desc": "Natural potassium source.", "image": "img/a2.png", "category": "fertilizers"}
]

# --- SCHEMES (From farmer.html) ---
schemes = [
    {
        "title": "Pradhan Mantri Fasal Bima Yojana",
        "desc": "A government-sponsored crop insurance scheme that integrates multiple stakeholders on a single platform.",
        "eligibility": "All farmers growing notified crops in notified areas.",
        "benefits": "Financial support in case of crop failure due to natural calamities.",
        "apply": "Apply through the official PMFBY portal or nearest CSC.",
        "link": "https://pmfby.gov.in/"
    },
    {
        "title": "Kisan Credit Card (KCC)",
        "desc": "Provides adequate and timely credit support to farmers from the banking system.",
        "eligibility": "All farmers, tenant farmers, oral lessees, and sharecroppers.",
        "benefits": "Short-term credit for cultivation and other needs.",
        "apply": "Visit your nearest bank branch.",
        "link": "https://pmkisan.gov.in/"
    },
    {
        "title": "Pradhan Mantri Krishi Sinchai Yojana",
        "desc": "Focuses on extending the coverage of irrigation 'Har Khet ko Pani' and improving water use efficiency.",
        "eligibility": "Farmers with cultivable land.",
        "benefits": "Subsidy on micro-irrigation systems.",
        "apply": "Apply through state agriculture department.",
        "link": "https://pmksy.gov.in/"
    },
    {
        "title": "e-NAM",
        "desc": "National Agriculture Market: A pan-India electronic trading portal networking mandis for unified national market.",
        "eligibility": "Farmers wishing to sell produce online.",
        "benefits": "Better price discovery and transparent auction process.",
        "apply": "Register on e-NAM portal.",
        "link": "https://enam.gov.in/"
    },
    {
        "title": "PM-KISAN",
        "desc": "Direct income support of ₹6,000 per year in three equal installments to all landholding farmer families.",
        "eligibility": "Small and marginal farmers.",
        "benefits": "₹6,000 per year.",
        "apply": "Register on PM-KISAN portal.",
        "link": "https://pmkisan.gov.in/"
    },
    {
        "title": "Soil Health Card",
        "desc": "Provides information to farmers on nutrient status of their soil along with recommendations.",
        "eligibility": "All farmers.",
        "benefits": "Knowledge of soil health and fertilizer dosage.",
        "apply": "Contact local agriculture office.",
        "link": "https://soilhealth.dac.gov.in/"
    },
    {
        "title": "Paramparagat Krishi Vikas Yojana",
        "desc": "Promotes organic farming through cluster approach and Participatory Guarantee System (PGS) certification.",
        "eligibility": "Farmers adopting organic farming.",
        "benefits": "Financial assistance for organic inputs and certification.",
        "apply": "Apply through Cluster formation.",
        "link": "https://pgsindia-ncof.gov.in/"
    },
    {
        "title": "NMSA",
        "desc": "National Mission on Sustainable Agriculture: Focuses on integrated farming, water use efficiency, and soil health.",
        "eligibility": "Farmers in rainfed areas.",
        "benefits": "Support for integrated farming systems.",
        "apply": "Contact state agriculture department.",
        "link": "https://nmsa.dac.gov.in/"
    },
    {
        "title": "PM Kisan Maandhan Yojana",
        "desc": "A voluntary and contributory pension scheme for small and marginal farmers, ensuring a monthly pension of ₹3,000.",
        "eligibility": "Farmers aged 18-40 years.",
        "benefits": "Pension of ₹3,000/month after age 60.",
        "apply": "Register at CSC or online.",
        "link": "https://maandhan.in/"
    },
    {
        "title": "RKVY",
        "desc": "Rashtriya Krishi Vikas Yojana: Aims at holistic development of agriculture and allied sectors by allowing states to choose their own agriculture plans.",
        "eligibility": "State specific.",
        "benefits": "Infrastructure development.",
        "apply": "Through State Govt.",
        "link": "https://rkvy.nic.in/"
    },
    {
        "title": "MIDH",
        "desc": "Mission for Integrated Development of Horticulture covering fruits, vegetables, root & tuber crops, mushrooms, spices, flowers, etc.",
        "eligibility": "Horticulture farmers.",
        "benefits": "Holistic growth of horticulture sector.",
        "apply": "State Horticulture Mission.",
        "link": "https://midh.gov.in/"
    },
    {
        "title": "Agriculture Infrastructure Fund",
        "desc": "Financing facility for investment in viable projects for post-harvest management infrastructure.",
        "eligibility": "Farmers, FPOs, PACS, Startups.",
        "benefits": "Interest subvention and credit guarantee.",
        "apply": "Online portal.",
        "link": "https://agriinfra.dac.gov.in/"
    }
]

# --- NEWS (Existing) ---
news_items = [
    {
        "title": "Rice Exports Expected to Hit Record Highs",
        "category": "Market",
        "date": "2026-02-02",
        "content": "Global demand for Basmati rice surges by 15% this quarter. Experts suggest farmers hold stock for better pricing in upcoming weeks."
    },
    {
        "title": "New Solar Pump Subsidy Announced",
        "category": "Subsidies",
        "date": "2026-02-01",
        "content": "Government increases subsidy from 40% to 60% for PM-KUSUM scheme. Applications open next Monday for the first 50,000 farmers."
    },
    {
        "title": "AI-Powered Soil Analysis Kits",
        "category": "Technology",
        "date": "2026-01-30",
        "content": "New portable kits can now detect nutrient deficiencies in under 5 minutes using smartphone cameras. Available at local KVKs from March."
    }
]

def repopulate():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # --- PRODUCTS ---
    cursor.execute('DROP TABLE IF EXISTS products')
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            image TEXT,
            category TEXT
        )
    ''')
    for p in products:
        cursor.execute('INSERT INTO products (name, price, description, image, category) VALUES (?, ?, ?, ?, ?)', 
                       (p['name'], p['price'], p['desc'], p['image'], p['category']))
    
    # --- SCHEMES ---
    cursor.execute('DROP TABLE IF EXISTS schemes')
    cursor.execute('''
        CREATE TABLE schemes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            eligibility TEXT,
            benefits TEXT,
            how_to_apply TEXT,
            link TEXT
        )
    ''')
    for s in schemes:
        cursor.execute('INSERT INTO schemes (title, description, eligibility, benefits, how_to_apply, link) VALUES (?, ?, ?, ?, ?, ?)',
                       (s['title'], s['desc'], s['eligibility'], s['benefits'], s['apply'], s['link']))

    # --- NEWS ---
    cursor.execute('DROP TABLE IF EXISTS news')
    cursor.execute('''
        CREATE TABLE news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT,
            date TEXT,
            content TEXT
        )
    ''')
    for n in news_items:
        cursor.execute('INSERT INTO news (title, category, date, content) VALUES (?, ?, ?, ?)',
                       (n['title'], n['category'], n['date'], n['content']))

    conn.commit()
    print("Database repopulated successfully with Products, Schemes, and News.")
    conn.close()

if __name__ == '__main__':
    repopulate()
