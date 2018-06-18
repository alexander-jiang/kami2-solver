import heapq

# Priority queue supports uniform cost search (to efficiently pick the next
# element from the frontier).
class PriorityQueue:
    def  __init__(self):
        self.REMOVED = -100000
        self.heap = []
        self.priorities = {}  # Map from state to priority

    # Insert state into heap (with the given priority) if state isn't in the
    # heap or if new priority < existing priority.
    # Return whether the priority queue was updated.
    def update(self, state, new_priority):
        old_priority = self.priorities.get(state)
        if old_priority == None or new_priority < old_priority:
            self.priorities[state] = new_priority
            heapq.heappush(self.heap, (new_priority, state))
            return True
        return False

    # Returns a pair: (state with minimum priority, priority)
    # or (None, None) if the priority queue is empty.
    def remove_min(self):
        while len(self.heap) > 0:
            priority, state = heapq.heappop(self.heap)
            if self.priorities[state] == self.REMOVED:
                # State was previously removed, skip
                continue
            self.priorities[state] = self.REMOVED
            return (state, priority)
        return (None, None) # Nothing left in the heap

    def empty(self):
        return len(self.heap) == 0
