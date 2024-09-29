import asyncio
from typing import List, Dict, Any
import aiohttp
from pydantic import BaseModel

class Question(BaseModel):
    id: int
    text: str
    topic: str
    importance: int
    expected_answer_type: str

class WorkflowManager:
    def __init__(self, questions: List[Question], model_api_url: str):
        self.questions = questions
        self.model_api_url = model_api_url
        self.current_question_index = 0
        self.collected_answers = {}

    async def start_workflow(self):
        while self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            answer = await self.ask_question(question)
            self.collected_answers[question.id] = answer
            
            next_action = await self.analyze_answer(question, answer)
            if next_action == "next_question":
                self.current_question_index += 1
            elif next_action == "follow_up":
                follow_up_question = await self.generate_follow_up(question, answer)
                follow_up_answer = await self.ask_question(follow_up_question)
                self.collected_answers[f"{question.id}_follow_up"] = follow_up_answer

        return await self.generate_summary()

    async def ask_question(self, question: Question) -> str:
        # 这里应该实现与前端的交互逻辑
        # 在实际应用中，这可能涉及发送WebSocket消息或更新数据库
        print(f"Asking question: {question.text}")
        # 模拟用户输入
        return input("Your answer: ")

    async def analyze_answer(self, question: Question, answer: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post(self.model_api_url, json={
                "task": "analyze_answer",
                "question": question.dict(),
                "answer": answer
            }) as response:
                result = await response.json()
                return result["next_action"]

    async def generate_follow_up(self, question: Question, answer: str) -> Question:
        async with aiohttp.ClientSession() as session:
            async with session.post(self.model_api_url, json={
                "task": "generate_follow_up",
                "question": question.dict(),
                "answer": answer
            }) as response:
                result = await response.json()
                return Question(**result["follow_up_question"])

    async def generate_summary(self) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            async with session.post(self.model_api_url, json={
                "task": "generate_summary",
                "collected_answers": self.collected_answers
            }) as response:
                return await response.json()

# 使用示例
questions = [
    Question(id=1, text="What is your name?", topic="Personal Info", importance=5, expected_answer_type="text"),
    Question(id=2, text="How old are you?", topic="Personal Info", importance=4, expected_answer_type="number"),
    # 添加更多问题...
]

async def main():
    workflow = WorkflowManager(questions, "http://your-model-api-url.com")
    summary = await workflow.start_workflow()
    print("Workflow completed. Summary:", summary)

if __name__ == "__main__":
    asyncio.run(main())