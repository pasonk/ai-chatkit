// 消息类型定义
export interface Message {
  id: string;
  type: "user" | "ai" | "tool";
  content: string;
  toolCall?: { calls: any[] };
}

// Chat组件props类型
export interface ChatComponentProps {
  threadId: string;
}