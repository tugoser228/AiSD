# Задание1
from collections import deque

# Узел BST — простой контейнер
class BSTNode:
    pass

def make_bst_node(key):
    node = BSTNode()
    node.key = key
    node.left = None
    node.right = None
    return node

class BST:
    # ---- Вставка ----
    def insert(self, key):
        parent = None
        current = getattr(self, "root", None)
        while current is not None:
            parent = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                return  # дубликат — ничего не делаем
        new_node = make_bst_node(key)
        if parent is None:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

    # ---- Поиск ----
    def search(self, key):
        current = getattr(self, "root", None)
        while current is not None:
            if key == current.key:
                return current
            current = current.left if key < current.key else current.right
        return None

    # ---- Минимум / максимум ----
    def find_min(self, start_node=None):
        cur = getattr(self, "root", None) if start_node is None else start_node
        while cur and cur.left:
            cur = cur.left
        return cur

    def find_max(self, start_node=None):
        cur = getattr(self, "root", None) if start_node is None else start_node
        while cur and cur.right:
            cur = cur.right
        return cur

    # ---- Удаление ----
    def delete(self, key):
        def delete_rec(node, key):
            if node is None:
                return None
            if key < node.key:
                node.left = delete_rec(node.left, key)
            elif key > node.key:
                node.right = delete_rec(node.right, key)
            else:
                if node.left is None: return node.right
                if node.right is None: return node.left
                succ = node.right
                while succ.left:
                    succ = succ.left
                node.key = succ.key
                node.right = delete_rec(node.right, succ.key)
            return node
        self.root = delete_rec(getattr(self, "root", None), key)

    # ---- Обходы ----
    def inorder(self):
        res = []
        def _in(node):
            if node:
                _in(node.left)
                res.append(node.key)
                _in(node.right)
        _in(getattr(self, "root", None))
        return res

    def preorder(self):
        res = []
        def _pre(node):
            if node:
                res.append(node.key)
                _pre(node.left)
                _pre(node.right)
        _pre(getattr(self, "root", None))
        return res

    def postorder(self):
        res = []
        def _post(node):
            if node:
                _post(node.left)
                _post(node.right)
                res.append(node.key)
        _post(getattr(self, "root", None))
        return res

    def breadth_first(self):
        res = []
        root = getattr(self, "root", None)
        if not root:
            return res
        q = deque([root])
        while q:
            n = q.popleft()
            res.append(n.key)
            if n.left: q.append(n.left)
            if n.right: q.append(n.right)
        return res

# Задание 2
from collections import deque

class AVLNode:
    pass

def make_avl_node(key):
    node = AVLNode()
    node.key = key
    node.left = None
    node.right = None
    node.height = 1
    return node

class AVLTree:
    # вспомогательные
    def height_of(self, node):
        return node.height if node else 0

    def update_height(self, node):
        node.height = 1 + max(self.height_of(node.left), self.height_of(node.right))

    def balance_factor(self, node):
        return self.height_of(node.left) - self.height_of(node.right)

    # повороты
    def rotate_right(self, y):
        x = y.left
        if x is None:
            return y
        y.left = x.right
        x.right = y
        self.update_height(y)
        self.update_height(x)
        return x

    def rotate_left(self, x):
        y = x.right
        if y is None:
            return x
        x.right = y.left
        y.left = x
        self.update_height(x)
        self.update_height(y)
        return y

    def rebalance_node(self, node):
        self.update_height(node)
        bf = self.balance_factor(node)
        # LL
        if bf > 1 and self.balance_factor(node.left) >= 0:
            return self.rotate_right(node)
        # LR
        if bf > 1 and self.balance_factor(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        # RR
        if bf < -1 and self.balance_factor(node.right) <= 0:
            return self.rotate_left(node)
        # RL
        if bf < -1 and self.balance_factor(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node

    # вставка (рекурсивно)
    def insert(self, key):
        def insert_rec(node, key):
            if node is None:
                return make_avl_node(key)
            if key < node.key:
                node.left = insert_rec(node.left, key)
            elif key > node.key:
                node.right = insert_rec(node.right, key)
            else:
                return node
            return self.rebalance_node(node)
        self.root = insert_rec(getattr(self, "root", None), key)

    # поиск
    def search(self, key):
        cur = getattr(self, "root", None)
        while cur:
            if key == cur.key:
                return cur
            cur = cur.left if key < cur.key else cur.right
        return None

    # удаление (рекурсивно)
    def delete(self, key):
        def min_node(node):
            while node.left:
                node = node.left
            return node

        def delete_rec(node, key):
            if node is None:
                return None
            if key < node.key:
                node.left = delete_rec(node.left, key)
            elif key > node.key:
                node.right = delete_rec(node.right, key)
            else:
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                succ = min_node(node.right)
                node.key = succ.key
                node.right = delete_rec(node.right, succ.key)
            return self.rebalance_node(node) if node else None
        self.root = delete_rec(getattr(self, "root", None), key)

    # обходы
    def inorder(self):
        result = []
        def inorder_recursive(node):
            if node is None:
                return
            inorder_recursive(node.left)
            result.append(node.key)
            inorder_recursive(node.right)
        inorder_recursive(getattr(self, "root", None))
        return result

    def preorder(self):
        result = []
        def preorder_recursive(node):
            if node is None:
                return
            result.append(node.key)
            preorder_recursive(node.left)
            preorder_recursive(node.right)
        preorder_recursive(getattr(self, "root", None))
        return result

    def postorder(self):
        result = []
        def postorder_recursive(node):
            if node is None:
                return
            postorder_recursive(node.left)
            postorder_recursive(node.right)
            result.append(node.key)
        postorder_recursive(getattr(self, "root", None))
        return result

    def breadth_first(self):
        result = []
        root = getattr(self, "root", None)
        if root is None:
            return result
        q = deque([root])
        while q:
            n = q.popleft()
            result.append(n.key)
            if n.left: q.append(n.left)
            if n.right: q.append(n.right)
        return result

# Задание 3
from collections import deque

RED = "R"
BLACK = "B"

class RBNode:
    def __init__(self, key=None, parent=None, color=BLACK):
        self.key = key
        self.left = None
        self.right = None
        self.parent = parent
        self.color = color

    def __repr__(self):
        return f"RBNode({self.key},{self.color})"

# Единый NIL-узел
NIL = RBNode(key=None, parent=None, color=BLACK)
NIL.left = NIL.right = NIL.parent = NIL

class RedBlackTree:
    def __init__(self):
        self.root = NIL

    # ---- Поиск ----
    def search(self, key):
        node = self.root
        while node is not NIL and node.key != key:
            node = node.left if key < node.key else node.right
        return None if node is NIL else node

    def tree_minimum(self, node=None):
        node = self.root if node is None else node
        if node is NIL:
            return None
        while node.left is not NIL:
            node = node.left
        return node

    def tree_maximum(self, node=None):
        node = self.root if node is None else node
        if node is NIL:
            return None
        while node.right is not NIL:
            node = node.right
        return node

    # ---- Повороты ----
    def left_rotate(self, x):
        y = x.right
        if y is NIL:
            return
        x.right = y.left
        if y.left is not NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is NIL:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, y):
        x = y.left
        if x is NIL:
            return
        y.left = x.right
        if x.right is not NIL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is NIL:
            self.root = x
        elif y is y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    # ---- Вставка ----
    def insert(self, key):
        new_node = RBNode(key=key, parent=NIL, color=RED)
        new_node.left = new_node.right = NIL
        parent = NIL
        current = self.root
        while current is not NIL:
            parent = current
            if new_node.key < current.key:
                current = current.left
            elif new_node.key > current.key:
                current = current.right
            else:
                return  # дубликат
        new_node.parent = parent
        if parent is NIL:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._insert_fixup(new_node)

    def _insert_fixup(self, z):
        while z.parent.color == RED:
            if z.parent is z.parent.parent.left:
                uncle = z.parent.parent.right
                if uncle.color == RED:
                    z.parent.color = BLACK
                    uncle.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z is z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.right_rotate(z.parent.parent)
            else:
                uncle = z.parent.parent.left
                if uncle.color == RED:
                    z.parent.color = BLACK
                    uncle.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z is z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.left_rotate(z.parent.parent)
        self.root.color = BLACK

    # ---- Удаление ----
    def _transplant(self, u, v):
        if u.parent is NIL:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete(self, key):
        z = self.search(key)
        if not z:
            return
        y = z
        y_original_color = y.color
        if z.left is NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right is NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = z.right
            while y.left is not NIL:
                y = y.left
            y_original_color = y.color
            x = y.right
            if y.parent is z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == BLACK:
            self._delete_fixup(x)

    def _delete_fixup(self, x):
        while x != self.root and x.color == BLACK:
            if x is x.parent.left:
                w = x.parent.right
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self.right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = BLACK

    # ---- Обходы ----
    def inorder(self):
        res = []
        def _in(node):
            if node is NIL:
                return
            _in(node.left)
            res.append(node.key)
            _in(node.right)
        _in(self.root)
        return res

    def breadth_first(self):
        res = []
        if self.root is NIL:
            return res
        q = deque([self.root])
        while q:
            node = q.popleft()
            res.append((node.key, node.color))
            if node.left is not NIL:
                q.append(node.left)
            if node.right is not NIL:
                q.append(node.right)
        return res

    # ---- Проверка свойств ----
    def validate_rb_properties(self) -> bool:

        if self.root is NIL:
            return True

        # 2) Корень чёрный
        if self.root.color != BLACK:
            return False

        # 4) У красного узла оба потомка — чёрные
        def no_red_parent_child(node):
            if node is NIL:
                return True
            if node.color == RED:
                if node.left.color == RED or node.right.color == RED:
                    return False
            return no_red_parent_child(node.left) and no_red_parent_child(node.right)

        if not no_red_parent_child(self.root):
            return False

        # 5) Проверка одинаковой чёрной высоты на всех путях
        black_counts = []

        def dfs_count(node, count):
            if node.color == BLACK:
                count += 1
            if node is NIL:
                black_counts.append(count)
                return
            dfs_count(node.left, count)
            dfs_count(node.right, count)

        dfs_count(self.root, 0)

        return len(set(black_counts)) == 1

