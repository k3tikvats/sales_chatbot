import React from 'react';
import { useCart } from '../contexts/CartContext';
import { Link } from 'react-router-dom';

const Cart: React.FC = () => {
  const { items, total, itemCount, updateQuantity, removeItem, clearCart } = useCart();

  const handleQuantityChange = (productId: number, quantity: number) => {
    if (quantity <= 0) {
      removeItem(productId);
    } else {
      updateQuantity(productId, quantity);
    }
  };

  const handleCheckout = () => {
    // In a real app, this would navigate to checkout
    alert('Checkout functionality would be implemented here!');
  };

  if (items.length === 0) {
    return (
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Shopping Cart</h1>
        
        <div className="text-center py-12">
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-2xl">🛒</span>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Your cart is empty</h3>
          <p className="text-gray-600 mb-6">
            Start shopping to add items to your cart
          </p>
          <div className="space-x-4">
            <Link to="/products" className="btn-primary">
              Browse Products
            </Link>
            <Link to="/chat" className="btn-secondary">
              Ask AI for Recommendations
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Shopping Cart</h1>
        <button
          onClick={clearCart}
          className="text-red-600 hover:text-red-800 text-sm font-medium"
        >
          Clear Cart
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        {/* Cart Header */}
        <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
          <div className="grid grid-cols-12 gap-4 text-sm font-medium text-gray-700">
            <div className="col-span-6">Product</div>
            <div className="col-span-2 text-center">Quantity</div>
            <div className="col-span-2 text-center">Price</div>
            <div className="col-span-2 text-center">Total</div>
          </div>
        </div>

        {/* Cart Items */}
        <div className="divide-y divide-gray-200">
          {items.map((item) => (
            <div key={item.product.id} className="px-6 py-4">
              <div className="grid grid-cols-12 gap-4 items-center">
                {/* Product Info */}
                <div className="col-span-6 flex items-center space-x-4">
                  <img
                    src={item.product.image_url}
                    alt={item.product.name}
                    className="w-16 h-16 object-cover rounded"
                  />
                  <div className="flex-1 min-w-0">
                    <Link
                      to={`/products/${item.product.id}`}
                      className="text-lg font-medium text-gray-900 hover:text-primary-600 line-clamp-2"
                    >
                      {item.product.name}
                    </Link>
                    <p className="text-sm text-gray-600">{item.product.brand}</p>
                    <div className="flex items-center mt-1">
                      <span className="text-yellow-400 text-sm">★</span>
                      <span className="text-sm text-gray-600 ml-1">
                        {item.product.rating} ({item.product.review_count} reviews)
                      </span>
                    </div>
                  </div>
                </div>

                {/* Quantity Controls */}
                <div className="col-span-2 flex items-center justify-center">
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => handleQuantityChange(item.product.id, item.quantity - 1)}
                      className="w-8 h-8 rounded-full bg-gray-100 hover:bg-gray-200 flex items-center justify-center text-gray-600"
                    >
                      -
                    </button>
                    <span className="w-8 text-center font-medium">{item.quantity}</span>
                    <button
                      onClick={() => handleQuantityChange(item.product.id, item.quantity + 1)}
                      disabled={item.quantity >= item.product.stock_quantity}
                      className="w-8 h-8 rounded-full bg-gray-100 hover:bg-gray-200 flex items-center justify-center text-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      +
                    </button>
                  </div>
                </div>

                {/* Unit Price */}
                <div className="col-span-2 text-center">
                  <span className="text-lg font-medium text-gray-900">
                    ${item.product.price}
                  </span>
                </div>

                {/* Total Price */}
                <div className="col-span-2 text-center">
                  <span className="text-lg font-bold text-primary-600">
                    ${(item.product.price * item.quantity).toFixed(2)}
                  </span>
                  <button
                    onClick={() => removeItem(item.product.id)}
                    className="block mx-auto mt-2 text-red-600 hover:text-red-800 text-sm"
                  >
                    Remove
                  </button>
                </div>
              </div>

              {/* Stock Warning */}
              {item.quantity >= item.product.stock_quantity && (
                <div className="mt-2 text-sm text-orange-600">
                  ⚠️ Maximum stock reached ({item.product.stock_quantity} available)
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Cart Summary */}
        <div className="px-6 py-4 border-t border-gray-200 bg-gray-50">
          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-600">
              {itemCount} item{itemCount !== 1 ? 's' : ''} in cart
            </div>
            <div className="text-right">
              <div className="text-lg font-medium text-gray-900">
                Subtotal: <span className="text-2xl font-bold text-primary-600">${total.toFixed(2)}</span>
              </div>
              <p className="text-sm text-gray-600 mt-1">
                Shipping and taxes calculated at checkout
              </p>
            </div>
          </div>

          <div className="mt-4 flex items-center justify-between">
            <Link
              to="/products"
              className="text-primary-600 hover:text-primary-500 font-medium"
            >
              ← Continue Shopping
            </Link>
            
            <div className="space-x-4">
              <Link
                to="/chat"
                className="btn-secondary inline-flex items-center"
              >
                <svg className="h-4 w-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clipRule="evenodd" />
                </svg>
                Ask AI for More
              </Link>
              
              <button
                onClick={handleCheckout}
                className="btn-primary"
              >
                Proceed to Checkout
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-medium text-gray-900 mb-3">Need Help?</h3>
          <p className="text-gray-600 mb-4">
            Our AI assistant can help you find similar products or answer questions about your cart items.
          </p>
          <Link
            to="/chat"
            className="btn-secondary w-full justify-center"
          >
            Chat with AI Assistant
          </Link>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-medium text-gray-900 mb-3">Save for Later</h3>
          <p className="text-gray-600 mb-4">
            Your cart items are automatically saved. Come back anytime to complete your purchase.
          </p>
          <div className="text-sm text-gray-500">
            Last updated: {new Date().toLocaleString()}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cart;
