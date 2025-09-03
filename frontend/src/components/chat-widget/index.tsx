import type { FunctionComponent } from "react";
import MessageInput from "./message-input";
import ChatHistory from "./chat-history";

interface ChatWidgetProps {

}

const ChatWidget: FunctionComponent<ChatWidgetProps> = () => {
    return (<div className="chat-widget">
        <ChatHistory />
        <MessageInput />
    </div>);
}

export default ChatWidget;