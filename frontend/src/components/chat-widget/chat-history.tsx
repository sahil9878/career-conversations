import { type FunctionComponent } from "react";
import type { Message } from "../../hooks/useSendMessage";

interface ChatHistoryProps {
    history: Message[]
}

const ChatHistory: FunctionComponent<ChatHistoryProps> = ({ history }) => {

    return (<div id="chat-history" className="chat-widget__chat-history">
        <div id="chat-history-scroller" className="chat-widget__chat-history-scroller">
            {history.map((msg, index) => (
                <div key={index} id={`chat-message-${index}`} className={`chat-widget__chat-message chat-widget__chat-message--${msg.user === "user" ? "user" : "bot"}`}>
                    <div className="chat-widget__chat-message-content">
                        {msg.message}
                    </div>
                </div>
            ))}
        </div>
    </div>);
}

export default ChatHistory;