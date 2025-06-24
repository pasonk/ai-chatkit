import React from 'react';
import { Button } from 'antd';
import { PlusOutlined } from '@ant-design/icons';

interface NewChatButtonProps {
  collapsed: boolean;
  onClick: () => void;
}

const NewChatButton: React.FC<NewChatButtonProps> = ({ collapsed, onClick }) => {
  return (
    <Button
      type="primary"
      onClick={onClick}
      icon={<PlusOutlined />}
      style={{ margin: "16px", width: collapsed ? "40px" : "calc(100% - 32px)" }}
      shape={collapsed ? "circle" : "round"}
    >
      {!collapsed && "NEW CHAT"}
    </Button>
  );
};

export default NewChatButton;