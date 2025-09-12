from src.memory.base_memory import BaseMemory
from typing import Optional, Dict, Any, List
from src.configs.configs import LTM_CONFIG
from mem0 import Memory
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _default_config() -> Dict[str, Any]:
    """Default configuration for LTM"""
    return LTM_CONFIG


class LongTermMemory(BaseMemory):
    """
    Long Term Memory for storing user preferences, style history,
    and persistent fashion choices
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Long Term Memory

        Args:
            config: Configuration dictionary for Mem0
        """
        self.config = config or _default_config()
        self.memory = Memory.from_config(self.config)
        self.memory_type = "long_term"
        logger.info("Long Term Memory initialized")

    def store(self, data: Dict[str, Any], user_id: str) -> bool:
        """
        Store long-term fashion preferences and history

        Args:
            data: Information to store (preferences, style history, etc.)
            user_id: Unique user identifier

        Returns:
            bool: Success status
        """
        try:
            # Add metadata for LTM classification
            enriched_data = {
                **data,
                "memory_type": self.memory_type,
                "category": data.get("category", "general_preference")
            }

            self.memory.add(
                messages=[enriched_data],
                user_id=user_id
            )

            logger.info(f"Stored LTM for user {user_id}: {data.get('category', 'general')}")
            return True

        except Exception as e:
            logger.error(f"Failed to store LTM: {e}")
            return False

    def retrieve(self, query: str, user_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant long-term memories

        Args:
            query: Search query
            user_id: User identifier
            limit: Maximum number of memories to retrieve

        Returns:
            List of relevant memories
        """
        try:
            memories = self.memory.search(
                query=query,
                user_id=user_id,
                limit=limit
            )

            logger.info(f"Retrieved {len(memories)} LTM entries for user {user_id}")
            return memories

        except Exception as e:
            logger.error(f"Failed to retrieve LTM: {e}")
            return []

    def delete(self, memory_id: str, user_id: str) -> bool:
        """Delete specific long-term memory"""
        try:
            self.memory.delete(memory_id=memory_id, user_id=user_id)
            logger.info(f"Deleted LTM {memory_id} for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete LTM: {e}")
            return False

    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """
        Get consolidated user fashion preferences

        Returns:
            Dictionary of user preferences
        """
        try:
            preferences = self.retrieve("fashion preferences style", user_id, limit=10)
            return {
                "style_preferences": preferences,
                "total_memories": len(preferences)
            }
        except Exception as e:
            logger.error(f"Failed to get user preferences: {e}")
            return {"style_preferences": [], "total_memories": 0}
