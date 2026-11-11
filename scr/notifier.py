import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class Notifier(ABC):
    @abstractmethod
    def send(selfself, message: str) -> bool:
        ...

class EmailNotifier(Notifier):
    def __init__(self):
        self.sent_message = []

    def send(self, message: str) -> bool:
        logger.info(f"[EMAIL] Отправлено: {message}")
        self.sent_message.append(message)
        return True