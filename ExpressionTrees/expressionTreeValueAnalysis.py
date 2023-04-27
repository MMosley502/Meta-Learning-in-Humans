import csv
import random
import copy

#Expression Tree class
class Node:
    def __init__(self, value=None, type=None, left=None, right=None, next=None):
        self.value = value
        self.type = type
        self.left = left
        self.right = right
        self.next = next

class Stack:
    def __init__(self):
        self.head = None

    def push(self, node):
        if not self.head:
            self.head = node
        else:
            node.next = self.head
            self.head = node

    def pop(self):
        if self.head:
            popped = self.head
            self.head = self.head.next
            return popped
        else:
            raise Exception("Stack is empty")

class ExpressionTree:
    # destructively prints the expression to console
    # x: stack.pop()
    def inorder(self, x):
        if not x:
            return
        print("(", end=" ")
        self.inorder(x.left)
        print(x.value, end=" ")
        self.inorder(x.right)
        print(")", end=" ")

    # destructively prints the expression to file
    # x: stack.pop()
    # file: output file
    def inorderFile(self, x, file):
        if not x:
            return
        file.write("(")
        self.inorderFile(x.left, file)
        file.write(x.value)
        self.inorderFile(x.right, file)
        file.write(")")

    # constructs tree using the generated list
    # list: [list] of tags and operators
    def makeTree(self, list):
        stack = Stack()
        for c in list:
            # make new non-leaf nond
            if c[0] in "+-*/^":
                z = Node(c, "operator")
                x = stack.pop()
                y = stack.pop()
                z.left = y
                z.right = x
                stack.push(z)
            # make leaf node
            else:
                stack.push(Node(c, "tag"))
        return stack    

    # destructively evaluates the tree and returns the value
    # branch: stack.pop()
    # tagList: [list] of all tags in the dataset
    def evaluate(self, branch, tagList):
        # returns value if node is a leaf
        if branch.type == "tag":
            return getTagValue(tagList, branch.value)
        # gets value of children
        val1 = self.evaluate(branch.left, tagList)
        val2 = self.evaluate(branch.right, tagList)

        # evaluates values of node
        match branch.value[0]:
            case "+":
                return val1 + val2
            case "-":
                return val1 - val2
            case "*":
                return val1 * val2
            case "/":
                if val2 == 0:
                    return 1
                return val1 / val2
            case _:
                return getTagValue(tagList, branch.value[0])

# generate a random tag from the tag list
# tagList: [list] of (tags, values) taken from the input dataset
def randTag(tagList):
    tagNum = random.randint(0,39)
    return tagList[tagNum][0]

# gets the assigned value of the input tag
# tagList: [list] of (tags, values)
# tag: the tag to find the value of
def getTagValue(tagList, tag):
    for valtag in tagList:
        if valtag[0] == tag:
            return valtag[1]

# given a set of tags and a number of operators. 
# gererates a expresion [list] that can be made into an expression tree
# setOfTags: [list] of 
def randomTreeString(setOfTags, numOfOps):
    operators = ["+", "-", "*"]
    numUsedTags = 0
    numUsedOps = 0
    expressionList = []
    tagPos = []
    tagNum = len(setOfTags)
    while (numOfOps > 0 or tagNum > 0):
        # add tag to tree
        # bias random to account for restictions 
        # ~33% chance to select tag
        # ~66% chance to select operator
        # nth operator can only be chosen if n+2 tags are selected
        rand = random.randint(0,2)
        if (rand == 0 or numOfOps == 0) and tagNum > 0:
            num = 0
            # randomize tag if multiple remaining 
            if tagNum > 1:
                num = random.randint(0, tagNum-1)
            tagNum -= 1
            tag = setOfTags[num]
            setOfTags.remove(tag)
            numUsedTags += 1
            tagPos.append(len(expressionList))
            expressionList.append(tag)
        # add operator to tree
        # makes sure valid tree is formed
        elif numOfOps > 0 and (numUsedTags >= (numUsedOps + 2)):
            num = random.randint(0, 2)
            numOfOps -= 1
            numUsedOps += 1
            expressionList.append(operators[num])

    # expresssion list is what makes the tree
    # tagPos gives the position of each tag in the expression list
    return expressionList, tagPos
    

#get feature names
file = open("list_attr_celeba_analysis.csv", "r")
data = list(csv.reader(file, delimiter=","))
file.close()

# makes list of tag names and associated value
# skips first column
tags = []
#set value to 2 to differentiate between x+x and x*x
for i in range(1, len(data[0]) - 1):
    tags.append((data[0][i], 2))

# select tags to make into tree
treeTags = []
tagPositions = []

# generates 4 random tags for tree creation 
# can have repeats
for x in range(4):
    # gets random tag
    temp = randTag(tags)
    # add tag position and tag to new list
    tagPositions.append(data[0].index(temp))
    treeTags.append(temp)

# copy tags so rand works
temp = copy.copy(treeTags)
s, pos = randomTreeString(temp, len(treeTags)-1)



# open file
outputFile = open("test.csv", 'w')
# prints image, value, and then expresssion as third column
outputFile.write("image, value, ")
fullTree = ExpressionTree()
stack = fullTree.makeTree(s)
fullTree.inorderFile(stack.pop(), outputFile)
outputFile.write("\n")


# calculate each 
# loop through each image 
for image in data:
    # skip tag row
    if image[0] == "files":
        continue
    # check if it contains the selected tags
    # adjust the values of all tags for correct calculation 
    for position in tagPositions:
        # -1 accounts for image column
        temp = list(tags[position-1])
        # sets tag value to 1 if not present in image 
        if (image[position] == "-1"):
            temp[1] = 1
            tags[position-1] = tuple(temp)
        else:
            temp[1] = 2
            tags[position-1] = tuple(temp)
    stack = fullTree.makeTree(s)
    outputFile.write(image[0] + ", " + str(fullTree.evaluate(stack.pop(), tags)) + "\n")
    
    
outputFile.close()