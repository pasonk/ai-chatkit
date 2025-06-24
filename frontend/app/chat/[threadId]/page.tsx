"use client";

import React from "react";
import ChatComponent from "../components/ChatComponent";

interface Props {
  params: { threadId: string };
}

export default function ChatPage({ params }: Props) {
  return (
    <ChatComponent
      threadId={params.threadId}
    />
  );
}
