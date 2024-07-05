import openai
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
from dotenv import load_dotenv
import os
import sys

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(base_path, '.env')
load_dotenv(env_path)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class SalesJobInterviewBot:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.gpt_model = "gpt-3.5-turbo"
        self.chat_history = []

    def extract_capabilities(self, job_description):
        response = self.client.chat.completions.create(
            model=self.gpt_model,
            messages=[{"role": "system", "content": f"请从以下职位描述中总结销售岗位所要求的核心能力，并以编号列表的形式展示：\n{job_description}"}]
        )
        capabilities = response.choices[0].message.content.strip()
        parsed_capabilities = [line.split('. ', 1)[1] for line in capabilities.split('\n') if '. ' in line]
        return parsed_capabilities

    def generate_interview_question(self, capabilities):
        prompt = "根据以下职位所需能力列表和应试者先前的对话内容（如有），生成一个新的面试问题："
        prompt += "\n\n职位所需能力：\n" + '\n'.join(capabilities)
        if self.chat_history:
            prompt += "\n\n应试者先前的对话:\n" + '\n'.join([f"{msg['role']}: {msg['content']}" for msg in self.chat_history])
        else:
            prompt += "\n\n应试者先前的对话：无"
        response = self.client.chat.completions.create(
            model=self.gpt_model,
            messages=[{"role": "system", "content": prompt}]
        )
        new_question = response.choices[0].message.content.strip()
        self.chat_history.append({"role": "system", "content": new_question})
        return new_question

    def simulate_interview_answer(self, question):
        print(question)
        simulated_answer = input("\n请输入您的回答: ")
        print("\n")
        self.chat_history.append({"role": "user", "content": simulated_answer})
        return simulated_answer

    def evaluate_capabilities(self, answers, capabilities):
        prompt = "根据以下职位所需能力和应试者的回答，评估应试者的能力匹配度（对于每个能力，你需要以编号列表的形式按顺序展示匹配度，满分为10分，比如\n1. 5\n2. 7\n3. 4）："
        prompt += "\n\n职位所需能力：\n" + '\n'.join(capabilities)
        prompt += "\n\n应试者的回答：\n" + '\n'.join(answers)
        response = self.client.chat.completions.create(
            model=self.gpt_model,
            messages=[{"role": "system", "content": prompt}]
        )
        evaluations = response.choices[0].message.content.strip()
        parsed_evaluations = [line.split('. ', 1)[1] for line in evaluations.split('\n') if '. ' in line]
        return list(map(int, parsed_evaluations))

    def visualize_capability_assessment(self, capabilities, evaluations):
        font = FontProperties(fname='C:/Windows/Fonts/simhei.ttf', size=14)

        if len(evaluations) > len(capabilities):
            evaluations = evaluations[:len(capabilities)]
        elif len(evaluations) < len(capabilities):
            evaluations += [0] * (len(capabilities) - len(evaluations))

        labels = np.array(capabilities)
        stats = np.array(evaluations)
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()

        stats = np.concatenate((stats, [stats[0]]))
        angles += [angles[0]]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.fill(angles, stats, color='red', alpha=0.25)
        ax.set_ylim(0, 10)
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontproperties=font)

        for angle, stat in zip(angles, stats):
            ax.text(angle, stat, f'{stat:.1f}', horizontalalignment='center', verticalalignment='bottom', fontproperties=font)

        plt.show()

bot = SalesJobInterviewBot()
with open("Job Description.txt", "r", encoding="utf-8") as jd:
    job_description = jd.read()
capabilities = bot.extract_capabilities(job_description)

questions = []
answers = []
for _ in range(4):
    question = bot.generate_interview_question(capabilities)
    questions.append(question)
    answer = bot.simulate_interview_answer(question)
    answers.append(answer)

evaluations = bot.evaluate_capabilities(answers, capabilities)
bot.visualize_capability_assessment(capabilities, evaluations)
