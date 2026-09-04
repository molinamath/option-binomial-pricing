from dataclasses import dataclass
from typing import Literal

from option_binomial_pricing.Entities.Portfolio import Portfolio
from option_binomial_pricing.Entities.stock import Stock


@dataclass
class Node:
    portfolio: Portfolio
    previous: "Node | None" = None
    up: "Node | None" = None
    down: "Node | None" = None
    
    def CreateFromNode(self, previous: "Node", bump: float, direction: Literal["up", "down"]) -> None:
        self.previous = previous
        multiplier = 1 + bump if direction == "up" else 1 - bump
        stock = Stock(previous.portfolio.stock.price * multiplier)
        self.portfolio = Portfolio(
            previous.portfolio.option,
            previous.portfolio.optionDirection,
            stock,
            previous.portfolio.stockDirection,
            previous.portfolio.delta,
        )

    def CreateChild(self, bump: float, direction: Literal["up", "down"]) -> "Node":
        child = Node(self.portfolio)
        child.CreateFromNode(self, bump, direction)
        return child
        
    def CalculateDelta(self) -> float:
        return self.portfolio.SetDelta(self.up.portfolio, self.down.portfolio)
