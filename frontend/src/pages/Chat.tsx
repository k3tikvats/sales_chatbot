import React, { useState, useEffect, useRef } from 'react';
import { useChat } from '../contexts/ChatContext';
import { useCart } from '../contexts/CartContext';
import { ChatMessage as ChatMessageType, Product } from '../types';

const Chat: React.FC = () => {
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  
  const {
    messages,
    isLoading,
    isTyping,
    error,
    suggestedProducts,
    sendMessage,
    resetChat,
    clearError
  } = useChat();
  
  const { addItem } = useCart();

  useEffect(() => {
    // Auto-scroll to bottom when new messages arrive
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  useEffect(() => {
    // Clear error after 5 seconds
    if (error) {
      const timer = setTimeout(() => {
        clearError();
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [error, clearError]);

  useEffect(() => {
    // Focus input on mount
    inputRef.current?.focus();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || isLoading) return;

    const message = inputMessage.trim();
    setInputMessage('');
    
    try {
      await sendMessage(message);
    } catch (error) {
      // Error handled by context
    }
  };

  const handleReset = async () => {
    try {
      await resetChat();
      setInputMessage('');
      inputRef.current?.focus();
    } catch (error) {
      // Error handled by context
    }
  };

  const handleAddToCart = (product: Product) => {
    addItem(product);
    // Send a follow-up message to the chat
    sendMessage(`Add ${product.name} to my cart`);
  };

  const handleQuickReply = (reply: string) => {
    setInputMessage(reply);
    inputRef.current?.focus();
  };

  const formatMessage = (content: string) => {
    // Simple markdown-like formatting
    return content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br>');
  };

  return (
    <div className="h-full flex flex-col bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
            <span className="text-xl">🤖</span>
          </div>
          <div>
            <h2 className="text-lg font-semibold text-gray-900">AI Shopping Assistant</h2>
            <p className="text-sm text-gray-600">
              {isTyping ? 'Typing...' : 'Ask me anything about our products!'}
            </p>
          </div>
        </div>
        
        <button
          onClick={handleReset}
          className="btn-secondary text-sm"
          disabled={isLoading}
        >
          Reset Chat
        </button>
      </div>

      {/* Error Banner */}
      {error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4 m-4 rounded animate-fade-in">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
        {messages.length === 0 && !isLoading && (
          <div className="text-center py-8">
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">💬</span>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Welcome to your AI Shopping Assistant!
            </h3>
            <p className="text-gray-600 mb-6">
              I'm here to help you find the perfect products. Try asking me:
            </p>
            <div className="space-y-2 max-w-md mx-auto">
              {[
                "Show me laptops under $1000",
                "I need running shoes",
                "What's trending in electronics?",
                "Help me find a gift"
              ].map((suggestion, index) => (
                <button
                  key={index}
                  onClick={() => handleQuickReply(suggestion)}
                  className="block w-full text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-lg text-sm transition-colors"
                >
                  "{suggestion}"
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((message) => (
          <ChatMessageComponent
            key={message.id}
            message={message}
            onAddToCart={handleAddToCart}
          />
        ))}

        {/* Typing indicator */}
        {isTyping && (
          <div className="flex items-start space-x-2">
            <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center flex-shrink-0">
              <span className="text-sm">🤖</span>
            </div>
            <div className="chat-bubble chat-bubble-bot">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Product Suggestions */}
      {suggestedProducts.length > 0 && (
        <div className="border-t border-gray-200 p-4">
          <h4 className="text-sm font-medium text-gray-900 mb-3">Suggested Products:</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {suggestedProducts.slice(0, 3).map((product) => (
              <div key={product.id} className="bg-gray-50 rounded-lg p-3 text-sm">
                <div className="flex items-center space-x-2">
                  <img
                    src={product.image_url}
                    alt={product.name}
                    className="w-10 h-10 object-cover rounded"
                  />
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-gray-900 truncate">{product.name}</p>
                    <p className="text-primary-600 font-bold">${product.price}</p>
                  </div>
                  <button
                    onClick={() => handleAddToCart(product)}
                    className="bg-primary-600 text-white px-2 py-1 rounded text-xs hover:bg-primary-700 transition-colors"
                  >
                    Add
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Input */}
      <form onSubmit={handleSubmit} className="border-t border-gray-200 p-4">
        <div className="flex space-x-2">
          <input
            ref={inputRef}
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Ask me about products..."
            className="flex-1 form-input"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !inputMessage.trim()}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            ) : (
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
              </svg>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

// Chat Message Component
interface ChatMessageProps {
  message: ChatMessageType;
  onAddToCart: (product: Product) => void;
}

const ChatMessageComponent: React.FC<ChatMessageProps> = ({ message, onAddToCart }) => {
  const isUser = message.message_type === 'user';
  const products = message.metadata?.products || [];
  const quickReplies = message.metadata?.quick_replies || [];

  return (
    <div className={`flex items-start space-x-2 ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
      {/* Avatar */}
      <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
        isUser ? 'bg-primary-100' : 'bg-gray-100'
      }`}>
        <span className="text-sm">{isUser ? '👤' : '🤖'}</span>
      </div>

      {/* Message Content */}
      <div className={`max-w-xs lg:max-w-md ${isUser ? 'items-end' : 'items-start'}`}>
        <div className={`chat-bubble ${isUser ? 'chat-bubble-user' : 'chat-bubble-bot'}`}>
          <div
            dangerouslySetInnerHTML={{
              __html: message.content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\n/g, '<br>')
            }}
          />
        </div>

        {/* Timestamp */}
        <p className={`text-xs text-gray-500 mt-1 ${isUser ? 'text-right' : 'text-left'}`}>
          {new Date(message.timestamp).toLocaleTimeString()}
        </p>

        {/* Products Grid */}
        {products.length > 0 && (
          <div className="mt-3 space-y-2">
            {products.slice(0, 3).map((product: Product) => (
              <div key={product.id} className="bg-white border border-gray-200 rounded-lg p-3 shadow-sm">
                <div className="flex items-center space-x-3">
                  <img
                    src={product.image_url}
                    alt={product.name}
                    className="w-12 h-12 object-cover rounded"
                  />
                  <div className="flex-1 min-w-0">
                    <h4 className="text-sm font-medium text-gray-900 truncate">
                      {product.name}
                    </h4>
                    <p className="text-xs text-gray-500 truncate">
                      {product.brand}
                    </p>
                    <div className="flex items-center space-x-2 mt-1">
                      <span className="text-lg font-bold text-primary-600">
                        ${product.price}
                      </span>
                      <div className="flex items-center text-xs text-gray-500">
                        <span className="text-yellow-400 mr-1">★</span>
                        {product.rating}
                      </div>
                    </div>
                  </div>
                  <button
                    onClick={() => onAddToCart(product)}
                    className="bg-primary-600 text-white px-3 py-1 rounded text-xs hover:bg-primary-700 transition-colors"
                  >
                    Add to Cart
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Quick Replies */}
        {quickReplies.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-2">
            {quickReplies.map((reply: string, index: number) => (
              <button
                key={index}
                onClick={() => {/* Handle quick reply */}}
                className="text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 px-2 py-1 rounded transition-colors"
              >
                {reply}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Chat;
