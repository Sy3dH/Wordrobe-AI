from src.memory.ltm import LongTermMemory
from src.memory.stm import ShortTermMemory
from typing import Tuple
from typing import Dict, Any, Optional
import logging
import os
from src.configs.settings import GOOGLE_API_KEY

os.environ["REDISVL_DISABLE_ANALYTICS"] = "1"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MemoryManager:
    """
    Central manager for coordinating LTM and STM operations
    """

    def __init__(self, ltm_config: Optional[Dict] = None, stm_config: Optional[Dict] = None):
        """
        Initialize Memory Manager

        Args:
            ltm_config: Configuration for Long Term Memory
            stm_config: Configuration for Short Term Memory
        """
        self.ltm = LongTermMemory(ltm_config)
        self.stm = ShortTermMemory(stm_config)
        logger.info("Memory Manager initialized")

    def store_preference(self, preference_data: Dict[str, Any], user_id: str, session_id: str) -> Tuple[bool,bool]:
        """Store user fashion preference in LTM"""
        return self.ltm.store(preference_data, user_id), self.stm.session_lived_store(preference_data, user_id, session_id)

    def store_context(self, context_data: Dict[str, Any], user_id: str) -> bool:
        """Store conversation context in STM"""
        return self.stm.store(context_data, user_id)

    def get_user_profile(self, user_id: str, session_id:str) -> Dict[str, Any]:
        """
        Get comprehensive user profile combining LTM and STM

        Returns:
            Complete user profile for fashion assistance
        """
        ltm_data = self.ltm.get_user_preferences(user_id)
        stm_data = self.stm.get_recent_context("recent_conversation",user_id, session_id)

        return {
            "user_id": user_id,
            "long_term_preferences": ltm_data,
            "recent_context": stm_data,
            "profile_complete": len(ltm_data["style_preferences"]) > 0
        }

if __name__ == "__main__":

    m = MemoryManager()
    test_json = [
        {"role": "user", "content": "I’m building a work wardrobe. Can you guide me?"},
        {"role": "assistant", "content": "Sure. Do you like more formal or business casual?"},
        {"role": "user", "content": "Business casual. I don’t like stiff suits."},
        {"role": "assistant", "content": "Understood. Any colors you prefer for work?"},
        {"role": "user", "content": "I like navy and beige for work outfits."},
    ]

    for item in test_json:
        m.store_preference(item, user_id="user_1", session_id="test_1")
    print(m.ltm.retrieve(query="What colors I like?",user_id="user_1"))