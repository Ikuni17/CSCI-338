'''
Bradley White & Johnathan Johnson
CSCI 338: Bin Packing
February 16, 2016

This solution sorts the rectangles into a dictionary with the width as the key
and a node object as the value. The node contains a list of rectangle objects
that each contain the rectangle's order number for output, dimensions and position.
Rectangles with the same width are placed in the same row, then rectangles with
next highest width are placed at the end of that row.

'''
# global variables
output = []             # List of rectangle position tuples to output to the driver
current_y = 0           # Keep track of next available y position
nodeHash = {}           # Dictionary with widths as keys and nodes as values
in_order = []           # List of rectangle objects that are appended as they are placed
nodeList = []           # List of nodes that are sorted by total length

# start module
def find_solution(squares):
    global output
    global current_y
    global nodeHash
    global in_order
    global nodeList
    
    output = []             # List of rectangle position tuples to output to the driver
    current_y = 0           # Keep track of next available y position
    nodeHash = {}           # Dictionary with widths as keys and nodes as values
    in_order = []           # List of rectangle objects that are appended as they are placed
    nodeList = [] 
    
    # call helper modules
    create_nodelist(squares)
    optimize()

    # sort the rectangle object based on their order from the input file
    in_order.sort(key=get_order)
    # update the output with the position of each rectangle in the correct order
    for i in range(0, len(in_order)):
        output.append(in_order[i].position)
    return output

# Populates the dictionary
def create_nodelist(squares):
    global output
    global current_y
    global nodeHash
    global in_order
    global nodeList
    created = 0     # order of node creation

    # Loop through all the tuples in squares.txt
    for i in range(0, len(squares)):
        # Store the width of rectangle as key
        key = squares[i][1]
        # Create a new rectangle object and pass order number and dimensions
        temp_rectangle = Rectangle(i, squares[i])

        # Check if the key is already in the hash or not
        if key in nodeHash:
            # Append the rectangle to the node's list
            nodeHash[key].rectangleList.append(temp_rectangle)
            nodeHash[key].total_length+=squares[i][0]
        # Create a new entry in the dictionary if key not found
        else:
            # Create a new node object and pass the width
            temp_node = Node(key, created)
            created += 1
            # Create a new entry in the dictionary
            nodeHash[key] = temp_node
            # Append the rectangle to the node's list
            nodeHash[key].rectangleList.append(temp_rectangle)
            # Keep track of the total length of a row
            nodeHash[key].total_length+=squares[i][0]

# places two consectutive lists on the graph
def optimize():
    global output
    global current_y
    global nodeHash
    global in_order
    global nodeList
    
    # append all nodes to a list
    for key in nodeHash:
        nodeList.append(nodeHash[key])
    
    # sort the list from largest width to smallest
    nodeList.sort(key=get_width)
    nodeList.reverse()

    # loop through all the nodes and place rectangles list together
    for i in range(0,(len(nodeList)),+2):
        # update the node with the next available y position
        nodeList[i].ylocal = current_y
        # check that there is an i+1 node
        if i < (len(nodeList) - 1):
            # update i+1 node with the same row as node i
            nodeList[i+1].ylocal = current_y
            # double check largest width and update the next available y position
            if nodeList[i].width > nodeList[i+1].width:
                current_y-=nodeList[i].width
            else:
                current_y-=nodeList[i+1].width
        else:
             current_y-=nodeList[i].width   
        # call helper module
        place_list(nodeList[i])
        if i < (len(nodeList)-1):
            nodeList[i+1].xlocal = nodeList[i].xlocal
            place_list(nodeList[i+1])

# helper module to place all the rectangles in a node's list within the graph
def place_list(node):
    global output
    global current_y
    global nodeHash
    global in_order
    global nodeList

    # Loop through all the rectangle objects in the node's list
    for i in range(0, len(node.rectangleList)):
        # Update the rectangles position with the next available position
        node.rectangleList[i].position = (node.xlocal, node.ylocal)
        # Append the rectangle object onto a list
        in_order.append(node.rectangleList[i])
        # Update the node's next available position
        node.xlocal += node.rectangleList[i].dimension[0]

# helper module for sorting the in_order list
def get_order(self):
    global output
    global current_y
    global nodeHash
    global in_order
    global nodeList

    # return original order number from squares.txt
    return self.order

# helper module for sorting the nodeList
def get_width(self):
    global output
    global current_y
    global nodeHash
    global in_order
    global nodeList
    
    # return the width of all rectangles in the node
    return self.width

# Object as value for hash table 
class Node(object):
    # Node constructor
    def __init__(self, width, create):
        self.rectangleList = []         # List of rectangle objects
        self.optimized = False          # Check if node has been placed
        self.xlocal = 0                 # Next available x position
        self.ylocal = 0                 # y position for whole list
        self.width = width              # width of rectanges in this node
        self.created = create           # order of node creation
        self.total_length = 0           # length of all rectangles in the list
        
# Object to hold values for each rectangle
class Rectangle(object):
    # Rectangle constructor
    def __init__(self, num, dim):
        self.order = num                # Original order from squares
        self.dimension = dim            # Dimensions tuple (width, length)
        self.position = None            # Position tuple (x, y)
        

def find_naive_solution (rectangles):   
    placement = []
    upper_left_x = 0
    upper_left_y = 0
    
    for rectangle in rectangles:
        width = rectangle[0]
        coordinate = (upper_left_x, upper_left_y)   # make a tuple
        placement.insert(0, coordinate)             # insert tuple at front of list
        upper_left_x = upper_left_x + width
        
    placement.reverse()                             # original order
    return placement     
