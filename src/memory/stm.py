from typing import Dict, List, Any, Optional
from src.memory.base_memory import BaseMemory
from src.configs.configs import STM_CONFIG
import logging
from mem0 import Memory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _default_config() -> Dict[str, Any]:
    """Default configuration for STM"""
    return STM_CONFIG


class ShortTermMemory(BaseMemory):
    """
    Short Term Memory for current conversation context,
    recent interactions, and session-based information
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Short Term Memory

        Args:
            config: Configuration dictionary for Mem0
        """
        self.config = config or _default_config()
        self.memory = Memory.from_config(self.config)
        self.memory_type = "short_term"
        logger.info("Short Term Memory initialized")

    def session_lived_store(self, data: Dict[str, Any], user_id: str, session_id: str) -> bool:
        """
        Store short-term conversation context

        Args:
            data: Conversation context, recent interactions
            user_id: Unique user identifier
            session_id: Unique session identifier

        Returns:
            bool: Success status
        """
        try:
            # Add metadata for STM classification
            enriched_data = {
                **data,
                "memory_type": self.memory_type,
                "context_type": data.get("context_type", "conversation")
            }

            self.memory.add(
                messages=[enriched_data],
                run_id=session_id,
                user_id=user_id
            )

            logger.info(f"Stored STM for user {user_id} -> within a session {session_id}: {data.get('context_type', 'conversation')}")
            return True

        except Exception as e:
            logger.error(f"Failed to store STM: {e}")
            return False

    def session_lived_retrieve(self, query: str, user_id: str, session_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant short-term memories

        Args:
            query: Search query
            user_id: User identifier
            session_id: Unique session identifier
            limit: Maximum number of memories to retrieve

        Returns:
            List of relevant memories
        """
        try:
            memories = self.memory.search(
                query=query,
                user_id=user_id,
                run_id=session_id,
                limit=limit
            )

            logger.info(f"Retrieved {len(memories)} STM entries for user {user_id}")
            return memories

        except Exception as e:
            logger.error(f"Failed to retrieve STM: {e}")
            return []

    def session_lived_delete(self,  user_id: str, session_id:str) -> bool:
        """Delete specific short-term memory"""
        try:
            self.memory.delete_all(run_id = session_id, user_id=user_id)
            logger.info(f"Deleted STM {session_id} for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete STM: {e}")
            return False

    def delete(self, memory_id: str) -> bool:
        """Delete specific short-term memory"""
        try:
            self.memory.delete(memory_id=memory_id)
            logger.info(f"Deleted STM {memory_id} for user")
            return True
        except Exception as e:
            logger.error(f"Failed to delete STM: {e}")
            return False

    def get_recent_context(self, query: str, user_id: str, session_id: str, limit: int = 5) -> Dict[str, Any]:
        """
        Get recent conversation context

        Returns:
            Dictionary of recent context
        """
        try:
            recent_context = self.session_lived_retrieve(query, user_id, session_id, limit=limit)
            return {
                "recent_interactions": recent_context,
                "context_count": len(recent_context)
            }
        except Exception as e:
            logger.error(f"Failed to get recent context: {e}")
            return {"recent_interactions": [], "context_count": 0}

    # ---- Long-term stubs (not used here) ----
    def store(self, data: Dict[str, Any], user_id: str) -> bool:
        logger.warning("Long-term store not supported in ShortTermMemory")
        return False

    def retrieve(self, query: str, user_id: str) -> List[Dict[str, Any]]:
        logger.warning("Long-term retrieve not supported in ShortTermMemory")
        return []
