// Chat message type
export interface Message {
  id: string;
  type: "user" | "ai" | "tool";
  content: string;
  toolCall?: { calls: any[] };
}

// Chat component props
export interface ChatComponentProps {
  threadId: string;
}