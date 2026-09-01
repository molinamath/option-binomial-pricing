from dataclasses import dataclass

from option_binomial_pricing.Entities.types import OptionType


@dataclass
class Option:
    strike: float
    type: OptionType

    def ShouldExert(self, stockPrice: float) -> bool:
        if self.type == "put":
            return stockPrice < self.strike

        return stockPrice > self.strike
    
    def OptionPrice(self, stockPrice: float) -> float:
        if not self.ShouldExert(stockPrice):
            return 0

        return abs(self.strike - stockPrice)


Optiton = Option
