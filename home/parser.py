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
        lectureName = workbook[u'6']['B1'].value

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
        parsing12_prob(workbook[u'12_2'])
        parsing12_prob(workbook[u'12_3'], "12_3.html")
        parsing12_prob(workbook[u'12_4'], "12_4.html")
        parsing12_5(workbook[u'12_5'])
        parsing13(workbook[u'13'])
    else:
        totalPage = course.pageNumDefault

        pass

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
    resultFile = open(settings.BASE_DIR + '/media/' + course.folderName + '/result/' + str(lecture) + "/" + fn, "w")
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

    writeFile(dict, fn)

def parsing2(worksheet, fn="02.html"):
    dict = {}
    initialize(dict)

    dict['currpage'] = 2
    dict['profname'] = worksheet['B1'].value

    temp = str(worksheet['B2'].value).split('\n')
    for idx in range(len(temp)):
        temp[idx] = '<dd>- ' + temp[idx] + '</dd>'
    temp = ''.join(temp)
    dict['studyhistory'] = temp

    temp = str(worksheet['B3'].value).split('\n')
    for idx in range(len(temp)):
        temp[idx] = '<dd>- ' + temp[idx] + '</dd>'
    temp = ''.join(temp)
    dict['history'] = temp

    writeFile(dict, fn)

def parsing3(worksheet, fn="03.html"):
    dict = {}
    initialize(dict)

    dict['currpage'] = 3
    dict['3video'] = worksheet['B1'].value

    writeFile(dict, fn)

def parsing4(worksheet, fn="04.html"):
    global course

    dict = {}
    initialize(dict)

    dict['currpage'] = 4

    week = 1
    lec = 1
    temp = str(worksheet['B1'].value).split('\n')
    for idx in range(len(temp)):
        temp[idx] = '<tr><td>' + str(week) + '주차 ' + str(lec) + '차시</td>' + '<td>' + temp[idx] + '</td></tr>'

        lec += 1
        if lec > course.lectureNumbersPerWeek:
            week += 1
            lec = 1
    temp = ''.join(temp)
    dict['lefttable'] = temp

    week = 8
    lec = 1
    temp = str(worksheet['B2'].value).split('\n')
    for idx in range(len(temp)):
        if week == 8 or week == 15:
            temp[idx] = '<tr><td>' + str(week) + '주차</td>' + '<td>' + temp[idx] + '</td></tr>'
        else:
            temp[idx] = '<tr><td>' + str(week) + '주차 ' + str(lec) + '차시</td>' + '<td>' + temp[idx] + '</td></tr>'

        if week == 8 or week == 15:
            lec = course.lectureNumbersPerWeek

        lec += 1
        if lec > course.lectureNumbersPerWeek:
            week += 1
            lec = 1
    temp = ''.join(temp)
    dict['righttable'] = temp

    writeFile(dict, fn)

def parsing5(worksheet, fn="05.html"):
    dict = {}
    initialize(dict)

    dict['currpage'] = 5

    writeFile(dict, fn)

def parsing6(worksheet, fn="06.html"):
    dict = {}
    initialize(dict)

    dict['currpage'] = 6

    writeFile(dict, fn)

def parsing7(worksheet, fn="07.html"):
    pass

def parsing8(worksheet, fn="08.html"):
    pass

def parsing9(worksheet, fn="09.html"):
    pass

def parsing10(worksheet, fn="10.html"):
    pass

def parsing11(worksheet, fn="11.html"):
    pass

def parsing12(worksheet, fn="12.html"):
    pass

def parsing12_prob(worksheet, fn="12_2.html"):
    pass

def parsing12_5(worksheet, fn="12_5.html"):
    pass

def parsing13(worksheet, fn="13.html"):
    pass