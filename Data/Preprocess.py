import os
import re
import argparse

def CreateSummaryFiles(inpath, outpath1, outpath2):
    data_file = open(inpath)
    current_name = ''
    current_tid = 0
    current_type = ''
    current_file = ''
    current_amount = 0
    dictionary = {}
    data_output1 = open(outpath1, 'w')
    data_output2 = open(outpath2, 'w')

    for line in data_file:
        elements = line.split(' ')
        proc_name = elements[2]
        proc_tid = int(elements[3])
        proc_direct = elements[4]
        proc_type = elements[5]

        # print(elements)

        # if proc_type == 'openat' and proc_direct == '<':
        #     print()
        #if ((proc_type != 'write' and proc_type != 'read') or proc_direct != '>') and ():

        if not (((proc_type == 'write' or proc_type == 'read') and proc_direct == '>') or (proc_type == 'openat' and proc_direct == '<')):
            continue

        if proc_type == 'openat':
            proc_size = 0
            # print(line)
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

        if current_name != proc_name or current_type != proc_type or current_file != proc_file:
            if current_tid != 0:
                print('{}, {}, {}, {}, {}'.format(current_name, current_tid, current_type, current_file, current_amount))
                data_output1.write('{}, {}, {}, {}, {}\n'.format(current_name, current_tid, current_type, current_file, current_amount))
            current_name = proc_name
            current_tid = proc_tid
            current_type = proc_type
            current_file = proc_file
            current_amount = proc_size
        else:
            current_amount += proc_size
    if current_tid != 0:
        print('{}, {}, {}, {}, {}'.format(current_name, current_tid, current_type, current_file, current_amount))
        data_output1.write('{}, {}, {}, {}, {}\n'.format(current_name, current_tid, current_type, current_file, current_amount))

    for k1 in dictionary.keys():
        # print(k1, dictionary[k1])
        tempdict = {}

        for k2 in dictionary[k1].keys():
            for k3 in dictionary[k1][k2]['write'].keys():
                if k3 not in tempdict.keys():
                    tempdict[k3] = 0
                tempdict[k3] += dictionary[k1][k2]['write'][k3]

        data_output2.write('{0:16}'.format(k1))
        # data_output2.write('\n')
        data_output2.write('write to ')

        wrs = ''
        for k in tempdict.keys():
            wrs += (k + '(' + str(tempdict[k]) + ') , ')

        wrs = re.sub(r' , $', '', wrs)
        data_output2.write(wrs)

        data_output2.write('\n                ')
        data_output2.write('read to ')

        tempdict = {}

        for k2 in dictionary[k1].keys():
            for k3 in dictionary[k1][k2]['read'].keys():
                if k3 not in tempdict.keys():
                    tempdict[k3] = 0
                tempdict[k3] += dictionary[k1][k2]['read'][k3]

        wrs = ''
        # for k2 in dictionary[k1]['read'].keys():
        #     wrs += (k2 + '(' + str(dictionary[k1]['read'][k2]) + ') , ')
        #
        for k in tempdict.keys():
            wrs += (k + '(' + str(tempdict[k]) + ') , ')
        wrs = re.sub(r' , $', '', wrs)
        data_output2.write(wrs)

        data_output2.write('\n')

    return dictionary

def main(opts):
    dictionary = CreateSummaryFiles(opts.input_dir, opts.summary1_dir, opts.summary2_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, default='process2.log')
    parser.add_argument('--summary1_dir', type=str, default='summary1.log')
    parser.add_argument('--summary2_dir', type=str, default='summary2.log')
    # parser.add_argument("--prog_name", type=str, default='grep')
    # parser.add_argument("--pid", type=int, default=8688)
    # parser.add_argument("--pid", type=int, default=14227)
    opts = parser.parse_args()
    main(opts)