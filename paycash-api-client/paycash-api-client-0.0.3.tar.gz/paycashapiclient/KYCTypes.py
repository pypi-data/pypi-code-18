from enum import Enum


class KYCTypes(Enum):
    PASSPORT = "PASSPORT"
    BILLING_ADDRESS = "BILLING_ADDRESS"
    DRIVING_LICENSE = "DRIVING_LICENSE"
    LEGAL_ENTITY_IDENTIFIER = "LEGAL_ENTITY_IDENTIFIER"
    CARD_ID = "CARD_ID"
    PERSONAL_IDENTITY = "PERSONAL_IDENTITY"
