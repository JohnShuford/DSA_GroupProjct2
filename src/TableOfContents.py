# !pip install pypdf
from pypdf import PdfReader

def importText(book):
    reader = PdfReader(book)
    page = reader.pages
    content = ['n', 'n']
    for chapter in range(1, 3):
        page = reader.pages[chapter]
        content[chapter-1] = page.extract_text().split('\n')

    full_text = [item for sublist in content for item in sublist]

    stripped = []
    
    for item in full_text:
        newItem = item.replace(' .', '')
        stripped.append(newItem)

    stripped.remove('Contents')
    stripped.remove('2')
    stripped.remove('3')

    basket = []
    
    for element in stripped:
        firstSplit = element.split(' ', 1)
        lastSplit = firstSplit[1].rsplit(' ', 1)
        combine = [firstSplit[0], lastSplit[0], lastSplit[-1]]
        basket.append(combine)
    
    return basket

class Node:
    def __init__(self, title):
        self.children = []
        self.title = title

    def addChild(self, title):
        self.children.append(Node(title))
        return self
    
    def __repr__(self, level=0):
        ret = "\t"*level+repr(self.title)+"\n"
        for child in self.children:
            ret += child.__repr__(level+1)
        return ret


def insertTOC(bookName, contents):
    tree = Node(bookName)
    for chapter in contents[1:]:
        dot = chapter[0]
        dotCount = dot.count('.')
        if dotCount == 0:
            tree.addChild(chapter[1])
        elif dotCount == 1:
            tree.children[-1].addChild(chapter[1])
        else:
            tree.children[-1].children[-1].addChild(chapter[1])

    return tree

def preorder_traversal(node):
    if node is None:
        return None
    print(node.title)
    for child in node.children:
        preorder_traversal(child)


def postorder_traversal(node):
    if node is None:
        return None
    for child in node.children:
        postorder_traversal(child)
    print(node.title)


def level_order_traversal(node):
    if node is None:
        return None
    
    queue = [node]
    while len(queue) > 0:
        current = queue[0]
        print(current.title)
        
        new_queue = []
        for i in range(1, len(queue)):
            new_queue.append(queue[i])
        queue = new_queue
        
        for child in current.children:
            queue.append(child)

def insert(root, path, title):
   
    current = root
    for i in range(len(path)):
        idx = path[i] - 1 

        while len(current.children) <= idx:
            current.children.append(Node(f"Placeholder {len(current.children) + 1}"))

        current = current.children[idx]

    current.addChild(title)

def print_toc(node, mode="plain", level=0, prefix=""):
    
    if node is None:
        return

    if mode == "plain":
        print(node.title)

    elif mode == "indented":
        print("    " * level + node.title)

    elif mode == "numbered":
        current_num = prefix + str(level) if level > 0 else ""
        if current_num != "":
            print(current_num + " " + node.title)
        else:
            print(node.title)

    for i, child in enumerate(node.children):
        if mode == "numbered":
            new_prefix = prefix + str(i + 1) + "."
            print_toc(child, mode, level + 1, new_prefix)
        else:
            print_toc(child, mode, level + 1)

def depth(root, title, current_depth=0):
    if root.title == title:
        return current_depth

    for child in root.children:
        d = depth(child, title, current_depth + 1)
        if d != -1:
            return d
    return -1

def height(node):
    if node is None:
        return 0
    if len(node.children) == 0:
        return 1
    max_height = 0
    for child in node.children:
        h = height(child)
        if h > max_height:
            max_height = h
    return max_height + 1
