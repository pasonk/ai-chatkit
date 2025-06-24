import { SetStateAction } from 'react';
import { Message } from '../types/chat.types';

interface UseChatActionsProps {
  setMessages: (value: SetStateAction<Message[]>) => void;
  setInput: (value: SetStateAction<string>) => void;
  isStreaming: boolean;
  setIsStreaming: (value: boolean) => void;
}

const useChatActions = ({ setMessages, setInput, isStreaming, setIsStreaming }: UseChatActionsProps) => {
  const handleNewChat = () => {
    setMessages([]);
    setInput("");
    if (isStreaming) {
      setIsStreaming(false);
    }
  };

  return { handleNewChat };
};

export default useChatActions;