import { useEffect, useState } from "react";
import { SSE, type SSEvent } from "sse.js";

export type Message = {
    user: "user" | "assistant";
    message: string
}

const useSendMessage = () => {

    const [history, setHistory] = useState<Message[]>([])
    const [streaming, setStreaming] = useState(false)
    const [chatId, setChatId] = useState<string | null>(null)
    const [loading, setLoading] = useState(false)


    useEffect(() => {
        const baseUrl = import.meta.env.VITE_BASE_URL || "http://localhost:8000";
        let eventSource: SSE;
        if (streaming && history.length > 1) {
            scrollLastMessageToTop(history)
            let buffer = ""

            eventSource = new SSE(`${baseUrl}/chat/`, {
                headers: {
                    "Content-Type": "application/json"
                },
                method: "POST",
                payload: JSON.stringify({ message: history[history.length - 2]?.message, chat_id: chatId }),
            })
            eventSource.addEventListener("chatCompletion", (e: SSEvent) => {
                const response = JSON.parse(e.data)
                buffer += response;
                const node = document.getElementById(`chat-message-${history.length - 1}`)
                if (!node) return
                node.textContent = node.textContent += response

            });
            eventSource.onreadystatechange = (state) => {
                if (state.readyState === SSE.CLOSED) {
                    setHistory((prev) => {
                        const newHistory = [...prev];
                        const lastMessage = newHistory[newHistory.length - 1];
                        lastMessage.message = buffer
                        return newHistory;
                    });
                    removeExtraPaddingFromChatWindow(history)
                    setStreaming(false)
                    setLoading(false)
                    eventSource.close()
                }
            }
        }

        return () => {
            eventSource?.close()
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [streaming])


    const sendMessage = async (message: string) => {
        let chat_id = chatId;
        if (!chat_id) {
            chat_id = crypto.randomUUID();
            setChatId(chat_id);
        }
        setLoading(true)
        const newHistory: Message[] = [...history, { user: "user", message }, { user: "assistant", message: "" }]
        setHistory(newHistory)
        setStreaming(true)
    }

    return { sendMessage, history, loading }
}

export default useSendMessage

const scrollLastMessageToTop = (history: Message[]) => {
    if (history.length > 0) {
        const chatWindow = document.getElementById("chat-history");
        const chatHistory = document.getElementById("chat-history-scroller");
        const userMsgId = `chat-message-${history.length - 2}`;
        const userMsgNode = document.getElementById(userMsgId);

        if (chatWindow && userMsgNode && chatHistory) {
            const chatWindowRect = chatWindow.getBoundingClientRect();
            const userMsgRect = userMsgNode.getBoundingClientRect();
            let spacer = document.getElementById("chat-window-spacer");
            if (!spacer) {
                spacer = document.createElement("div");
                spacer.id = "chat-window-spacer";
            }
            spacer.style.paddingTop = `${chatWindowRect.height - userMsgRect.height - 48}px`;
            chatHistory.appendChild(spacer);
            spacer.scrollIntoView({ behavior: "smooth" });
        }
    }
}

const removeExtraPaddingFromChatWindow = (history: Message[]) => {
    const chatWindow = document.getElementById("chat-history");
    const chatHistory = document.getElementById("chat-history-scroller");
    const userMsgId = `chat-message-${history.length - 1}`;
    const userMsgNode = document.getElementById(userMsgId);
    if (chatWindow && userMsgNode && chatHistory) {
        const chatWindowRect = chatWindow.getBoundingClientRect();
        const userMsgRect = userMsgNode.getBoundingClientRect();
        const offset = chatWindowRect.bottom - userMsgRect.bottom;
        let spacer = document.getElementById("chat-window-spacer");
        if (!spacer) {
            spacer = document.createElement("div");
            spacer.id = "chat-window-spacer";
        }
        spacer.style.paddingTop = `${offset - 8}px`;
        chatHistory.appendChild(spacer);
    }
}


