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

    def CalculateDelta(up: "Portfolio", down: "Portfolio") -> float:
        return (up.option.OptionPrice(up.stock.price) - down.option.OptionPrice(down.stock.price)) / (up.stock.price - down.stock.price)
    
    def SetDelta(self, up: "Portfolio", down: "Portfolio") -> float:
        if(up is None or down is None):
            return 0
        self.delta = Portfolio.CalculateDelta(up, down)
        return self.delta

Portolio = Portfolio
