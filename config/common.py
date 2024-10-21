import enum

class PriorityEnum(str, enum.Enum):
    low = "low"
    high = "high"

class StatusEnum(str, enum.Enum):
    inprogress = "inprogress"
    completed = "completed"
    pending = "pending"
