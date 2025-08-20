import { message } from "antd";
import { Message } from "../types/chat.types";

interface UseStreamChatProps {
  currentThreadId: string;
  agentId: string;
  setMessages: (messages: Message[]) => void;
  isStreaming: boolean;
  setIsStreaming: (value: boolean) => void;
}


export const useStreamChat = ({
  currentThreadId,
  agentId,
  setMessages,
  isStreaming,
  setIsStreaming,
}: UseStreamChatProps) => {
  const handleStream = async (input: string) => {
    if (!input.trim() || isStreaming) return;
    setIsStreaming(true);

    const newUserMessage: Message = {
      id: `user_${Date.now()}`,
      type: "user",
      content: input,
    };
    const newAiMessage: Message = {
      id: `ai_${Date.now()}`,
      type: "ai",
      content: "",
    };
    setMessages((prev: Message[]) => [...prev, newUserMessage, newAiMessage]);

    try {
      const requestMsg = {
        thread_id: currentThreadId,
        role: "user",
        message: input,
        agent_id: agentId,
      };

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/chat/stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestMsg),
      });
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      while (reader) {
        const { done, value } = await reader.read();
        if (done) break;
        const dataChunk = decoder.decode(value, { stream: true });

        dataChunk.split("\n").forEach((line) => {
          if (line.startsWith("data: ")) {
            const data = JSON.parse(line.replace("data: ", ""));
            switch (data.type) {
              case "message":
                handleMessageData(data.content);
                break;
              case "token":
                handleTokenData(data.content);
                break;
              case "end":
                setIsStreaming(false);
                reader.cancel();
                break;
            }
          }
        });
      }
    } catch (error) {
      console.error(" Request Failed:", error);
      message.error(" Request Failed, Please try again later.");
      setIsStreaming(false);
    }
  };

  const handleMessageData = (content: any) => {
    if (content.type === "ai" && content.tool_calls.length > 0) {
      setMessages((prev) =>{
        var addCalls = []
        const calls = prev[prev.length - 1].toolCall?.calls || []
        const toolCalls = content.tool_calls;
        if(calls.length === 0){
          addCalls = toolCalls;
        }else{
          calls.map((call) => {
            for (const toolCall of toolCalls) {
              if (call.id != toolCall.id) {
                if(addCalls.find((c) => c.id === toolCall.id) == null){
                  addCalls.push(toolCall);
                }
              }
            }
          });
        }
        return prev.map((msg, i) =>
          i === prev.length - 1
            ? {
                ...msg,
                toolCall: { ...msg.toolCall, calls: [...(msg?.toolCall?.calls || []), ...addCalls] },
              }
            : msg
        )
      }
      );
    }else if (content.type === "ai" && content.content) {
      setMessages((prev) =>
        prev.map((msg, i) =>
          i === prev.length - 1 ? { ...msg, content: content.content } : msg
        )
      );
    }
    if (content.type === "tool") {
      setMessages((prev) => {
        const updatedCalls = prev[prev.length - 1].toolCall.calls.map((call) =>
          call.id === content.tool_call_id
            ? { ...call, result: content.content }
            : call
        );
        return prev.map((msg, i) =>
          i === prev.length - 1
            ? {
                ...msg,
                toolCall: { ...msg.toolCall, calls: [...updatedCalls] },
              }
            : msg
        );
      });
    }
  };

  const handleTokenData = (token: string) => {
    setMessages((prev) =>
      prev.map((msg, i) =>
        i === prev.length - 1 ? { ...msg, content: msg.content + token } : msg
      )
    );
  };


  return { handleStream };
};
