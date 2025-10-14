import type { FunctionComponent } from "react";
import MessageInput from "./message-input";
import ChatHistory from "./chat-history";
import useSendMessage from "../../hooks/useSendMessage";



const ChatWidget: FunctionComponent = () => {

    const { sendMessage, history, loading } = useSendMessage();
    return (<div id="chat-window" className="chat-widget">
        <ChatHistory history={history} />
        <MessageInput sendMessage={sendMessage} loading={loading} />
    </div>);
}

export default ChatWidget;