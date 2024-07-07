from enum import Enum

class TransactionTypeEnum(str, Enum):
     IN = "IN"
     OUT = "OUT"

class OrderStatusEnum(str, Enum):
     PENDING = "PENDING"
     APPROVED = "APPROVED"
     SHIPPED = "SHIPPED"
     CANCEL = "CANCEL"

class PaymentTypeEnum(str, Enum):
     STRIPE = "STRIPE"
     PAYPAL = "PAYPAL"
     GOPAYFAST = "GOPAYFAST"