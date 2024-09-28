class Node:
    def __init__(self,key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1

class Bin_Object_Node(Node):
    def __init__(self, key, size, color):
        super().__init__(key)
        self.size = size
        self.color = color

class Capacity_Node(Node):
    def __init__(self, capacity,bin_id):
        super().__init__((capacity,bin_id))

class Object_Tree_Node(Node):
    def __init__(self, obj_id,my_bin_id):
        super().__init__(obj_id)
        self.my_bin_id = my_bin_id