from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_, and_
from app import db
from app.models import Product, Category

products_bp = Blueprint('products', __name__)

@products_bp.route('', methods=['GET'])
def get_products():
    """Get products with optional filtering and pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        category_id = request.args.get('category_id', type=int)
        brand = request.args.get('brand')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        search = request.args.get('search')
        sort_by = request.args.get('sort_by', 'name')
        sort_order = request.args.get('sort_order', 'asc')
        
        # Build query
        query = Product.query.filter(Product.is_active == True)
        
        # Apply filters
        if category_id:
            query = query.filter(Product.category_id == category_id)
        
        if brand:
            query = query.filter(Product.brand.ilike(f'%{brand}%'))
        
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        if search:
            search_term = f'%{search}%'
            query = query.filter(
                or_(
                    Product.name.ilike(search_term),
                    Product.description.ilike(search_term),
                    Product.brand.ilike(search_term)
                )
            )
        
        # Apply sorting
        if sort_by == 'name':
            order_column = Product.name
        elif sort_by == 'price':
            order_column = Product.price
        elif sort_by == 'rating':
            order_column = Product.rating
        elif sort_by == 'created_at':
            order_column = Product.created_at
        else:
            order_column = Product.name
        
        if sort_order == 'desc':
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column.asc())
        
        # Paginate
        products = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'products': [product.to_dict() for product in products.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': products.total,
                'pages': products.pages,
                'has_next': products.has_next,
                'has_prev': products.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get products', 'details': str(e)}), 500

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get specific product by ID"""
    try:
        product = Product.query.filter_by(id=product_id, is_active=True).first()
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify({'product': product.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get product', 'details': str(e)}), 500

@products_bp.route('/search', methods=['GET'])
def search_products():
    """Advanced product search"""
    try:
        query_text = request.args.get('q', '')
        if not query_text:
            return jsonify({'error': 'Search query is required'}), 400
        
        # Perform search
        search_term = f'%{query_text}%'
        products = Product.query.filter(
            and_(
                Product.is_active == True,
                or_(
                    Product.name.ilike(search_term),
                    Product.description.ilike(search_term),
                    Product.brand.ilike(search_term)
                )
            )
        ).limit(50).all()
        
        return jsonify({
            'products': [product.to_dict() for product in products],
            'query': query_text,
            'count': len(products)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Search failed', 'details': str(e)}), 500

@products_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all product categories"""
    try:
        categories = Category.query.filter_by(is_active=True).all()
        
        return jsonify({
            'categories': [category.to_dict() for category in categories]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get categories', 'details': str(e)}), 500

@products_bp.route('/recommendations', methods=['GET'])
@jwt_required()
def get_recommendations():
    """Get product recommendations for user"""
    try:
        user_id = get_jwt_identity()
        limit = request.args.get('limit', 10, type=int)
        
        # Simple recommendation: popular products
        products = Product.query.filter_by(is_active=True)\
                                .order_by(Product.rating.desc(), Product.review_count.desc())\
                                .limit(limit).all()
        
        return jsonify({
            'recommendations': [product.to_dict() for product in products]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get recommendations', 'details': str(e)}), 500
