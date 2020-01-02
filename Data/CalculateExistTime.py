import re
import pandas as pd
import argparse

class Process:
    def __init__(self, *args):
        self.id = int(args[1])
        self.name = args[2]
        self.time = pd.to_datetime(args[3], format="%Y-%m-%d %H:%M:%S.%f")

class Record:
    def __init__(self, id, time):
        self.id = id
        self.time = time

class Node:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.parent = None
        self.children = []

    def SetParent(self, parent):
        self.parent = parent

    def RemoveChild(self, child):
        for i in range(len(self.children)):
            if child.id == self.children[i].id and child.name == self.children[i].name:
                temp = self.children[i]
                del self.children[i]
                return temp

    def IsChild(self, child):
        for c in self.children:
            if child.id == c.id and child.name == c.name:
                return True
        return False

    def FindChild(self, child):
        result = None
        for c in self.children:
            if child.id == c.id and child.name == c.name:
                return c
            result = c.FindChild(child)

            if result is not None:
                return result

        return None

    def AddChild(self, child):
        self.children.append(child)

def CleanElements(elements):
    for i in range(len(elements)):
        elements[i] = re.sub('^ *', '', elements[i])
        elements[i] = re.sub(' *$', '', elements[i])
    return elements

def UpdataGraph(root, temp_parent, temp_child):
    if root.IsChild((temp_child)):
        child = root.RemoveChild(temp_child)
    else:
        child = temp_child

    parent = root.FindChild(temp_parent)
    if parent is None:
        parent = temp_parent
        root.AddChild(parent)
        parent.SetParent(root)

    child.SetParent(parent)
    parent.AddChild(child)

    return root

def ProcessMatch(id_dict, elements, name_dict, root):
    id = int(elements[1])
    time = pd.to_datetime(elements[2], format="%Y-%m-%d %H:%M:%S.%f")
    pid = int(elements[3][4:])
    parent_name = elements[4]

    if id in id_dict.keys():
        p = id_dict[id]
        id_dict.pop(id)
        # print('{}: {}, {}'.format(p.name, p.id, (p.time - time)))

        if p.name not in name_dict.keys():
            name_dict[p.name] = []

        name_dict[p.name].append(Record(p.id, (p.time - time)))

        temp_parent = Node(pid, parent_name)
        temp_child = Node(p.id, p.name)
        root = UpdataGraph(root, temp_parent, temp_child)

    return id_dict, name_dict, root

def ShowGraph(node, counter):
    for i in range(counter):
        print('\t\t', end='')
    print('{}, {}'.format(node.id, node.name))
    for c in node.children:
        ShowGraph(c, counter+1)

def main(opts):
    data_file = open(opts.data_dir)
    data_lines = data_file.readlines()
    id_dict = {}
    name_dict = {}
    root = Node(0, 'root')

    for i in range(data_lines.__len__()-1, -1, -1):
        elements = CleanElements(data_lines[i][:-1].split('   '))
        if elements[0] == 'proexit':
            p = Process(*elements)
            if p.id in id_dict.keys():
                print('Error!')
                return
            else:
                id_dict[p.id] = p

        if elements[0] == 'clone':
            id_dict, name_dict, root = ProcessMatch(id_dict, elements, name_dict, root)

    for k in name_dict.keys():
        print(k)
        for l in name_dict[k]:
            print('    {}, {}'.format(l.id, l.time))

    ShowGraph(root, 0)

    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='result.txt')
    opts = parser.parse_args()
    main(opts)