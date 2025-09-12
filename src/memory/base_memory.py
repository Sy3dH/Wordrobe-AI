from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import logging
from mem0 import Memory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseMemory(ABC):
    """Abstract base class for memory operations"""

    @abstractmethod
    def store(self, data: Dict[str, Any], user_id: str) -> bool:
        """Store information in memory"""
        pass

    @abstractmethod
    def session_lived_store(self, data: Dict[str, Any], user_id: str, session_id:str) -> bool:
        """Store information in memory"""
        pass

    @abstractmethod
    def retrieve(self, query: str, user_id: str) -> List[Dict[str, Any]]:
        """Retrieve information from memory"""
        pass

    @abstractmethod
    def session_lived_retrieve(self, query: str, user_id: str, session_id:str) -> List[Dict[str, Any]]:
        """Retrieve information from memory"""
        pass

    @abstractmethod
    def delete(self, memory_id: str, user_id: str) -> bool:
        """Delete specific memory"""
        pass

    @abstractmethod
    def session_lived_delete(self, user_id: str, session_id:str) -> bool:
        """Delete specific memory"""
        pass