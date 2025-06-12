import re
import os
import json
from typing import Dict, List, Any, Optional
from sqlalchemy import or_
from flask import current_app
import google.generativeai as genai
from app.models import Product, Category

class ChatService:
    """Service class for processing chat messages using Google Gemini AI"""
    
    def __init__(self):
        self.intent_patterns = {
            'greeting': [
                r'\b(hi|hello|hey|good morning|good afternoon|good evening)\b',
                r'\bwhat\'s up\b',
                r'\bhow are you\b'
            ],
            'search_product': [
                r'\b(looking for|search|find|want|need|show me)\b.*\b(product|item|thing)\b',
                r'\b(do you have|got any|sell)\b',
                r'\b(price of|cost of|how much)\b'
            ],
            'category_browse': [
                r'\b(category|categories|section|browse|explore)\b',
                r'\b(electronics|books|clothing|home|garden|sports)\b'
            ],
            'product_details': [
                r'\b(details|specifications|specs|features|info|information)\b',
                r'\btell me (more )?about\b',
                r'\bwhat is\b'
            ],
            'add_to_cart': [
                r'\b(add to cart|buy|purchase|order|get this)\b',
                r'\bi want (to buy|this)\b'
            ],
            'help': [
                r'\b(help|assist|support|guide)\b',
                r'\bwhat can you do\b',
                r'\bhow does this work\b'
            ],
            'goodbye': [
                r'\b(bye|goodbye|see you|thanks|thank you)\b',
                r'\bthat\'s all\b',
                r'\bi\'m done\b'
            ]
        }
        
        # Initialize Gemini AI
        self._initialize_gemini()
    
    def _initialize_gemini(self):
        """Initialize Google Gemini AI client"""
        try:
            api_key = current_app.config.get('GEMINI_API_KEY')
            if not api_key:
                print("Warning: GEMINI_API_KEY not found. Using fallback responses.")
                self.gemini_client = None
                return
            
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(
                model_name=current_app.config.get('GEMINI_MODEL', 'gemini-2.0-flash-exp')
            )
            self.gemini_client = True
            print(f"Gemini AI initialized with model: {current_app.config.get('GEMINI_MODEL', 'gemini-2.0-flash-exp')}")
        except Exception as e:
            print(f"Error initializing Gemini AI: {str(e)}")
            self.gemini_client = None
    
    def process_message(self, message: str, session_id: int) -> Dict[str, Any]:
        """Process user message and return appropriate response"""
        message_lower = message.lower().strip()
        
        # Detect intent
        intent = self._detect_intent(message_lower)
        
        # Handle different intents
        if intent == 'greeting':
            return self._handle_greeting()
        elif intent == 'search_product':
            return self._handle_product_search(message)
        elif intent == 'category_browse':
            return self._handle_category_browse(message)
        elif intent == 'product_details':
            return self._handle_product_details(message)
        elif intent == 'add_to_cart':
            return self._handle_add_to_cart()
        elif intent == 'help':
            return self._handle_help()
        elif intent == 'goodbye':
            return self._handle_goodbye()
        else:
            # Use Gemini AI for complex queries
            return self._handle_gemini_response(message)
    
    def _detect_intent(self, message: str) -> str:
        """Detect user intent from message"""
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message, re.IGNORECASE):
                    return intent
        return 'general'
    
    def _handle_greeting(self) -> Dict[str, Any]:
        """Handle greeting messages"""
        return {
            'content': "Hello! 👋 Welcome to our e-commerce store! I'm your AI shopping assistant. I can help you find products, answer questions, and make your shopping experience amazing. What are you looking for today?",
            'metadata': {'type': 'greeting'}
        }
    
    def _handle_product_search(self, message: str) -> Dict[str, Any]:
        """Handle product search queries"""
        # Extract search terms
        search_terms = self._extract_product_keywords(message)
        
        if not search_terms:
            return {
                'content': "I'd be happy to help you find products! Could you tell me what specific item you're looking for? For example, 'laptops', 'smartphones', 'books', etc.",
                'metadata': {'type': 'search_clarification'}
            }
        
        # Search for products
        products = self._search_products(search_terms)
        
        if products:
            product_list = []
            response_content = f"Great! I found some {search_terms[0]} for you:\n\n"
            
            for product in products[:5]:  # Limit to 5 products
                product_list.append({
                    'id': product.id,
                    'name': product.name,
                    'price': float(product.price),
                    'image_url': product.image_url
                })
                response_content += f"🛍️ **{product.name}** - ${product.price:.2f}\n"
            
            response_content += "\nWould you like more details about any of these products, or should I search for something else?"
            
            return {
                'content': response_content,
                'metadata': {
                    'type': 'product_search_results',
                    'products': product_list,
                    'search_terms': search_terms
                }
            }
        else:
            return {
                'content': f"I couldn't find any products matching '{' '.join(search_terms)}'. Try searching for categories like electronics, books, clothing, or home & garden items.",
                'metadata': {'type': 'no_results'}
            }
    
    def _handle_category_browse(self, message: str) -> Dict[str, Any]:
        """Handle category browsing requests"""
        categories = Category.query.all()
        
        if not categories:
            return {
                'content': "Sorry, I couldn't load our product categories right now. Please try again later.",
                'metadata': {'type': 'error'}
            }
        
        category_list = []
        response_content = "Here are our product categories:\n\n"
        
        for category in categories:
            category_list.append({
                'id': category.id,
                'name': category.name,
                'description': category.description
            })
            product_count = Product.query.filter_by(category_id=category.id).count()
            response_content += f"📂 **{category.name}** ({product_count} items)\n   {category.description}\n\n"
        
        response_content += "Which category interests you? Just ask me to 'show electronics' or 'find books' for example!"
        
        return {
            'content': response_content,
            'metadata': {
                'type': 'category_list',
                'categories': category_list
            }
        }
    
    def _handle_product_details(self, message: str) -> Dict[str, Any]:
        """Handle requests for product details"""
        return {
            'content': "I'd love to help you with product details! Please click on any product in our catalog to see its full specifications, or ask me something like 'tell me about the iPhone 14' with a specific product name.",
            'metadata': {'type': 'product_details_request'}
        }
    
    def _handle_add_to_cart(self) -> Dict[str, Any]:
        """Handle add to cart requests"""
        return {
            'content': "To add items to your cart, you can click the 'Add to Cart' button on any product page, or tell me exactly which product you want to buy. I can help you find it first!",
            'metadata': {'type': 'add_to_cart_guidance'}
        }
    
    def _handle_help(self) -> Dict[str, Any]:
        """Handle help requests"""
        return {
            'content': """I'm here to help you shop! Here's what I can do:

🔍 **Search Products**: Ask me to find laptops, smartphones, books, etc.
📂 **Browse Categories**: Say 'show categories' to see all product types
💡 **Product Advice**: Ask 'what's the best laptop under $1000?'
🛒 **Shopping Help**: I can guide you through adding items to cart
📋 **Order Assistance**: Help with placing orders and tracking

Just ask me anything about our products or shopping process!""",
            'metadata': {
                'type': 'help',
                'capabilities': ['search', 'browse', 'recommend', 'cart_help', 'order_help']
            }
        }
    
    def _handle_goodbye(self) -> Dict[str, Any]:
        """Handle goodbye messages"""
        return {
            'content': "Thank you for shopping with us! 😊 If you need any more help, just ask. Have a great day!",
            'metadata': {'type': 'goodbye'}
        }
    
    def _handle_gemini_response(self, message: str) -> Dict[str, Any]:
        """Handle complex queries using Gemini AI"""
        if not self.gemini_client:
            return {
                'content': "I'm sorry, I'm having trouble understanding that right now. Could you try asking about our products, categories, or say 'help' to see what I can do?",
                'metadata': {
                    'type': 'fallback',
                    'reason': 'gemini_unavailable'
                }
            }
        
        try:
            # Get some context about available products
            context = self._get_shop_context()
            
            # Create a detailed prompt for Gemini
            prompt = f"""You are a helpful e-commerce shopping assistant. The user asked: "{message}"

Here's information about our store:
{context}

Please provide a helpful, friendly response. If the user is asking about products:
1. Suggest relevant products from our inventory
2. Include specific product names and prices when possible
3. Ask follow-up questions to better help them
4. Keep responses conversational and under 200 words

If the user is asking general questions, provide helpful shopping advice while staying focused on our e-commerce store."""

            response = self.model.generate_content(prompt)
            
            return {
                'content': response.text,
                'metadata': {
                    'type': 'gemini_response',
                    'query': message
                }
            }
            
        except Exception as e:
            print(f"Gemini AI error: {str(e)}")
            return {
                'content': "I'm having trouble processing that request right now. Could you try asking about specific products or categories? For example, 'show me laptops' or 'what smartphones do you have?'",
                'metadata': {
                    'type': 'error',
                    'error': str(e)
                }
            }
    
    def _extract_product_keywords(self, message: str) -> List[str]:
        """Extract product-related keywords from message"""
        # Common product keywords
        product_keywords = [
            'laptop', 'computer', 'smartphone', 'phone', 'tablet', 'headphone', 'speaker',
            'book', 'novel', 'textbook', 'ebook', 'shirt', 'jeans', 'dress', 'shoes',
            'camera', 'watch', 'keyboard', 'mouse', 'monitor', 'tv', 'television',
            'electronics', 'sports', 'fitness', 'home', 'garden', 'kitchen', 'furniture'
        ]
        
        words = re.findall(r'\b\w+\b', message.lower())
        found_keywords = [word for word in words if word in product_keywords]
        
        return found_keywords if found_keywords else words[:3]  # Return first 3 words if no keywords found
    
    def _search_products(self, search_terms: List[str]) -> List[Product]:
        """Search for products based on terms"""
        query = Product.query
        
        # Create search conditions for each term
        conditions = []
        for term in search_terms:
            conditions.extend([
                Product.name.ilike(f'%{term}%'),
                Product.description.ilike(f'%{term}%')
            ])
        
        # Join conditions with OR
        if conditions:
            query = query.filter(or_(*conditions))
        
        return query.limit(10).all()
    
    def _get_shop_context(self) -> str:
        """Get context about the shop for Gemini AI"""
        try:
            # Get category summary
            categories = Category.query.all()
            category_info = []
            
            for category in categories[:5]:  # Limit to 5 categories
                product_count = Product.query.filter_by(category_id=category.id).count()
                category_info.append(f"- {category.name}: {product_count} products")
            
            # Get some sample products
            sample_products = Product.query.limit(5).all()
            product_info = []
            
            for product in sample_products:
                product_info.append(f"- {product.name}: ${product.price}")
            
            context = f"""
STORE CATEGORIES:
{chr(10).join(category_info)}

SAMPLE PRODUCTS:
{chr(10).join(product_info)}

We have over 100 products across multiple categories including electronics, books, clothing, and more.
"""
            return context
        except Exception as e:
            return "We have a wide variety of products across multiple categories including electronics, books, clothing, and home items."
