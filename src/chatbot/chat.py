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


def _extract_preferences(response_text: str) -> Optional[Dict[str, Any]]:
    match = re.search(r"<preferences>(.*?)</preferences>", response_text, re.DOTALL)
    if not match:
        return None
    try:
        data = json.loads(match.group(1).strip())
        if any(v for v in data.values() if v):
            return data
    except json.JSONDecodeError:
        logger.warning("Could not parse <preferences> block.")
    return None


def _clean_response(response_text: str) -> str:
    return re.sub(r"<preferences>.*?</preferences>", "", response_text, flags=re.DOTALL).strip()


class FashionChatbot:
    """
    Gemini-powered fashion chatbot backed by a MemoryManager for
    persistent (LTM) and session-scoped (STM) memory.

    Multi-turn is handled by storing a `genai.Chat` object per session_id.
    History is managed automatically by the SDK — just keep calling
    chat.send_message() on the same Chat object.
    """

    def __init__(self, model_name: str, generation_config: Dict, memory: MemoryManager):
        self.model_name = model_name
        self.generation_config = generation_config
        self.memory = memory
        # Keyed by session_id → genai.Chat object
        self._sessions: Dict[str, genai.chats.Chat] = {}
        logger.info("FashionChatbot initialised")

    def _get_or_create_session(self, session_id: str) -> genai.chats.Chat:
        """Return the existing Chat session for this session_id, or create a new one."""
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
        assistant_message: str,
        preferences: Optional[Dict[str, Any]],
    ) -> None:
        context_data = {
            "type": "conversation_turn",
            "timestamp": datetime.utcnow().isoformat(),
            "user_message": user_message,
            "assistant_message": assistant_message,
        }
        self.memory.store_context(context_data, user_id)

        if preferences:
            preference_data = {
                "type": "style_preference",
                "timestamp": datetime.utcnow().isoformat(),
                "source": "chat_extraction",
                **preferences,
            }
            ltm_saved, stm_saved = self.memory.store_preference(preference_data, user_id, session_id)
            logger.info("Preferences stored — LTM: %s | STM: %s", ltm_saved, stm_saved)

    def chat(
        self,
        user_message: str,
        user_id: str,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Process one conversational turn.
        Multi-turn context is maintained automatically within the same session_id.
        """
        session_id = session_id or str(uuid.uuid4())

        # Inject user profile as context alongside the message
        user_profile = self.memory.get_user_profile(user_id, session_id)
        context_block = _build_context_prompt(user_profile)
        full_user_message = f"{context_block}\nUser: {user_message}"

        # Get (or create) the persistent Chat session for this session_id
        chat_session = self._get_or_create_session(session_id)

        try:
            # The SDK automatically appends each turn to internal history
            response = chat_session.send_message(full_user_message)
        except Exception as exc:
            logger.error("Gemini API error: %s", exc)
            raise

        raw_text = response.text
        preferences = _extract_preferences(raw_text)
        clean_response = _clean_response(raw_text)

        self._store_turn(user_id, session_id, user_message, clean_response, preferences)
        logger.info("Turn complete for user=%s session=%s", user_id, session_id)

        return {
            "response": clean_response,
            "preferences": preferences,
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

    # Same session_id = same Chat object = true multi-turn
    r1 = bot.chat("I love earthy tones and minimalist styles.", user_id="user_1", session_id="test_1")
    print(r1["response"])

    r2 = bot.chat("What outfit would work for a dinner date?", user_id="user_1", session_id="test_1")
    print(r2["response"])  # Model remembers the earthy tones preference