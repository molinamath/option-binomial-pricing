from dataclasses import dataclass
from typing import Literal
import numpy as np

from option_binomial_pricing.Entities.Portfolio import Portfolio
from option_binomial_pricing.Entities.RiskFreeRate import RiskFreeRate
from option_binomial_pricing.Entities.stock import Stock


@dataclass
class Node:
    portfolio: Portfolio
    previous: "Node | None" = None
    up: "Node | None" = None
    down: "Node | None" = None
    p : float = 0 # probability of up move
    stepSize: float = 0 # stepSize in years
    optionPrice: float | None = None # option price at this node calculated based on a risk free valuation of either up and down
    
    @staticmethod
    def CreateFirstNode(portfolio: Portfolio, stepSize: float, bump: float) -> "Node":
        node = Node(portfolio, stepSize=stepSize)
        node.portfolio = portfolio
        node.stepSize = stepSize
        node.p = node.GetUpProbability(RiskFreeRate.GetRate(), bump) # we assume a bump of 10% for the first node
        return node
    
    def CreateFromNode(self, previous: "Node", bump: float, direction: Literal["up", "down"]) -> None:
        self.previous = previous
        self.stepSize = previous.stepSize # we assume that the time for next iteration is the same for all nodes
        multiplier = 1 + bump if direction == "up" else 1 - bump
        stock = Stock(previous.portfolio.stock.price * multiplier)
        self.portfolio = Portfolio(
            previous.portfolio.option,
            previous.portfolio.optionDirection,
            stock,
            previous.portfolio.stockDirection,
            previous.portfolio.delta,
        )
        self.p = self.GetUpProbability(RiskFreeRate.GetRate(), bump)

    def CreateChild(self, bump: float, direction: Literal["up", "down"]) -> "Node":
        child = Node(self.portfolio, stepSize=self.stepSize)
        child.CreateFromNode(self, bump, direction)
        return child
        
    def CalculateDelta(self) -> float:
        return self.portfolio.SetDelta(self.up.portfolio, self.down.portfolio)
    
    def GetUpProbability(self, riskFreeRate: float, bump: float) -> float:
        riskFreeReturn = np.exp(riskFreeRate * self.stepSize)
        return (riskFreeReturn - (1 - bump)) / ((1 + bump) - (1 - bump))
    
    def GetOptionPriceOnNode(self) -> float:
        ## in case it has already been computed by the recursive walk through the tree
        if self.optionPrice is not None:
            return self.optionPrice

        if self.up is None or self.down is None:
            self.optionPrice = self.portfolio.option.OptionPrice(self.portfolio.stock.price)
            return self.optionPrice
        
        upPrice = self.up.GetOptionPriceOnNode();
        downPrice = self.down.GetOptionPriceOnNode();
        discountFactor = np.exp(-RiskFreeRate.GetRate() * self.stepSize)
        self.optionPrice = discountFactor * (self.p * upPrice + (1 - self.p) * downPrice)
        return self.optionPrice
        
