import type { FunctionComponent } from "react";
import ChatWidget from "./chat-widget";

interface ChatSectionProps {

}

const ChatSection: FunctionComponent<ChatSectionProps> = () => {
    return (<section className='conversation'>
        <p>
            Want to learn more about me? Ask my AI assistant!
        </p>
        <ChatWidget />
    </section>);
}

export default ChatSection;