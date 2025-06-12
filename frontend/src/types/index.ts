export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  created_at?: string;
  last_login?: string;
}

export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  category: string;
  brand: string;
  sku: string;
  stock_quantity: number;
  image_url: string;
  rating: number;
  review_count: number;
  specifications: Record<string, any>;
  is_active: boolean;
  created_at?: string;
}

export interface Category {
  id: number;
  name: string;
  description: string;
  parent_id?: number;
  image_url?: string;
  is_active: boolean;
}

export interface ChatMessage {
  id: number;
  session_id: number;
  message_type: 'user' | 'bot';
  content: string;
  metadata?: any;
  timestamp: string;
}

export interface ChatSession {
  id: number;
  user_id: number;
  session_token: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface Order {
  id: number;
  user_id: number;
  order_number: string;
  status: 'pending' | 'confirmed' | 'shipped' | 'delivered' | 'cancelled';
  total_amount: number;
  shipping_address: any;
  billing_address: any;
  payment_method: string;
  created_at: string;
  updated_at: string;
  items: OrderItem[];
}

export interface OrderItem {
  id: number;
  order_id: number;
  product_id: number;
  product_name: string;
  quantity: number;
  unit_price: number;
  total_price: number;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}

export interface AuthResponse {
  message: string;
  access_token: string;
  user: User;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

export interface ProductFilters {
  category_id?: number;
  brand?: string;
  min_price?: number;
  max_price?: number;
  search?: string;
  sort_by?: 'name' | 'price' | 'rating' | 'created_at';
  sort_order?: 'asc' | 'desc';
  page?: number;
  per_page?: number;
}

export interface PaginationInfo {
  page: number;
  per_page: number;
  total: number;
  pages: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface ProductsResponse {
  products: Product[];
  pagination: PaginationInfo;
}

export interface ChatResponse {
  session_token: string;
  user_message: ChatMessage;
  bot_response: ChatMessage;
}

export interface CartItem {
  product: Product;
  quantity: number;
}

export interface QuickReply {
  text: string;
  action?: string;
}

export interface MessageMetadata {
  type?: string;
  products?: Product[];
  categories?: Category[];
  quick_replies?: string[];
  total_count?: number;
  search_terms?: string[];
}
