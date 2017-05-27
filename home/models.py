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


    def __str__(self):
        return self.title + " lectureNumber : " + str(self.lectureNumbers)

class Institute(models.Model):
    name = models.CharField(max_length=100, null=False)

    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.name

def createDirectory(sender, **kwargs):
    course = kwargs['instance']
    directoryName = 'result/' + course.folderName

    absPath = os.path.abspath(directoryName)

    makeDir(absPath)

    print absPath

def makeDir(path):
    try:
        os.mkdir(path)
    except OSError as e:
        if e.errno == 17:
            # Dir already exists.
            pass

models.signals.post_save.connect(createDirectory, sender=Course)