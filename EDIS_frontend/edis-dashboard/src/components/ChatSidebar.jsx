export default function ChatSidebar({ chats, activeChatId, setActiveChatId, onClearChat }) {
  return (
    <aside className="chat-sidebar">
      <h3>EDIS Chats</h3>

      {chats.map(chat => (
        <div
          key={chat.id}
          className={`chat-item ${chat.id === activeChatId ? "active" : ""}`}
          onClick={() => setActiveChatId(chat.id)}
        >
          {chat.title}
        </div>
      ))}

      <button 
        className="clear-chat-btn" 
        onClick={onClearChat}
        title="Clear chat history"
      >
        🗑️ Clear Chat
      </button>
    </aside>
  );
}
