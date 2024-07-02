from enum import Enum

class OrderStatusEnum(str, Enum):
    pending = "pending"
    approved = "approved"
    in_progress = "in_progress"
    delivered = "delivered"
    rejected = "rejected"
