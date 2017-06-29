from enum import Enum


class AccountAssetTypes(Enum):
    PRINCIPAL = "PRINCIPAL"
    PROVISIONING = "PROVISIONING"
    RISK = "RISK"
    GUARANTEED = "GUARANTEED"
