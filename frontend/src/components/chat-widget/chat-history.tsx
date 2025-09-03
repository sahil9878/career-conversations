import { useEffect, type FunctionComponent } from "react";
import type { Message } from "../../hooks/useSendMessage";

interface ChatHistoryProps {
    history: Message[]
    loading: boolean
}

const ChatHistory: FunctionComponent<ChatHistoryProps> = ({ history, loading }) => {

    useEffect(() => {
        const chatHistoryDiv = document.querySelector('.chat-widget__chat-history');
        if (chatHistoryDiv) {
            const lastMessage = chatHistoryDiv.lastElementChild;
            if (lastMessage) {
                lastMessage.scrollIntoView({ behavior: 'smooth' });
            }
        }
    }, [history]);


    return (<div className="chat-widget__chat-history">
        {history.map((msg, index) => (
            <div key={index} className={`chat-widget__chat-message chat-widget__chat-message--${msg.user === "user" ? "user" : "bot"}`}>
                <div className="chat-widget__chat-message-content">
                    {msg.message}
                </div>
            </div>
        ))}
        {loading && (
            <div className="chat-widget__chat-message chat-widget__chat-message--bot">
                <div className="chat-widget__chat-message-content">
                    Typing...
                </div>
            </div>
        )}
    </div>);
}

export default ChatHistory;