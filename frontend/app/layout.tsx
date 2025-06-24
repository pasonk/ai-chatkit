"use client";

import React from "react";

import { Layout, Menu, Button, Select } from "antd";
import { useState, useEffect, useRef } from "react";
import { BarsOutlined, PlusOutlined } from "@ant-design/icons";
import "./globals.css";
import { v4 as uuidv4 } from "uuid";
import { LayoutContext } from "./layout-context";
import SessionListItem from './components/SessionListItem';
import AgentSelector from './components/AgentSelector';
import SiderComponent from './components/SiderComponent';

const { Header, Content } = Layout;

// 由于 ReactNode 可能无法正常导入，使用更通用的类型 any 替代
export default function RootLayout({ children }: { children: any }) {
  const [collapsed, setCollapsed] = useState(false);
  const [sessions, setSessions] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem("chatSessions") || "[]");
    } catch (e) {
      return [];
    }
  });


  const [currentThreadId, setCurrentThreadId] = useState(null);

  const [agentId, setAgentId] = useState("oa-assistant");


  //监听new-chat事件
  useEffect(() => {
    const addSession = (event: CustomEvent) => {
      const { threadId, msg } = event.detail;
      handleAddSession(threadId, msg);
    };
    window.addEventListener("add-session", addSession);
    return () => {
      window.removeEventListener("add-session", addSession);
    };
  }, []);

  const handleAddSession = (newThreadId: string, startMsg: string) => {
    if (!newThreadId) {
      newThreadId = uuidv4();
    }
    if (!startMsg) {
      startMsg = `greet ${new Date().toLocaleString()}`;
    }
    const newSession = {
      threadId: newThreadId,
      name: startMsg.substring(0, 10),
      lastUpdated: Date.now(),
    };
    // 左边栏的会话列表自动选择新会话
    setSessions((prev) => [...prev, newSession]);
    setCurrentThreadId(newThreadId);
    localStorage.setItem(
      "chatSessions",
      JSON.stringify([...sessions, newSession])
    );
    window.history.pushState({}, "", `/chat/${newThreadId}`);
  };

  // 删除会话处理函数
  const handleDeleteSession = (delThreadId: string) => {
    const newSessions = sessions.filter(
      (session) => session.threadId !== delThreadId
    );
    setSessions(newSessions);
    localStorage.setItem("chatSessions", JSON.stringify(newSessions));
    localStorage.removeItem( "chatMessages-" + delThreadId);
    if(newSessions.length > 0){
      setCurrentThreadId([...newSessions].reverse()[0]?.threadId || "");
      window.history.pushState({}, "", `/chat/${currentThreadId}`);
    }else{
      setCurrentThreadId(null);
      window.history.pushState({}, "", "/chat");
    }
  };

  const handlerNewChat = () => {
    setCurrentThreadId(null);
    window.history.pushState({}, "", "/chat");
  };

  const selectAgent = (value: string) => {
    console.log("selectAgent", value);
    setAgentId(value);
    handlerNewChat();
  };

  const [items, setItems] = useState([]);
  useEffect(() => {
    const reversedSessions = [...sessions].reverse();
    setItems(() => {
      return reversedSessions.map((session) => ({
        key: session.threadId,
        label: <SessionListItem session={session} onDelete={handleDeleteSession} />,
      }));
    });
  }, [sessions]);

  return (
    <LayoutContext.Provider value={{ agentId, setAgentId, currentThreadId, setCurrentThreadId }}>
      <html>
        <body className="min-h-screen">
          <Layout style={{ minHeight: "auto" }}>
            <SiderComponent
              collapsed={collapsed}
              onCollapse={setCollapsed}
              sessions={sessions}
              handleDeleteSession={handleDeleteSession}
              handlerNewChat={handlerNewChat}
              items={items}
              onSelectSession={(key) => {
                setCurrentThreadId(key);
                const newPath = `/chat/${key}`;
                window.history.pushState({}, "", newPath);
              }}
            />
            <Layout>
              <Header className="bg-white p-0 flex flex-nowrap">
                <BarsOutlined
                  onClick={() => setCollapsed(!collapsed)}
                  className="ml-4 text-xl"
                />
                <div className="flex items-center ml-8 flex-none shrink-0">
                  <span className="text-base">AI-Agent:</span>
                  <AgentSelector value={agentId} onChange={selectAgent} />
                </div>
              </Header>
              <Content className="m-4 p-6 bg-white min-h-[calc(100vh-120px)]">
                  {children}
              </Content>
            </Layout>
          </Layout>
        </body>
      </html>
    </LayoutContext.Provider>

  );
}
