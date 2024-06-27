import openai
import matplotlib.pyplot as plt
import numpy as np

class SalesJobInterviewBot:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OpenAI_API_Key)
    
    def extract_capabilities(self, job_description):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": f"请从以下职位描述中总结销售岗位所要求的核心能力：\n{job_description}"}]
        )
        capabilities = response.choices[0].message["content"]
        return capabilities.split('\n')

    def generate_interview_questions(self, capabilities):
        prompt = "根据以下能力列表，生成一套针对销售岗位的面试题：\n" + '\n'.join(capabilities)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )
        questions = response.choices[0].message["content"]
        return questions.split('\n')

    def simulate_interview_answers(self, questions):
        answers = []
        for question in questions:
            simulated_answer = input(question)
            answers.append(simulated_answer)
        return answers

    def evaluate_capabilities(self, answers, capabilities):
        prompt = "根据以下回答和所需能力，评估应试者的能力匹配度：\n" + '\n'.join(answers + capabilities)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )
        evaluations = response.choices[0].message["content"]
        return list(map(int, evaluations.split('\n')))

    def visualize_capability_assessment(self, capabilities, evaluations):
        labels = np.array(capabilities)
        stats = np.array(evaluations)
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        stats = np.concatenate((stats, [stats[0]]))
        angles += angles[:1]
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.fill(angles, stats, color='red', alpha=0.25)
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        plt.show()

# Usage
bot = SalesJobInterviewBot()
job_description = "Your job description here"
capabilities = bot.extract_capabilities(job_description)
questions = bot.generate_interview_questions(capabilities)
answers = bot.simulate_interview_answers(questions)
evaluations = bot.evaluate_capabilities(answers, capabilities)
bot.visualize_capability_assessment(capabilities, evaluations)
