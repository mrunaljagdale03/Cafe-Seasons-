CREATE DATABASE IF NOT EXISTS seasons_cafe_db;
USE seasons_cafe_db;

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS menu_items;
DROP TABLE IF EXISTS admin;

CREATE TABLE admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO admin (username, password) VALUES ('admin', 'admin123');

CREATE TABLE menu_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(120) NOT NULL,
    category VARCHAR(60) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    description TEXT,
    image VARCHAR(255),
    availability ENUM('Available','Unavailable') DEFAULT 'Available'
);

INSERT INTO menu_items (item_name, category, price, description, image, availability) VALUES
('Margherita Pizza', 'Pizza', 149, 'Classic cheese pizza with rich tomato base.', 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800', 'Available'),
('Farmhouse Pizza', 'Pizza', 229, 'Loaded veg pizza with capsicum, onion, corn and cheese.', 'https://images.unsplash.com/photo-1593560708920-61dd98c46a4e?w=800', 'Available'),
('Peri Peri Pizza', 'Pizza', 249, 'Spicy peri peri flavored pizza for spice lovers.', 'https://images.unsplash.com/photo-1601924582975-7fa4eaf7f894?w=800', 'Available'),
('Cheese Burger', 'Burger', 119, 'Soft bun burger with cheese, patty and fresh veggies.', 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800', 'Available'),
('Veg Burger', 'Burger', 99, 'Crispy veg patty burger with sauces.', 'https://images.unsplash.com/photo-1550547660-d9450f859349?w=800', 'Available'),
('Paneer Burger', 'Burger', 139, 'Paneer patty burger with creamy sauce.', 'https://images.unsplash.com/photo-1594212699903-ec8a3eca50f5?w=800', 'Available'),
('Veg Grilled Sandwich', 'Sandwich', 109, 'Grilled sandwich with vegetables and cheese.', 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=800', 'Available'),
('Cheese Corn Sandwich', 'Sandwich', 129, 'Cheesy corn filling grilled sandwich.', 'https://images.unsplash.com/photo-1553909489-cd47e0907980?w=800', 'Available'),
('White Sauce Pasta', 'Fast Food', 169, 'Creamy pasta with herbs and vegetables.', 'https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=800', 'Available'),
('French Fries', 'Fast Food', 89, 'Crispy salted fries served with dip.', 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=800', 'Available'),
('Cold Coffee', 'Coffee', 99, 'Chilled coffee with chocolate and cream.', 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=800', 'Available'),
('Cappuccino', 'Coffee', 109, 'Hot coffee with smooth foam.', 'https://images.unsplash.com/photo-1511920170033-f8396924c348?w=800', 'Available'),
('Oreo Shake', 'Cafe', 139, 'Thick oreo milkshake with cream.', 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=800', 'Available'),
('Chocolate Brownie', 'Desserts', 119, 'Soft brownie with chocolate sauce.', 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=800', 'Available'),
('Chocolate Pastry', 'Bakery', 99, 'Fresh chocolate pastry slice.', 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800', 'Available');

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    table_no VARCHAR(20),
    total_amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    payment_status VARCHAR(50) DEFAULT 'Pending',
    order_status VARCHAR(50) DEFAULT 'Pending',
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    item_name VARCHAR(120) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
);
