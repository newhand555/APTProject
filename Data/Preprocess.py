import os
import re

def main():
    data_file = open('process2.log')
    current_name = ''
    current_tid = 0
    current_type = ''
    current_file = ''
    current_amount = 0
    dictionary = {}
    data_output1 = open('output1.log', 'w')
    data_output2 = open('output2.log', 'w')

    for line in data_file:
        elements = line.split(' ')
        proc_name = elements[2]
        proc_tid = int(elements[3])
        proc_direct = elements[4]
        proc_type = elements[5]

        if (proc_type != 'write' and proc_type != 'read') or proc_direct != '>':
            continue

        proc_file = re.sub(r'.*\(', '', elements[6])[:-1]
        proc_size = int(re.sub('size=', '', elements[7]))

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

if __name__ == '__main__':
    main()