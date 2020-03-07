import re
import pandas as pd
import argparse

class Node:
    def __init__(self):
        self.type = None

class ProcessNode(Node):
    def __init__(self, pid, time):
        super(Node, self).__init__()
        self.type = 'proc'
        self.pid = pid
        self.time = time
        self.parent = None
        self.children = []
        self.files = set()
        self.active = True

    def SetParent(self, parent):
        self.parent = parent

    def RemoveChild(self, child):
        for i in range(len(self.children)):
            if child.pid == self.children[i].pid and child.time == self.children[i].name:
                temp = self.children[i]
                del self.children[i]
                return temp

    def IsChild(self, child):
        for c in self.children:
            if child.pid == c.pid and child.time == c.name:
                return True
        return False

    def FindChild(self, child):
        result = None
        for c in self.children:
            if child.pid == c.pid and child.time == c.time:
                return c
            result = c.FindChild(child)

            if result is not None:
                return result
        return None

    def FindActiveDescend(self, ppid):
        result = None
        for c in self.children:
            if ppid == c.pid and c.active == True:
                return c
            result = c.FindActiveDescend(ppid)
            if result is not None:
                return result
        return None

    def AddChild(self, child):
        self.children.append(child)

    def FindActiveChild(self, tid):
        for c in self.children:
            if tid == c.pid and c.active == True:
                return c
        return None

class FileNode(Node):
    def __init__(self, location):
        super(Node, self).__init__()
        self.type = 'file'
        self.location = location
        self.procs = set()

def CleanSpace(elements):
    for i in range(len(elements)):
        elements[i] = re.sub('^ *', '', elements[i])
        elements[i] = re.sub(' *$', '', elements[i])
    return elements

def ProcessClone(root, elements):
    ppid = int(elements[5][5:])
    temp_grand = root.FindActiveDescend(ppid)

    if temp_grand is None:
        temp_grand = ProcessNode(ppid, None)
        temp_grand.SetParent(root)
        root.AddChild(temp_grand)

    pid = int(elements[3][4:])
    temp_parent = temp_grand.FindActiveDescend(pid)

    if temp_parent is None:
        temp_parent = root.FindActiveChild(pid)

    if temp_parent is None:
        temp_parent = ProcessNode(pid, None)
        temp_parent.SetParent(temp_grand)
        temp_grand.AddChild(temp_parent)

    tid = int(elements[1])
    time = pd.to_datetime(elements[2], format="%Y-%m-%d %H:%M:%S.%f")
    temp_child = ProcessNode(tid, time)
    temp_child.SetParent(temp_parent)
    temp_parent.AddChild(temp_child)

def ProcessProcexit(root, elements):
    pid = int(elements[2])
    temp_node = root.FindActiveDescend(pid)
    temp_node.active = False

def ProcessKill(root, elements):
    kid = int(elements[1])
    temp_node = root.FindActiveDescend(kid)
    temp_node.active = False
    return

def FindFileFromList(file_list, file):
    for f in file_list:
        if f.location == file:
            return f
    return None

def ProcessFile(root, file_list, elements):
    location = elements[5]
    temp_file = FindFileFromList(location)

    if temp_file is None:
        temp_file = FileNode(location)
        file_list.append(temp_file)

    tid = int(elements[4])
    temp_proc = root.FindActiveDescend(tid)

    if temp_proc is None:
        temp_proc = ProcessNode(tid, None)
        temp_proc.SetParent(root)
        root.AddChild(temp_proc)

    temp_file.procs.add(temp_proc)
    temp_proc.files.add(temp_file)

def ProcessRecord(root, file_list, record):
    elements = CleanSpace(record[:-1].split('   '))
    if elements[0] == 'clone':
        ProcessClone(root, elements)
    elif elements[0] == 'folk':
        return
    elif elements[0] == 'kill':
        ProcessKill()
        return
    elif elements[0] == 'procexit':
        ProcessProcexit()
        return
    elif elements[0] == 'file':
        ProcessFile()
        return
    elif elements[0] == 'network':
        return
    else:
        return None

def ShowGraph(node, counter):
    for i in range(counter):
        print('\t\t', end='')
    print('{}, {}'.format(node.pid, node.time))
    for c in node.children:
        ShowGraph(c, counter+1)

def main(opts):
    data_file = open(opts.data_dir)
    data_lines = data_file.readlines()
    root = ProcessNode(pid=-1, time=None)
    file_list = []
    for i in range(len(data_lines)):
        ProcessRecord(root, file_list, data_lines[i])

    ShowGraph(root, 0)
    tid = 20275
    time = pd.to_datetime('2019-12-30 18:26:33.457836947', format="%Y-%m-%d %H:%M:%S.%f")
    a = ProcessNode(tid, time)
    a = root.FindChild(a)
    print(a.children)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='result.txt')
    opts = parser.parse_args()
    main(opts)