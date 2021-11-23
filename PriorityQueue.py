import heapq
import itertools

class PriorityQueue:
    REMOVED = '<removed-node>'
    counter = itertools.count(0, -1)

    def __init__(self):
        self.heap = []
        self.finder = {}
        pass

    def push(self, item, priority):
        if item in self.finder:
            self.removeItem(item)
        count = next(self.counter)
        entry = [priority, count, item]
        self.finder[item] = entry
        heapq.heappush(self.heap, entry)
        pass

    def pop(self):
        while not self.isEmpty():
            priority, count, item = heapq.heappop(self.heap)
            if item is not self.REMOVED:
                del self.finder[item]
                return item
        raise RuntimeError("Empty queue cannot be popped")

    def removeItem(self, item):
        entry = self.finder[item]
        entry[-1] = self.REMOVED

    def isEmpty(self):
        if self.heap:
            return False
        else:
            return True