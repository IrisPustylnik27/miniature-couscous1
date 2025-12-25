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
    #O(1)
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
    #O(1)
    def is_real_node(self):
        return self.key is not None


"""
A class implementing an AVL tree.
"""

class AVLTree(object):

    """
    Constructor, you are allowed to add more fields.
    """
    #O(1)
    def __init__(self):
        self.sizeOfTree = 0
        self.root = None
        self.exLeaf = AVLNode(None, None)

    #O(1)
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

    #calls O(logn)
    def search(self, key):
        return self.down_search(self.root, key)


    """searches for a node in the dictionary corresponding to the key, starting at the max
        
    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    #O(logn)
    def finger_search(self, key):
        e1 = 1
        currNode = self.max_node()
        if currNode is None: return None, 1
        if currNode.key < key: return None, 1
        while currNode.key > key:
            if currNode.parent is None: break
            currNode = currNode.parent
            e1 += 1
        node, e2 = self.down_search(currNode, key)
        return node, e1+e2-1

    """searches for a node in the dictionary corresponding to the key, starting at the given node

        @type key: int
        @param key: a key to be searched
        @type currNode: AVLNode
        @param currNode: starting node for searching
        @rtype: (AVLNode,int)
        @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
        and e is the number of edges on the path between the starting node and ending node+1.
        """

    #O(logn)
    def down_search(self, currNode, key):
        if currNode is None: return None, 1
        e = 1
        while currNode is not None:
            if currNode.key == key:
                return currNode, e
            elif currNode.key < key:
                currNode = currNode.right
            else:
                currNode = currNode.left
            e += 1
        return None, e



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
    #calls O(logn)
    def insert(self, key, val):
        x = self.root
        y, h = self.searching_for_insert(x, key)
        newNode = self.new_node(key, val)
        self.inserting_node(y, newNode)
        self.sizeOfTree += 1
        promoteCases = 0
        if y is not None:
            promoteCases = self.balance_AVLtree(y, 1, promoteCases)

        return newNode, h+1, promoteCases


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
    #O(logn)
    def finger_insert(self, key, val):
        x = self.max_node()
        newNode = self.new_node(key, val)
        if x is None:
            self.inserting_node(None, newNode)
            self.sizeOfTree += 1
            return newNode, 1, 0
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

        return newNode, edgesUp+edgesDown+1, promoteCases

    """searching for the place to insert new node

    @type key: int
    @param key: key of item that is to be inserted to self
    @type x: AVLNode
    @param val: current Node from which we start searching
    @rtype: (AVLNode,int)
    @returns: y - parent of new node, h - edges took to find y
    """

    #O(logn)
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


    """inserts a new node into the dictionary with given parent

    @type par: AVLNode
    @param par: parent of the new node
    @type node: AVLNode
    @param node: new node we need to insert
    """
    #O(1)
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
    #calls O(logn)
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
        self.sizeOfTree -= 1
        
        #now AVL addition
        if parent is not None:
            self.balance_AVLtree(parent,-1, 0)


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
    #worst case O(logn)
    def join(self, tree2, key, val):
        #check who's height is bigger
        h1 = self.get_height(self.root) if self.root else -1
        h2 = tree2.get_height(tree2.root) if tree2.root else -1
        newSize = tree2.sizeOfTree + self.sizeOfTree + 1
        #need to add check that none of the trees is None
        if not self.root:
            tree2.insert(key, val)
            self.root = tree2.root
            self.sizeOfTree = tree2.sizeOfTree
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
            self.sizeOfTree = newSize
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
            while b.height > t1.get_height(t1.root) + 1:
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
            t1.root.parent = node
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
        self.sizeOfTree = newSize
        
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

    #worst case O(h*logn) -> O((logn)^2)
    def split(self, node):
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
                leftTree.join(t, parent.key, parent.value)
            else:
                #child is parent left
                t.root = parent.right
                if t.root is not None: t.root.parent = None
                #right = (right_tree) + parent + (t)
                rightTree.join(t, parent.key, parent.value)
            child = parent
            parent = grand
            self.detach_node(child)
            if leftTree.root is not None:
                leftTree.root.parent = None
            if rightTree.root is not None:
                rightTree.root.parent = None

        self.root = None
        self.sizeOfTree = 0

        self.detach_node(node)

        return leftTree, rightTree

    """detaching given node from the tree

    @type node: AVLNode
    @pre: node is in self
    @param node: the node in the dictionary we need to detach
    """

    #O(1)
    def detach_node(self, node):
        node.parent = None
        node.left = None
        node.right = None
        return



    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of tuples (key, value) representing the data structure
    """
    #calls O(n)
    def avl_to_array(self):
        avlArray = []
        self.in_order(self.root, avlArray)
        return avlArray

    #O(m), m is number of nodes in subtree of currNode
    def in_order(self, currNode, avlArray):
        if currNode is None: return
        self.in_order(currNode.left, avlArray)
        avlArray.append((currNode.key, currNode.value))
        self.in_order(currNode.right, avlArray)
        return

    """returns the node with the maximal key in the dictionary

    @rtype: AVLNode
    @returns: the maximal node, None if the dictionary is empty
    """
    #O(logn)
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
    #O(1)
    def size(self):
        return self.sizeOfTree


    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """
    #O(1)
    def get_root(self):
        return self.root

    """performs rotation

    @type node: AVLNode
    @param node: the node in the dictionary with balance factor 2 or -2
    @type dirc: int
    @param dirc: tells in which direction the node is to be rotated: 1 is rotation right, -1 is rotation left
    """
    #O(1)
    def rotation(self,nodeB,dirc):
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

        return


    """performs balancing from the given node

    @type node: AVLNode
    @param node: the node in the dictionary we are starting the balancing from
    @type dtype: int
    @param dtype: tells if we called for balancing from insert or from delete
    @type promoteCases: int
    @param promoteCases: the number of rotations
    @rtype: (int)
    @returns: an int - number of rotations performed
    """
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

    """returns the balance factor of the given node

    @type node: AVLNode
    @param node: the node in the dictionary whom balance factor is needed
    @rtype: int
    @returns: the balance factor of the given node
    """
    # time complexity of O(1)
    def balance_factor(self,node):
        if node is None: return 0
        return self.get_height(node.left) - self.get_height(node.right)
    

    """returns the height of the given node
    
    @type node: AVLNode
    @param node: the node in the dictionary whom height is needed
    @rtype: int
    @returns: the height of the subtree rooted at the given node
    """
    # time complexity of O(1)
    def get_height(self, node):
        if not node:
            return -1
        return node.height

    """updates the height of a node

    @type node: AVLNode
    @param node: the node in the dictionary we need to update height to
    """
    # time complexity of O(1)
    def update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        return

    """returns the successor of the given node
    
    @type node: AVLNode
    @param node: the node in the dictionary we need to find successor for
    @rtype: AVLNode
    @returns: the successor of node
    """
    #time complexity of O(logn)
    def successor(self,node):
        if node.right is not None:
            return self.minNode(node.right)
        y = node.parent
        while y is not None and node == y.right:
            node = y
            y = node.parent
        return y

    """returns the node with the minimal key in the dictionary

    @rtype: AVLNode
    @returns: the minimal node, None if the dictionary is empty
    """
    #time complexity of O(logn)
    def minNode(self,node):
        if node is None: return None
        while node.left is not None:
            node = node.left
        return node





    

