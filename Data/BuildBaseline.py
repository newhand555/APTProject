import os
import re
import argparse

def CreateSummaryFiles(inpath):
    data_file = open(inpath)
    dictionary = {}

    for line in data_file:
        elements = line.split(' ')
        proc_name = elements[2]
        proc_tid = int(elements[3])
        proc_direct = elements[4]
        proc_type = elements[5]

        if not (((proc_type == 'write' or proc_type == 'read') and proc_direct == '>') or (proc_type == 'openat' and proc_direct == '<')):
            continue

        if proc_type == 'openat':
            if re.search('O_RDONLY', line) != None:
                proc_type = 'read'
            elif re.search('O_RDRW', line) != None:
                proc_type = 'write'
            else:
                continue
            proc_size = 0

        else:
            proc_size = int(re.sub('size=', '', elements[7]))

        proc_file = re.sub(r'.*\(', '', elements[6])[:-1]

        if proc_name not in dictionary.keys():
            dictionary[proc_name] = {}
            # dictionary[proc_name] = {'write': {}, 'read': {}}
        if proc_tid not in dictionary[proc_name].keys():
            dictionary[proc_name][proc_tid] = {'write': {}, 'read': {}}

        if proc_file not in dictionary[proc_name][proc_tid][proc_type].keys():
            dictionary[proc_name][proc_tid][proc_type][proc_file] = proc_size
        else:
            dictionary[proc_name][proc_tid][proc_type][proc_file] += proc_size

    return dictionary

def ProgNameOnly(dictionary, proc_name):
    # print(dictionary['grep'][1260]['write'])
    if proc_name not in dictionary.keys():
        print("Not found the {} process.".format(proc_name))
        return None, None

    print("{} processes found.".format(proc_name))

    flag = True
    for k in dictionary[proc_name].keys():
        if flag == True:
            flag = False
            result_w = set(dictionary[proc_name][k]['write'].keys())
            result_r = set(dictionary[proc_name][k]['read'].keys())
        else:
            result_w = set.intersection(set(dictionary[proc_name][k]['write'].keys()), result_w)
            result_r = set.intersection(set(dictionary[proc_name][k]['read'].keys()), result_r)

    print("Read List")
    for s in result_r:
        print(s)
    print("Write List")
    for s in result_w:
        print(s)

    return result_w, result_r

def ProgNameWithID(dictionary, proc_name, proc_tid, result_w, result_r):
    if proc_tid not in dictionary[proc_name].keys():
        print("Not found pid {}.".format(proc_tid))
        return

    print("New read list for {}".format(proc_tid))
    for s in dictionary[proc_name][proc_tid]['read'].keys():
        if s not in result_r:
            print(s)

    print("New write list for {}".format(proc_tid))
    for s in dictionary[proc_name][proc_tid]['write'].keys():
        if s not in result_w:
            print(s)

def main(opts):
    dictionary = CreateSummaryFiles(opts.input_dir)
    result_w, result_r = ProgNameOnly(dictionary, opts.prog_name)
    if opts.pid != 0 and result_w == None and result_r==None:
        ProgNameWithID(dictionary, opts.prog_name, opts.pid, result_w, result_r)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, default='process2.log')
    # parser.add_argument('--summary1_dir', type=str, default='summary1.log')
    # parser.add_argument('--summary2_dir', type=str, default='summary2.log')
    parser.add_argument("--prog_name", type=str, default='grep')
    # parser.add_argument("--pid", type=int, default=8688)
    parser.add_argument("--pid", type=int, default=14227)
    opts = parser.parse_args()
    main(opts)