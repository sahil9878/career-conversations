import { useRef, useState, type FunctionComponent } from "react";
import SendMessage from "../../assets/send-message";

interface MessageInputProps { }

const MessageInput: FunctionComponent<MessageInputProps> = () => {
    const [inputText, setInputText] = useState("");
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    const onInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setInputText(e.target.value);

        if (textareaRef.current) {
            textareaRef.current.style.height = "auto";
            textareaRef.current.style.height = textareaRef.current.scrollHeight + "px";
        }
    };

    const onSendClick = (e: React.MouseEvent<HTMLButtonElement>) => {
        console.log(`Sent text ${inputText}`)
        setInputText("")
    }

    return (
        <div className="chat-widget__message-input">
            <textarea
                ref={textareaRef}
                name="chat-message"
                id="chat-message"
                value={inputText}
                onChange={onInputChange}
                placeholder="Type a message..."
                rows={1}
                style={{ overflow: "hidden", resize: "none" }}
            />
            <button onClick={onSendClick}>

                <SendMessage width={24} height={24} />
            </button>
        </div>
    );
};

export default MessageInput;