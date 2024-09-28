from node import Node
# using swap function in delete function
def swap_1(node_1, node_2):
    node_1.key = node_2.key

class AVLTree:
    def __init__(self, swap_function=swap_1):
        self.root = None
        self.size = 0
        self.swap_func = swap_function

    def isRoot(self,p):
        if p is None:
            return False
        return p==self.root

    def isLeaf(self,p):
        if p is None:
            return False
        if ((p.left is None) and (p.right is None)):
            return True
        return False
    
    def isLeftChild(self,p):
        if p is None:
            return False
        if self.isRoot(p):
            return False
        r = p.parent
        if r.left is p:
            return True
        return False
    
    def isRightChild(self,p):
        if p is None:
            return False
        if self.isRoot(p):
            return False
        r = p.parent
        if r.right is p:
            return True
        return False

    def getDepth(self,p):
        if p is None:
            return -1
        if self.isRoot(p):
            return 0
        return 1+self.getDepth(p.parent)

    def getHeight(self,p):
        if p is None:
            return -1
        return p.height

    def recomputeHeight(self,p): #recompute heights of all ancestors of p
        if p is None:
            return
        if self.isLeaf(p):
            p.height = 0
            p = p.parent
        while p is not None:
            old_height = p.height
            p.height = 1+max(self.getHeight(p.left),self.getHeight(p.right))
            if(old_height==p.height):
                return
            p = p.parent

    def isBalanced(self,p):
        if p is None:
            return True
        return abs(self.getHeight(p.left)-self.getHeight(p.right))<=1

    def successor(self,p):
        if p is None:
            return None
        if p.right is not None: # when right child is present
            p = p.right
            while p.left is not None:
                p = p.left
            return p
        while self.isRightChild(p): # when right child is not present
            p = p.parent
        return p.parent

    def inorder(self,p): # just for checking the functioning of avl tree
        if(p is None):
            return
        self.inorder(p.left)
        print(p.key,end=" ")
        print(self.getHeight(p))
        self.inorder(p.right)

    def getList(self,p, li = None): #convert tree into a list using inorder traversal
        if li is None:
            li = []
        if p is None:
            return li
        self.getList(p.left,li)
        li.append(p.key)
        self.getList(p.right,li)
        return li

    def leftRotate(self,p): #left rotation about node p
        height_p = p.height
        t1 = self.getHeight(p.left)
        if not(self.isRoot(p)):
            temp = self.isRightChild(p)
        q = p.right         #store right child of p in q
        t2 = self.getHeight(q.left)
        t3 = self.getHeight(q.right)
        # updating the child and parent relation
        if q.left is not None:
            q.left.parent = p
        p.right = q.left
        q.parent = p.parent
        q.left = p
        p.parent = q
        if q.parent is None:
            self.root = q
        else:
            if temp==True:
                q.parent.right = q
            else:
                q.parent.left = q
        # updating the height of all the affected nodes
        p.height = max(t1,t2)+1
        q.height = max(t3,p.height)+1
        if(q.height!=height_p):
            self.recomputeHeight(q.parent)

    def rightRotate(self,p): #right rotation about node p
        height_p = p.height
        t1 = self.getHeight(p.right)
        if not(self.isRoot(p)):
            temp = self.isLeftChild(p)
        q = p.left          #store right child of p in q
        t2 = self.getHeight(q.right)
        t3 = self.getHeight(q.left)
        # updating the child and parent relation
        if q.right is not None:
            q.right.parent = p
        p.left = q.right
        q.parent = p.parent
        q.right = p
        p.parent = q
        if q.parent is None:
            self.root = q
        else:
            if temp==True:
                q.parent.left = q
            else:
                q.parent.right = q
        # updating the height of all the affected nodes
        p.height = max(t1,t2)+1
        q.height = max(t3,p.height)+1
        if(q.height!=height_p):
            self.recomputeHeight(q.parent)

    def rebalance(self,p):
        hleft = self.getHeight(p.left)
        hright = self.getHeight(p.right)
        # check for heavy side first for p and then for its children
        # then rotate accordingly for rebalancing
        if(hleft>hright):
            if(self.getHeight(p.left.left)>=self.getHeight(p.left.right)):
                self.rightRotate(p)
            else:
                self.leftRotate(p.left)
                self.rightRotate(p)
        else:
            if(self.getHeight(p.right.right)>=self.getHeight(p.right.left)):
                self.leftRotate(p)
            else:
                self.rightRotate(p.right)
                self.leftRotate(p)

    def search(self,k):
        p = self.root
        while p is not None:
            if k==p.key:
                return p
            elif k<p.key:
                p = p.left
            else:
                p = p.right
        return None

    def insert(self,p):
        if p is None:
            return
        self.size += 1
        if(self.root is None): #edge case for root node
            p.height = 0
            self.root = p
            return
        r = self.root
        # searching for appropriate position and inserting as a leaf node
        while True:
            if p.key < r.key:
                if r.left is None:
                    r.left = p
                    break
                r = r.left
            elif p.key > r.key:
                if r.right is None:
                    r.right = p
                    break
                r = r.right
            else:
                raise Exception("Same elements in the tree")
        p.parent = r
        p.height = 0
        # now recomputing the height of ancestors of p
        self.recomputeHeight(r)
        # then check whether tree is balanced or not 
        while r is not None:
            if self.isBalanced(r):
                r = r.parent
            else:
                self.rebalance(r)
                r = r.parent

    def deleteLeaf(self,p):
        if p is None:
            return
        if not(self.isLeaf(p)):
            raise Exception("deleteLeaf called for non leaf node")
        self.size -= 1
        if self.isRoot(p): #edge case for root node
            self.root = None
            return
        r = p.parent
        if r.left is p:
            r.left = None
        else:
            r.right = None
        # after deletion recompute height and check balancing
        self.recomputeHeight(r)
        while r is not None:
            if self.isBalanced(r):
                r = r.parent
            else:
                self.rebalance(r)
                r = r.parent

    def deleteNodeWithSingleChild(self,p):
        if p is None:
            return
        if p.left is not None and p.right is not None:
            raise Exception("deleteNodeWithSingleChild called on node with two child")
        self.size -= 1
        if self.isRoot(p): #handling edge case for root node
            if p.left is None:
                self.root = p.right
            else:
                self.root = p.left
            self.root.parent = None
            return
        # here deletion happens
        if p.left is None:
            r = p.right
        else:
            r = p.left
        if self.isLeftChild(p):
            p.parent.left = r
        else:
            p.parent.right = r
        r.parent = p.parent
        # after deletion recompute height and check balancing
        self.recomputeHeight(r.parent)
        while r is not None:
            if self.isBalanced(r):
                r = r.parent
            else:
                self.rebalance(r)
                r = r.parent

    def delete(self,p):
        # handles leaf node case and single child case separately
        if p is None:
            return
        if self.isLeaf(p):
            self.deleteLeaf(p)
            return
        if (p.left is None) or (p.right is None):
            self.deleteNodeWithSingleChild(p)
            return
        # two children case
        # swap p with its successor and then delete
        q = self.successor(p)
        self.swap_func(p,q)
        if self.isLeaf(q):
            self.deleteLeaf(q)
        elif (q.left is None) or (q.right is None):
            self.deleteNodeWithSingleChild(q)
        else:
            raise Exception("Error in deletion")