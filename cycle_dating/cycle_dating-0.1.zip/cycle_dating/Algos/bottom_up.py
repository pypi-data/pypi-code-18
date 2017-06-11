import time

from cycle_dating.Utilities import use_data as ud, series
from cycle_dating.Algos import optim_virtual
from cycle_dating.Algos.Utilities.LinkedList import LinkedList


class Node:
    """
    defines a node, which will be used to store a value in the heap
    actual values are stored in the linked list. the node accesses the
    element in the linked list via the link variable
    comparison operators are also defined for convenience
    """
    __slots__ = ["link"]
    def __init__(self, link):
        self.link = link
    def __le__(self, other):
        return self.link.val <= other
    def __lt__(self, other):
        return self.link.val < other
    def __ge__(self, other):
        return self.link.val >= other
    def __gt__(self, other):
        return self.link.val > other
    def __eq__(self, other):
        return self.link.val == other
    def __ne__(self, other):
        return not (self.link.val == other)

class BU(optim_virtual.Optim):
    """
    Class implementation for BSA-BU algorithm

    Args:
        dim           (int): Number of buy-sell points, K
        long          (bool): True if long sequence if buy-sell points is required
        trans_cost    (float): transaction cost
        from_hierarch (bool): True if instance is used in hierarchical method, False if not
    """
    def __init__(self, dim, long=True, trans_cost=0.0, from_hierarch=False, **kwargs):
        self.ident = "BU"
        super().__init__(dim, long, trans_cost, from_hierarch)

    def get_name(self):
        return "BU"

    def get_params(self):
        return {"Name": self.get_name()}

    def set_data(self, data):
        super().set_data(data)
        self.data.fix_long_short(long=self.long)
        self.series = self.data.reduced
        self.pos = LinkedList()
        for idx in range(len(self.series)):
            self.pos.push_back(idx)
        self.pos.assign_vals(self.series)
        if self.dim > len(self.series):
            self.dim = len(self.series)
            return
        self.heap_create()

    def _optimise(self, **kwargs):
        while self.pos.size > self.dim:
            self.remove_lowest_el()
        self.pos = self.pos.make_pos_list()
        return self.pos, self.evaluate()

    def heap_create(self):
        ordinary_pos_list = self.pos.make_ordinary_list()
        self.node_list = [Node(link=link) for link in ordinary_pos_list[:-1]]
        self.heap = []
        for node in self.node_list:
            self.heap_insert(node)
        return self.heap

    def heap_insert(self, val):
        """inserts a value into the heap

        Args
            val (float): value to be inserted
        returns None
        """
        self.heap.append(val)
        val.link.heap_idx = len(self.heap) - 1
        n = len(self.heap) - 1
        self.heap_bubble_up(n)

    def heap_bubble_up(self, idx):
        """Adjust value at position idx

        called when an adjustment must be made. idx is the array index of the element
        that was removed. this function is called when the element that replaced
        the removed element at idx is smaller than its parent

        Args
            idx (int): index of element to be adjusted (in heap array)
        Returns:
            None
        """
        if idx > 0:
            parent_idx = (idx - 1)//2
            if self.heap[parent_idx] > self.heap[idx]:
                temp = self.heap[parent_idx]
                self.heap[parent_idx] = self.heap[idx]
                self.heap[idx] = temp
                self.heap[idx].link.heap_idx = idx
                self.heap[parent_idx].link.heap_idx = parent_idx
                idx = parent_idx
                self.heap_bubble_up(idx)

    def heap_bubble_down(self, idx):
        """Adjust value at position idx

        called when an adjustment must be made. idx is the array index of the element
        that was removed. this function is called when the element that replaced
        the removed element at idx is larger than one of its children

        Args
            idx (int): index of element to be adjusted (in heap array)
        Returns:
            None
        """
        child1_idx, child2_idx = 2*idx + 1, 2*idx + 2
        repl_value = float("inf")
        repl_idx = None
        try:
            if self.heap[child1_idx] < self.heap[idx]:
                repl_value = self.heap[child1_idx]
                repl_idx = child1_idx
        except IndexError:
            pass
        try:
            if self.heap[child2_idx] < self.heap[idx]:
                if self.heap[child2_idx] < repl_value:
                    repl_value = self.heap[child2_idx]
                    repl_idx = child2_idx
        except IndexError:
            pass
        if repl_idx is not None:
            temp = self.heap[repl_idx]
            self.heap[repl_idx] = self.heap[idx]
            self.heap[idx] = temp
            self.heap[repl_idx].link.heap_idx = repl_idx
            self.heap[idx].link.heap_idx = idx
            self.heap_bubble_down(repl_idx)

    def heap_remove(self, idx):
        """Remove a specific element from the heap, identified by idx

        Args
            idx (int): the index of the element in the heap array
        returns (Node):
            heap node that was removed
        """
        ret_val = self.heap[idx]
        self.heap[idx] = self.heap[-1]
        self.heap[idx].link.heap_idx = idx
        del self.heap[-1]
        if idx < len(self.heap):
            if self.heap[idx] > ret_val:
                self.heap_bubble_down(idx)
            elif self.heap[idx] < ret_val:
                self.heap_bubble_up(idx)
        return ret_val

    def remove_lowest_el(self):
        """Remove lowest element from the heap (the root)

        removes the lowest (topmost) element from the heap
        and adjusts the heap accordingly

        Returns:
            None
        """
        rem_node = self.heap[0]
        if rem_node.link.next is self.pos.back:
            self.pos.del_node(rem_node.link.next)
            self.heap_remove(rem_node.link.prev.heap_idx)
            self.heap_remove(rem_node.link.heap_idx)
            self.pos.del_node(rem_node.link)
        elif rem_node.link is self.pos.root:
            self.heap_remove(rem_node.link.heap_idx)
            self.heap_remove(rem_node.link.next.heap_idx)
            self.pos.del_node(rem_node.link.next)
            self.pos.del_node(rem_node.link)
        else:
            if rem_node.link is self.pos.back:
                print ("INVALID: rem_node.link is self.pos.back")
            try:
                self.heap_remove(rem_node.link.heap_idx)
                self.heap_remove(rem_node.link.next.heap_idx)
            except IndexError:
                while rem_node.link is not None:
                    print (rem_node.link.idx)
                    print (rem_node.link.next.heap_idx)
                    print (len(self.heap))
                    rem_node = self.heap[rem_node.link.next.heap_idx]
                raise IndexError
            new_first_link = rem_node.link.prev
            new_2nd_link = rem_node.link.next.next
            self.pos.del_node(rem_node.link.next)
            self.pos.del_node(rem_node.link)
            new_first_link.val = abs(self.series[new_2nd_link.idx].val - self.series[
            new_first_link.idx].val)
            self.heap_bubble_down(new_first_link.heap_idx)

def main2():
    bu_obj = BU(10, long=True)
    series_obj = series.Series(series_len=5000, seed=10)
    begin_time = time.time()
    bu_obj.set_data(series_obj)
    pos, fitness = bu_obj.optimise()
    print ("Time taken: ", time.time() - begin_time)
    ud.plot_solution(series_obj, pos, scatter=True, linewidth=2.3)

if __name__ == "__main__":
    main2()