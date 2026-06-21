from typing import Dict, List
import os
import httpx
import time
import traceback
from loguru import logger

from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

from src.prompts import custom_instructions, summary_prompt
from src.app_config import MODEL_NAME, TEMPERATURE, LLM_MODEL_TYPE


class AIModel:
    name = ""

    def invoke(self, prompt: ChatPromptTemplate) -> BaseMessage:
        logger.info(f"Got access to model via {self.name} API")
        prompt_messages = [SystemMessage(content=custom_instructions)] + prompt.messages
        try:
            response = self.model.invoke(prompt_messages)
            return response
        except Exception:
            tb_str = traceback.format_exc()
            if self.llm_proxy:
                logger.error(
                    f"LLM access error using proxy {self.llm_proxy.split('@')[-1]}: \n Traceback: {tb_str}"
                )
            else:
                logger.error(f"LLM access error: \n Traceback: {tb_str}")
            time.sleep(3)


class GeminiModel(AIModel):
    """Get access to Gemini model"""

    name = "Gemini"

    def __init__(self, api_key: str, llm_model: str, llm_proxy: str) -> None:
        from google.genai import types
        from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory

        # os.environ["https_proxy"] = llm_proxy
        http_options = types.HttpOptions(
            client_args={"proxy": llm_proxy}, async_client_args={"proxy": llm_proxy}
        )
        self.google_api_key = api_key
        self.model = ChatGoogleGenerativeAI(
            model=llm_model,
            google_api_key=self.google_api_key,
            temperature=TEMPERATURE,
            thinking_level="minimal",
            safety_settings={
                HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DEROGATORY: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_TOXICITY: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_VIOLENCE: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUAL: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_MEDICAL: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            },
            http_options=http_options,
        )


class OpenAIModel(AIModel):
    """Get access to OpenAI model"""

    name = "OpenAI"

    def __init__(self, api_key: str, llm_model: str, llm_proxy: str = None) -> None:
        from langchain_openai import ChatOpenAI

        if llm_proxy:
            http_client = httpx.Client(proxy=llm_proxy)
        else:
            http_client = None
        self.llm_proxy = llm_proxy
        self.model_name = llm_model
        self.openai_api_key = api_key
        self.model = ChatOpenAI(
            model_name=self.model_name,
            openai_api_key=self.openai_api_key,
            http_client=http_client,
            temperature=1 if "o1" in self.model_name or "gpt-5" in self.model_name else TEMPERATURE,
            presence_penalty=0,
            frequency_penalty=0,
            timeout=60,
            reasoning_effort="minimal",
        )


class OpenRouterModel(AIModel):
    """Get access to models via OpenRouter API"""

    name = "OpenRouter"

    def __init__(self, api_key: str, llm_model: str, llm_proxy: str = None) -> None:
        from langchain_openai import ChatOpenAI

        http_client = httpx.Client(proxy=llm_proxy) if llm_proxy else None
        self.llm_proxy = llm_proxy
        self.model_name = llm_model
        self.model = ChatOpenAI(
            model_name=self.model_name,
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            http_client=http_client,
            temperature=TEMPERATURE,
            timeout=60,
        )


class LoggerChatModel:
    def __init__(self, llm):
        self.llm = llm

    def __call__(self, messages: List[Dict[str, str]]) -> str:
        while True:
            try:
                reply = self.llm.invoke(messages)
                return reply
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    time.sleep(30)
                else:
                    time.sleep(30)
            except Exception as e:
                print(f"Error invoking model: {e}")
                raise e


def generate_summary(input_text: str) -> str:
    """
    Summarize the text and extract main ideas.
    """
    print(f"Summarizing text length: {len(input_text)} chars...")
    llm_api_key = os.getenv("llm_api_key")
    llm_proxy = os.getenv("llm_proxy")

    prompt_template = ChatPromptTemplate.from_template(summary_prompt)

    if LLM_MODEL_TYPE == "gemini":
        llm = GeminiModel(llm_api_key, MODEL_NAME, llm_proxy)
    elif LLM_MODEL_TYPE == "openai":
        llm = OpenAIModel(llm_api_key, MODEL_NAME, llm_proxy)
    elif LLM_MODEL_TYPE == "openrouter":
        llm = OpenRouterModel(llm_api_key, MODEL_NAME, llm_proxy)
    else:
        raise ValueError(f"Model type {LLM_MODEL_TYPE} is not supported")

    llm_wrapper = LoggerChatModel(llm)
    chain = prompt_template | llm_wrapper

    # We pass input_text. Language detection is handled by the LLM implicitly via prompts.
    result = chain.invoke({"input_text": input_text})

    return result.content
