from src.memory.base_memory import BaseMemory
from typing import Optional, Dict, Any, List
from src.configs.configs import LTM_CONFIG
from src.prompts.prompts import UPDATE_MEMORY_PROMPT
from mem0 import Memory
from google import genai
from google.genai import types
import json
from src.models.feedback_schema import AllBlocks
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

    def delete(self, memory_id: str) -> bool:
        """Delete specific long-term memory"""
        try:
            self.memory.delete(memory_id=memory_id)
            logger.info(f"Deleted LTM {memory_id} for user")
            return True
        except Exception as e:
            logger.error(f"Failed to delete LTM: {e}")
            return False

    def update(self, memory_id: str, user_id: str, data: str) -> bool:
        """Delete specific long-term memory"""
        try:
            self.memory.update(memory_id=memory_id, user_id=user_id, data=data)
            logger.info(f"Updated LTM {memory_id} for user {user_id}")
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
            preferences = self.retrieve("fashion preferences style", user_id)
            return {
                "style_preferences": preferences,
                "total_memories": len(preferences)
            }
        except Exception as e:
            logger.error(f"Failed to get user preferences: {e}")
            return {"style_preferences": [], "total_memories": 0}

    def apply_feedback(self, user_feedback: str, user_id: str, model: str = "gemini-2.5-flash") -> bool:
            """
            Given a user feedback string (e.g. "I preferred slim-fit jeans"),
            compare that with existing memory by calling Gemini + UPDATE_MEMORY_PROMPT,
            get structured instructions, and apply them to Mem0.
            """
            try:
                existing_memories = self.memory.get_all(user_id=user_id)
                print(existing_memories)
                formatted_memory = []
                for idx, mem in enumerate(existing_memories["results"]):
                    mem_id = str(mem.get("id", idx))
                    mem_text = mem.get("memory", None)
                    formatted_memory.append({"id": mem_id, "text": mem_text})

                prompt_text = f"""{UPDATE_MEMORY_PROMPT}
                Old Memory:
                {formatted_memory}
                            
                User Feedback:
                ["{user_feedback}"]
                """

                # Step 3: call Gemini
                client = genai.Client()
                response = client.models.generate_content(
                    model=model,
                    contents=prompt_text,
                    config = {
                    "response_mime_type": "application/json",
                    "response_schema": AllBlocks,
                    }
                )
                gemini_output = response.text
                logger.info(f"Gemini response for memory update: {gemini_output}")

                # Step 4: parse JSON output
                feedback_json = json.loads(gemini_output)

                # Step 5: apply operations
                for item in feedback_json.get("memory", []):
                    print(item)
                    event = item.get("event")
                    memory_id = item.get("id")
                    text = item.get("text")

                    if event == "ADD":
                        self.store({"content": text}, user_id)
                        logger.info(f"ADD → {text}")

                    elif event == "UPDATE":
                        self.update(memory_id, user_id, text)
                        logger.info(f"UPDATE → {text} (old id {memory_id})")

                    elif event == "DELETE":
                        self.delete(memory_id)
                        logger.info(f"DELETE → Removed memory {memory_id}")

                    elif event == "NONE":
                        logger.info(f"NONE → No change for memory {memory_id}")

                    else:
                        logger.warning(f"Unknown event type: {event}")

                return True

            except Exception as e:
                logger.error(f"apply_feedback failed: {e}")
                return False

    def session_lived_store(self, data: Dict[str, Any], user_id: str, session_id: str) -> bool:
        logger.warning("Session-lived storage not supported in LongTermMemory")
        return False

    def session_lived_retrieve(self, query: str, user_id: str, session_id: str) -> List[Dict[str, Any]]:
        logger.warning("Session-lived retrieval not supported in LongTermMemory")
        return []

    def session_lived_delete(self, user_id: str, session_id: str) -> bool:
        logger.warning("Session-lived deletion not supported in LongTermMemory")
        return False

