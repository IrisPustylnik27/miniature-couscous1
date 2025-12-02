#id1:[REDACTED_ID]
#name1:iris [REDACTED_USERNAME]
#username1:[REDACTED_USERNAME]
#id2: [REDACTED_ID]
#name2: ksenia yaremenko
#username2: [REDACTED_USERNAME]
"""A class represnting a node in an AVL tree"""

class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1


    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """
    def is_real_node(self):
        return False


"""
A class implementing an AVL tree.
"""

class AVLTree(object):

    """
    Constructor, you are allowed to add more fields.
    """
    # add a size for the whole tree, need to update ++ in insert for every insert
    # add external leaf for simple use
    def __init__(self):
        self.size = None
        self.root = None
        self.exLeaf = AVLNode(None, None)


    """searches for a node in the dictionary corresponding to the key (starting at the root)
        
    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    def search(self, key):
        curr_node = self.root
        e = -1
        while curr_node is not None:
            if curr_node.key == key:
                return curr_node, e
            elif curr_node < key:
                curr_node = curr_node.right
            else:
                curr_node = curr_node.left
            e+=1
        return None, -1


    """searches for a node in the dictionary corresponding to the key, starting at the max
        
    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    def finger_search(self, key):
        return None, -1


    """inserts a new node into the dictionary with corresponding key and value (starting at the root)

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int)
    @returns: a 3-tuple (x,e,h) where x is the new node,
    e is the number of edges on the path between the starting node and new node before rebalancing,
    and h is the number of PROMOTE cases during the AVL rebalancing
    """
    def insert(self, key, val):
        return None, -1, -1


    """inserts a new node into the dictionary with corresponding key and value, starting at the max

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int)
    @returns: a 3-tuple (x,e,h) where x is the new node,
    e is the number of edges on the path between the starting node and new node before rebalancing,
    and h is the number of PROMOTE cases during the AVL rebalancing
    """
    def finger_insert(self, key, val):
        return None, -1, -1


    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """
    def delete(self, node):
        return


    """joins self with item and another AVLTree

    @type tree2: AVLTree 
    @param tree2: a dictionary to be joined with self
    @type key: int 
    @param key: the key separting self and tree2
    @type val: string
    @param val: the value corresponding to key
    @pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
    or the opposite way
    """
    def join(self, tree2, key, val):
        return


    """splits the dictionary at a given node

    @type node: AVLNode
    @pre: node is in self
    @param node: the node in the dictionary to be used for the split
    @rtype: (AVLTree, AVLTree)
    @returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
    dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
    dictionary larger than node.key.
    """
    def split(self, node):
        return None, None


    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """
    def avl_to_array(self):
        avl_array = []
        self.in_order(self.root, avl_array)
        return avl_array

    def in_order(self, curr_node, avl_array):
        self.in_order(curr_node.left, avl_array)
        avl_array.append(curr_node)
        self.in_order(curr_node.right, avl_array)
        return 0

    """returns the node with the maximal key in the dictionary

    @rtype: AVLNode
    @returns: the maximal node, None if the dictionary is empty
    """
    def max_node(self):
        curr_node = self.root
        while curr_node.right.key is not None:
            curr_node = curr_node.right
        return curr_node

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """
    # returns the val itself (getter)
    def size(self):
        return self.size


    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """
    # return the root that is in init(getter)
    def get_root(self):
        return self.root
    
    #rotation func. insert a node you want to rotate and in which dir
    def rotation(self,nodeB,dirc):
        # 1 is right, -1 is left
        if dirc == 1:
            nodeA = nodeB.left
            if nodeA is None : return
            nodeB.left = nodeA.right
            if nodeB.left is not None:
                nodeB.left.parent = nodeB
            nodeA.right = nodeB
            if nodeB.parent is None:
                self.root = nodeA
            elif nodeB == nodeB.parent.right :
                nodeB.parent.right = nodeA
            else:
                nodeB.parent.left = nodeA
            nodeA.parent = nodeB.parent
            nodeB.parent = nodeA
        #אין כמו שכפול קוד:)
        else:
            nodeA = nodeB.right
            if nodeA is None : return
            nodeB.right = nodeA.left
            if nodeB.right is not None:
                nodeB.right.parent = nodeB
            nodeA.left = nodeB
            if nodeB.parent is None:
                self.root = nodeA
            elif nodeB == nodeB.parent.left :
                nodeB.parent.left = nodeA
            else:
                nodeB.parent.right = nodeA
            nodeA.parent = nodeB.parent
            nodeB.parent = nodeA
        #update the height after rotation
        nodeB.height = 1 + max(self.get_height(nodeB.left), self.get_height(nodeB.right))
        nodeA.height = 1 + max(self.get_height(nodeA.left), self.get_height(nodeA.right))

    def balance_AVLtree(self, node, dtype):
        # 1 for insert, -1 for delete
        if node is None : return
        BFy = self.balance_factor(node)
        currHeight = 1 + max(self.get_height(node.left), self.get_height(node.right))
        heightChanged = (node.height != currHeight)
        node.height = currHeight
        if abs(BFy) < 2 : 
            if not heightChanged: return
            self.balance_AVLtree(node.parent, dtype)
        else:
            bfRightSon = self.balance_factor(node.right)
            bfLeftSon = self.balance_factor(node.left)
            if dtype == 1: 
                #insert
                if BFy == 2 :
                    if bfLeftSon == 1: self.rotation(node,1)
                    else:
                        self.rotation(node.left,-1)
                        self.rotation(node,1)
                else:
                    if bfRightSon == -1: self.rotation(node,-1)
                    else:
                        self.rotation(node.right,1)
                        self.rotation(node,-1)
            else:
                #delete
                if BFy == 2 :
                    if bfLeftSon >= 0: self.rotation(node,1)
                    else:
                        self.rotation(node.left,-1)
                        self.rotation(node,1)
                else:
                    if bfRightSon <= 0: self.rotation(node,-1)
                    else:
                        self.rotation(node.right,1)
                        self.rotation(node,-1)
                if node.parent: self.balance_AVLtree(node.parent, dtype)
        return
    
    #balance factor of a node
    def balance_factor(self,node):
        if node is None: return 0
        return self.get_height(node.left) - self.get_height(node.right)
    
    #getter for height
    def get_height(self, node):
        if not node:
            return -1
        return node.height
    
    #helper to update height
    def update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))




    

