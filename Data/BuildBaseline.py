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

def ProgNameOnlyBin(dictionary, proc_name):
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

def ProgNameWithIDBin(dictionary, proc_name, proc_tid, result_w, result_r):
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

def ProgNameOnlySoft(dictionary, proc_name):
    if proc_name not in dictionary.keys():
        print("Not found the {} process.".format(proc_name))
        return None, None

    print("{} processes found.".format(proc_name))

    counter_read_dict = {}
    counter_write_dict = {}

    for k1 in dictionary[proc_name].keys():
        for k2 in dictionary[proc_name][k1]['read'].keys():
            if k2 not in counter_read_dict.keys():
                counter_read_dict[k2] = 1
            else:
                counter_read_dict[k2] += 1
        for k2 in dictionary[proc_name][k1]['write'].keys():
            if k2 not in counter_write_dict.keys():
                counter_write_dict[k2] = 1
            else:
                counter_write_dict[k2] += 1
    # print(counter_read_dict)
    # print(counter_write_dict)
    print("Read List")

    for c in counter_read_dict.keys():
        print("{}: {:.2%}".format(c, counter_read_dict[c] / len(dictionary[proc_name].keys())))

    print("Write List")

    for c in counter_write_dict.keys():
        print("{}: {:.2%}".format(c, counter_write_dict[c] / len(dictionary[proc_name].keys())))



    return counter_write_dict, counter_read_dict

def ProgNameWithIDSoft(dictionary, proc_name, proc_tid, result_w, result_r):
    if proc_tid not in dictionary[proc_name].keys():
        print("Not found pid {}.".format(proc_tid))
        return

    print("New read list for {}".format(proc_tid))

    print("New read list for {}".format(proc_tid))
    for s in dictionary[proc_name][proc_tid]['read'].keys():
        # if s not in result_r.keys():
        # print(result_r[s] / len(dictionary[proc_name].keys()))
        print('{}: {:.2%}'.format(s, 1 * (result_r[s] / len(dictionary[proc_name].keys()))))

    print("New write list for {}".format(proc_tid))
    for s in dictionary[proc_name][proc_tid]['write'].keys():
        # if s not in result_w.keys():
        print('{}: {:.2%}'.format(s, 1 * (result_w[s] / len(dictionary[proc_name].keys()))))

def main(opts):
    dictionary = CreateSummaryFiles(opts.input_dir)
    # result_w, result_r = ProgNameOnlyBin(dictionary, opts.prog_name)
    result_w, result_r = ProgNameOnlySoft(dictionary, opts.prog_name)
    ProgNameWithIDSoft(dictionary, opts.prog_name, opts.pid, result_w, result_r)
    # if opts.pid != 0 and result_w == None and result_r==None:
    #     ProgNameWithIDBin(dictionary, opts.prog_name, opts.pid, result_w, result_r)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, default='process2.log')
    # parser.add_argument('--summary1_dir', type=str, default='summary1.log')
    # parser.add_argument('--summary2_dir', type=str, default='summary2.log')
    parser.add_argument("--prog_name", type=str, default='sh')
    # parser.add_argument("--pid", type=int, default=8688)
    parser.add_argument("--pid", type=int, default=14227)
    opts = parser.parse_args()
    main(opts)