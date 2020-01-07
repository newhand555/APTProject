# BuildBaseline.py
import re

def NameOnly(inpath, pname):
    data_file = open(inpath)

    read_list = set()
    write_list = set()

    for line in data_file:
        elements = line.split(' ')
        proc_name = elements[2]
        proc_tid = int(elements[3])
        proc_direct = elements[4]
        proc_type = elements[5]

        if (proc_type != 'write' and proc_type != 'read') or proc_direct != '>' or proc_name != pname:
            continue

        proc_file = re.sub(r'.*\(', '', elements[6])[:-1]

        if proc_type == 'read':
            read_list.add(proc_file)
        else:
            write_list.add(proc_file)

    print(proc_name+" processes found.")
    print("Read list")

    for e in read_list:
        print(e)

    print("Write list")

    for e in write_list:
        print(e)
    return

def NameWithPID(inpath, pname, pid):
    data_file = open(inpath)

    read_list = set()
    write_list = set()

    for line in data_file:
        elements = line.split(' ')
        proc_name = elements[2]
        proc_tid = int(elements[3])
        proc_direct = elements[4]
        proc_type = elements[5]

        if (proc_type != 'write' and proc_type != 'read') or proc_direct != '>' or proc_name != pname or pid != proc_tid:
            continue

        proc_file = re.sub(r'.*\(', '', elements[6])[:-1]

        if proc_type == 'read':
            read_list.add(proc_file)
        else:
            write_list.add(proc_file)

    print(proc_name + " processes found.")
    print(pid + " executed with the following command,")
    print("Read list")

    for e in read_list:
        print(e)

    print("Write list")

    for e in write_list:
        print(e)
    return

def main():
    NameOnly('process2.log', 'grep')

if __name__ == '__main__':
    main()