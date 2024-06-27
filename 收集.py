import openai

class StartupInternBot:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OpenAI_API_Key)
        self.chat_history = []

    def generate_question(self):
        prompt = ("请根据以下对话内容生成一个问题（注意只需一个问题不要有其他对话内容），帮助进一步明确初创公司实习生的职位描述需求。"
                "这个问题应该能帮助收集制定职位描述所需的详细信息。请确保问题是新的且与之前的问题不重复：")
        for message in self.chat_history:
            role = "老板" if message['role'] == 'user' else "系统"
            prompt += f"\n{role}: {message['content']}"
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "system", "content": prompt}]
        )
        next_question = response.choices[0].message.content
        return next_question

    def ask_question(self, question):
        print(question)
        user_response = input("请输入您的回答: ")
        self.chat_history.append({"role": "system", "content": question})
        self.chat_history.append({"role": "user", "content": user_response})
        return user_response

    def generate_job_description(self):
        prompt = "基于以下对话，生成一个关于初创公司实习生的工作描述："
        for message in self.chat_history:
            role = "老板" if message['role'] == 'user' else "系统"
            prompt += f"\n{role}: {message['content']}"
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "system", "content": prompt}]
        )
        job_description = response.choices[0].message.content
        return job_description

    def interview_boss(self):
        print("您好！我在这里了解您对初创公司实习生的需求。")
        initial_question = "您能描述一下您希望招聘的实习生的类型吗？"
        user_response = self.ask_question(initial_question)

        num_questions = 5
        for _ in range(num_questions):
            next_question = self.generate_question()
            if next_question.strip() == "":
                break
            user_response = self.ask_question(next_question)

        job_description = self.generate_job_description()
        print("\n感谢您的时间！以下是生成的职位描述：")
        print("\n职位描述：")
        print(job_description)

bot = StartupInternBot()
bot.interview_boss()
