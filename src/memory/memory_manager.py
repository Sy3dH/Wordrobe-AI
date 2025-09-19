from src.memory.ltm import LongTermMemory
from src.memory.stm import ShortTermMemory
from src.utils import get_combined_config
from src.configs.configs import (LTM_CONFIG, STM_CONFIG)
                                 #LTM_LLM_CONFIG, LLM_CONFIG, EMBEDDING_CONFIG)
from openinference.instrumentation.google_genai import GoogleGenAIInstrumentor
from typing import Dict, Any, Optional
import logging
import os
from src.configs.settings import GOOGLE_API_KEY,ARIZE_API_KEY
from arize.otel import register
import json

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

    def store_context(self, context_data: Dict[str, Any], user_id: str, session_id: str) -> bool:
        """Store conversation context in STM"""
        return self.stm.session_lived_store(context_data, user_id, session_id)

    def store_user_profile(self, context_data: Dict[str, Any], user_id: str, session_id: str) -> tuple[bool, bool]:
        """Store user profile in STM & LTM (It will be stored in LTM if the context has facts)"""
        return self.store_preference(context_data, user_id), self.store_context(context_data, user_id, session_id)


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

    import pandas as pd

    # test_json_list = [
    #     {
    #         "role": "user",
    #         "content": "Hey, I just joined the app. Can you help me personalize my style?"
    #     },
    #     {
    #         "role": "assistant",
    #         "content": "Of course! Let’s start with some basics. Do you have favorite colors you like to wear?"
    #     }
    # ]

    tracer_provider = register(
        space_id="U3BhY2U6MjgyNjc6Sm10Kw==",
        api_key=ARIZE_API_KEY,
        project_name="Wordrobe_chatbot",
    )

    m = MemoryManager()
    GoogleGenAIInstrumentor().instrument(tracer_provider=tracer_provider)

    file_path = "D:\9D Tech Work\Wardrobe-POC\POC-4\Wordrobe-AI\\fashion_assistant_conversations_with_memory.csv"
    df = pd.read_csv(file_path)

    for (user_id, session_id), group in df.groupby(["user_id", "session_id"]):
        group_sorted = group.sort_values("turn")
        for _, row in group_sorted.iterrows():
            item = {
                "role": row["role"],
                "content": row["content"],
                "memory": row["memory"]
            }
            m.store_user_profile(item, user_id=user_id, session_id=session_id)

    user_ids = df["user_id"].unique().tolist()
    for user_id in user_ids:
        print(user_id)
        ltm_data = m.ltm.memory.get_all(user_id=user_id)
        stm_data = m.stm.memory.get_all(user_id=user_id)

        combined = {
            "user_id": user_id,
            "LTM": ltm_data,
            "STM": stm_data
        }

        file_out = f"D:\9D Tech Work\Wardrobe-POC\POC-4\Wordrobe-AI\src\experiments\conversations\\user_based\\{user_id}_conversation.json"
        with open(file_out, "w") as f:
            json.dump(combined, f, indent=2)

        print(f"Exported conversation for {user_id} → {file_out}")