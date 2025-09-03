import type { FunctionComponent } from "react";
import MessageInput from "./message-input";
import ChatHistory from "./chat-history";
import useSendMessage from "../../hooks/useSendMessage";

interface ChatWidgetProps {

}

const ChatWidget: FunctionComponent<ChatWidgetProps> = () => {

    const { sendMessage, history, loading } = useSendMessage();
    return (<div className="chat-widget">
        <ChatHistory history={history} loading={loading} />
        <MessageInput sendMessage={sendMessage} loading={loading} />
    </div>);
}

export default ChatWidget;