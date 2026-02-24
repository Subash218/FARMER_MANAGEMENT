from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

# Configure Flask to serve static files from the current directory
app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

DB_FILE = 'farmportal.db'

def init_db():
    """Initialize the database with users and products tables."""
    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        cursor = conn.cursor()
        
        # Create Users Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                work_type TEXT,
                role TEXT DEFAULT 'user'
            )
        ''')

        # Check if role column exists (for migration)
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'role' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")

        # Check for products table columns (for migration)
        cursor.execute("PRAGMA table_info(products)")
        prod_columns = [column[1] for column in cursor.fetchall()]
        if 'specs' not in prod_columns:
            cursor.execute("ALTER TABLE products ADD COLUMN specs TEXT")
        if 'features' not in prod_columns:
            cursor.execute("ALTER TABLE products ADD COLUMN features TEXT")

        # Create Products Table (using icon or image path)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                description TEXT,
                image TEXT,
                category TEXT,
                specs TEXT,
                features TEXT
            )
        ''')
        
        # Create Orders Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                items TEXT NOT NULL,
                total REAL NOT NULL,
                date DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'Pending'
            )
        ''')

        # Create Schemes Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schemes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                eligibility TEXT,
                benefits TEXT,
                how_to_apply TEXT,
                link TEXT
            )
        ''')

        # Create News Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT,
                date TEXT,
                content TEXT
            )
        ''')
        
        conn.commit()
        print("Database initialized.")
    finally:
        conn.close()

# --- Static File Routes ---
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# --- API Routes ---

@app.route('/api/products', methods=['GET'])
def get_products():
    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products')
        rows = cursor.fetchall()
        products = [dict(row) for row in rows]
        return jsonify(products), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        row = cursor.fetchone()
        if row:
            return jsonify(dict(row)), 200
        else:
            return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    required_fields = ['full_name', 'email', 'username', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (full_name, age, gender, email, username, password, work_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['full_name'],
            data.get('age'),
            data.get('gender'),
            data['email'],
            data['username'],
            data['password'],
            data.get('work_type')
            
        ))
        print(data)
        conn.commit()
        return jsonify({'message': 'Registration successful'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username or Email already exists'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if 'userid' not in data or 'password' not in data:
        return jsonify({'error': 'Missing userid or password'}), 400
        
    username = data['userid']
    password = data['password']
    
    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        
        if user:
            return jsonify({
                'message': 'Login successful', 
                'user': {
                    'id': user[0],
                    'name': user[1],
                    'full_name': user[1],
                    'age': user[2],
                    'gender': user[3],
                    'email': user[4],
                    'username': user[5],
                    'work_type': user[7],
                    'role': user[8]
                }
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/orders', methods=['POST'])
def place_order():
    data = request.json
    if not data or 'username' not in data or 'items' not in data or 'total' not in data:
        return jsonify({'error': 'Missing order data'}), 400
        
    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO orders (username, items, total)
            VALUES (?, ?, ?)
        ''', (data['username'], data['items'], data['total']))
        conn.commit()
        return jsonify({'message': 'Order placed successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/orders/<username>', methods=['GET'])
def get_user_orders(username):
    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE username = ? ORDER BY date DESC', (username,))
        rows = cursor.fetchall()
        orders = [dict(row) for row in rows]
        return jsonify(orders), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/profile/<username>', methods=['GET'])
def get_profile(username):
    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT id, full_name, age, gender, email, username, work_type FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if user:
            return jsonify(dict(user)), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# --- Admin Routes ---

@app.route('/api/admin/users', methods=['GET'])
def admin_get_users():
    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT id, full_name, email, username, role FROM users')
        users = [dict(row) for row in cursor.fetchall()]
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
def admin_delete_user(user_id):
    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        cursor = conn.cursor()
        if 'full_name' in data:
            cursor.execute('UPDATE users SET full_name = ? WHERE id = ?', (data['full_name'], user_id))
        if 'email' in data:
            cursor.execute('UPDATE users SET email = ? WHERE id = ?', (data['email'], user_id))
        
        conn.commit()
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user_row = cursor.fetchone()
        user = {
            "id": user_row[0], 
            "full_name": user_row[1],
            "age": user_row[2],
            "gender": user_row[3],
            "email": user_row[4], 
            "username": user_row[5],
            "work_type": user_row[7],
            "role": user_row[8]
        }
        return jsonify(user), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/admin/products/<int:product_id>', methods=['PUT'])
def admin_update_product(product_id):
    data = request.json
    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE products SET name = ?, price = ?, description = ?, image = ?, category = ?
            WHERE id = ?
        ''', (data['name'], data['price'], data['description'], data['image'], data['category'], product_id))
        conn.commit()
        return jsonify({'message': 'Product updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/admin/products', methods=['POST'])
def admin_add_product():
    data = request.json
    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (name, price, description, image, category)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['name'], data['price'], data['description'], data['image'], data['category']))
        conn.commit()
        return jsonify({'message': 'Product added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/admin/products/<int:product_id>', methods=['PUT', 'DELETE'])
def admin_manage_product(product_id):
    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        cursor = conn.cursor()
        if request.method == 'PUT':
            data = request.json
            cursor.execute('''
                UPDATE products SET price = ?, description = ?, category = ?
                WHERE id = ?
            ''', (data['price'], data['description'], data['category'], product_id))
            conn.commit()
            return jsonify({'message': 'Product updated successfully'}), 200
        elif request.method == 'DELETE':
            cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
            conn.commit()
            return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/admin/orders', methods=['GET'])
def admin_get_orders():
    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders ORDER BY date DESC')
        orders = [dict(row) for row in cursor.fetchall()]
        return jsonify(orders), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/admin/orders/<int:order_id>', methods=['PUT', 'DELETE'])
def admin_manage_order(order_id):
    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        cursor = conn.cursor()
        if request.method == 'PUT':
            data = request.json
            if 'status' not in data:
                return jsonify({'error': 'Missing status'}), 400
            cursor.execute('UPDATE orders SET status = ? WHERE id = ?', (data['status'], order_id))
            conn.commit()
            return jsonify({'message': 'Order status updated successfully'}), 200
        elif request.method == 'DELETE':
            cursor.execute('DELETE FROM orders WHERE id = ?', (order_id,))
            conn.commit()
            return jsonify({'message': 'Order deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# --- Schemes & News Routes ---

@app.route('/api/schemes', methods=['GET'])
def get_schemes():
    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM schemes')
        schemes = [dict(row) for row in cursor.fetchall()]
        return jsonify(schemes), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/admin/schemes', methods=['POST'])
def admin_add_scheme():
    data = request.json
    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO schemes (title, description, eligibility, benefits, how_to_apply, link)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['title'], data['description'], data['eligibility'], data['benefits'], data['how_to_apply'], data['link']))
        conn.commit()
        return jsonify({'message': 'Scheme added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/admin/schemes/<int:scheme_id>', methods=['PUT'])
def admin_update_scheme(scheme_id):
    data = request.json
    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE schemes SET title = ?, description = ?, eligibility = ?, benefits = ?, how_to_apply = ?, link = ?
            WHERE id = ?
        ''', (data['title'], data['description'], data['eligibility'], data['benefits'], data['how_to_apply'], data['link'], scheme_id))
        conn.commit()
        return jsonify({'message': 'Scheme updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/admin/schemes/<int:scheme_id>', methods=['DELETE'])
def admin_delete_scheme(scheme_id):
    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM schemes WHERE id = ?', (scheme_id,))
        conn.commit()
        return jsonify({'message': 'Scheme deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/news', methods=['GET'])
def get_news():
    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM news ORDER BY date DESC')
        news = [dict(row) for row in cursor.fetchall()]
        return jsonify(news), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/admin/news', methods=['POST'])
def admin_add_news():
    data = request.json
    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO news (title, category, date, content)
            VALUES (?, ?, ?, ?)
        ''', (data['title'], data['category'], data['date'], data['content']))
        conn.commit()
        return jsonify({'message': 'News added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/admin/news/<int:news_id>', methods=['PUT'])
def admin_update_news(news_id):
    data = request.json
    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE news SET title = ?, category = ?, date = ?, content = ?
            WHERE id = ?
        ''', (data['title'], data['category'], data['date'], data['content'], news_id))
        conn.commit()
        return jsonify({'message': 'News updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/admin/news/<int:news_id>', methods=['DELETE'])
def admin_delete_news(news_id):
    conn = sqlite3.connect(DB_FILE, timeout=20)
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM news WHERE id = ?', (news_id,))
        conn.commit()
        return jsonify({'message': 'News deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
