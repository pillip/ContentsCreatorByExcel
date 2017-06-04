# -*- coding:UTF-8 -*-
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Institute, Course
import json
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .parser import parse
import shutil
import os

flag = 0

def main(request):
    institute_list = Institute.objects.all()
    course_list = institute_list[0].courses.all()

    global  flag
    msg = ''
    if flag == 1:
        msg = 'success'
    elif flag == 2:
        msg = 'fail'
    flag = 0

    print msg

    return render(request, 'base.html',
                  { 'institute' : institute_list[0],
                    'course' : course_list[0],
                    'institutes' : institute_list,
                    'courses' : course_list,
                    'numbers' : range(course_list[0].lectureNumbers),
                    'msg' : msg})

def changeCourse(request):
    if request.method == 'GET' and request.is_ajax:
        institute = Institute.objects.get(id=request.GET['instituteId'])
        course = Course.objects.get(id=request.GET['courseId'])

        dict = {'newInstituteName' : institute.name,
                'newCourseName' : course.title,
                'numbers' : course.lectureNumbers }

        return HttpResponse(json.dumps(dict), content_type='application/json')

def changeInstitute(request):
    if request.method == 'GET' and request.is_ajax:
        institute = Institute.objects.get(id=request.GET['instituteId'])
        course_list = institute.courses.all()
        course = course_list[0]

        courses = {}

        counter = 0
        for c in course_list:
            courses[counter] = { 'id' : c.id,
                                 'title' : c.title }
            counter = counter + 1

        dict = {'newInstituteName' : institute.name,
                'newCourseName' : course.title,
                'newCourseId' : course.id,
                'numbers' : course.lectureNumbers,
                'courses' : json.dumps(courses) }

        return HttpResponse(json.dumps(dict), content_type='application/json')

def upload(request, institute, course, lecture):
    global flag

    if request.method == 'POST' and 'myfile' in request.FILES:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()

        currCourse = Course.objects.get(id=course)

        try :
            os.remove(settings.BASE_DIR + '/media/' + currCourse.folderName + '/result/' + myfile.name)
        except:
            pass

        fileName = fs.save(currCourse.folderName + '/result/' + myfile.name, myfile)
        uploaded_file_url = fs.url(fileName)

        print fileName
        print uploaded_file_url

        parse(uploaded_file_url, institute, course, lecture)

        flag = 1
        return HttpResponseRedirect('/')
    else:
        flag = 2
        return HttpResponseRedirect('/')