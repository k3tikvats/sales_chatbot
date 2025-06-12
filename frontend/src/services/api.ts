import axios, { AxiosResponse } from 'axios';
import {
  AuthResponse,
  LoginCredentials,
  RegisterData,
  User,
  Product,
  ProductsResponse,
  ProductFilters,
  Category,
  ChatResponse,
  ChatMessage,
  ChatSession,
  Order,
  OrderItem
} from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response: AxiosResponse<AuthResponse> = await api.post('/auth/login', credentials);
    return response.data;
  },

  register: async (data: RegisterData): Promise<AuthResponse> => {
    const response: AxiosResponse<AuthResponse> = await api.post('/auth/register', data);
    return response.data;
  },

  getCurrentUser: async (): Promise<{ user: User }> => {
    const response: AxiosResponse<{ user: User }> = await api.get('/auth/me');
    return response.data;
  },

  logout: async (): Promise<{ message: string }> => {
    const response: AxiosResponse<{ message: string }> = await api.post('/auth/logout');
    return response.data;
  },
};

export const productsAPI = {
  getProducts: async (filters?: ProductFilters): Promise<ProductsResponse> => {
    const params = new URLSearchParams();
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          params.append(key, value.toString());
        }
      });
    }
    
    const response: AxiosResponse<ProductsResponse> = await api.get(`/products?${params}`);
    return response.data;
  },

  getProduct: async (id: number): Promise<{ product: Product }> => {
    const response: AxiosResponse<{ product: Product }> = await api.get(`/products/${id}`);
    return response.data;
  },

  searchProducts: async (query: string): Promise<{ products: Product[]; query: string; count: number }> => {
    const response = await api.get(`/products/search?q=${encodeURIComponent(query)}`);
    return response.data;
  },

  getCategories: async (): Promise<{ categories: Category[] }> => {
    const response: AxiosResponse<{ categories: Category[] }> = await api.get('/products/categories');
    return response.data;
  },

  getRecommendations: async (limit?: number): Promise<{ recommendations: Product[] }> => {
    const params = limit ? `?limit=${limit}` : '';
    const response = await api.get(`/products/recommendations${params}`);
    return response.data;
  },
};

export const chatAPI = {
  sendMessage: async (message: string, sessionToken?: string): Promise<ChatResponse> => {
    const data: any = { message };
    if (sessionToken) {
      data.session_token = sessionToken;
    }
    
    const response: AxiosResponse<ChatResponse> = await api.post('/chat/message', data);
    return response.data;
  },

  getChatHistory: async (sessionToken: string): Promise<{ session: ChatSession; messages: ChatMessage[] }> => {
    const response = await api.get(`/chat/history?session_token=${sessionToken}`);
    return response.data;
  },

  getChatSessions: async (page?: number, perPage?: number): Promise<{ sessions: ChatSession[]; pagination: any }> => {
    const params = new URLSearchParams();
    if (page) params.append('page', page.toString());
    if (perPage) params.append('per_page', perPage.toString());
    
    const response = await api.get(`/chat/sessions?${params}`);
    return response.data;
  },

  resetChat: async (sessionToken?: string): Promise<{ message: string }> => {
    const data = sessionToken ? { session_token: sessionToken } : {};
    const response = await api.post('/chat/reset', data);
    return response.data;
  },
};

export const ordersAPI = {
  createOrder: async (orderData: {
    items: { product_id: number; quantity: number }[];
    shipping_address: any;
    billing_address?: any;
    payment_method?: string;
  }): Promise<{ message: string; order: Order }> => {
    const response = await api.post('/orders', orderData);
    return response.data;
  },

  getOrders: async (page?: number, perPage?: number, status?: string): Promise<{ orders: Order[]; pagination: any }> => {
    const params = new URLSearchParams();
    if (page) params.append('page', page.toString());
    if (perPage) params.append('per_page', perPage.toString());
    if (status) params.append('status', status);
    
    const response = await api.get(`/orders?${params}`);
    return response.data;
  },

  getOrder: async (id: number): Promise<{ order: Order }> => {
    const response = await api.get(`/orders/${id}`);
    return response.data;
  },

  cancelOrder: async (id: number): Promise<{ message: string; order: Order }> => {
    const response = await api.post(`/orders/${id}/cancel`);
    return response.data;
  },
};

export default api;
