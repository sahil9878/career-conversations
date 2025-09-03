import { useRef, useState, type FunctionComponent } from "react";
import SendMessage from "../../assets/send-message";

interface MessageInputProps {
    sendMessage: (message: string) => void;
    loading: boolean;
}

const MessageInput: FunctionComponent<MessageInputProps> = ({ sendMessage, loading }) => {
    const [inputText, setInputText] = useState("");
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    const onInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setInputText(e.target.value);

        if (textareaRef.current) {
            textareaRef.current.style.height = "auto";
            textareaRef.current.style.height = textareaRef.current.scrollHeight + "px";
        }
    };

    const onSendClick = () => {
        sendMessage(inputText);
        setInputText("")
    }

    const onKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            if (!loading && inputText.trim() !== "") {
                onSendClick();
            }
        }
    }

    return (
        <div className="chat-widget__message-input">
            <textarea
                ref={textareaRef}
                name="chat-message"
                id="chat-message"
                value={inputText}
                onChange={onInputChange}
                onKeyDown={onKeyDown}
                placeholder="Type a message..."
                rows={1}
                style={{ overflow: "hidden", resize: "none" }}
            />
            <button disabled={loading} onClick={onSendClick}>
                <SendMessage width={24} height={24} />
            </button>
        </div>
    );
};

export default MessageInput;