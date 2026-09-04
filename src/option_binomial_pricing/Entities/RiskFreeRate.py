from typing import ClassVar


class RiskFreeRate:
    rate: ClassVar[float] = 0

    @classmethod
    def SetRate(cls, rate: float) -> None:
        cls.rate = rate

    @classmethod
    def GetRate(cls) -> float:
        return cls.rate

    @classmethod
    def DiscountFactor(cls, time: float = 1) -> float:
        return 1 / ((1 + cls.rate) ** time)

    @classmethod
    def Discount(cls, value: float, time: float = 1) -> float:
        return value * cls.DiscountFactor(time)
