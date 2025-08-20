from enum import StrEnum
from typing import TypeAlias

DEFAULT_MODEL = "deepseek-chat"


class OpenAIModelName(StrEnum):
    """https://platform.openai.com/docs/models/gpt-4o"""

    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4O = "gpt-4o"

class DeepseekModelName(StrEnum):
    """https://api-docs.deepseek.com/quick_start/pricing"""
    DEEPSEEK_CHAT = "deepseek-chat"

class OllamaModelName(StrEnum):
    """https://ollama.com/search"""

    OLLAMA_GENERIC = "ollama"

class FakeModelName(StrEnum):
    """Fake model for testing."""
    FAKE = "fake"
    
class TongYiModelName(StrEnum):
    """TongYi model"""
    QWEN_PLUS = "qwen-plus"
    QWEN_MAX = "qwen-max"
    



AllModelEnum: TypeAlias = (
    OpenAIModelName
    | DeepseekModelName
    | OllamaModelName
    | FakeModelName
    | TongYiModelName
)
