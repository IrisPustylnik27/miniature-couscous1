#id1:[REDACTED_ID]
#name1:iris [REDACTED_USERNAME]
#username1:[REDACTED_USERNAME]
#id2: [REDACTED_ID]
#name2: ksenia yaremenko
#username2: [REDACTED_USERNAME]
"""A class representing a node in an AVL tree"""

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
        if self.left.key is None and self.right.key is None: return False
        return True


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

    #creating new node with height 0 for not repeating the code
    def new_node(self, key, value):
        newNode = AVLNode(key, value)
        newNode.height = 0
        return newNode


    """searches for a node in the dictionary corresponding to the key (starting at the root)
        
    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """

    #does it need to be 1 when we searched for key in root?
    def search(self, key):
        return self.down_search(self.root, key)

    def down_search(self, currNode, key):
        if currNode is None: return None, -1
        e = 1
        while currNode is not None:
            if currNode.key == key:
                return currNode, e
            elif currNode.key < key:
                currNode = currNode.right
            else:
                currNode = currNode.left
            e += 1
        return None, -1


    """searches for a node in the dictionary corresponding to the key, starting at the max
        
    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    def finger_search(self, key):
        e1 = 1
        currNode = self.max_node()
        if currNode is None: return None, -1
        if currNode.key < key: return None, -1
        while currNode.key > key:
            if currNode.parent is None: break
            currNode = currNode.parent
            e1 += 1
        node, e2 = self.down_search(currNode, key)
        return node, e1+e2-1


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
        x = self.root
        y, h = self.searching_for_insert(x, key)
        newNode = self.new_node(key, val)
        self.inserting_node(y, newNode)
        self.size += 1

        promoteCases = 0
        if y is not None:
            promoteCases = self.balance_AVLtree(y, 1, promoteCases)

        return newNode, h, promoteCases


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
        x = self.max_node()
        newNode = self.new_node(key, val)
        if x is None:
            self.inserting_node(None, newNode)
            return newNode, 0, 0
        edgesUp = 0
        edgesDown = 0
        if x.key < key:
            self.inserting_node(x, newNode)
            y = x
            edgesDown += 1
        else:
            while x.key > key:
                if x.parent is None: break
                x = x.parent
                edgesUp += 1
            y, edgesDown = self.searching_for_insert(x, key)
            self.inserting_node(y, newNode)

        promoteCases = 0
        if y is not None:
            promoteCases = self.balance_AVLtree(y, 1, promoteCases)

        return newNode, edgesUp+edgesDown, promoteCases


    def searching_for_insert(self, x, key):
        y = None
        h = 0
        while x is not None:
            y = x
            if key < x.key:
                x = x.left
            else:
                x = x.right
            h += 1
        return y, h


    def inserting_node(self, par, node):
        if par is None:
            self.root = node
        elif node.key < par.key:
            par.left = node
        else:
            par.right = node
        node.parent = par
        return


    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """
    def delete(self, node):
        if node is None:
            return
        
        parent = node.parent
        # normal BSTs deletion
        #case 1: no leaf
        if node.left is None and node.right is None:
            if parent is None: self.root = None
            elif parent.left is node: parent.left = None
            else: parent.right = None
        
        #case 2: 1 leaf
        elif node.left is None or node.right is None:
            child = node.left if node.left else node.right
            child.parent = parent
            if parent is None: self.root = child
            elif parent.left is node: parent.left = child
            else: parent.right = child
        
        #case 3: 2 leaf
        else: 
            succ = self.successor(node)
            node.value = succ.value
            node.key = succ.key
            self.delete(succ)
            return
        self.size -= 1
        
        #now AVL addition
        if parent is not None:
            self.balance_AVLtree(parent,-1)


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
        #check who's height is bigger
        h1 = self.get_height(self.root) if self.root else -1
        h2 = tree2.get_height(tree2.root) if tree2.root else -1
        newSize = tree2.size + self.size + 1
        #need to add check that none of the trees is None
        if not self.root:
            tree2.insert(key, val)
            self.root = tree2.root
            self.size = tree2.size
            return

        if not tree2.root:
            self.insert(key, val)
            return
    
        # if close by height
        if abs(h1 - h2) <= 1:
            new_root = AVLNode(key, val)
            if self.root.key < key :
                new_root.left = self.root
                new_root.right = tree2.root
            else:
                new_root.right = self.root
                new_root.left = tree2.root
            if self.root: self.root.parent = new_root
            if tree2.root: tree2.root.parent = new_root
            
            self.root = new_root
            self.root.height = 1 + max(h1, h2)
            self.size = newSize 
            return 
        
        #else
        if h2 > h1 : 
            t2 = tree2
            t1 = self
        else: 
            t2 = self
            t1 = tree2
        
        node = AVLNode(key,val)
        if t2.root.key > key:
            b = t2.root
            while(b.height > t1.get_height(t1.root) + 1):
                b = b.left
            t1.root.parent = node
            c = b.parent
            b.parent =  node
            node.parent = c
            if c is None: t2.root = node
            else: c.left = node
            node.left = t1.root
            node.right = b
        else:
            b = t2.root
            while b.height > t1.get_height(t1.root) + 1:
                b = b.right
            c = b.parent
            b.parent =  node
            node.parent = c
            if c is None: t2.root = node
            else: c.right = node
            node.right = t1.root
            node.left = b
        node.height = 1 + max(node.left.height if node.left else -1, node.right.height if node.right else -1)
        t2.balance_AVLtree(c,-1,0)
        self.root = t2.root
        self.size = newSize
        
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
        #need to add size to all the trees
        leftTree, rightTree = AVLTree(), AVLTree()
        leftTree.root = node.left
        if leftTree.root is not None: leftTree.root.parent = None
        rightTree.root = node.right
        if rightTree.root is not None: rightTree.root.parent = None
        node.left, node.right = None, None

        child = node
        parent = node.parent
        while parent is not None:
            grand = parent.parent
            t = AVLTree()
            if child is parent.right:
                t.root = parent.left
                if t.root is not None: t.root.parent = None
                parent.left = None
                parent.right = None
                parent.parent = None
                leftTree.join(t, parent.key, parent.value)
            else:
                #child is parent left
                t.root = parent.right
                if t.root is not None: t.root.parent = None
                parent.left = None
                parent.right = None
                parent.parent = None
                #right = (right_tree) + parent + (t)
                rightTree.join(t, parent.key, parent.value)
            child = parent
            parent = grand
            if leftTree.root is not None:
                leftTree.root.parent = None
            if rightTree.root is not None:
                rightTree.root.parent = None

        return leftTree, rightTree



    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of tuples (key, value) representing the data structure
    """
    def avl_to_array(self):
        avlArray = []
        self.in_order(self.root, avlArray)
        return avlArray

    def in_order(self, currNode, avlArray):
        self.in_order(currNode.left, avlArray)
        avlArray.append(currNode)
        self.in_order(currNode.right, avlArray)
        return 0

    """returns the node with the maximal key in the dictionary

    @rtype: AVLNode
    @returns: the maximal node, None if the dictionary is empty
    """
    def max_node(self):
        currNode = self.root
        if currNode is None: return None
        while currNode.right is not None:
            currNode = currNode.right
        return currNode

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """
    # returns the val itself (getter)
    # time complexity of O(1)
    def size(self):
        return self.size


    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """
    # return the root that is in init(getter)
    # time complexity of O(1)
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


    # time complexity of O(logn)
    def balance_AVLtree(self, node, dtype, promoteCases):
        # 1 for insert, -1 for delete, promoteCases is how many times we needed to rebalance (rotations cases)
        if node is None : return promoteCases

        BFy = self.balance_factor(node)

        currHeight = 1 + max(self.get_height(node.left), self.get_height(node.right))
        heightChanged = (node.height != currHeight)
        node.height = currHeight

        if abs(BFy) < 2 :
            if (not heightChanged) and (dtype == 1): return promoteCases
            return self.balance_AVLtree(node.parent, dtype, promoteCases)

        promoteCases += 1

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
            if node.parent: return self.balance_AVLtree(node.parent, dtype, promoteCases)
        return promoteCases
    
    #balance factor of a node
    # time complexity of O(1)
    def balance_factor(self,node):
        if node is None: return 0
        return self.get_height(node.left) - self.get_height(node.right)
    

    #getter for height
    # time complexity of O(1)
    def get_height(self, node):
        if not node:
            return -1
        return node.height
    

    #helper to update height
    # time complexity of O(1)
    def update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))


    #helper for finding the successor
    #time complexity of O(logn)
    def successor(self,node):
        if node.right is not None:
            return self.min(node.right)
        y = node.parent
        while y is not None and node == y.right:
            node = y
            y = node.parent
        return y
    

    #helper to find the minimum
    #time complexity of O(logn)
    def min(self,node):
        while node.left is not None:
            node = node.left
        return node




    

