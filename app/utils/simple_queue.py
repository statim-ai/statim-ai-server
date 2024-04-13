import queue

from utils.simple_logger import SimpleLogger


class SimpleQueue:
    _instance = None
    queue = queue.Queue()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.logger = SimpleLogger()
        return cls._instance

    def is_empty(self):
        self.logger.debug("[SimpleQueue] is_empty")
        return self.queue.empty()

    def enqueue(self, item):
        self.logger.debug("[SimpleQueue] enqueue")
        self.queue.put(item)

    def dequeue(self):
        self.logger.debug("[SimpleQueue] waiting on dequeue")
        return self.queue.get(block=True)

    def size(self):
        self.logger.debug("[SimpleQueue] size")
        return self.queue.qsize()
