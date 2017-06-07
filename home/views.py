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

def main(request):
    institute_list = Institute.objects.all()
    course_list = institute_list[0].courses.all()

    return render(request, 'base.html',
                  { 'institute' : institute_list[0],
                    'course' : course_list[0],
                    'lecture' : 1,
                    'institutes' : institute_list,
                    'courses' : course_list,
                    'numbers' : range(course_list[0].lectureNumbers)})

def complete(request, institute, course, lecture):
    print "in complete"
    institute_list = Institute.objects.all()
    course_list = Institute.objects.get(id=institute).courses.all()
    lecture = int(lecture)

    if lecture + 1 <= Course.objects.get(id=course).lectureNumbers:
        lecture += 1

    return render(request, 'base.html',
                  { 'institute' : Institute.objects.get(id=institute),
                    'course' : Course.objects.get(id=course),
                    'lecture' : lecture,
                    'institutes' : institute_list,
                    'courses' : course_list,
                    'numbers' : range(Course.objects.get(id=course).lectureNumbers),
                    'msg' : 'Parsing Complete'})

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
    if request.method == 'POST' and 'file' in request.FILES:
        myfile = request.FILES['file']
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

        return HttpResponseRedirect('/complete/'+institute+"/"+course+"/"+lecture)
    else:
        print "???  "
        return HttpResponseRedirect('/')