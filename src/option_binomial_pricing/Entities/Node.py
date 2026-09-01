from dataclasses import dataclass
from typing import Literal

from option_binomial_pricing.Entities import Option, Portfolio, Stock
from option_binomial_pricing.Entities.types import Direction


@dataclass
class Node:
    portfolio: Portfolio
    previous: "Node | None" = None
    up: "Node | None" = None
    down: "Node | None" = None
    
    def CreateFromNode(self, previous: "Node| None", bump, direction: Literal["up","down"]):
        self.previous = previous;
        multiplier = 1+ bump if direction == "up" else 1 - bump;
        self.portfolio = Portfolio(previous.portfolio.option, previous.portfolio.optionDirection, previous.portfolio.stock * multiplier, previous.portfolio.stockDirection, previous.portfolio.delta)