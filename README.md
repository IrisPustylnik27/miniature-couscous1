# AVL Tree Dictionary Implementation

This project implements an AVL Tree-based dictionary in Python.
The project was developed as part of a Data Structures course.

## Overview

The implementation provides a self-balancing binary search tree that stores key-value pairs.
It supports standard dictionary operations, AVL rebalancing, and additional advanced operations such as finger search, finger insertion, join, and split.

The goal of the project was to practice balanced search trees, pointer-based tree logic, rotations, complexity analysis, and edge-case handling.

## Features

* AVL Tree implementation for key-value pairs
* Core dictionary operations:

  * `search`
  * `insert`
  * `delete`
* Advanced operations:

  * `finger_search`
  * `finger_insert`
  * `join`
  * `split`
  * `avl_to_array`
* AVL balancing logic:

  * Single rotations
  * Double rotations
  * Height updates
  * Balance factor calculation
* Tree utilities:

  * Find minimum node
  * Find maximum node
  * Find successor
  * Convert tree to sorted array
* Operation metrics:

  * Number of edges during search/insert
  * Number of promote/rebalancing cases

## Technologies

* Python
* Object-Oriented Programming
* Data Structures

## Main Concepts Practiced

* AVL Tree structure and invariants
* Binary search tree operations
* Tree rotations
* Recursive and iterative tree traversal
* Join and split operations
* Finger search optimization
* Complexity analysis
* Debugging pointer-based data structures

## Project Structure

```text
AVLTree.py
```

The main file contains:

* `AVLNode` — represents a node in the AVL Tree
* `AVLTree` — contains the tree implementation and all supported operations

## Example Usage

```python
tree = AVLTree()

tree.insert(10, "A")
tree.insert(5, "B")
tree.insert(15, "C")

node, edges = tree.search(5)

tree.delete(node)

array = tree.avl_to_array()
```

## Team

This project was developed by:

* Ksenia Iaremenko
* Iris Pustylnik

## Notes

This project was created for academic purposes as part of a university Data Structures course.
