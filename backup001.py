import os
import re

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
            dictionary[proc_name] = {'write': {}, 'read': {}}

        if proc_file not in dictionary[proc_name][proc_type].keys():
            dictionary[proc_name][proc_type][proc_file] = proc_size
        else:
            dictionary[proc_name][proc_type][proc_file] += proc_size

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
        print(k1, dictionary[k1])
        data_output2.write('{0:16}'.format(k1))
        # data_output2.write('\n')
        data_output2.write('write to ')

        wrs = ''
        for k2 in dictionary[k1]['write'].keys():
            wrs += (k2 + '(' + str(dictionary[k1]['write'][k2]) + ') , ')

        wrs = re.sub(r' , $', '', wrs)
        data_output2.write(wrs)

        data_output2.write('\n                ')
        data_output2.write('read to ')

        wrs = ''
        for k2 in dictionary[k1]['read'].keys():
            wrs += (k2 + '(' + str(dictionary[k1]['read'][k2]) + ') , ')

        wrs = re.sub(r' , $', '', wrs)
        data_output2.write(wrs)

        data_output2.write('\n')

    return

def main():
    CreateSummaryFiles('process2.log', 'summary1.log', 'summary2.0.log')

if __name__ == '__main__':
    main()