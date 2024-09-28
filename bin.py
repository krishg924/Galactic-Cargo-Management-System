from avl import AVLTree
from node import Bin_Object_Node
from node import Node

def swap_bin_object(obj_1, obj_2):
    obj_1.key = obj_2.key
    obj_1.size = obj_2.size
    obj_1.color = obj_2.color

class Bin(Node):
    def __init__(self, bin_id, capacity):
        super().__init__(bin_id)
        self.capacity = capacity
        self.bin_object = AVLTree(swap_function=swap_bin_object)

    def add_object(self, object):
        # Implement logic to add an object to this bin
        if object.size>self.capacity:
            return
        a = Bin_Object_Node(object.object_id,object.size,object.color)
        self.bin_object.insert(a)
        self.capacity -= object.size

    def remove_object(self, object_id):
        # Implement logic to remove an object by ID
        temp = self.bin_object.search(object_id)
        if temp is None:
            return
        self.capacity += temp.size
        self.bin_object.delete(temp)