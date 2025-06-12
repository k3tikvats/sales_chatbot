from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import uuid
from app import db
from app.models import Order, OrderItem, Product, User

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('', methods=['POST'])
@jwt_required()
def create_order():
    """Create a new order"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data.get('items') or not isinstance(data['items'], list):
            return jsonify({'error': 'Order items are required'}), 400
        
        if not data.get('shipping_address'):
            return jsonify({'error': 'Shipping address is required'}), 400
        
        # Calculate total amount and validate items
        total_amount = 0
        order_items = []
        
        for item_data in data['items']:
            product_id = item_data.get('product_id')
            quantity = item_data.get('quantity', 1)
            
            if not product_id or quantity <= 0:
                return jsonify({'error': 'Invalid item data'}), 400
            
            product = Product.query.get(product_id)
            if not product or not product.is_active:
                return jsonify({'error': f'Product {product_id} not found'}), 404
            
            if product.stock_quantity < quantity:
                return jsonify({'error': f'Insufficient stock for {product.name}'}), 400
            
            item_total = float(product.price) * quantity
            total_amount += item_total
            
            order_items.append({
                'product': product,
                'quantity': quantity,
                'unit_price': product.price,
                'total_price': item_total
            })
        
        # Create order
        order = Order(
            user_id=user_id,
            order_number=f'ORD-{uuid.uuid4().hex[:8].upper()}',
            total_amount=total_amount,
            shipping_address=data['shipping_address'],
            billing_address=data.get('billing_address', data['shipping_address']),
            payment_method=data.get('payment_method', 'card')
        )
        
        db.session.add(order)
        db.session.flush()
        
        # Create order items and update stock
        for item_data in order_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data['product'].id,
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price'],
                total_price=item_data['total_price']
            )
            db.session.add(order_item)
            
            # Update product stock
            item_data['product'].stock_quantity -= item_data['quantity']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order created successfully',
            'order': order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create order', 'details': str(e)}), 500

@orders_bp.route('', methods=['GET'])
@jwt_required()
def get_orders():
    """Get user's orders"""
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        status = request.args.get('status')
        
        query = Order.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        orders = query.order_by(Order.created_at.desc())\
                     .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'orders': [order.to_dict() for order in orders.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': orders.total,
                'pages': orders.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get orders', 'details': str(e)}), 500

@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get specific order"""
    try:
        user_id = get_jwt_identity()
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        return jsonify({'order': order.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get order', 'details': str(e)}), 500

@orders_bp.route('/<int:order_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_order(order_id):
    """Cancel an order"""
    try:
        user_id = get_jwt_identity()
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        if order.status not in ['pending', 'confirmed']:
            return jsonify({'error': 'Order cannot be cancelled'}), 400
        
        # Restore product stock
        for item in order.items:
            item.product.stock_quantity += item.quantity
        
        order.status = 'cancelled'
        order.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order cancelled successfully',
            'order': order.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to cancel order', 'details': str(e)}), 500
