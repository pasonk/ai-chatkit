import React from "react";
import { Button, Input } from "antd";

interface MessageInputProps {
  input: string;
  setInput: (value: string) => void;
  handleSend: () => void;
  isStreaming: boolean;
}

const MessageInput: React.FC<MessageInputProps> = ({ input, setInput, handleSend, isStreaming }) => {
  return (
    <div className="p-4 border-t">
      <div className="flex gap-2 items-center">
        <Input.TextArea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Send a message..."
          onKeyPress={(e) => e.key === "Enter" && handleSend()}
          //ctrl + enter 换行
          onKeyDown={(e) => {
            if (e.key === "Enter" && e.ctrlKey) {
              e.preventDefault();
              setInput(input + "\n");
            }
          }}
          disabled={isStreaming}
          className="flex-1 min-h-[80px] p-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-blue-500 transition-colors"
          autoSize={{ minRows: 3, maxRows: 5 }}
        />
        <Button
          type="primary"
          className="bg-blue-500 hover:bg-blue-600 text-white h-24 px-6 rounded-lg transition-colors font-semibold shadow-md"
          onClick={handleSend}
          disabled={!input.trim() || isStreaming}
        >
          {isStreaming ? "generating..." : "send"}
        </Button>
      </div>
    </div>
  );
};

export default MessageInput;