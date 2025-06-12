from faker import Faker
import random
from app import db
from app.models import User, Product, Category, Order, OrderItem

fake = Faker()

def create_sample_data():
    """Create sample data for the e-commerce platform"""
    
    # Create categories
    categories_data = [
        {
            'name': 'Electronics',
            'description': 'Computers, smartphones, tablets, and electronic accessories',
            'subcategories': [
                {'name': 'Smartphones', 'description': 'Mobile phones and accessories'},
                {'name': 'Laptops', 'description': 'Portable computers and accessories'},
                {'name': 'Headphones', 'description': 'Audio devices and accessories'},
                {'name': 'Tablets', 'description': 'Tablet computers and accessories'}
            ]
        },
        {
            'name': 'Books',
            'description': 'Fiction, non-fiction, textbooks, and digital books',
            'subcategories': [
                {'name': 'Fiction', 'description': 'Novels, short stories, and fiction literature'},
                {'name': 'Non-Fiction', 'description': 'Biography, history, science, and educational books'},
                {'name': 'Textbooks', 'description': 'Academic and educational textbooks'},
                {'name': 'Children\'s Books', 'description': 'Books for children and young adults'}
            ]
        },
        {
            'name': 'Clothing',
            'description': 'Fashion and apparel for men, women, and children',
            'subcategories': [
                {'name': 'Men\'s Clothing', 'description': 'Shirts, pants, jackets, and men\'s fashion'},
                {'name': 'Women\'s Clothing', 'description': 'Dresses, tops, bottoms, and women\'s fashion'},
                {'name': 'Shoes', 'description': 'Footwear for all occasions'},
                {'name': 'Accessories', 'description': 'Bags, jewelry, watches, and fashion accessories'}
            ]
        },
        {
            'name': 'Home & Garden',
            'description': 'Furniture, appliances, and home improvement items',
            'subcategories': [
                {'name': 'Furniture', 'description': 'Chairs, tables, beds, and home furniture'},
                {'name': 'Appliances', 'description': 'Kitchen and home appliances'},
                {'name': 'Decor', 'description': 'Home decoration and design items'},
                {'name': 'Garden', 'description': 'Gardening tools and outdoor equipment'}
            ]
        }
    ]
    
    print("Creating categories...")
    category_objects = {}
    
    for cat_data in categories_data:
        # Create main category
        category = Category(
            name=cat_data['name'],
            description=cat_data['description'],
            is_active=True
        )
        db.session.add(category)
        db.session.flush()
        category_objects[cat_data['name']] = category
        
        # Create subcategories
        for subcat_data in cat_data['subcategories']:
            subcategory = Category(
                name=subcat_data['name'],
                description=subcat_data['description'],
                parent_id=category.id,
                is_active=True
            )
            db.session.add(subcategory)
            db.session.flush()
            category_objects[subcat_data['name']] = subcategory
    
    db.session.commit()
    print(f"Created {len(category_objects)} categories")
    
    # Product data templates
    products_data = {
        'Smartphones': [
            {'name': 'iPhone 15 Pro', 'brand': 'Apple', 'price_range': (999, 1199), 'specs': {'storage': '128GB', 'ram': '8GB', 'camera': '48MP'}},
            {'name': 'Samsung Galaxy S24', 'brand': 'Samsung', 'price_range': (799, 999), 'specs': {'storage': '256GB', 'ram': '8GB', 'camera': '50MP'}},
            {'name': 'Google Pixel 8', 'brand': 'Google', 'price_range': (699, 899), 'specs': {'storage': '128GB', 'ram': '8GB', 'camera': '50MP'}},
            {'name': 'OnePlus 12', 'brand': 'OnePlus', 'price_range': (599, 799), 'specs': {'storage': '256GB', 'ram': '12GB', 'camera': '50MP'}},
            {'name': 'Xiaomi 14 Pro', 'brand': 'Xiaomi', 'price_range': (499, 699), 'specs': {'storage': '256GB', 'ram': '12GB', 'camera': '50MP'}}
        ],
        'Laptops': [
            {'name': 'MacBook Air M3', 'brand': 'Apple', 'price_range': (1099, 1599), 'specs': {'processor': 'M3', 'ram': '16GB', 'storage': '512GB SSD'}},
            {'name': 'Dell XPS 13', 'brand': 'Dell', 'price_range': (999, 1499), 'specs': {'processor': 'Intel i7', 'ram': '16GB', 'storage': '512GB SSD'}},
            {'name': 'ThinkPad X1 Carbon', 'brand': 'Lenovo', 'price_range': (1299, 1899), 'specs': {'processor': 'Intel i7', 'ram': '16GB', 'storage': '1TB SSD'}},
            {'name': 'Surface Laptop 5', 'brand': 'Microsoft', 'price_range': (999, 1699), 'specs': {'processor': 'Intel i7', 'ram': '16GB', 'storage': '512GB SSD'}},
            {'name': 'HP Spectre x360', 'brand': 'HP', 'price_range': (1199, 1799), 'specs': {'processor': 'Intel i7', 'ram': '16GB', 'storage': '1TB SSD'}}
        ],
        'Headphones': [
            {'name': 'AirPods Pro 2', 'brand': 'Apple', 'price_range': (199, 249), 'specs': {'type': 'Wireless', 'battery': '30 hours', 'noise_cancelling': True}},
            {'name': 'Sony WH-1000XM5', 'brand': 'Sony', 'price_range': (299, 399), 'specs': {'type': 'Over-ear', 'battery': '30 hours', 'noise_cancelling': True}},
            {'name': 'Bose QuietComfort 45', 'brand': 'Bose', 'price_range': (279, 349), 'specs': {'type': 'Over-ear', 'battery': '24 hours', 'noise_cancelling': True}},
            {'name': 'Sennheiser HD 660S', 'brand': 'Sennheiser', 'price_range': (399, 499), 'specs': {'type': 'Wired', 'impedance': '150 ohms', 'open_back': True}}
        ],
        'Fiction': [
            {'name': 'The Seven Husbands of Evelyn Hugo', 'brand': 'Taylor Jenkins Reid', 'price_range': (12, 18)},
            {'name': 'Atomic Habits', 'brand': 'James Clear', 'price_range': (15, 22)},
            {'name': 'Where the Crawdads Sing', 'brand': 'Delia Owens', 'price_range': (14, 20)},
            {'name': 'The Silent Patient', 'brand': 'Alex Michaelides', 'price_range': (13, 19)}
        ],
        'Men\'s Clothing': [
            {'name': 'Premium Cotton T-Shirt', 'brand': 'Nike', 'price_range': (25, 45)},
            {'name': 'Slim Fit Jeans', 'brand': 'Levi\'s', 'price_range': (60, 90)},
            {'name': 'Casual Button Down Shirt', 'brand': 'Ralph Lauren', 'price_range': (80, 120)},
            {'name': 'Hoodie Sweatshirt', 'brand': 'Adidas', 'price_range': (45, 75)}
        ],
        'Shoes': [
            {'name': 'Air Max 270', 'brand': 'Nike', 'price_range': (130, 180)},
            {'name': 'Chuck Taylor All Star', 'brand': 'Converse', 'price_range': (55, 85)},
            {'name': 'Stan Smith Sneakers', 'brand': 'Adidas', 'price_range': (75, 105)},
            {'name': 'Classic Leather Boots', 'brand': 'Dr. Martens', 'price_range': (150, 200)}
        ]
    }
    
    print("Creating products...")
    created_products = 0
    
    for category_name, product_list in products_data.items():
        category = category_objects.get(category_name)
        if not category:
            continue
        
        for product_template in product_list:
            # Create multiple variants of each product
            for i in range(3):
                price = random.uniform(*product_template['price_range'])
                
                product = Product(
                    name=f"{product_template['name']}" + (f" - Variant {i+1}" if i > 0 else ""),
                    description=fake.text(max_nb_chars=200),
                    price=round(price, 2),
                    category_id=category.id,
                    brand=product_template['brand'],
                    sku=f"SKU-{fake.unique.random_number(digits=8)}",
                    stock_quantity=random.randint(0, 100),
                    image_url=f"https://via.placeholder.com/400x400?text={product_template['name'].replace(' ', '+')}",
                    rating=round(random.uniform(3.5, 5.0), 1),
                    review_count=random.randint(10, 500),
                    specifications=product_template.get('specs', {}),
                    is_active=True
                )
                
                db.session.add(product)
                created_products += 1
    
    # Add some additional random products to reach 100+
    additional_categories = list(category_objects.keys())
    while created_products < 120:
        category_name = random.choice(additional_categories)
        category = category_objects[category_name]
        
        product = Product(
            name=fake.catch_phrase(),
            description=fake.text(max_nb_chars=200),
            price=round(random.uniform(10, 500), 2),
            category_id=category.id,
            brand=fake.company(),
            sku=f"SKU-{fake.unique.random_number(digits=8)}",
            stock_quantity=random.randint(0, 100),
            image_url=f"https://via.placeholder.com/400x400?text=Product+{created_products}",
            rating=round(random.uniform(3.0, 5.0), 1),
            review_count=random.randint(5, 200),
            specifications={'feature': fake.word(), 'color': fake.color_name()},
            is_active=True
        )
        
        db.session.add(product)
        created_products += 1
    
    db.session.commit()
    print(f"Created {created_products} products")
    
    # Create sample users
    print("Creating sample users...")
    sample_users = []
    
    for i in range(10):
        user = User(
            username=fake.user_name(),
                    email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        user.set_password('password123')
        db.session.add(user)
        sample_users.append(user)
    
    db.session.commit()
    print(f"Created {len(sample_users)} sample users")
    
    print("Sample data creation completed!")
    print(f"Total categories: {len(category_objects)}")
    print(f"Total products: {created_products}")
    print(f"Total users: {len(sample_users)}")

def populate_sample_data():
    """Populate the database with sample data"""
    create_sample_data()

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create sample data
        create_sample_data()
        
        print("Database initialization completed!")
