from __future__ import unicode_literals

from django.db import models

# Create your models here.
import os

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Course(models.Model):
    title = models.CharField(max_length=100, null=False)
    lectureNumbers = models.IntegerField(null=False)
    folderName = models.CharField(max_length=20, null=False)
    pageNumOT = models.IntegerField(default=5, null=False)
    pageNumDefault = models.IntegerField(default=8, null=False)
    lectureNumbersPerWeek = models.IntegerField(default=2, null=False)

    def __str__(self):
        return self.title + " lectureNumber : " + str(self.lectureNumbers)

class Institute(models.Model):
    name = models.CharField(max_length=100, null=False)

    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.name

class UploadedFile(models.Model):
    filePath = models.FilePathField(null=False)
    lectureNumber = models.IntegerField(null=False)
    courseNumber = models.IntegerField(null=False)

def createDirectory(sender, **kwargs):
    course = kwargs['instance']

    directoryName = 'media/' + course.folderName
    absPath = os.path.abspath(directoryName)
    makeDir(absPath)

    directoryName = 'media/' + course.folderName + '/templates'
    absPath = os.path.abspath(directoryName)
    makeDir(absPath)

    directoryName = 'media/' + course.folderName + '/templates/1'
    absPath = os.path.abspath(directoryName)
    makeDir(absPath)

    directoryName = 'media/' + course.folderName + '/templates/2'
    absPath = os.path.abspath(directoryName)
    makeDir(absPath)

    directoryName = 'media/' + course.folderName + '/templates/inc'
    absPath = os.path.abspath(directoryName)
    makeDir(absPath)

    directoryName = 'media/' + course.folderName + '/result'
    absPath = os.path.abspath(directoryName)
    makeDir(absPath)

    directoryName = 'media/' + course.folderName + '/result/inc'
    absPath = os.path.abspath(directoryName)
    makeDir(absPath)

    for n in range(course.lectureNumbers):
        if n + 1 < 10:
            directoryName = 'media/' + course.folderName + '/result/0' + str(n + 1)
        else:
            directoryName = 'media/' + course.folderName + '/result/' + str(n+1)

        absPath = os.path.abspath(directoryName)
        makeDir(absPath)

def makeDir(path):
    try:
        os.mkdir(path)
    except OSError as e:
        if e.errno == 17:
            # Dir already exists.
            pass

models.signals.post_save.connect(createDirectory, sender=Course)