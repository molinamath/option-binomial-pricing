from dataclasses import dataclass, field

from option_binomial_pricing.Entities.Option import Option
from option_binomial_pricing.Entities.stock import Stock
from option_binomial_pricing.Entities.types import Direction


@dataclass
class Portfolio:
    option: Option
    optionDirection: Direction
    stock: Stock
    stockDirection: Direction
    delta: float = field(default=0)

    def __post_init__(self):
        self.delta = abs(self.delta)

    def PortfolioValue(self) -> float:
        stockMultiplier = 1 if self.stockDirection == "buy" else -1
        optionMultiplier = 1 if self.optionDirection == "buy" else -1
        
        return stockMultiplier * self.stock.price * self.delta - optionMultiplier * self.option.OptionPrice(self.stock.price)


Portolio = Portfolio
