# -*- coding:UTF-8 -*-

import openpyxl
from django.conf import settings
from .models import Institute, Course

institute = None
course = None
lecture = None
totalPage = 0
lectureName = None

def parse(filename, instNum, courseNum, lectureNum):
    global institute, course, lecture, totalPage, lectureName
    workbook = openpyxl.load_workbook(settings.BASE_DIR + filename)
    institute = Institute.objects.get(id=instNum)
    course = Course.objects.get(id=courseNum)
    lecture = int(lectureNum)

    if lecture == 1:
        totalPage = course.pageNumDefault + course.pageNumOT
        lectureName = str(workbook[u'6']['B1'].value)

        parsing1(workbook[u'1'])
        parsing2(workbook[u'2'])
        parsing3(workbook[u'3'])
        parsing4(workbook[u'4'])
        parsing5(workbook[u'5'])
        parsing6(workbook[u'6'])
        parsing7(workbook[u'7'])
        parsing8(workbook[u'8'])
        parsing9(workbook[u'9'])
        parsing10(workbook[u'10'])
        parsing11(workbook[u'11'])
        parsing12(workbook[u'12'])
        parsing12_prob(workbook)
        parsing13(workbook[u'13'])
    else:
        totalPage = course.pageNumDefault
        lectureName = workbook[u'1']['B1'].value

        parsing6(workbook[u'1'], "01.html")
        parsing7(workbook[u'2'], "02.html")
        parsing8(workbook[u'3'], "03.html")
        parsing9(workbook[u'4'], "04.html")
        parsing10(workbook[u'5'], "05.html")
        parsing11(workbook[u'6'], "06.html")
        parsing12(workbook[u'7'], "07.html")
        parsing12_prob(workbook, "07_2.html")
        parsing13(workbook[u'8'], "08.html")


def initialize(dict):
    global institute, course, lecture, totalPage, lectureName
    # instname, coursename, totalpage, weeks, weeknum, lecnum, lecturename
    dict['instname'] = institute.name
    dict['coursename'] = course.title
    dict['totalpage'] = totalPage
    dict['weeks'] = course.lectureNumbers / course.lectureNumbersPerWeek
    dict['weeknum'] = (lecture - 1) / course.lectureNumbersPerWeek + 1
    dict['lecnum'] = (lecture - 1) % course.lectureNumbersPerWeek + 1
    dict['lecturename'] = lectureName

def writeFile(dict, fn):
    global lecture, course

    templateDir = 2
    if lecture == 1:
        templateDir = 1

    try:
        os.remove(settings.BASE_DIR + '/media/' + course.folderName + '/result/' + str(lecture) + "/" + fn)
    except:
        pass

    templateFile = open(settings.BASE_DIR + '/media/' + course.folderName + '/templates/' + str(templateDir) + '/' + fn, "r")

    if int(lecture) < 10:
        resultFile = open(settings.BASE_DIR + '/media/' + course.folderName + '/result/0' + str(lecture) + "/" + fn, "w")
    else:
        resultFile = open(settings.BASE_DIR + '/media/' + course.folderName + '/result/' + str(lecture) + "/" + fn, "w")

    for line in templateFile:
        if line.find('][') != -1:
            newLine = line.split('][')
            newLine[1] = str(dict[newLine[1]])

            if len(newLine) >= 5:
                newLine[3] = str(dict[newLine[3]])

            if len(newLine) >= 7:
                newLine[5] = str(dict[newLine[5]])

            newLine = ''.join(newLine)

            resultFile.write(newLine)
        else:
            resultFile.write(line)

def writeIncFile(dict, fn):
    global lecture, course

    templateDir = 2
    if lecture == 1:
        templateDir = 1

    try:
        os.remove(settings.BASE_DIR + '/media/' + course.folderName + '/result/' + "/inc/" + fn)
    except:
        pass

    templateFile = open(
        settings.BASE_DIR + '/media/' + course.folderName + '/templates/' + '/inc/' + fn, "r")
    resultFile = open(settings.BASE_DIR + '/media/' + course.folderName + '/result/' + "/inc/" + fn, "w")
    for line in templateFile:
        if line.find('][') != -1:
            newLine = line.split('][')
            newLine[1] = str(dict[newLine[1]])

            if len(newLine) >= 5:
                newLine[3] = str(dict[newLine[3]])

            newLine = ''.join(newLine)

            resultFile.write(newLine)
        else:
            resultFile.write(line)

def parsing1(worksheet, fn="01.html"):
    dict = {}
    initialize(dict)

    dict['currpage'] = 1
    dict['time'] = worksheet['D1'].value

    writeFile(dict, fn)

def parsing2(worksheet, fn="02.html"):
    dict = {}
    initialize(dict)

    dict['currpage'] = 2
    dict['time'] = worksheet['D1'].value

    dict['profname'] = worksheet['B1'].value

    dict['studyhistory'] = str(worksheet['B2'].value)

    dict['history'] = str(worksheet['B3'].value)

    writeFile(dict, fn)
    writeIncFile(dict, "teacher.html")

def parsing3(worksheet, fn="03.html"):
    dict = {}
    initialize(dict)

    dict['currpage'] = 3
    dict['time'] = worksheet['D1'].value

    dict['3video'] = worksheet['B1'].value

    writeFile(dict, fn)
    writeIncFile(dict, "class.html")

def parsing4(worksheet, fn="04.html"):
    global course

    dict = {}
    initialize(dict)

    dict['currpage'] = 4
    dict['time'] = worksheet['D1'].value

    week = 1
    lec = 1
    num = int(worksheet['B2'].value)
    temp = []
    for idx in range(3, num + 3):
        temp.append('<tr><td>' + str(week) + '주차 ' + str(lec) + '차시</td>' + '<td><pre>' + str(worksheet['B'+str(idx)].value) + '</pre></td></tr>')

        lec += 1
        if lec > course.lectureNumbersPerWeek:
            week += 1
            lec = 1
    temp = ''.join(temp)
    dict['lefttable'] = temp

    week = 8
    lec = 1
    num = int(worksheet['D2'].value)
    temp = []
    for idx in range(3, num + 3):
        if week == 8 or week == 15:
            temp.append('<tr><td>' + str(week) + '주차</td>' + '<td><pre>' + str(worksheet['D' + str(idx)].value) + '</pre></td></tr>')
        else:
            temp.append('<tr><td>' + str(week) + '주차 ' + str(lec) + '차시</td>' + '<td><pre>' + str(worksheet['D' + str(idx)].value) + '</pre></td></tr>')

        if week == 8 or week == 15:
            lec = course.lectureNumbersPerWeek

        lec += 1
        if lec > course.lectureNumbersPerWeek:
            week += 1
            lec = 1
    temp = ''.join(temp)
    dict['righttable'] = temp

    writeFile(dict, fn)
    writeIncFile(dict, "running.html")

def parsing5(worksheet, fn="05.html"):
    dict = {}
    initialize(dict)

    dict['currpage'] = 5
    dict['time'] = worksheet['D1'].value

    writeFile(dict, fn)

def parsing6(worksheet, fn="06.html"):
    dict = {}
    initialize(dict)

    global lecture
    if lecture == 1:
        dict['currpage'] = 6
    else:
        dict['currpage'] = 1

    dict['time'] = worksheet['D1'].value

    writeFile(dict, fn)

def parsing7(worksheet, fn="07.html"):
    dict = {}
    initialize(dict)

    global lecture
    if lecture == 1:
        dict['currpage'] = 7
    else:
        dict['currpage'] = 2

    dict['time'] = worksheet['D1'].value

    dict['7video'] = worksheet['B1'].value

    writeFile(dict, fn)

def parsing8(worksheet, fn="08.html"):
    dict = {}
    initialize(dict)

    global lecture
    if lecture == 1:
        dict['currpage'] = 8
    else:
        dict['currpage'] = 3

    dict['time'] = worksheet['D1'].value

    dict['8problem1'] = worksheet['B1'].value
    dict['8answer1'] = worksheet['B2'].value
    dict['8explanation1'] = worksheet['B3'].value

    dict['8problem2'] = worksheet['B4'].value
    dict['8answer2'] = worksheet['B5'].value
    dict['8explanation2'] = worksheet['B6'].value

    dict['8problem3'] = worksheet['B7'].value
    dict['8answer3'] = worksheet['B8'].value
    dict['8explanation3'] = worksheet['B9'].value

    writeFile(dict, fn)

def parsing9(worksheet, fn="09.html"):
    dict = {}
    initialize(dict)

    global lecture
    if lecture == 1:
        dict['currpage'] = 9
    else:
        dict['currpage'] = 4

    dict['time'] = worksheet['D1'].value

    dict['9video'] = worksheet['B4'].value

    temp = str(worksheet['B5'].value).split('\n')
    for idx in range(len(temp)):
        temp[idx] = '<li>' + temp[idx] + '</li>'
    temp = ''.join(temp)
    dict['9list'] = temp

    writeFile(dict, fn)

def parsing10(worksheet, fn="10.html"):
    dict = {}
    initialize(dict)

    global lecture
    if lecture == 1:
        dict['currpage'] = 10
    else:
        dict['currpage'] = 5

    dict['time'] = worksheet['D1'].value

    n = int(worksheet['B1'].value)
    dict['10content'] = ''
    for idx in range(2, n * 2 + 1, 2):
        title = '<b>' + str(idx / 2) + '. ' + str(worksheet['B' + str(idx)].value) + '</b><br>'

        if worksheet['B' + str(idx + 1)].value == None:
            content = '<pre></pre><br>'
        else:
            content = '<pre>' + str(worksheet['B' + str(idx + 1)].value) + '</pre><br>'

        dict['10content'] += title + content

    writeFile(dict, fn)

def parsing11(worksheet, fn="11.html"):
    dict = {}
    initialize(dict)

    global lecture
    if lecture == 1:
        dict['currpage'] = 11
    else:
        dict['currpage'] = 6

    dict['time'] = worksheet['D1'].value

    writeFile(dict, fn)

def parsing12(worksheet, fn="12.html"):
    dict = {}
    initialize(dict)

    global lecture
    if lecture == 1:
        dict['currpage'] = 12
    else:
        dict['currpage'] = 7

    dict['time'] = worksheet['D1'].value

    writeFile(dict, fn)

def parsing12_prob(workbook, fn="12_2.html"):
    dict = {}
    initialize(dict)

    global lecture
    if lecture == 1:
        dict['currpage'] = 12
    else:
        dict['currpage'] = 7

    if lecture == 1:
        worksheet = workbook['12_2']
    else:
        worksheet = workbook['7_2']

    for idx in range(1, 4):
        cells = []
        for i in range(1, 7):
            cells.append('B'+ str((idx-1) * 6 + i))

        flag = int(worksheet[cells[0]].value)
        dict['12problem' + str(idx)] = str(worksheet[cells[1]].value)
        dict['12example' + str(idx)] = str(worksheet[cells[2]].value)

        if flag == 1: # 단답형
            dict['12flag' + str(idx)] = '2'
            onchangeFunc = ' onchange="changeText(' + str(idx) + ',' + "$('#answer" + str(idx) + "')" + '.val());"'
            dict['12options' + str(idx)] = '<textarea id="answer' + str(idx) + '"' + onchangeFunc + ' class="p12_2_a3" placeholder="이곳에 정답을 입력하세요."></textarea>'
        else: # 객관식
            dict['12flag' + str(idx)] = '1'
            t = (idx - 1) * 6 + 4
            temp = []
            temp.append(worksheet['B' + str(t)].value)
            temp.append(worksheet['C' + str(t)].value)
            temp.append(worksheet['D' + str(t)].value)
            temp.append(worksheet['E' + str(t)].value)
            for i in range(len(temp)):
                temp[i] = '<li><a style="cursor:pointer;" class="opt-' + str(i + 1) + '" onclick="changeNum(' + str(idx) + ',' + str(i+1) + ');"' + '>' + '<pre style="overflow-x:hidden;">' + str(i + 1) + ". " + temp[i] + "</pre>" + '</a></li>'
            temp = '<ul class="p12_2_v2">' + ''.join(temp) + '</ul>'
            dict['12options' + str(idx)] = temp

        dict['12answernum' + str(idx)] = str(worksheet[cells[4]].value)
        dict['12answernum' + str(idx) + '_1'] = str(worksheet[cells[4]].value).split('/')[0]
        dict['12answer' + str(idx)] = str(worksheet[cells[5]].value)

    writeFile(dict, fn)

def parsing13(worksheet, fn="13.html"):
    global course

    dict = {}
    initialize(dict)

    global lecture
    if lecture == 1:
        dict['currpage'] = 13
    else:
        dict['currpage'] = 8

    dict['time'] = worksheet['D1'].value

    dict['nextlecturename'] = str(worksheet['B1'].value)
    if int(dict['weeknum']) != 8 and int(dict['weeknum']) != 15 and int(dict['lecnum']) + 1 <= course.lectureNumbersPerWeek:
        dict['nextweeknum'] = dict['weeknum']
        dict['nextlecnum'] = int(dict['lecnum']) + 1
    else:
        dict['nextweeknum'] = int(dict['weeknum']) + 1
        dict['nextlecnum'] = 1

    writeFile(dict, fn)