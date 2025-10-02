import { useState } from "react";


export type Message = {
    user: "user" | "assistant";
    message: string
}

const useSendMessage = () => {

    const [history, setHistory] = useState<Message[]>([])
    const [chatId, setChatId] = useState<string | null>(null)
    const [loading, setLoading] = useState(false)


    const sendMessage = async (message: string) => {
        let chat_id = chatId;
        if (!chat_id) {
            chat_id = crypto.randomUUID();
            setChatId(chat_id);
        }
        setLoading(true)
        setHistory((prev) => [...prev, { user: "user", message }])
        try {
            const baseUrl = import.meta.env.VITE_BASE_URL || "http://localhost:8000";
            const response = await fetch(`${baseUrl}/chat/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message, chat_id })
            })
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            const data = await response.json()
            setHistory((prev) => [...prev, { user: "assistant", message: data.response }])
        } catch (error) {
            console.error("Error sending message:", error);
        } finally {
            setLoading(false)
        }
    }

    return { sendMessage, history, loading }
}

export default useSendMessage