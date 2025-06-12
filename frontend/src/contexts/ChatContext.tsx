import React, { createContext, useContext, useReducer, ReactNode } from 'react';
import { ChatMessage, ChatSession, Product, MessageMetadata } from '../types';
import { chatAPI } from '../services/api';

interface ChatState {
  messages: ChatMessage[];
  currentSession: ChatSession | null;
  sessionToken: string | null;
  isLoading: boolean;
  isTyping: boolean;
  error: string | null;
  suggestedProducts: Product[];
}

type ChatAction =
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_TYPING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'ADD_MESSAGE'; payload: ChatMessage }
  | { type: 'SET_MESSAGES'; payload: ChatMessage[] }
  | { type: 'SET_SESSION'; payload: { session: ChatSession | null; token: string | null } }
  | { type: 'SET_SUGGESTED_PRODUCTS'; payload: Product[] }
  | { type: 'RESET_CHAT' };

interface ChatContextType extends ChatState {
  sendMessage: (message: string) => Promise<void>;
  resetChat: () => Promise<void>;
  loadChatHistory: (sessionToken: string) => Promise<void>;
  clearError: () => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

const initialState: ChatState = {
  messages: [],
  currentSession: null,
  sessionToken: null,
  isLoading: false,
  isTyping: false,
  error: null,
  suggestedProducts: [],
};

function chatReducer(state: ChatState, action: ChatAction): ChatState {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    case 'SET_TYPING':
      return { ...state, isTyping: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    case 'ADD_MESSAGE':
      return { ...state, messages: [...state.messages, action.payload] };
    case 'SET_MESSAGES':
      return { ...state, messages: action.payload };
    case 'SET_SESSION':
      return {
        ...state,
        currentSession: action.payload.session,
        sessionToken: action.payload.token,
      };
    case 'SET_SUGGESTED_PRODUCTS':
      return { ...state, suggestedProducts: action.payload };
    case 'RESET_CHAT':
      return {
        ...initialState,
        // Keep the same session token for continuity
        sessionToken: state.sessionToken,
      };
    default:
      return state;
  }
}

export function ChatProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  const sendMessage = async (message: string) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      dispatch({ type: 'SET_ERROR', payload: null });

      // Add user message immediately
      const userMessage: ChatMessage = {
        id: Date.now(), // Temporary ID
        session_id: 0,
        message_type: 'user',
        content: message,
        timestamp: new Date().toISOString(),
      };
      dispatch({ type: 'ADD_MESSAGE', payload: userMessage });

      // Show typing indicator
      dispatch({ type: 'SET_TYPING', payload: true });

      // Send message to API
      const response = await chatAPI.sendMessage(message, state.sessionToken || undefined);

      // Update session token if new
      if (response.session_token !== state.sessionToken) {
        dispatch({
          type: 'SET_SESSION',
          payload: { session: null, token: response.session_token },
        });
      }

      // Add bot response
      dispatch({ type: 'ADD_MESSAGE', payload: response.bot_response });

      // Extract and set suggested products from metadata
      const metadata: MessageMetadata = response.bot_response.metadata || {};
      if (metadata.products && metadata.products.length > 0) {
        dispatch({ type: 'SET_SUGGESTED_PRODUCTS', payload: metadata.products });
      }

    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 'Failed to send message';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      
      // Add error message to chat
      const errorChatMessage: ChatMessage = {
        id: Date.now(),
        session_id: 0,
        message_type: 'bot',
        content: `Sorry, I encountered an error: ${errorMessage}`,
        timestamp: new Date().toISOString(),
      };
      dispatch({ type: 'ADD_MESSAGE', payload: errorChatMessage });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
      dispatch({ type: 'SET_TYPING', payload: false });
    }
  };

  const resetChat = async () => {
    try {
      if (state.sessionToken) {
        await chatAPI.resetChat(state.sessionToken);
      }
      dispatch({ type: 'RESET_CHAT' });
      
      // Send welcome message
      const welcomeMessage: ChatMessage = {
        id: Date.now(),
        session_id: 0,
        message_type: 'bot',
        content: "Hello! Welcome to our e-commerce store! 👋 I'm here to help you find the perfect products. What are you looking for today?",
        timestamp: new Date().toISOString(),
      };
      dispatch({ type: 'ADD_MESSAGE', payload: welcomeMessage });
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 'Failed to reset chat';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
    }
  };

  const loadChatHistory = async (sessionToken: string) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const response = await chatAPI.getChatHistory(sessionToken);
      
      dispatch({
        type: 'SET_SESSION',
        payload: { session: response.session, token: sessionToken },
      });
      dispatch({ type: 'SET_MESSAGES', payload: response.messages });
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 'Failed to load chat history';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const clearError = () => {
    dispatch({ type: 'SET_ERROR', payload: null });
  };

  const value: ChatContextType = {
    ...state,
    sendMessage,
    resetChat,
    loadChatHistory,
    clearError,
  };

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
}

export function useChat() {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
}
