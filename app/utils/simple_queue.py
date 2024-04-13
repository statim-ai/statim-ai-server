"""Module for the SimpleQueue class."""

import queue

from utils.simple_logger import SimpleLogger


class SimpleQueue:
    """Singleton class that provides an interface to interact with a queue (FIFO)."""

    _instance = None
    queue = queue.Queue()

    def __new__(cls, *args, **kwargs):
        """Construtor that implements the Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.logger = SimpleLogger()
        return cls._instance

    def is_empty(self):
        """Returns True if the queue if empty, Fals otherwise."""
        self.logger.debug("[SimpleQueue] is_empty")
        return self.queue.empty()

    def enqueue(self, item):
        """Add an item to the queue."""
        self.logger.debug("[SimpleQueue] enqueue")
        self.queue.put(item)

    def dequeue(self):
        """Removes and returns a item from the queue."""
        self.logger.debug("[SimpleQueue] waiting on dequeue")
        return self.queue.get(block=True)

    def size(self):
        """Return the size of the queue."""
        self.logger.debug("[SimpleQueue] size")
        return self.queue.qsize()
