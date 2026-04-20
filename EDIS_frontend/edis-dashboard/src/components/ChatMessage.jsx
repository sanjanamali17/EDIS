import ReactMarkdown from 'react-markdown';

export default function ChatMessage({ role, content }) {
  return (
    <div className={`chat-message ${role}`}>
      <div className="chat-bubble">
        {role === 'assistant' ? (
          <ReactMarkdown
            components={{
              // Custom styling for different markdown elements
              h1: ({children}) => <h1 className="chat-markdown-h1">{children}</h1>,
              h2: ({children}) => <h2 className="chat-markdown-h2">{children}</h2>,
              h3: ({children}) => <h3 className="chat-markdown-h3">{children}</h3>,
              h4: ({children}) => <h4 className="chat-markdown-h4">{children}</h4>,
              h5: ({children}) => <h5 className="chat-markdown-h5">{children}</h5>,
              h6: ({children}) => <h6 className="chat-markdown-h6">{children}</h6>,
              p: ({children}) => <p className="chat-markdown-p">{children}</p>,
              ul: ({children}) => <ul className="chat-markdown-ul">{children}</ul>,
              ol: ({children}) => <ol className="chat-markdown-ol">{children}</ol>,
              li: ({children}) => <li className="chat-markdown-li">{children}</li>,
              strong: ({children}) => <strong className="chat-markdown-strong">{children}</strong>,
              em: ({children}) => <em className="chat-markdown-em">{children}</em>,
              code: ({inline, children}) => 
                inline ? 
                  <code className="chat-markdown-inline-code">{children}</code> : 
                  <pre className="chat-markdown-code-block"><code>{children}</code></pre>,
              blockquote: ({children}) => <blockquote className="chat-markdown-blockquote">{children}</blockquote>,
              br: () => <br className="chat-markdown-br" />
            }}
          >
            {content}
          </ReactMarkdown>
        ) : (
          content
        )}
      </div>
    </div>
  );
}
