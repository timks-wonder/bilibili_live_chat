# import ollama
ollama = []

class Chatter:
    def __init__(self, prompts=None):
        if prompts is not None:
            self.prompts = prompts
        else:
            self.prompts = [{'role': 'user', 'content': '下面请扮演一个爱拆台，爱反驳的小女孩，与我对话，在对话中请尽量不要提到AI相关的概念，请不要让我察觉到我在和AI对话。'}]
        self.user_in = None
        self.response = ollama.chat(
            model="starling-lm:latest",
            messages=self.prompts
        )
        self.prompts.append(self.response['message'])

    def chat(self, words):
        self.user_in = {'role': 'user', 'content': words}
        self.prompts.append(self.user_in)
        self.response = ollama.chat(
            model="starling-lm:latest",
            messages=self.prompts
        )
        self.prompts.append(self.response['message'])
        return self.response['message'][1]
