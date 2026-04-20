import { useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage";

export default function ChatWindow({ messages }) {
  const bottomRef = useRef(null);

  // Auto scroll to bottom when new message arrives
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="chat-window">
      {messages.map((msg, index) => (
        <ChatMessage
          key={index}
          role={msg.role}
          content={msg.content}
        />
      ))}
      <div ref={bottomRef} />
    </div>
  );
}
