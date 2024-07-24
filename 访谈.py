import openai
from dotenv import load_dotenv
import os
import sys

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(base_path, '.env')
load_dotenv(env_path)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GPT_VERSION = "gpt-4o-mini"

class StartupInternBot:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.chat_history = []

    def interview_boss(self):
        print("您好！我在这里了解您对初创公司实习生的需求。")
        initial_question = "您能描述一下您希望招聘的实习生的类型吗？"
        self.ask_question(initial_question)

        num_questions = 5
        for _ in range(num_questions):
            next_question = self.generate_question()
            if next_question.strip() == "":
                break
            self.ask_question(next_question)

        job_description = self.generate_job_description()
        print("\n感谢您的时间！以下是生成的职位描述：")
        print("\n职位描述：")
        print(job_description)
    
    def generate_question(self):
        prompt = ("你是系统，你要负责访谈初创公司老板。请根据以下对话历史生成一个新的问题，注意不要重复已经问过的问题，其目的是进一步访谈老板并询问其对于实习生的要求（你不需要以“系统：”开头，直接问问题即可）：")
        for message in self.chat_history:
            role = "老板" if message['role'] == 'user' else "系统"
            prompt += f"\n{role}: {message['content']}"
        response = self.client.chat.completions.create(
            model=GPT_VERSION,
            messages=[{"role": "system", "content": prompt}]
        )
        next_question = response.choices[0].message.content
        return next_question

    def ask_question(self, question):
        print(question)
        user_response = input("请输入您的回答: ")
        print("\n")
        self.chat_history.append({"role": "system", "content": question})
        self.chat_history.append({"role": "user", "content": user_response})
        return user_response

    def generate_job_description(self):
        prompt = "基于以下对话，生成一份初创公司实习生的职位描述，并以编号列表的形式展示："
        for message in self.chat_history:
            role = "老板" if message['role'] == 'user' else "系统"
            prompt += f"\n{role}: {message['content']}"
        response = self.client.chat.completions.create(
            model=GPT_VERSION,
            messages=[{"role": "system", "content": prompt}]
        )
        job_description = response.choices[0].message.content
        return job_description

bot = StartupInternBot()
bot.interview_boss()
