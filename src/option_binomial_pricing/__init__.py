from option_binomial_pricing.Entities import Node, Option, Portfolio, Stock


def BuildTree(root: Node, treeDepth: int, bump: float) -> Node:
    currentLevel = [root]
    currentDepth = 0

    while currentDepth < treeDepth:
        nextLevel = []

        for node in currentLevel:
            node.up = node.CreateChild(bump, "up")
            node.down = node.CreateChild(bump, "down")
            node.CalculateDelta()
            nextLevel.append(node.up)
            nextLevel.append(node.down)

        currentLevel = nextLevel
        currentDepth += 1

    return root


def main() -> None:
    treeDepth = int(input("Enter the depth of the tree: "))
    strike = float(input("Enter the strike price: "))
    stockPrice = float(input("Enter the stock price: "))
    bump = float(input("Enter the bump: "))
    optionType = input("Enter the option type (call/put): ")
    optionDirection = input("Enter the option direction (buy/sell): ")
    stockDirection = input("Enter the stock direction (buy/sell): ")
    
    ## Fast testing
    # treeDepth = int(input("Enter the depth of the tree: "))
    # strike = 21
    # stockPrice = 20
    # bump = 0.1
    # optionType = "call"
    # optionDirection = "sell"
    # stockDirection = "buy"

    stock = Stock(stockPrice)
    option = Option(strike, optionType)
    portfolio = Portfolio(option, optionDirection, stock, stockDirection)
    root = Node(portfolio)
    tree = BuildTree(root, treeDepth, bump)
    print(tree)
