import React, { useState, useEffect, useRef } from "react";
import { Send, Loader } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";

const InteractiveChat = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    // 组件挂载时添加初始消息
    setMessages([{ content: getInitialMessage(), sender: "bot" }]);
  }, []);

  useEffect(scrollToBottom, [messages]);

  const getInitialMessage = () => {
    return "你好！我是你的虚拟助手，很高兴为你服务。让我们开始对话吧！";
  };

  const onSendMessage = async (message) => {
    // 这里模拟与后端API的通信
    // 在实际应用中，这里应该调用真实的API
    setIsLoading(true);
    try {
      // 模拟API调用的延迟
      await new Promise((resolve) => setTimeout(resolve, 1000));

      // 模拟API响应
      const response = `收到你的消息: "${message}"。这是一个模拟的回复。`;
      return response;
    } catch (error) {
      console.error("Error sending message:", error);
      return "抱歉，处理你的消息时出现了错误。";
    } finally {
      setIsLoading(false);
    }
  };

  const handleSend = async () => {
    if (inputValue.trim() === "") return;

    const userMessage = { content: inputValue, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);

    try {
      const response = await onSendMessage(inputValue);
      const botMessage = { content: response, sender: "bot" };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
      const errorMessage = {
        content: "抱歉，处理你的消息时出现了错误。",
        sender: "bot",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardContent className="p-4">
        <div className="h-96 overflow-y-auto mb-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`mb-2 p-2 rounded-lg ${
                message.sender === "user"
                  ? "bg-blue-100 ml-auto"
                  : "bg-gray-100"
              } max-w-[80%]`}
            >
              {message.content}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
        <div className="flex items-center">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleSend()}
            placeholder="输入你的消息..."
            className="flex-grow mr-2"
          />
          <Button onClick={handleSend} disabled={isLoading}>
            {isLoading ? (
              <Loader className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default InteractiveChat;
