from src.memory.ltm import LongTermMemory
from src.memory.stm import ShortTermMemory
from src.utils import get_combined_config
from src.configs.configs import (LTM_CONFIG, STM_CONFIG)
                                 #LTM_LLM_CONFIG, LLM_CONFIG, EMBEDDING_CONFIG)
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

    def store_preference(self, preference_data: Dict[str, Any], user_id: str) -> bool:
        """Store user fashion preference in LTM"""
        return self.ltm.store(preference_data, user_id)

    def store_context(self, context_data: Dict[str, Any], user_id: str) -> bool:
        """Store conversation context in STM"""
        return self.stm.store(context_data, user_id)

    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Get comprehensive user profile combining LTM and STM

        Returns:
            Complete user profile for fashion assistance
        """
        ltm_data = self.ltm.get_user_preferences(user_id)
        stm_data = self.stm.get_recent_context(user_id)

        return {
            "user_id": user_id,
            "long_term_preferences": ltm_data,
            "recent_context": stm_data,
            "profile_complete": len(ltm_data["style_preferences"]) > 0
        }

if __name__ == "__main__":
    #ltm_config = get_combined_config(LTM_CONFIG, EMBEDDING_CONFIG, LTM_LLM_CONFIG)
    #stm_config = get_combined_config(STM_CONFIG, EMBEDDING_CONFIG, LLM_CONFIG)
    #print(ltm_config)
    m = MemoryManager()
    test_json = {
    "role": "user",
    "content": "I prefer wearing pastel colors in summer, especially light blue and mint green.",
    "category": "color_preference"
    }

    test_json_list = [
  {
    "role": "user",
    "content": "I prefer wearing pastel colors in summer, especially light blue and mint green.",
    "category": "color_preference"
  },
  {
    "role": "user",
    "content": "I usually wear casual outfits like jeans and sneakers during weekdays.",
    "category": "style_history"
  },
  {
    "role": "user",
    "content": "I cannot wear wool sweaters because they make my skin itchy.",
    "category": "allergy_constraint"
  },
  {
    "role": "user",
    "content": "For weddings, I like wearing traditional outfits with embroidery.",
    "category": "occasion_wear"
  },
  {
    "role": "user",
    "content": "I want to explore sustainable fashion brands that use organic fabrics.",
    "category": "future_preference"
  }
]

    m.store_preference(preference_data= test_json, user_id="test_user_id")
    m.ltm.retrieve("Suggest me some nice colors", "test_user_id")