from langchain_openai import ChatOpenAI


class LLMProvider:

    def __init__(self,model_name: str ="gpt-4.1-mini",temperature : float =0.0):
        self.model_name=model_name
        self.temperature=temperature

        self.llm = ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature
        )

    def get(self):
        return self.llm
