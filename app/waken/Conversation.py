from tenacity import retry, stop_after_attempt, wait_exponential
import jieba
from openai import OpenAI
import os
import sys

# waken 参数
PROMPT_ROOT = "./app/waken/prompts"

sys.path.append("D:\Projects\WeChatMsg")
# from app.config import *
from app.log import logger


def tokens(msg):
    return list(jieba.cut(msg))


def token_len_of(msg):
    return len(tokens(msg))


class Conversation:
    def __init__(self):
        self.qwen_client = OpenAI(
            api_key=os.getenv("QWEN_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        self.qwen_models = ['qwen-max', 'qwen-plus', 'qwen-turbo', 'qwen-long']

        self.deepseek_client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com",
        )
        # 模型列表：https://api-docs.deepseek.com/zh-cn/quick_start/pricing
        self.deepseek_models = ['deepseek-reasoner', 'deepseek-chat']

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_response_from_llm(self, rule=None, question="你好", client=None, model=None):
        '''
        rule: 你希望模型扮演的角色
        question: 你想问该模型的问题
        client: qwen_client or deepseek_client
        model: ['qwen-max', 'qwen-plus', 'qwen-turbo', 'qwen-long'], ['deepseek-reasoner', 'deepseek-chat']
        '''
        if rule is None:
            rule = "你是一个有用的助手"

        if client is None or client == "qwen_client":
            client = self.qwen_client
        elif client == "deepseek_client":
            client = self.deepseek_client
        else:
            raise ValueError("client should be deepseek_client or qwen_client")

        if model is None:
            model = self.qwen_models[0] if client == self.qwen_client else self.deepseek_models[0]
        if model not in self.qwen_models + self.deepseek_models:
            raise ValueError("model should be in list")

        logger.info(f"sending msg having {token_len_of(rule+question)}~ ")
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': rule},
                {'role': 'user', 'content': question}
            ]
        )
        ret = completion.choices[0].message.content
        logger.info(f"\nfor question: {question}, got answer: {ret}\n")
        return ret


if __name__ == "__main__":
    Conversation().get_response_from_llm(question="嘿嘿 你好呀")
