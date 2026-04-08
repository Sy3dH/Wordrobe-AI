from src.memory.memory_manager import MemoryManager
from typing import Dict, Any, Optional
import logging
import json
import re
import uuid
from datetime import datetime
from google import genai
from google.genai import types
from src.configs.settings import GOOGLE_API_KEY
from src.prompts.prompts import FASHION_SYSTEM_PROMPT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = genai.Client(api_key=GOOGLE_API_KEY)


def _build_context_prompt(user_profile: Dict[str, Any]) -> str:
    return f"\n<user_profile>\n{json.dumps(user_profile, indent=2)}\n</user_profile>\n"


class FashionChatbot:
    def __init__(self, model_name: str, generation_config: Dict, memory: MemoryManager):
        self.model_name = model_name
        self.generation_config = generation_config
        self.memory = memory
        self._sessions: Dict[str, genai.chats.Chat] = {}
        logger.info("FashionChatbot initialised")

    def _get_or_create_session(self, session_id: str) -> genai.chats.Chat:
        if session_id not in self._sessions:
            self._sessions[session_id] = client.chats.create(
                model=self.model_name,
                config=types.GenerateContentConfig(
                    system_instruction=FASHION_SYSTEM_PROMPT,
                    **self.generation_config,
                ),
            )
            logger.info("Created new chat session: %s", session_id)
        return self._sessions[session_id]

    def _store_turn(
        self,
        user_id: str,
        session_id: str,
        user_message: str,
    ) -> None:
        """
        Pass the raw conversation turn to memory.
        LTM intelligently decides whether to extract and persist any preferences.
        """
        turn_data = {"role": "user", "content": user_message}

        ltm_saved, _ = self.memory.store_preference(turn_data, user_id, session_id)
        if ltm_saved:
            logger.info("Saved preference for %s:",turn_data)

    def chat(
        self,
        user_message: str,
        user_id: str,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        session_id = session_id or str(uuid.uuid4())

        user_profile = self.memory.get_user_profile(user_id, session_id)
        context_block = _build_context_prompt(user_profile)
        full_user_message = f"{context_block}\n User: {user_message}"

        chat_session = self._get_or_create_session(session_id)

        try:
            response = chat_session.send_message(full_user_message)
            print("response:", response)
        except Exception as exc:
            logger.error("Gemini API error: %s", exc)
            raise

        clean_response = response.text

        self._store_turn(user_id, session_id, user_message)
        logger.info("Turn complete for user=%s session=%s", user_id, session_id)

        return {
            "response": clean_response,
            "session_id": session_id,
        }


def create_fashion_chatbot(
    ltm_config: Optional[Dict] = None,
    stm_config: Optional[Dict] = None,
    model_name: str = "gemini-2.5-flash",
    generation_config: Optional[Dict] = None,
) -> FashionChatbot:
    _generation_config = generation_config or {
        "temperature": 0.8,
        "top_p": 0.95,
        "max_output_tokens": 1024,
    }
    memory = MemoryManager(ltm_config=ltm_config, stm_config=stm_config)
    return FashionChatbot(model_name=model_name, generation_config=_generation_config, memory=memory)


if __name__ == "__main__":
    bot = create_fashion_chatbot()

    r1 = bot.chat("I love earthy tones and minimalist styles.", user_id="user_1", session_id="test_1")
    print(r1["response"])

    r2 = bot.chat("What outfit would work for a dinner date?", user_id="user_1", session_id="test_1")
    print(r2["response"])