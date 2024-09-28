from bin import Bin
from avl import AVLTree
from object import Object, Color
from exceptions import NoBinFoundException
from node import Object_Tree_Node,Bin_Object_Node,Capacity_Node

def swap_object(obj_1, obj_2):
    obj_1.key = obj_2.key
    obj_1.my_bin_id = obj_2.my_bin_id

class GCMS:
    def __init__(self):
        # Maintain all the Bins and Objects in GCMS
        self.binTree = AVLTree()
        self.objectTree = AVLTree(swap_function=swap_object)
        self.capacityTree = AVLTree()

    def find_max_capacity(self): #returns the max capacity node in capacity tree
        r = self.capacityTree.root
        while r.right is not None:
            r = r.right
        return r

    def find_compact_fit_capacity(self,size): #returns the node with minimum capacity  
        p = self.capacityTree.root            #greater than or equal to given size in capacity tree
        while True:
            if size==p.key[0]:
                return p
            elif size<p.key[0]:
                if p.left is None:
                    return p
                p = p.left
            else:
                if p.right is None:
                    return self.capacityTree.successor(p)
                p = p.right

    def help_least(self,p,cap): # returns the node with least id having
        prev = p                # its capacity equal to given capacity
        while p is not None:
            if p.key[0]==cap:
                prev = p
                p = p.left
            elif p.key[0]<cap:
                p = p.right
        return prev
    
    def help_greatest(self,p,cap): # returns the node with greatest id having
        prev = p                   # its capacity equal to given capacity
        while p is not None:
            if p.key[0]==cap:
                prev = p
                p = p.right
            elif p.key[0]>cap:
                p = p.left
        return prev

    def find_first_cap(self,cap): # returns first node having capacity equal to cap
        r = self.capacityTree.root
        while 1:
            if(cap<r.key[0]):
                r = r.left
            elif cap>r.key[0]:
                r = r.right
            else:
                return r

    def add_bin(self, bin_id, capacity):
        # updating bin and capacity tree
        a = Bin(bin_id,capacity)
        self.binTree.insert(a)
        b = Capacity_Node(capacity,bin_id)
        self.capacityTree.insert(b)

    def add_object(self, object_id, size, color):
        if self.binTree.size==0: # if there is no bin raise exception
            raise NoBinFoundException
        # variable to store required bin id
        id = 0
        # if color is red or green find the max capacity of the capacity tree
        if color == Color.RED or color == Color.GREEN:
            r = self.find_max_capacity()
            if r.key[0]<size:
                raise NoBinFoundException
            else:
                if color == Color.GREEN:
                    id = r.key[1]
                    duplicate = Capacity_Node(r.key[0]-size,id)
                    self.capacityTree.delete(r)
                    self.capacityTree.insert(duplicate)
                else:
                    # red color case
                    # first go to first node having max capacity and then call help least function
                    cap = r.key[0]
                    first_max = self.find_first_cap(cap)
                    ans = self.help_least(first_max,cap)
                    id = ans.key[1]
                    duplicate = Capacity_Node(ans.key[0]-size,id)
                    self.capacityTree.delete(ans)
                    self.capacityTree.insert(duplicate)
        else:
            u = self.find_compact_fit_capacity(size)
            if u is None:
                raise NoBinFoundException
            cap = u.key[0]
            if cap<size:
                raise NoBinFoundException
            else:
                first_cap = self.find_first_cap(cap)
                if color == Color.BLUE:
                    ans = self.help_least(first_cap,cap)
                    id = ans.key[1]
                    duplicate = Capacity_Node(ans.key[0]-size,id)
                    self.capacityTree.delete(ans)
                    self.capacityTree.insert(duplicate)
                else:
                    ans = self.help_greatest(first_cap,cap)
                    id = ans.key[1]
                    duplicate = Capacity_Node(ans.key[0]-size,id)
                    self.capacityTree.delete(ans)
                    self.capacityTree.insert(duplicate)
        new_obj = Object_Tree_Node(object_id,id)
        self.objectTree.insert(new_obj)
        l = self.binTree.search(id)
        k = Object(object_id,size,color)
        l.add_object(k)

    def delete_object(self, object_id):
        # Implement logic to remove an object from its bin
        v = self.objectTree.search(object_id)
        if v is None:
            return
        id = v.my_bin_id
        self.objectTree.delete(v)
        w = self.binTree.search(id)
        old_cap = w.capacity
        w.remove_object(object_id)
        temp = self.capacityTree.search((old_cap,id))
        self.capacityTree.delete(temp)
        y = Capacity_Node(w.capacity,id)
        self.capacityTree.insert(y)

    def bin_info(self, bin_id):
        # returns a tuple with current capacity of the bin and the list of objects in the bin (int, list[int])
        v = self.binTree.search(bin_id)
        if v is None:
            raise Exception("No bin found")
        li = v.bin_object.getList(v.bin_object.root)
        return (v.capacity,li)
        

    def object_info(self, object_id):
        # returns the bin_id in which the object is stored
        v = self.objectTree.search(object_id)
        if v is None:
            raise Exception("No object found")
        return v.my_bin_id