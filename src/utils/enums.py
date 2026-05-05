from enum import Enum


class AccountTypeEnum(str, Enum):
    """Tipos de cuentas."""
    CASH = "CASH"
    BANK = "BANK"
    DIGITAL = "DIGITAL"


class TransactionTypeEnum(str, Enum):
    """Tipos de movimientos (ingreso o gasto)."""
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"


class DebtTypeEnum(str, Enum):
    """Tipo de deuda: debo o me deben."""
    I_OWE = "I_OWE"
    THEY_OWE_ME = "THEY_OWE_ME"


class DebtStatusEnum(str, Enum):
    """Estado de la deuda."""
    PENDING = "PENDING"
    PAID = "PAID"
