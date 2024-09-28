# Galactic Cargo Management System (GCMS)

## Project Overview
The **Galactic Cargo Management System (GCMS)** is designed to efficiently manage a collection of bins and objects based on their colors, capacities, and specific allocation algorithms. It uses **AVL trees** to maintain bin and object data structures, ensuring operations such as adding objects, deleting objects, and retrieving information are performed efficiently.

The system follows different algorithms for object placement based on the object's color:
- **Compact Fit Algorithm** for Blue and Yellow objects (with different tie-breaking rules).
- **Largest Fit Algorithm** for Red and Green objects (with different tie-breaking rules).

### Key Features:
- Add bins with unique capacities.
- Place and remove objects into bins using color-based algorithms.
- Retrieve information on bins and objects.
- Efficient handling of operations with AVL tree data structures.

### Complexity:
- **Time complexity**: O(log(n) + log(m)) for all operations except bin_info function.
- **Space complexity**: O(n + m), where `n` is the number of bins and `m` is the number of objects.

### Algorithms:
- **Compact Fit**: Selects the smallest capacity bin that can accommodate the object.
- **Largest Fit**: Selects the largest capacity bin that can accommodate the object.

### Technologies Used:
- Python
- AVL Trees
- OOPS Concept

---
