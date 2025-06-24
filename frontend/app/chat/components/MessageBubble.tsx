import React from 'react';
import { Avatar, Collapse, Spin } from 'antd';
import { UserOutlined, RobotOutlined } from '@ant-design/icons';
import ReactMarkdown from 'react-markdown';
import { Message } from '../types/chat.types';


interface MessageBubbleProps {
  message: Message;
  isStreaming: boolean;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message, isStreaming }) => {
  const { type, content, toolCall } = message;

  return (
    <div className={`mb-4 ${type === 'user' ? 'text-right flex justify-end' : 'text-left'}`}>
      <div className={`flex ${type === 'user' ? 'flex-row-reverse' : 'flex-row'} items-start gap-3 max-w-2xl`}>
        <Avatar
          size={40}
          className={`${type === 'user' ? 'bg-blue-500' : 'bg-gray-500'} text-white`}
        >
          {type === 'user' ? <UserOutlined /> : <RobotOutlined />}
        </Avatar>
        <div className={`p-3 rounded-lg ${type === 'user' ? 'bg-blue-50' : 'bg-gray-50'} flex-1`}>
          {type === 'ai' && isStreaming && content === '' ? (
            toolCall ? <div><Spin size="small" /> invoking tool...</div> : <Spin size="small" />
          ) : (
            <> 
              {toolCall?.calls && (
                <Collapse defaultActiveKey={['0']} className="mt-2">
                  {toolCall.calls.map((call: any, index: number) => (
                    <Collapse.Panel header={`Tool ${index + 1}: ${call.name}`} key={index}>
                      <p className="mb-2">input：{JSON.stringify(call.args)}</p>
                      {call.result && <p>result：{call.result}</p>}
                    </Collapse.Panel>
                  ))}
                </Collapse>
              )}
              <ReactMarkdown>{content}</ReactMarkdown>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;