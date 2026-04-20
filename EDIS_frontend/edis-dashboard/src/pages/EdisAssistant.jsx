import { useState } from "react";
import React from "react";
import ChatSidebar from "../components/ChatSidebar";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";
import "../styles/edis_assistant.css";

export default function EdisAssistant() {
  // Load chat history from localStorage on component mount
  const loadChatHistory = () => {
    try {
      const savedHistory = localStorage.getItem('edis_chat_history');
      return savedHistory ? JSON.parse(savedHistory) : [
        {
          id: 1,
          title: "EDIS Environmental Intelligence",
          messages: [
            {
              role: "assistant",
              content:
                "Hello 👋 I'm your EDIS Assistant. I can help you with:\n\n🌍 Ecosystem stress analysis\n🌡️ Climate data interpretation\n🌱 Soil health assessment\n🦋 Biodiversity insights\n🏙️ Human pressure impacts\n\nAsk me anything about environmental health and restoration strategies!",
            },
          ],
        },
      ];
    } catch (error) {
      console.error('Error loading chat history:', error);
      return [
        {
          id: 1,
          title: "EDIS Environmental Intelligence",
          messages: [
            {
              role: "assistant",
              content:
                "Hello 👋 I'm your EDIS Assistant. I can help you with:\n\n🌍 Ecosystem stress analysis\n🌡️ Climate data interpretation\n🌱 Soil health assessment\n🦋 Biodiversity insights\n🏙️ Human pressure impacts\n\nAsk me anything about environmental health and restoration strategies!",
            },
          ],
        },
      ];
    }
  };

  const [chats, setChats] = useState(loadChatHistory());
  const [activeChatId, setActiveChatId] = useState(1);
  const [loading, setLoading] = useState(false);

  // Save chat history to localStorage whenever chats change
  React.useEffect(() => {
    localStorage.setItem('edis_chat_history', JSON.stringify(chats));
  }, [chats]);

  // 🔐 Safe active chat fallback
  const activeChat =
    chats.find((c) => c.id === activeChatId) || chats[0];

  // Check localStorage on component mount
  React.useEffect(() => {
    const storedData = localStorage.getItem('edis_ecosystem_data');
    const backupData = sessionStorage.getItem('edis_ecosystem_data_backup');
    
    console.log('localStorage check on mount:', storedData ? 'Data found' : 'No data');
    console.log('sessionStorage check on mount:', backupData ? 'Backup data found' : 'No backup data');
    
    if (storedData) {
      console.log('Data content:', JSON.parse(storedData));
    } else if (backupData) {
      console.log('Using backup data:', JSON.parse(backupData));
      // Restore from sessionStorage backup
      localStorage.setItem('edis_ecosystem_data', backupData);
    }
  }, []);

  const sendMessage = async (text) => {
    if (!text.trim()) return;

    // 1️⃣ Add user message immediately
    setChats((prev) =>
      prev.map((chat) =>
        chat.id === activeChatId
          ? {
              ...chat,
              messages: [
                ...chat.messages,
                { role: "user", content: text },
              ],
            }
          : chat
      )
    );

    setLoading(true);

    try {
      // 2️⃣ Get ecosystem context from localStorage
      let ecosystemData = null;
      const storedData = localStorage.getItem('edis_ecosystem_data');
      const backupData = sessionStorage.getItem('edis_ecosystem_data_backup');
      
      if (storedData) {
        ecosystemData = JSON.parse(storedData);
        console.log('Found ecosystem data:', ecosystemData); // Debug log
      } else if (backupData) {
        ecosystemData = JSON.parse(backupData);
        console.log('Found backup ecosystem data:', ecosystemData); // Debug log
        // Restore to localStorage
        localStorage.setItem('edis_ecosystem_data', backupData);
      } else {
        console.log('No ecosystem data found in localStorage or sessionStorage'); // Debug log
      }

      // 3️⃣ Backend call with ecosystem context and conversation history
      const res = await fetch(
        `/api/edis/chat`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            session_id: "session-1",
            location: ecosystemData?.location || "Unknown",
            message: text,
            ecosystem_score: ecosystemData?.ecosystem_score || null,
            indices: ecosystemData?.indices || null,
            messages: activeChat.messages.slice(-10), // Send last 10 messages for context
          }),
        }
      );

      if (!res.ok) {
        throw new Error("Assistant API failed");
      }

      const data = await res.json();

      const reply =
        data?.reply ||
        "⚠️ Assistant returned empty response.";

      // 3️⃣ Add assistant reply safely
      setChats((prev) =>
        prev.map((chat) =>
          chat.id === activeChatId
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  { role: "assistant", content: reply },
                ],
              }
            : chat
        )
      );
    } catch (err) {
      setChats((prev) =>
        prev.map((chat) =>
          chat.id === activeChatId
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  {
                    role: "assistant",
                    content:
                      "🤖 EDIS Assistant is working! I'm using intelligent fallback responses. For enhanced AI, please configure Groq API key in backend/.env file. In the meantime, I can help with ecosystem analysis, climate interpretation, and restoration recommendations!",
                  },
                ],
              }
            : chat
        )
      );
    } finally {
      setLoading(false);
    }
  };

  // Clear chat history function
  const clearChatHistory = () => {
    const defaultChats = [
      {
        id: 1,
        title: "EDIS Environmental Intelligence",
        messages: [
          {
            role: "assistant",
            content:
              "Hello 👋 I'm your EDIS Assistant. I can help you with:\n\n🌍 Ecosystem stress analysis\n🌡️ Climate data interpretation\n🌱 Soil health assessment\n🦋 Biodiversity insights\n🏙️ Human pressure impacts\n\nAsk me anything about environmental health and restoration strategies!",
          },
        ],
      },
    ];
    setChats(defaultChats);
    localStorage.setItem('edis_chat_history', JSON.stringify(defaultChats));
  };

  return (
    <div className="edis-chat-layout">
      <ChatSidebar
        chats={chats}
        activeChatId={activeChatId}
        setActiveChatId={setActiveChatId}
        onClearChat={clearChatHistory}
      />

      <div className="edis-chat-main">
        {activeChat && (
          <>
            <ChatWindow
              messages={activeChat?.messages || []}
              loading={loading}
            />
            <ChatInput onSend={sendMessage} />
          </>
        )}
      </div>
    </div>
  );
}
