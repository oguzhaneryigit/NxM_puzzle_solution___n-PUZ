import math

import numpy
import random


def swap(matrix, x1, y1, x2, y2):
    tempArray = []
    for i in range(len(matrix)):
        tempArray.append([])
        for j in range(len(matrix[i])):
            tempArray[i].append(matrix[i][j])
    try:
        temp = tempArray[x1][y1]
        tempArray[x1][y1] = tempArray[x2][y2]
        tempArray[x2][y2] = temp
        return tempArray
    except:
        print("Swap hatası")


def findZero(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                return (i, j)

    # normal şartlarda bura çalışmamalı
    print("0 bulunamadı")
    return (-1, -1)

def findElement(matrix,n):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == n:
                return (i, j)

    # normal şartlarda bura çalışmamalı
    print("0 bulunamadı")
    return (-1, -1)

def findPossibleMoves(matrix, previusMovement=""):
    x, y = findZero(matrix)
    liste = []
    if x != 0:
        liste.append("u")
    if x != len(matrix) - 1:
        liste.append("d")
    if y != 0:
        liste.append("l")
    if y != len(matrix[0]) - 1:
        liste.append("r")
    # print(liste)
    if previusMovement != "":
        if previusMovement == "l" and "r" in liste:
            liste.remove("r")

        if previusMovement == "r" and "l" in liste:
            liste.remove("l")

        if previusMovement == "u" and "d" in liste:
            liste.remove("d")

        if previusMovement == "d" and "u" in liste:
            liste.remove("u")
    return liste


def printMatrix(matrix):
    try:
        print("--------------- head of matrix")
        for i in range(len(matrix)):
            row = matrix[i]
            print(row)
        print("--------------- end of matrix\n")
    except:
        print("matris boş veya hata var")
        print("--------------- end of matrix\n")


def defineNxMmatrix(n, m):
    matrix = []  # define empty matrix
    numbers = list(range(n * m))
    random.shuffle(numbers)
    # print(numbers)
    k = 0
    for i in range(n):  # total row is 3
        row = []
        for j in range(m):  # total column is 3
            row.append(numbers[k])
            k += 1
        matrix.append(row)  # add fully defined column into the row
    # print(matrix)
    # printMatrix(matrix)
    return matrix
def defineMatrix(n):
    solvedMatrix= defineDestinationMatrix(n)
    for i in range(619):
        moves=findPossibleMoves(solvedMatrix)
        nextMove=random.choice(moves)
        zeroX,zeroY=findZero(solvedMatrix)
        if "l" ==nextMove:
            solvedMatrix = swap(solvedMatrix, zeroX,zeroY, zeroX, zeroY - 1)

        if "r" ==nextMove:
            solvedMatrix = swap(solvedMatrix, zeroX, zeroY,zeroX, zeroY + 1)

        if "u" ==nextMove:
            solvedMatrix = swap(solvedMatrix, zeroX, zeroY, zeroX - 1, zeroY)

        if "d" ==nextMove:
            solvedMatrix = swap(solvedMatrix, zeroX, zeroY, zeroX + 1, zeroY)

    return solvedMatrix
def defineDestinationMatrix(n):
    n = math.ceil(math.sqrt(n + 1))
    matrix = []  # define empty matrix
    numbers = list(range(n * n))
    k = 1
    for i in range(n):  # total row is 3
        row = []
        for j in range(n):  # total column is 3
            row.append(k)
            k += 1
        matrix.append(row)
    matrix[n-1][n-1]=0
    return matrix
def verifyMatrix(matrix):
    temp = 1
    for i in matrix:
        for j in i:
            if j == 0:
                continue
            if j == temp:
                temp += 1
            else:
                # print("matrix uygun değil")
                return False
    # birden fazla 0 var ise kontrol edelim
    if temp == len(matrix) * len(matrix[0]):
        print("matrix uygun")
        printMatrix(matrix)
        return True
    else:
        # normal şartlarda bura çalışmamalı
        print("matrix uygun değil")
        return False


class Node:
    def __init__(self, matrix,depth, prevMovement=""):
        self.matrix = matrix
        self.prevMovement = prevMovement
        self.moves = findPossibleMoves(matrix, prevMovement)
        self.zeroX, self.zeroY = findZero(matrix)
        self.left = None
        self.right = None
        self.upper = None
        self.down = None
        self.isValidGraph = verifyMatrix(self.matrix)
        self.depth =depth
        self.destMatrix = defineDestinationMatrix(len(matrix)*len(matrix)-1)
        self.cost= calculateHeuristic(matrix,self.destMatrix)
        self.astarcost=self.cost+self.depth


    def hasValidChild(self):

        if "l" in self.moves:
            if self.left.isValidGraph:
                return self.left

        if "r" in self.moves:
            if self.right.isValidGraph:
                return self.right

        if "u" in self.moves:
            if self.upper.isValidGraph:
                return self.upper

        if "d" in self.moves:
            if self.down.isValidGraph:
                return self.down
        return None

    def addChildren(self):
        tempNodeList = []
        if "l" in self.moves:
            self.left = Node(swap(self.matrix, self.zeroX, self.zeroY, self.zeroX, self.zeroY - 1), self.depth+1,"l")
            tempNodeList.append(self.left)

        if "r" in self.moves:
            self.right = Node(swap(self.matrix, self.zeroX, self.zeroY, self.zeroX, self.zeroY + 1),self.depth+1, "r")
            tempNodeList.append(self.right)

        if "u" in self.moves:
            self.upper = Node(swap(self.matrix, self.zeroX, self.zeroY, self.zeroX - 1, self.zeroY), self.depth+1,"u")
            tempNodeList.append(self.upper)

        if "d" in self.moves:
            self.down = Node(swap(self.matrix, self.zeroX, self.zeroY, self.zeroX + 1, self.zeroY), self.depth+1,"d")
            tempNodeList.append(self.down)

        return tempNodeList

    def printAllNodes(self):
        print("kendisi")
        printMatrix(self.matrix)
        if "l" in self.moves:
            print("left")
            printMatrix(self.left.matrix)

        if "r" in self.moves:
            print("right")
            printMatrix(self.right.matrix)

        if "u" in self.moves:
            print("up")
            printMatrix(self.upper.matrix)

        if "d" in self.moves:
            print("down")
            printMatrix(self.down.matrix)





def bfsWithAdder(root):
    queue = []
    queue.append(root)
    counter = 0
    while (len(queue) > 0):
        indexNode = queue.pop(0)
        printMatrix(indexNode.matrix)
        print(indexNode.moves)
        counter += 1
        print(counter)
        children = indexNode.addChildren()
        if type(indexNode.hasValidChild()) == Node:
            print(f"SONUÇ {counter}. ADIMDA BULUNDU")
            printMatrix(indexNode.hasValidChild().matrix)
            break
        queue.extend(children)

def greedyBestSearch(root):
    sortedQueue=[]
    sortedQueue.append(root)
    counter = 0
    while (len(sortedQueue) > 0):
        indexNode = sortedQueue.pop(0)
        printMatrix(indexNode.matrix)
        print(indexNode.moves)
        counter += 1
        print(counter)
        children = indexNode.addChildren()
        if type(indexNode.hasValidChild()) == Node:
            print(f"SONUÇ {counter}. ADIMDA BULUNDU")
            printMatrix(indexNode.hasValidChild().matrix)
            break
        for i in range(len(children)):
            for j in range(len(children)):
                if children[i].cost<children[j].cost:
                    temp=children[i]
                    children[i]=children[j]
                    children[j]=temp

        if len(sortedQueue)==0:
            sortedQueue.extend(children)
        else:
            for i in range(len(children)):
                added=False
                for j in range(len(sortedQueue)):
                    if children[i].cost<sortedQueue[j].cost:
                        sortedQueue.insert(j,children[i])
                        added=True
                        break
                if added==False:
                    sortedQueue.append(children[i])

def uniformCostSearch(root):
    sortedQueue=[]
    sortedQueue.append(root)
    counter = 0
    while (len(sortedQueue) > 0):
        indexNode = sortedQueue.pop(0)
        printMatrix(indexNode.matrix)
        print(indexNode.moves)
        counter += 1
        print(counter)
        children = indexNode.addChildren()
        if type(indexNode.hasValidChild()) == Node:
            print(f"SONUÇ {counter}. ADIMDA BULUNDU")
            printMatrix(indexNode.hasValidChild().matrix)
            break
        for i in range(len(children)):
            for j in range(len(children)):
                if children[i].depth<children[j].depth:
                    temp=children[i]
                    children[i]=children[j]
                    children[j]=temp

        if len(sortedQueue)==0:
            sortedQueue.extend(children)
        else:
            for i in range(len(children)):
                added=False
                for j in range(len(sortedQueue)):
                    if children[i].depth<sortedQueue[j].depth:
                        sortedQueue.insert(j,children[i])
                        added=True
                        break
                if added==False:
                    sortedQueue.append(children[i])

def aStar(root):
    sortedQueue=[]
    sortedQueue.append(root)
    counter = 0
    while (len(sortedQueue) > 0):
        indexNode = sortedQueue.pop(0)
        printMatrix(indexNode.matrix)
        print(indexNode.moves)
        counter += 1
        print(counter)
        children = indexNode.addChildren()
        if type(indexNode.hasValidChild()) == Node:
            print(f"SONUÇ {counter}. ADIMDA BULUNDU")
            printMatrix(indexNode.hasValidChild().matrix)
            break
        for i in range(len(children)):
            for j in range(len(children)):
                if children[i].astarcost<children[j].astarcost:
                    temp=children[i]
                    children[i]=children[j]
                    children[j]=temp

        if len(sortedQueue)==0:
            sortedQueue.extend(children)
        else:
            for i in range(len(children)):
                added=False
                for j in range(len(sortedQueue)):
                    if children[i].astarcost<sortedQueue[j].astarcost:
                        sortedQueue.insert(j,children[i])
                        added=True
                        break
                if added==False:
                    sortedQueue.append(children[i])

def depthLimitedSearch(root,limit):
    stack=[]
    stack.append(root)
    counter = 0
    while (len(stack) > 0):
        indexNode = stack.pop()
        printMatrix(indexNode.matrix)
        print(indexNode.moves)
        counter += 1
        print(counter)
        children = indexNode.addChildren()
        if type(indexNode.hasValidChild()) == Node:
            print(f"SONUÇ {counter}. ADIMDA BULUNDU.  derinlik={indexNode.depth}")
            printMatrix(indexNode.hasValidChild().matrix)
            break
        if children[0].depth>limit:
            continue
        else:
            stack.extend(children)

    if len(stack)==0:
        print("loop has broken and result could not  found")


def depthFirstSearch(root):
    stack = []
    stack.append(root)
    counter = 0
    while (len(stack) > 0):
        indexNode = stack.pop()
        printMatrix(indexNode.matrix)
        print(indexNode.moves)
        counter += 1
        print(counter)
        children = indexNode.addChildren()
        if type(indexNode.hasValidChild()) == Node:
            print(f"SONUÇ {counter}. ADIMDA BULUNDU.  derinlik={indexNode.depth}")
            printMatrix(indexNode.hasValidChild().matrix)
            break
        stack.extend(children)

def calculateHeuristic(matrix,destMatrix):
    n= len(matrix)

    cost=0
    for i in range(n):
        for j in range(n):
            value=matrix[i][j]
            desti,destj = findElement(destMatrix,value)
            cost+= math.fabs(desti-i)+math.fabs(destj-j)
    return cost

def main():
    n=8
    matrix = defineMatrix(n)
    # # matrix = [
    # #     [5, 2, 6],
    # #     [1, 4, 3],
    # #     [0, 8, 7]
    # # ]
    # printMatrix(defineDestinationMatrix(n))
    printMatrix(matrix)
    input("hesaplamaya başlamak için herhangi bir tuşa basın")
    verifyMatrix(matrix)

    root = Node(matrix,0)
    print()
    # aStar(root)
    bfsWithAdder(root)
    # depthLimitedSearch(root,20)
    # depthFirstSearch(root)
    # uniformCostSearch(root)
if __name__ == '__main__':
    main()


