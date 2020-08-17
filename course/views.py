from django.shortcuts import render,HttpResponse
import csv,os
from . import models
from server import settings
'''
    "Offering_Unit": "FAH",
    "Offering_Department": "CJS",
    "New_code": "JAPN1000",
    "Old_code": "FAH-CJS-JPNB110",
    "courseTitleEng": "PRACTICAL JAPANESE I",
    "courseTitleChi": "實用日語 I",
    "Credits": "6.0",
    "Course_Duration": "Semester"
'''
def importclass(request):
    n=1
    d=models.course.objects.all()
    for i in d:
        if len(models.course_noporf.objects.filter(New_code=i.New_code)) ==0:
            course=models.course_noporf(
              Offering_Unit=i.Offering_Unit,
              Offering_Department=i.Offering_Department,
              New_code=i.New_code,
              Old_code=i.Old_code,
              courseTitleEng=i.courseTitleEng,
              courseTitleChi=i.courseTitleChi,
              Credits=i.Credits,
              Course_Duration=i.Course_Duration,
              Medium_of_Instruction=i.Medium_of_Instruction
            )
            course.save()
        print(n)
        n+=1
    return HttpResponse('Success')

def importprof(request):
    n=1
    d=models.course.objects.all()
    for i in d:
        if len(models.prof_info.objects.filter(name=i.Teacher_Information))==0:
            prof=models.prof_info(
                name=i.Teacher_Information
            )
            prof.save()
        print(n)
        n+=1
    return HttpResponse('Success')

def connect_prof_course(request):
    n=1
    d=models.course.objects.all()
    for i in d:
        if len(models.prof_with_course.objects.filter(prof=models.prof_info.objects.filter(name=i.Teacher_Information).first(),
                                                      course=models.course_noporf.objects.filter(New_code=i.New_code).first()
                                                      )
               )==0:
            course=models.prof_with_course(
                prof=models.prof_info.objects.filter(name=i.Teacher_Information).first(),
                course=models.course_noporf.objects.filter(New_code=i.New_code).first()
            )
            course.save()
        print(n)
        n += 1
    return HttpResponse('Success')
