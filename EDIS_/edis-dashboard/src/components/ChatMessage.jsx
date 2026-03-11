export default function ChatMessage({ role, content }) {
  return (
    <div className={`chat-message ${role}`}>
      <div className="chat-bubble">
        {content}
      </div>
    </div>
  );
}
