# -*- coding: cp936 -*-
import json
import sys

danger_check_file = './finalResult/validation_result_'
file_header = ''
extracted_dir = './extractedJson'
link_result_dir = '../cloneEvo/LinkResults'
output_file = './ModifyType_'
placeholders = ['%A', '%a', '%C', '%c', '%d', '%E', '%f', '%g', '%G', '%i', '%o', '%p', '%s', '%x', '%X', '%%']

clone_group_ids = dict()
clone_group_info = dict()
group_id_list = list()

def init():
    global file_header
    index = 0
    f = open(danger_check_file, 'r')
    for line in f:
        if index == 0:
            file_header = line.strip()
            index += 1
            continue
        line = line.strip()
        tmp = line.split(',')
        clone_group_ids[tmp[0]] = set()
        clone_group_info[tmp[0]] = line
        group_id_list.append(tmp[0])
    f.close()

def get_modify_type(code1, code2):
    """识别代码修改的类型，2表示变量格式化，3表示变量初始化，4表示其他"""
    code1_set = set(code1.split('\n'))
    code2_set = set(code2.split('\n'))
    code_list1 = code1.split('\n')
    code_list2 = code2.split('\n')
    first1Line = code_list1[0].replace('\t', '')
    first2Line = code_list2[0].replace('\t', '')
    code1_diff_list = list(code1_set.difference(code2_set))
    code2_diff_list = list(code2_set.difference(code1_set))
    code1_diff_list = [code.replace('\t', '') for code in code1_diff_list if code != '']
    code2_diff_list = [code.replace('\t', '') for code in code2_diff_list if code != '']

    tmp_code1 = code1.replace('\n', '').replace(' ', '')
    tmp_code2 = code2.replace('\n', '').replace(' ', '')
    if tmp_code1 == tmp_code2 and tmp_code1 != '':
        return '2'

    code1_diff_list.sort()
    code2_diff_list.sort()
    cnt = 0

    
    typeThree = ''
    typeSet = set()
    for diff in code1_diff_list:
        if '=' in diff:
            temp = diff.split('=')
            num = temp[1].replace(' ', '').replace(';', '')
            diffLen = len(diff)
            if('(' not in num):
                typeSet.add('3')

    for diff in code2_diff_list:
        if '=' in diff:
            temp = diff.split('=')
            num = temp[1].replace(' ', '').replace(';', '')
            diffLen = len(diff)
            if('(' not in num):
                typeSet.add('3')

    for diff in code1_diff_list:
        if "if" in diff:
            typeSet.add('4')
        if "for" in diff:
            typeSet.add('5')
        if "case" in diff:
            typeSet.add('6')
        for placeholder in placeholders:
            if placeholder in diff:
                typeSet.add('7')
                break
        if first1Line in diff:
            typeSet.add('8')
    for diff in code2_diff_list:
        if "if" in diff:
            typeSet.add('4')
        if "for" in diff:
            typeSet.add('5')
        if "case" in diff:
            typeSet.add('6')
        for placeholder in placeholders:
            if placeholder in diff:
                typeSet.add('7')
                break
        if first2Line in diff:
            typeSet.add('8')
    if(len(typeSet) == 0):
        typeSet.add('9')
    
    return typeSet

def process():
    cnt = 0
    for group_id in clone_group_ids:
        cnt += 1
        print('%.2f%%' % (cnt * 100.0 / len(clone_group_ids)))
        with open('%s/%s.json' % (link_result_dir, group_id), 'r') as fLink:
            try:
                commitsLink = json.load(fLink)
            except Exception as e:
                clone_group_ids[group_id].add('0')
                print(group_id + "-----")
                continue
            for commit in commitsLink:
                for code in commit['codes']:
                    if 'methodName' in code:
                        if '[' in code['methodName']:
                            clone_group_ids[group_id].add('1')
                            break
        if('1' in clone_group_ids[group_id]):
            continue
        with open('%s/%s.json' % (extracted_dir, group_id), 'r') as f:
            try:
                commitsExtracted = json.load(f)
            except Exception as e:
                clone_group_ids[group_id].add('0')
                print(group_id + "-----")
                continue
            for commit in commitsExtracted:
                #print(clone_group_info[group_id])
                infoArr = clone_group_info[group_id].split(',')
                if(infoArr[8] == '0'):
                    clone_group_ids[group_id].add('0')
                    break
                for code in commit['codes']:
                    if code['status'] == 'M':
                        modify_type = get_modify_type(code['preCode'], code['curCode'])
                        clone_group_ids[group_id] = modify_type
    pass

def output():
    global file_header
    file_header += ',ModifyType\n'
    f = open(output_file, 'w', encoding='utf8')
    f.write(file_header)
    for group_id in group_id_list:
        modify_type = clone_group_ids[group_id]
        modify_type_str = '@'.join(modify_type)
        if('0' in modify_type_str):
            modify_type_str = '0'
        line = clone_group_info[group_id] + ',' + modify_type_str + '\n'
        f.write(line)
    f.close()
    pass


if __name__ == '__main__':
    proName = sys.argv[1]
    danger_check_file = danger_check_file + proName + '.csv'
    output_file = output_file + proName + '.csv'
    print(danger_check_file)
    print('init...')
    init()
    print('proces...')
    process()
    print('output...')
    output()
    print('task finish')
