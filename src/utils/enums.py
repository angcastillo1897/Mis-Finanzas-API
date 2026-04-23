from enum import Enum


class AccountTypeEnum(str, Enum):
    """Tipos de cuentas."""
    CASH = "efectivo"
    BANK = "banco"
    DIGITAL = "digital"


class TransactionTypeEnum(str, Enum):
    """Tipos de movimientos (ingreso o gasto)."""
    INCOME = "ingreso"
    EXPENSE = "gasto"


class DebtTypeEnum(str, Enum):
    """Tipo de deuda: debo o me deben."""
    I_OWE = "yo_debo"
    THEY_OWE_ME = "el_me_debe"


class DebtStatusEnum(str, Enum):
    """Estado de la deuda."""
    PENDING = "pendiente"
    PAID = "pagada"
