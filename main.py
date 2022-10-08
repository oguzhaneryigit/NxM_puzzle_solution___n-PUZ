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
    def __init__(self, matrix, prevMovement=""):
        self.matrix = matrix
        self.prevMovement = prevMovement
        self.moves = findPossibleMoves(matrix, prevMovement)
        self.zeroX, self.zeroY = findZero(matrix)
        self.left = None
        self.right = None
        self.upper = None
        self.down = None
        self.isValidGraph = verifyMatrix(self.matrix)

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
            self.left = Node(swap(self.matrix, self.zeroX, self.zeroY, self.zeroX, self.zeroY - 1), "l")
            tempNodeList.append(self.left)

        if "r" in self.moves:
            self.right = Node(swap(self.matrix, self.zeroX, self.zeroY, self.zeroX, self.zeroY + 1), "r")
            tempNodeList.append(self.right)

        if "u" in self.moves:
            self.upper = Node(swap(self.matrix, self.zeroX, self.zeroY, self.zeroX - 1, self.zeroY), "u")
            tempNodeList.append(self.upper)

        if "d" in self.moves:
            self.down = Node(swap(self.matrix, self.zeroX, self.zeroY, self.zeroX + 1, self.zeroY), "d")
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


def main():
    # matrix = defineNxMmatrix(2, 3)
    matrix = [
        [7, 2, 4],
        [5, 0, 6],
        [8, 3, 1]
    ]
    verifyMatrix(matrix)

    root = Node(matrix)
    bfsWithAdder(root)


if __name__ == '__main__':
    main()

# For simplicity, you can use a Queue to perform BFS non recursively. You need two data structures here.
#
# A Queue to maintain the BFS order.
# List item hash table (or set) to look for duplicates.
# This is the algorithm:
#
# Enqueue the initial point on the graph into the queue and also the hash table.
# If the queue is not empty
#
# Dequeue from the queue.
# çocuklarını ekle
# çocuklar içinde true var mı hesapla
# true yok ise
# çocukları ekle
# true var ise çocukları ekle ve  diğer düğümlere çocuk eklemeyi  iptal et
# En queue all neighbors of the dequeued element to the queue and insert them into the set if they are not already present in the set.
# Print (/access/process) the dequeued element.
# Repeat steps 2 through 4 until the queue is exhausted.
# You can find many examples and optimizations online. Eg:
