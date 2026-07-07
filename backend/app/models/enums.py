# app/models/enums.py

from enum import Enum


class AccountType(str, Enum):
    NGO = "NGO"
    DONOR = "DONOR"


class ListingCondition(str, Enum):
    EXCELLENT = "EXCELLENT"
    GOOD = "GOOD"
    DECENT = "DECENT"
    BAD = "BAD"


class ListingStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    TAKEN = "TAKEN"
    REMOVED = "REMOVED"


class VerificationStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class NeedStatus(str, Enum):
    PENDING = "PENDING"
    RECEIVED = "RECEIVED"
    CLOSED = "CLOSED"


class ClaimStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    COMPLETED = "COMPLETED"


class NotificationType(str, Enum):
    DONATION = "DONATION"
    CLAIM = "CLAIM"
    MESSAGE = "MESSAGE"
    LISTING = "LISTING"
    SYSTEM = "SYSTEM"


class PickupStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"