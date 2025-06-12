from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import uuid
import re
from app import db
from app.models import ChatSession, ChatMessage, Product, Category
from app.services.chat_service import ChatService

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/message', methods=['POST'])
@jwt_required()
def send_message():
    """Process chat message and return bot response"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('message'):
            return jsonify({'error': 'Message is required'}), 400
        
        session_token = data.get('session_token')
        
        # Get or create chat session
        if session_token:
            session = ChatSession.query.filter_by(
                session_token=session_token,
                user_id=user_id,
                is_active=True
            ).first()
        else:
            session = None
        
        if not session:
            session = ChatSession(
                user_id=user_id,
                session_token=str(uuid.uuid4())
            )
            db.session.add(session)
            db.session.flush()
        
        # Save user message
        user_message = ChatMessage(
            session_id=session.id,
            message_type='user',
            content=data['message']
        )
        db.session.add(user_message)
        
        # Process message and generate response
        chat_service = ChatService()
        bot_response = chat_service.process_message(data['message'], session.id)
          # Save bot response
        bot_message = ChatMessage(
            session_id=session.id,
            message_type='bot',
            content=bot_response['content'],
            extra_data=bot_response.get('metadata')
        )
        db.session.add(bot_message)
        
        # Update session timestamp
        session.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'session_token': session.session_token,
            'user_message': user_message.to_dict(),
            'bot_response': bot_message.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to process message', 'details': str(e)}), 500

@chat_bp.route('/history', methods=['GET'])
@jwt_required()
def get_chat_history():
    """Get chat history for current session"""
    try:
        user_id = get_jwt_identity()
        session_token = request.args.get('session_token')
        
        if not session_token:
            return jsonify({'error': 'Session token is required'}), 400
        
        session = ChatSession.query.filter_by(
            session_token=session_token,
            user_id=user_id
        ).first()
        
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        messages = ChatMessage.query.filter_by(session_id=session.id)\
                                   .order_by(ChatMessage.timestamp.asc()).all()
        
        return jsonify({
            'session': session.to_dict(),
            'messages': [message.to_dict() for message in messages]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get chat history', 'details': str(e)}), 500

@chat_bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_chat_sessions():
    """Get all chat sessions for user"""
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        
        sessions = ChatSession.query.filter_by(user_id=user_id)\
                                   .order_by(ChatSession.updated_at.desc())\
                                   .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'sessions': [session.to_dict() for session in sessions.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': sessions.total,
                'pages': sessions.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get chat sessions', 'details': str(e)}), 500

@chat_bp.route('/reset', methods=['POST'])
@jwt_required()
def reset_chat():
    """Reset/end current chat session"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        session_token = data.get('session_token')
        
        if session_token:
            session = ChatSession.query.filter_by(
                session_token=session_token,
                user_id=user_id
            ).first()
            
            if session:
                session.is_active = False
                db.session.commit()
        
        return jsonify({'message': 'Chat session reset successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to reset chat', 'details': str(e)}), 500
