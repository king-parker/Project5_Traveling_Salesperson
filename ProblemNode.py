from math import inf
from copy import copy, deepcopy


class ProblemNode:
    cities = None
    ncities = None
    costMatrix = None
    bound = None
    tour = None
    depth = None

    def __init__(self):
        pass

    @classmethod
    def parentNode(cls, scenario, startCity = 0):
        node = cls.__new__(cls)
        node.cities = scenario.getCities()
        node.ncities = len(node.cities)
        node.costMatrix = node.createCostMatrix()
        node.bound = 0
        node.tour = [startCity]
        node.reduceCostMaxtrix()
        node.depth = 0
        return node

    @classmethod
    def fromParent(cls, parent, nextCity):
        node = cls.__new__(cls)
        node.cities = parent.getCities()
        node.ncities = len(node.cities)
        node.costMatrix = deepcopy(parent.getCostMatrix())
        node.bound = copy(parent.getBound())
        node.tour = copy(parent.getTour())
        node.depth = copy(parent.getDepth())
        node.processState(nextCity)
        return node
        pass

    def processState(self, nextCity):
        prevCity = self.tour[-1]
        self.tour.append(nextCity)
        self.bound += self.costMatrix[prevCity][nextCity]
        for i in range(self.ncities):
            self.costMatrix[prevCity][i] = inf
            self.costMatrix[i][nextCity] = inf
        self.costMatrix[nextCity][prevCity] = inf
        self.reduceCostMaxtrix()
        self.depth += 1
        pass

    def reduceCostMaxtrix(self):
        for row in range(self.ncities):
            minCost = inf
            for col in range(self.ncities):
                checkCost = self.costMatrix[row][col]
                if checkCost < minCost:
                    minCost = checkCost
                pass
            if minCost < inf:
                for col in range(self.ncities):
                    self.costMatrix[row][col] -= minCost
                    pass
                self.bound += minCost
            pass

        for col in range(self.ncities):
            minCost = inf
            for row in range(self.ncities):
                checkCost = self.costMatrix[row][col]
                if checkCost < minCost:
                    minCost = checkCost
                pass
            if minCost < inf:
                for row in range(self.ncities):
                    self.costMatrix[row][col] -= minCost
                    pass
                self.bound += minCost
            pass
        pass

    def createCostMatrix(self):
        costMatrix = []
        for row in range(self.ncities):
            costMatrix.append([])
            for col in range(self.ncities):
                costMatrix[row].append(self.cities[row].costTo(self.cities[col]))
        return costMatrix

    def getCities(self):
        return self.cities

    def getCostMatrix(self):
        return self.costMatrix

    def getBound(self):
        return self.bound

    def getTour(self):
        return self.tour

    def getRoute(self):
        return [self.cities[i] for i in self.tour]

    def getDepth(self):
        return self.depth

    def toString_costMatrix(self):
        delimeter = '\t'
        newLine = '\n'
        rows = []
        for row in range(self.ncities):
            elements = []
            for col in range(self.ncities):
                elements.append(str(self.costMatrix[row][col]))
            rows.append(delimeter.join(elements))
        return newLine.join(rows)

    def toString_bound(self):
        return str(self.bound)

    def toString_tour(self):
        delimeter = ', '
        cities = []
        for i in range(len(self.tour)):
            city = self.cities[self.tour[i]]._name
            cities.append(city)
        return delimeter.join(cities)

    def toString_state(self):
        result = []
        result.append('Cost Matrix:')
        result.append(self.toString_costMatrix())
        result.append('Bound: ' + self.toString_bound())
        result.append('Tour: ' + self.toString_tour())
        result.append('Depth: ' + str(self.depth))
        result.append('')
        return '\n'.join(result)