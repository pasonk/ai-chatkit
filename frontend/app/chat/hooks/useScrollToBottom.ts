import { useEffect, useRef } from 'react';
import { Message } from '../types/chat.types';

const useScrollToBottom = (messagesEndRef: React.RefObject<HTMLDivElement>, messages: Message[]) => {
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);
};

export default useScrollToBottom;