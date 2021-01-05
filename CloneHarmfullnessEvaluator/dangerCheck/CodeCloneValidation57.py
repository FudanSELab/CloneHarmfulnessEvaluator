import math
import os
import sys

def sortedDictByKeys(adict): 
    """sort clone group"""
    keys = adict.keys()
    keys = list(keys)
    keys.sort()
    return [adict[key] for key in keys]

def startValidation(filePath):
    resultDict = dict()
    resultDict = {'1': list(), '2': list(), '3': list(), '4': list()}

    header = ""
    with open(filePath, 'r') as f:
        dangerDegree = 0
        cnt = 0
        for line in f:
            cnt += 1
            if( cnt % 100 == 0):
                print("curId: ", cnt)
            lineArr = line.split(',')
            if(lineArr[0] == 'groupId'):
                header = line
                continue
            if(lineArr[7] == '0'):
                dangerDegree = 1
            elif(int(lineArr[7]) > 0 and float(lineArr[10]) == 0.0 ):
                dangerDegree = 1
            elif(int(lineArr[7]) > 0 and float(lineArr[10]) > 0.0 and int(lineArr[13]) == 0):
                dangerDegree = 2
            elif(int(lineArr[7]) > 0 and float(lineArr[10]) > 0.0 and int(lineArr[13]) > 0):
                dangerDegree = 3
            if(int(lineArr[-7]) > 0 and (int(lineArr[13]) != 0 or int(lineArr[-1]) > 0)):
                dangerDegree = 4
            lineArr[-1] = str(dangerDegree)
            resultDict[str(dangerDegree)].append(lineArr)
            
    return resultDict, header

def modifyCountDistribution(modifyCountList):
    '''
       granularity
       0, 1, 2, 3, 4
       5 <= & < 10
       > 10
    '''
    modifyCountList.sort(reverse=True)
    curDistribution = [0, 0, 0, 0, 0, 0, 0]
    for count in modifyCountList:
        if(count == 0):
            curDistribution[0] += 1
        elif(count == 1):
            curDistribution[1] += 1
        elif(count == 2):
            curDistribution[2] += 1
        elif(count == 3):
            curDistribution[3] += 1
        elif(count == 4):
            curDistribution[4] += 1
        elif(count >= 5 and count < 10):
            curDistribution[5] += 1
        else:
            curDistribution[6] += 1

    outputFilePath = '%s/moidfy_count_distribution.csv' % resultDir
    header = 'modify count(mc),0, 1, 2, 3, 4, 5<=mc<10, mc>=10'
    outputToFile(outputFilePath, header, curDistribution)

def fModifyCountDistribution(modifyCountList):
    '''
       granularity
       0, 1, 2, 3, 4
       5 <= & < 10
       > 10
    '''
    modifyCountList.sort(reverse=True)
    curDistribution = list()
    headNum = list()
    for i in range(53):
        curDistribution.append(0)
        headNum.append('mpi=' + str('%.1f' % (0.1 * i)))
    for count in modifyCountList:
        count = math.ceil(count * 10)
        count /= 10
        if(count == 0):
            curDistribution[0] += 1
        elif(count >= 5 and count < 10):
            curDistribution[51] += 1
        elif(count >= 10):
            curDistribution[52] += 1
        else:
            curDistribution[int(count * 10)] += 1
        

    outputFilePath = '%s/moidfy_count_distribution1.csv' % resultDir
    headStr = ",".join(headNum)
    header = 'modify count(mc),' + headStr
    
    for i in range(len(curDistribution)):
        if(i > 0):
            curDistribution[i] = curDistribution[i] + curDistribution[i - 1]

    outputToFile(outputFilePath, header, curDistribution)

def ratioDistribution(consistRatioList):
    curDistribution = [0 for i in range(12)]
    for ratio in consistRatioList:
        index = math.ceil(ratio * 10)
        if ratio == 1:
            index = 11
        curDistribution[index] += 1
        
    outputFilePath = '%s/consistent_ratio_distribution.csv' % resultDir
    header = 'consistent ratio(cr),cr=0, 0<cr<=0.1, 0.1<cr<=0.2, 0.2<cr<=0.3, 0.3<cr<=0.4, 0.4<cr<=0.5, 0.5<cr<=0.6,  0.6<cr<=0.7,  0.7<cr<=0.8,  0.8<cr<=0.9,  0.9<cr<1.0, cr=1'
    outputToFile(outputFilePath, header, curDistribution)

    # merge area to 0, (0, 0.2], (0.2, 0.4], (0.4, 0.6), [0.6, 0.8), [0.8, 1), 1
    curDistribution1 = [0 for i in range(7)]
    for ratio in consistRatioList:
        index = ratio * 10
        if ratio >= 0.6:
            index = math.floor(index / 2)
            #if(ratio != 1):
                #print(ratio, index)
            index += 1
        if ratio < 0.6:
            index = math.ceil(index / 2)
        curDistribution1[index] += 1

    outputFilePath1 = '%s/consistent_ratio_distribution1.csv' % resultDir
    header1 = 'consistent ratio(cr),cr=0, 0<cr<=0.2, 0.2<cr<=0.4, 0.4<cr<0.6, 0.6<=cr<0.8, 0.8<=cr<1, cr=1'
    outputToFile(outputFilePath1, header1, curDistribution1)

def consistIntervalDistribution(consistIntervalList):
    consistIntervalList.sort(reverse=True)
    weekNum = math.floor(consistIntervalList[0] / (7 * 24 * 60 * 60)) + 1
    monthNum = math.floor(consistIntervalList[0] / (30 * 24 * 60 * 60)) + 1
    yearNum = math.floor(consistIntervalList[0] / (365 * 24 * 60 * 60)) + 1
    
    weekDistribution = getIntervalDistribution(consistIntervalList, weekNum, 7 * 24 * 60 * 60)
    monthDistribution = getIntervalDistribution(consistIntervalList, monthNum, 30 * 24 * 60 * 60)
    yearDistribution = getIntervalDistribution(consistIntervalList, yearNum, 365 * 24 * 60 * 60)

    outputFilePath = '%s/consistent_interval_distribution_week.csv' % resultDir
    header = 'Interval(i), 0<i<=1, 1<i<=2, 2<i<=3, 3<i<=4'
    weekDistribution = weekDistribution[:5]
    del weekDistribution[0]
    outputToFile(outputFilePath, header, weekDistribution)

    outputFilePath = '%s/consistent_interval_distribution_month.csv' % resultDir
    header = 'Interval(i), 0<i<=1, 1<i<=2, 2<i<=3, 3<i<=4, 4<i<=5, 5<i<=6, 6<i<=7, 7<i<=8, 8<i<=9, 9<i<=10, 10<i<=11, 11<i<=12'
    monthDistribution = monthDistribution[:13]
    del monthDistribution[0]
    outputToFile(outputFilePath, header, monthDistribution)

    outputFilePath = '%s/consistent_interval_distribution_year.csv' % resultDir
    header = 'Interval(i), 0<i<=1, 1<i<=2, 2<i<=3, 3<i<=4, 4<i<=5, 5<i<=6, 6<i<=7, 7<i<=8, 8<i<=9, 9<i<=10'
    del yearDistribution[0]
    outputToFile(outputFilePath, header, yearDistribution)

def outputToFile(outputFilePath, header, distribution):
    f = open(outputFilePath, 'a', encoding='utf8')
    if os.path.getsize(outputFilePath) == 0:
        f.write(header + '\n')
    f.write(sys.argv[1] + ', ')
    for i in range(len(distribution)):
        if i != len(distribution) - 1:
            f.write(str(distribution[i]) + ', ')
        else:
            f.write(str(distribution[i]) + '\n')
    f.close()
                
def getIntervalDistribution(consistIntervalList, num, unit):
    curDistribution = [0 for i in range(num + 1)]
    zeroNum = 0
    nonZeroNum = 0
    for i in range(len(consistIntervalList)):
        for index in range(num):
            if(consistIntervalList[i] == 0 and index == 0):
                #print(str(curDistribution[0]) + "=>" + str(consistIntervalList[i]))
                curDistribution[0] += 1
                break
            if(consistIntervalList[i] > index * unit and consistIntervalList[i] <= (index + 1) * unit and index != (num - 1)):
                curDistribution[index + 1] += 1
                break
            if(consistIntervalList[i] > index * unit and index == (num - 1)):
                curDistribution[index + 1] += 1
                break
            
    return curDistribution

def getMetricDistribution(filePath):
    modifyCountList = list()
    consistRatioList = list()
    consistIntervalList = list()
    floatModifyCountList = list()
    with open(filePath, 'r') as f:
        for line in f:
            lineArr = line.strip().split(',')
            if(lineArr[0] == 'groupId'):
                continue
            CPI = int(lineArr[8]) / int(lineArr[1])
            modifyCountList.append(int(CPI))
            floatModifyCountList.append(float('%.2f' % CPI))
            if(float(lineArr[8]) != 0):
                consistRatioList.append(float(lineArr[10]))
            if(int(lineArr[13]) > 0):
                consistIntervalList.append(int(lineArr[15])) #average
    modifyCountDistribution(modifyCountList)
    fModifyCountDistribution(floatModifyCountList)
    ratioDistribution(consistRatioList)
    consistIntervalDistribution(consistIntervalList)
    consistentIntervalCloneGroupDistribution(consistIntervalList)
    newConsistentIntervalCloneGroupDistribution(consistIntervalList)


def consistentIntervalCloneGroupDistribution(consistIntervalList):
    """8小时内，1天内，1周内，一月内，一年内，一年外有时间差的克隆组个数统计"""
    interval_8hours_group_count = 0
    interval_1day_group_count = 0
    interval_1week_group_count = 0
    interval_1month_group_count = 0
    interval_1year_group_count = 0
    interval_more_years_group_count = 0
    time_8hours = 8 * 60 * 60
    time_1day = 3 * time_8hours
    time_1week = 7 * time_1day
    time_1month = 30 * time_1day
    time_1year = 365 * time_1day

    for interval in consistIntervalList:
        if interval <= time_8hours:
            interval_8hours_group_count += 1
        elif interval > time_8hours and interval <= time_1day:
            interval_1day_group_count += 1
        elif interval > time_1day and interval <= time_1week:
            interval_1week_group_count += 1
        elif interval > time_1week and interval <= time_1month:
            interval_1month_group_count += 1
        elif interval > time_1month and interval <= time_1year:
            interval_1year_group_count += 1
        else:
            interval_more_years_group_count += 1
    print('8hours: %d' % interval_8hours_group_count)
    print('1day: %d' % interval_1day_group_count)
    print('1week: %d' % interval_1week_group_count)
    print('1month: %d' % interval_1month_group_count)
    print('1year: %d' % interval_1year_group_count)
    print('more year: %d' % interval_more_years_group_count)

def newConsistentIntervalCloneGroupDistribution(consistIntervalList):
    """8小时内，1天内，1周内，一月内，一年内，一年外有时间差的克隆组个数统计"""
    interval_1day_group_count = 0
    interval_2day_group_count = 0
    interval_3day_group_count = 0
    interval_4day_group_count = 0
    interval_5day_group_count = 0
    interval_1week_group_count = 0
    interval_1month_group_count = 0
    interval_6month_group_count = 0
    interval_1year_group_count = 0
    interval_more_years_group_count = 0
    
    time_1day = 24 * 60 * 60
    time_2day = 2 * time_1day
    time_3day = 3 * time_1day
    time_4day = 4 * time_1day
    time_5day = 5 * time_1day
    time_1week = 7 * time_1day
    time_1month = 30 * time_1day
    time_6month = 180 * time_1day
    time_1year = 365 * time_1day

    for interval in consistIntervalList:
        if interval <= time_1day:
            interval_1day_group_count += 1
        elif interval > time_1day and interval <= time_2day:
            interval_2day_group_count += 1
        elif interval > time_2day and interval <= time_3day:
            interval_3day_group_count += 1
        elif interval > time_3day and interval <= time_4day:
            interval_4day_group_count += 1
        elif interval > time_4day and interval <= time_5day:
            interval_5day_group_count += 1
        elif interval > time_5day and interval <= time_1week:
            interval_1week_group_count += 1
        elif interval > time_1week and interval <= time_1month:
            interval_1month_group_count += 1
        elif interval > time_1month and interval <= time_6month:
            interval_6month_group_count += 1
        elif interval > time_6month and interval <= time_1year:
            interval_1year_group_count += 1
        else:
            interval_more_years_group_count += 1
    
    print('1day: %d' % interval_1day_group_count)
    print('2day: %d' % interval_2day_group_count)
    print('3day: %d' % interval_3day_group_count)
    print('4day: %d' % interval_4day_group_count)
    print('5day: %d' % interval_5day_group_count)
    print('1week: %d' % interval_1week_group_count)
    print('1month: %d' % interval_1month_group_count)
    print('6month: %d' % interval_6month_group_count)
    print('1year: %d' % interval_1year_group_count)
    print('more year: %d' % interval_more_years_group_count)



resultDir = 'finalResult'
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage: python x.py project csvpath')
        sys.exit(0)

    print("start validation")
    resultDict, header = startValidation(sys.argv[2])
    validationResult = list()
    for key in resultDict:
        resultDict[key].sort(key=lambda x: x[-3], reverse = True)
    resultList = sortedDictByKeys(resultDict)
    resultList.reverse()
    for childResult in resultList:
        validationResult += childResult
    
    if not os.path.exists(resultDir):
        os.mkdir(resultDir)
    resultF = open("%s/validation_result_%s.csv" % (resultDir, sys.argv[1]), 'w')
    resultF.write(header)
    for line in validationResult:
        resultF.write(",".join(line) + '\n')
    resultF.close()
    print("validation complete\n")

    print("start analyse distribution")
    getMetricDistribution(sys.argv[2])
