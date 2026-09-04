from option_binomial_pricing.Entities import Node, Option, Portfolio, RiskFreeRate, Stock


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

    root.GetOptionPriceOnNode()

    return root


def FormatNode(node: Node) -> str:
    stockPrice = node.portfolio.stock.price
    delta = node.portfolio.delta
    optionPrice = node.GetOptionPriceOnNode()
    nodeP = node.p

    return f"S={stockPrice:.2f}, delta={delta:.4f}, optionPrice={optionPrice:.4f}, p={nodeP:.4f}"


def PrintTree(node: Node) -> None:
    PrintTreeNode(node, "", "root", True)


def PrintTreeNode(node: Node, prefix: str, branchName: str, isLast: bool) -> None:
    connector = "" if branchName == "root" else "`-- " if isLast else "|-- "
    print(f"{prefix}{connector}{branchName}: {FormatNode(node)}")

    childPrefix = prefix if branchName == "root" else prefix + ("    " if isLast else "|   ")
    children = [
        ("up", node.up),
        ("down", node.down),
    ]
    children = [(name, child) for name, child in children if child is not None]

    for index, (name, child) in enumerate(children):
        isLastChild = index == len(children) - 1

        PrintTreeNode(child, childPrefix, name, isLastChild)


def main() -> None:
    ## Fast testing
    treeDepth = 1
    riskFreeRate = 0.12
    maturity = 6
    strike = 21
    stockPrice = 20
    bump = 0.1
    optionType = "call"
    optionDirection = "sell"
    stockDirection = "buy"
    
    treeDepth = int(input("Enter the depth of the tree: "))
    # riskFreeRate = float(input("Enter the risk-free rate: "))
    # strike = float(input("Enter the strike price: "))
    # stockPrice = float(input("Enter the stock price: "))
    # bump = float(input("Enter the bump: "))
    # optionType = input("Enter the option type (call/put): ")
    # optionDirection = input("Enter the option direction (buy/sell): ")
    # maturity = float(input("Enter the maturity in months: "))
    # stockDirection = input("Enter the stock direction (buy/sell): ")
    

    stepInTime = 0.25

    RiskFreeRate.SetRate(riskFreeRate)
    stock = Stock(stockPrice)
    option = Option(strike, optionType)
    portfolio = Portfolio(option, optionDirection, stock, stockDirection)
    root = Node.CreateFirstNode(portfolio, stepInTime, bump)
    tree = BuildTree(root, treeDepth, bump)
    PrintTree(tree)
