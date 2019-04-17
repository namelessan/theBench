#!/usr/bin/env python3

import json
import sys


def load_query():
    list_args = sys.argv
    filename = list_args[list_args.index('./smart_db.py') + 1]
    # print(filename)
    with open(filename, 'r') as json_file:
        json_data = json.load(json_file)
    json_file.close()
    return json_data


def compare(a, b, c):
    if b == '=' and a == c:
        return True
    elif b == '>' and a > c:
        return True
    elif b == '<' and a < c:
        return True
    elif b == '!=' and a != c:
        return True
    return False


def check_condition(query, data):  # format({},['a','b','c'])
    pos = {'first_name': 0, 'last_name': 1, 'username': 2, 'age': 3,
           'gender': 4, 'city': 5}
    for x in pos.keys():
        if x in query['left']:  # format x = 'fd'
            value = data[pos[x]]
            break
    if 'first_letter' in query['left']:  # case with condition: 'first_letter'
        value = value[0]
    elif 'age' in query['left']:
        #  if query['left'] == 'age' convert query['right'] to int to compare
        query['right'] = int(query['right'])
    return compare(value, query['op'], query['right'])


# main function
def main():
    result = []
    pos = {'first_name': 0, 'last_name': 1, 'username': 2, 'age': 3,
           'gender': 4, 'city': 5}
    lines = sys.stdin.readlines()  # read all of lines file csv
    query = load_query()  # get query
    for line in lines:
        line = line.split(',')
        line[3] = int(line[3])  # convert to interger (1)
        line[5] = line[5][:len(line[5]) - 1]
        for x in range(len(query)):
            result.append([])  # create a list in list for n query input
            flag = 1
            if "where_and" in query[x].keys():
                for a in query[x]['where_and']:
                    # x = {'left': 'fd','op': 'fd','right': 'fd'}
                    if check_condition(a, line) is False:
                        flag = 0
                        break
            elif "where_or" in query[x].keys():
                flag = 0
                for b in query[x]['where_or']:
                    # x = {'left': 'fd','op': 'fd','right': 'fd'}
                    if check_condition(b, line) is True:
                        flag = 1
                        break
            if flag == 1:
                result[x].append(line)

    for x in range(len(query)):
        final = []
        if 'order' in query[x].keys():
            # sort by order
            result[x].sort(key=lambda k: k[pos[query[x]['order']]])
        for y in result[x]:
            temp = []
            # select a field name in query[x]
            for z in query[x]['select'].split(", "):
                temp.append(y[pos[z]])
            final.append(temp)
        get_result(final)


# Because of joining to be a string we have to revert a field name to str.
def get_result(list1):
    for x in range(len(list1)):
        for e in range(len(list1[x])):
            list1[x][e] = str(list1[x][e])
        print(', '.join(list1[x]))


if __name__ == '__main__':
    main()
