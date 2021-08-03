# coding:utf-8
class Node(object):
    def __init__(self, elem):
        self.elem = elem
        self.next = None


class SingleLink(object):
    def __init__(self):
        self._head = None

    def is_empty(self):
        """链表是否为空"""
        return self._head == None

    def length(self):
        """链表长度"""
        # cur游标，用来移动遍历节点
        cur = self._head
        # count记录数据
        count = 0
        while cur != None:
            count += 1
            cur = cur.next
        return count

    def travel(self):
        """遍历整个链表"""
        # cur游标，用来移动遍历节点
        cur = self._head
        # count记录数据
        count = 0
        while cur != None:
            print(cur.elem)
            cur = cur.next

    def append(self, item):
        """尾部插入节点"""
        node = Node(item)
        if self.is_empty():
            self._head = node
        else:
            cur = self._head
            while cur.next != None:
                cur = cur.next
            cur.next = node


if __name__ == '__main__':
    ll = SingleLink()
    print(ll.is_empty())
    print(ll.length())

    ll.append(1)
    print(ll.is_empty())
    print(ll.length())

    ll.append(2)
    ll.append(3)
    ll.append(4)
    ll.append(5)
    ll.travel()
