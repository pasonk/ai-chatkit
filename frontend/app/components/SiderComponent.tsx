import React from 'react';
import { Layout, Menu } from 'antd';
import NewChatButton from './NewChatButton';
import { useLayoutContext } from '../layout-context'


interface SiderComponentProps {
  collapsed: boolean;
  onCollapse: (collapsed: boolean) => void;
  sessions: Array<{ threadId: string; name: string; lastUpdated: number }>;
  handleDeleteSession: (threadId: string) => void;
  handlerNewChat: () => void;
  items: Array<{ key: string; label: React.ReactNode }>;
  onSelectSession: (key: string) => void;
}

const { Sider } = Layout;

const SiderComponent: React.FC<SiderComponentProps> = ({ 
  collapsed, 
  onCollapse, 
  sessions, 
  handleDeleteSession, 
  handlerNewChat, 
  items,
  onSelectSession
}) => {
  const { currentThreadId, setCurrentThreadId } = useLayoutContext()

  return (
    <Sider
      collapsible
      collapsed={collapsed}
      onCollapse={onCollapse}
      width={200}
    >
      {!collapsed && (
        <div className="logo flex items-center justify-center h-16 text-white text-lg">
          AI-CHATKIT
        </div>
      )}
      <NewChatButton collapsed={collapsed} onClick={handlerNewChat} />
      {!collapsed && (
        <Menu
          theme="dark"
          className="max-h-[calc(100vh-180px)] overflow-y-auto"
          defaultSelectedKeys={[currentThreadId]}
          selectedKeys={[currentThreadId]}
          mode="inline"
          items={items}
          onSelect={({ key }) => {
            onSelectSession(key);
          }}
        />
      )}
    </Sider>
  );
};

export default SiderComponent;