class LinkedNode:
    __slots__ = ["val", "idx", "heap_idx", "next", "prev"]

    def __init__(self, idx, prev, next):
        self.idx = idx
        #self.val = val
        self.next = next
        self.prev = prev

class LinkedList:
    def __init__(self):
        self.root = None
        #self.back = self.root
        self.size = 0

    def push_back(self, idx):
        if hasattr(self, "back"):
            self.back.next = LinkedNode(idx, self.back, None)
            self.back = self.back.next
        else:
            self.root = LinkedNode(idx, None, None)
            self.back = self.root
        self.size += 1

    def assign_vals(self, series):
        curr_node = self.root
        if curr_node is not None:
            while curr_node.next is not None:
                curr_node.val = abs(series[curr_node.next.idx].val - series[curr_node.idx].val)
                curr_node = curr_node.next

    def push_front(self, val):
        temp = LinkedNode(val, None, self.root)
        self.root = temp

    def del_idx(self, idx):
        incr = 1
        attr_name = "next"
        curr_idx = 0
        curr_node = self.root
        if idx > self.size/2:
            curr_idx = self.size - 1
            incr = -1
            curr_node = self.back
            attr_name = "prev"
        while not (curr_idx == idx):
            curr_idx += incr
            curr_node = getattr(curr_node, attr_name)
        if curr_node is not self.root:
            curr_node.prev.next = curr_node.next
        else:
            self.root = curr_node.next
        if curr_node is not self.back:
            curr_node.next.prev = curr_node.prev
        else:
            self.back = curr_node.prev
        del curr_node
        self.size -= 1

    def del_node(self, node_ref):
        if node_ref is not self.root:
            node_ref.prev.next = node_ref.next
        else:
            self.root = node_ref.next
        if node_ref is not self.back:
            node_ref.next.prev = node_ref.prev
        else:
            self.back = node_ref.prev
        self.size -= 1

    def show_list(self):
        curr_node = self.root
        while True:
            print (str(curr_node.val), end="")
            if curr_node.next is not None:
                print (" -> ", end="")
                curr_node = curr_node.next
            else:
                break
        print ()

    def make_ordinary_list(self):
        ret_list = [None for i in range(self.size)]
        idx = 0
        curr_node = self.root
        while curr_node is not None:
            ret_list[idx] = curr_node
            curr_node = curr_node.next
            idx += 1
        return ret_list

    def make_pos_list(self):
        curr_node = self.root
        pos = []

        while curr_node is not None:
            pos.append(curr_node.idx)
            curr_node = curr_node.next

        return pos

def main():
    my_list = LinkedList()
    for i in range(5):
        my_list.push_back(i + 10)
    lst = my_list.make_ordinary_list()
    print (lst)

if __name__ == "__main__":
    main()