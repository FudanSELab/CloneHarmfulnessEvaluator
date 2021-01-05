import time
import os
import re
import json
import sys

comment_pattern = re.compile(r'/\*.*?\*/', re.S)
comment_pattern2 = re.compile(r'//.*?\n', re.S)
consis_result_dir = 'consistResult/'
extracted_Json_dir = 'extractedJson/'
pre_clone_group_info_file = 'result/preCloneGroupInfo.csv'
danger_check_file = './finalResult/validation_result_'
output_file = 'type123_ori_'

clone_group_ids = dict()
clone_group_type_infos = dict()

def get_type(code1, code2):
    tmp1 = comment_pattern.sub('', code1)
    tmp1 = comment_pattern2.sub('', tmp1)
    code1_lines = tmp1.split('\n')
    code1_lines = [line for line in code1_lines if line.replace(' ', '') != '']
    tmp1 = '\n'.join(code1_lines)

    tmp2 = comment_pattern.sub('', code2)
    tmp2 = comment_pattern2.sub('', tmp2)
    code2_lines = tmp2.split('\n')
    code2_lines = [line for line in code2_lines if line.replace(' ', '') != '']
    tmp2 = '\n'.join(code2_lines)

    if tmp1 == tmp2:
        return '1'
    #if len(code1_lines) == len(code2_lines):
        #return '2'
    if isTypeTwoClone(tmp1, tmp2):
        return '2'
    return '3'

def isTypeTwoClone(code1, code2):
    codeOneWord = code1.replace("\n", "")
    codeOneWord = codeOneWord.replace("\t", " ")
    codeOneWord = codeOneWord.replace(";", "")
    codeOneWord = codeOneWord.replace(", ", ",")
    codeOneWord = codeOneWord.split(" ")

    codeTwoWord = code2.replace("\n", "")
    codeTwoWord = codeTwoWord.replace("\t", " ")
    codeTwoWord = codeTwoWord.replace(";", "")
    codeTwoWord = codeTwoWord.replace(", ", ",")
    codeTwoWord = codeTwoWord.split(" ")

    isTypeTwo = False
    if(len(codeOneWord) == len(codeTwoWord)):
        isTypeTwo = True

    return isTypeTwo

def init():
    global clone_group_ids
    f = open(danger_check_file, 'r')
    for line in f:
        tmp = line.strip().split(',')
        group_id = tmp[0]
        if not group_id.isdigit():
            continue
        danger_degree = tmp[-1]
        clone_group_ids[group_id] = danger_degree
    f.close()

def get_start_clone_type_ori(group_id):
    with open('%s/%s.json' % (extracted_Json_dir, group_id), 'r') as f:
        #commits = json.load(f)
        try:
            commits = json.load(f)
        except Exception as e:
            return '1'
    birth_codes = dict()
    instance_num = len(commits[0]['codes'])
    for commit in commits:
        if len(birth_codes) == instance_num:
            break
        codes = commit['codes']
        for i in range(instance_num):
            if i in birth_codes:
                continue
            if codes[i]['status'] in ['B', 'N']:
                birth_codes[i] = codes[i]
    result_set = set()
    for i in range(0, len(birth_codes) - 1):
        for j in range(i+1, len(birth_codes)):
            try:
                clone_type = get_type(birth_codes[i]['preCode'], birth_codes[j]['preCode'])
            except Exception as e:
                clone_type = '1'
            result_set.add(clone_type)
    result = ''
    for t in result_set:
        result += t + '@'
    return result[0:-1]

def get_start_clone_type(group_id):
    """start clone type"""
    with open('%s/%s.json' % (extracted_Json_dir, group_id), 'r') as f:
        #commits = json.load(f)
        try:
            commits = json.load(f)
        except Exception as e:
            return '1'
    birth_codes = dict()
    instance_num = len(commits[0]['codes'])
    birthList = list()
    for commit in commits:
        codes = commit['codes']
        for i in range(instance_num):
            if codes[i]['status'] in ['B', 'N', 'M']:
                birthList.append(i)
    for commit in commits:
        if len(birth_codes) == len(birthList):
            break
        codes = commit['codes']
        for i in range(instance_num):
            if i not in birthList:
                continue
            if i in birth_codes:
                continue
            if codes[i]['status'] in ['B', 'N', 'M']:
                birth_codes[i] = codes[i]
    result_set = set()
    # if(len(birthList) < 2):
    #     return ""
    for i in range(0, len(birth_codes) - 1):
        for j in range(i+1, len(birth_codes)):
            try:
                clone_type = get_type(birth_codes[i]['preCode'], birth_codes[j]['preCode'])
            except Exception as e:
                clone_type = '1'
            result_set.add(clone_type)
    result = ''
    for t in result_set:
        result += t + '@'
    return result[0:-1]

def get_end_clone_type(group_id):
    with open('%s/%s.json' % (extracted_Json_dir, group_id), 'r') as f:
        try:
            commits = json.load(f)
        except Exception as e:
            return '1'
    commits.reverse()
    final_codes = dict()
    instance_num = len(commits[0]['codes'])
    for commit in commits:
        if len(final_codes) == instance_num:
            break
        codes = commit['codes']
        for i in range(instance_num):
            if i in final_codes:
                continue
            if codes[i]['status'] != 'D':
                final_codes[i] = codes[i]
    result_set = set()
    for i in range(0, len(final_codes) - 1):
        for j in range(i+1, len(final_codes)):
            try:
                clone_type = get_type(final_codes[i]['curCode'], final_codes[j]['curCode'])
            except Exception as e:
                clone_type = '1'
            result_set.add(clone_type)
    result = ''
    for t in result_set:
        result += t + '@'
    return result[0:-1]

def get_consis_clone_pair_type(group_id):
    with open('%s/%s.json' % (consis_result_dir, group_id), 'r') as f:
        #pairs = json.load(f)
        try:
            pairs = json.load(f)
        except Exception as e:
            return '1'
    with open('%s/%s.json' % (extracted_Json_dir, group_id), 'r') as f:
        #commits = json.load(f)
        try:
            commits = json.load(f)
        except Exception as e:
            return '1'
    result_set = set()
    for pair in pairs:
        tmp = pair.split(',')
        pair_id1 = int(tmp[0])
        pair_id2 = int(tmp[1])
        similarity = float(tmp[2])
        if similarity <= 0.5:
            continue
        pre_codes = list()
        for commit in commits:
            if len(pre_codes) == 2:
                break
            codes = commit['codes']
            for code in codes:
                if code['id'] in [pair_id1, pair_id2]:
                    pre_codes.append(code['preCode'])
        clone_type = get_type(pre_codes[0], pre_codes[1])
        result_set.add(clone_type)
    result = ''
    for t in result_set:
        result += t + '@'
    return result[0:-1]

def process():
    global clone_group_ids, clone_group_type_infos
    f = open(output_file, 'w')
    cnt = 0
    size = len(clone_group_ids)
    for group_id in clone_group_ids:
        cnt += 1
        print('%.2f%%' % (cnt*100.0/size))
        start_clone_type = get_start_clone_type(group_id)
        end_clone_type = get_end_clone_type(group_id)
        clone_pair_type = get_consis_clone_pair_type(group_id)
        danger_degree = clone_group_ids[group_id]
        f.write('%s,%s,%s,%s,%s\n' % (group_id, start_clone_type, end_clone_type, clone_pair_type, danger_degree))
    f.close()

if __name__ == '__main__':
    proName = sys.argv[1]
    danger_check_file = danger_check_file + proName + '.csv'
    output_file = output_file + proName + '.csv'
    init()
    process()
    pass
