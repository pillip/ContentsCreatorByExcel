# -*- coding:UTF-8 -*-
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Institute, Course
import json

def main(request):
    institute_list = Institute.objects.all()
    course_list = institute_list[0].courses.all()

    return render(request, 'base.html',
                  { 'institute' : institute_list[0],
                    'course' : course_list[0],
                    'institutes' : institute_list,
                    'courses' : course_list,
                    'numbers' : range(course_list[0].lectureNumbers) })

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
