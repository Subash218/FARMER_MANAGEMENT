import sqlite3
import os

DB_FILE = 'farmportal.db'

# Define products with image paths instead of icon classes
# Images are mapped based on available files in img/ directory
products = [
    # SEEDS
    {
        "name": "Hybrid Wheat Seeds",
        "price": 450,
        "desc": "Premium quality hybrid wheat seeds designed for high yield and drought resistance.",
        "image": "img/whe.png",
        "category": "seeds"
    },
    {
        "name": "Organic Tomato Seeds",
        "price": 120,
        "desc": "Certified organic tomato seeds. Fast growing variety with excellent disease resistance.",
        "image": "img/tom.png",
        "category": "seeds"
    },
    {
        "name": "Golden Corn Seeds",
        "price": 300,
        "desc": "High-yield corn seeds suitable for all seasons. Sweet and crunchy kernels.",
        "image": "img/s1.png",
        "category": "seeds"
    },
    {
        "name": "Sunflower Seeds",
        "price": 280,
        "desc": "Rich oil-content sunflower seeds. Vibrant blooms and excellent harvest.",
        "image": "img/sun.png", # Using generic image
        "category": "seeds"
    },

    # TOOLS
    {
        "name": "Heavy Duty Shovel",
        "price": 850,
        "desc": "Ergonomic shovel with a reinforced steel head and comfortable grip handle.",
        "image": "img/shovel.jpg",
        "category": "tools"
    },
    {
        "name": "Sprayer 5L",
        "price": 1200,
        "desc": "Manual pressure sprayer with 5L capacity. Ideal for applying pesticides.",
        "image": "img/spray.jpeg",
        "category": "tools"
    },
    {
        "name": "Garden Trowel",
        "price": 450,
        "desc": "Stainless steel trowel for digging, transplanting, and moving soil.",
        "image": "img/tw.png", # Using generic farm image
        "category": "tools"
    },
    {
        "name": "Pruning Shears",
        "price": 650,
        "desc": "Sharp and durable shears for trimming plants and harvesting fruits.",
        "image": "img/sc.png", # Using generic farm image
        "category": "tools"
    },

    # FERTILIZERS
    {
        "name": "NPK 19-19-19",
        "price": 2500,
        "desc": "Balanced water-soluble fertilizer for all crops. Promotes healthy vegetative growth.",
        "image": "img/npk.png", # Using generic image
        "category": "fertilizers"
    },
    {
        "name": "Organic Vermicompost",
        "price": 350,
        "desc": "Nutrient-rich organic manure produced by earthworms. Improves soil structure.",
        "image": "img/vermi.jpg",
        "category": "fertilizers"
    },
    {
        "name": "Neem Cake",
        "price": 550,
        "desc": "Organic fertilizer and pest repellent. Protects roots from nematodes.",
        "image": "img/nc.png", # Using generic image
        "category": "fertilizers"
    },
    {
        "name": "Bio-Potash",
        "price": 400,
        "desc": "Natural source of potassium helps in crop maturation and fruit quality.",
        "image": "img/bp.png", # Using generic image
        "category": "fertilizers"
    }
]

def migrate():
    # Helper to clean up and migrate. 
    # NOTE: This will DROP the table to ensure schema update from 'image_icon' to 'image' work if not done.
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Check if we need to migrate schema (simple heuristic: just drop and recreate for this dev environment)
    print("Resetting database to ensure correct schema and data...")
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
        cursor.execute('''
            INSERT INTO products (name, price, description, image, category)
            VALUES (?, ?, ?, ?, ?)
        ''', (p['name'], p['price'], p['desc'], p['image'], p['category']))
    
    conn.commit()
    print(f"Migration successful! {len(products)} products active.")
    conn.close()

if __name__ == '__main__':
    migrate()
