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
def test_course(request):
    
def index(request):
    return HttpResponse('Test')
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

def importcomment(request):
    num = 1
    path=os.path.join(settings.BASE_DIR,'static')
    path=os.path.join(path,'rank.csv')
    csvFile = open(path, "r",encoding='utf-8')
    reader = csv.reader(csvFile)
    for item in reader:
        course = models.prof_with_course.objects.filter(
            prof=models.prof_info.objects.filter(name=item[0]).first(),
            course=models.course_noporf.objects.filter(New_code=item[1]).first()
        )
        if len(course)!=0:
            for i in range(2,10):
                if item[i]=='':
                    item[i]='0'
                if item[i]=='每次' or item[i]=='多种' or item[i]=='个人' or  item[i]=='多種' or item[i]=='個人':
                    item[i]='1.0'
                if item[i]=='抽查' or item[i]=='小组' or item[i]=='小組':
                    item[i]='2.5'
                if item[i]=='不需要':
                    item[i]='5.0'
                if item[i]=='null':
                    item[i]='0.0'
            comment=models.comment(course=course.first(),
                                   attendance=float(item[2]),
                                   pre=float(item[3]),
                                   grade=float(item[4]),
                                   hard=float(item[5]),
                                   reward=float(item[6]),
                                   recommend=float(item[7]),
                                   assignment=float(item[8]),
                                   content=item[9]
                                   )
            comment.result = (comment.assignment +
                                  comment.attendance +
                                  comment.pre +
                                  comment.grade +
                                  comment.hard +
                                  comment.reward +
                                  comment.recommend) / 7
            comment.save()
    d=models.comment.objects.all()
    for i in d:
        n=7
        # if i.content=='0':
        #     i.content=''
        #     i.save()
        if i.attendance==0:
            n-=1
        if i.pre==0:
            n-=1
        if i.grade==0:
            n-=1
        if i.hard==0:
            n-=1
        if i.reward==0:
            n-=1
        if i.recommend==0:
            n-=1
        if i.assignment==0:
            n-=1
        i.result=(i.attendance+i.pre+i.grade+i.hard+i.reward+i.recommend+i.assignment)/n
        i.save()
        print(num)
        num += 1
    return HttpResponse('Success')

def cal_grade(request):
    n=0
    d=models.prof_with_course.objects.all()
    for course in d:
        comments = models.comment.objects.filter(course=course)
        grade = 0.0
        if len(comments) != 0:
            for comment in comments:
                grade += comment.hard
            grade = grade / len(comments)
            course.hard = grade

        grade = 0.0
        if len(comments) != 0:
            for comment in comments:
                grade += comment.result
            grade = grade / len(comments)
            course.result = grade

        grade = 0.0
        if len(comments) != 0:
            for comment in comments:
                grade += comment.grade
            grade = grade / len(comments)
            course.grade = grade

        grade = 0.0
        if len(comments) != 0:
            for comment in comments:
                grade += comment.reward
            grade = grade / len(comments)
            course.reward = grade
        course.save()
        print(grade,n)
        n+=1
    return HttpResponse('Success')