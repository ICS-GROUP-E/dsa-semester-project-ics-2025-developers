from datetime import datetime
from typing import Optional, Tuple, List, Dict, Union

class ActivityNode:
    """
    Node for storing activity information in the stack.
    Attributes:
        action: Type of action performed (e.g., "ADD", "DELETE")
        details: Additional information about the action
        timestamp: When the action occurred
        next: Reference to the next node
    """
    def __init__(self, action: str, details: str):
        self.action = action
        self.details = details
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.next: Optional[ActivityNode] = None

class ActivityStack:
    """
    Stack implementation for tracking library activities.
    Features:
        - Maximum size of 10 activities
        - LIFO (Last In First Out) operation
        - Automatic removal of oldest activity when full
    """
    def __init__(self):
        self.top: Optional[ActivityNode] = None
        self.size: int = 0
        self.max_size: int = 10

    def push(self, action: str, details: str) -> str:
        """Add a new activity to the stack."""
        new_node = ActivityNode(action, details)
        new_node.next = self.top
        self.top = new_node
        self.size += 1
        if self.size > self.max_size:
            self._remove_last()
        return f"Logged: {action}"

    def pop(self) -> Optional[Tuple[str, str, str]]:
        """Remove and return the most recent activity."""
        if not self.top:
            return None
        popped = self.top
        self.top = self.top.next
        self.size -= 1
        return (popped.action, popped.details, popped.timestamp)

    def peek(self) -> Optional[Tuple[str, str]]:
        """View the most recent activity without removing it."""
        return (self.top.action, self.top.details) if self.top else None

    def _remove_last(self) -> None:
        """Remove the oldest activity when stack is full."""
        if not self.top or not self.top.next:
            return
        current = self.top
        while current.next and current.next.next:
            current = current.next
        current.next = None
        self.size -= 1

    def get_all_actions(self) -> List[Dict[str, str]]:
        """Return list of all activities in the stack."""
        actions = []
        current = self.top
        while current:
            actions.append({
                "action": current.action,
                "details": current.details,
                "timestamp": current.timestamp
            })
            current = current.next
        return actions

    def clear_stack(self) -> None:
        """Remove all activities from the stack."""
        self.top = None
        self.size = 0
