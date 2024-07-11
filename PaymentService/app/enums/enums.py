from enum import Enum

class TransactionTypeEnum(str, Enum):
     IN = "IN"
     OUT = "OUT"



class PaymentTypeEnum(str, Enum):
     STRIPE = "STRIPE"
     PAYPAL = "PAYPAL"
     GOPAYFAST = "GOPAYFAST"
     COD = "COD"

class PaymentStatusEnum(str, Enum):
     APPROVED = "APPROVED"
     FAILED = "FAILED"
     PENDING = "PENDING"
