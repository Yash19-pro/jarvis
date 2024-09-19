import sqlite3

# Connect to the database (it will create the database if it doesn't exist)
conn = sqlite3.connect('bakery.db')
c = conn.cursor()

# Create tables
c.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    quantity INTEGER,
    total_price REAL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products (id)
)
''')

conn.commit()
conn.close()

def add_product(name, price, quantity):
    conn = sqlite3.connect('bakery.db')
    c = conn.cursor()
    c.execute('INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)', (name, price, quantity))
    conn.commit()
    conn.close()
    print(f"Product {name} added successfully!")

def update_product(product_id, name=None, price=None, quantity=None):
    conn = sqlite3.connect('bakery.db')
    c = conn.cursor()
    if name:
        c.execute('UPDATE products SET name = ? WHERE id = ?', (name, product_id))
    if price:
        c.execute('UPDATE products SET price = ? WHERE id = ?', (price, product_id))
    if quantity is not None:
        c.execute('UPDATE products SET quantity = ? WHERE id = ?', (quantity, product_id))
    conn.commit()
    conn.close()
    print(f"Product {product_id} updated successfully!")

def delete_product(product_id):
    conn = sqlite3.connect('bakery.db')
    c = conn.cursor()
    c.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
    print(f"Product {product_id} deleted successfully!")

def list_products():
    conn = sqlite3.connect('bakery.db')
    c = conn.cursor()
    c.execute('SELECT * FROM products')
    products = c.fetchall()
    conn.close()
    return products

def record_sale(product_id, quantity):
    conn = sqlite3.connect('bakery.db')
    c = conn.cursor()
    
    # Get product details
    c.execute('SELECT name, price, quantity FROM products WHERE id = ?', (product_id,))
    product = c.fetchone()
    
    if not product:
        print("Product not found!")
        return

    name, price, current_quantity = product
    if quantity > current_quantity:
        print(f"Not enough stock for {name}. Available quantity: {current_quantity}")
        return
    
    total_price = price * quantity
    c.execute('INSERT INTO sales (product_id, quantity, total_price) VALUES (?, ?, ?)', (product_id, quantity, total_price))
    c.execute('UPDATE products SET quantity = quantity - ? WHERE id = ?', (quantity, product_id))
    
    conn.commit()
    conn.close()
    print(f"Sale recorded: {quantity} x {name} for ${total_price}")

def list_sales():
    conn = sqlite3.connect('bakery.db')
    c = conn.cursor()
    c.execute('''
    SELECT sales.id, products.name, sales.quantity, sales.total_price, sales.date
    FROM sales
    JOIN products ON sales.product_id = products.id
    ''')
    sales = c.fetchall()
    conn.close()
    return sales

def main():
    while True:
        print("\nBakery Management System")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. List Products")
        print("5. Record Sale")
        print("6. List Sales")
        print("7. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            quantity = int(input("Enter product quantity: "))
            add_product(name, price, quantity)
        
        elif choice == '2':
            product_id = int(input("Enter product ID to update: "))
            name = input("Enter new name (leave blank to skip): ")
            price = input("Enter new price (leave blank to skip): ")
            quantity = input("Enter new quantity (leave blank to skip): ")
            update_product(product_id, name if name else None, float(price) if price else None, int(quantity) if quantity else None)
        
        elif choice == '3':
            product_id = int(input("Enter product ID to delete: "))
            delete_product(product_id)
        
        elif choice == '4':
            products = list_products()
            print("\nProducts:")
            for product in products:
                print(f"ID: {product[0]}, Name: {product[1]}, Price: ${product[2]:.2f}, Quantity: {product[3]}")
        
        elif choice == '5':
            product_id = int(input("Enter product ID to sell: "))
            quantity = int(input("Enter quantity to sell: "))
            record_sale(product_id, quantity)
        
        elif choice == '6':
            sales = list_sales()
            print("\nSales:")
            for sale in sales:
                print(f"ID: {sale[0]}, Product: {sale[1]}, Quantity: {sale[2]}, Total Price: ${sale[3]:.2f}, Date: {sale[4]}")
        
        elif choice == '7':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
