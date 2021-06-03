from django.shortcuts import render, HttpResponse
import csv, os
from . import models
from server import settings
from django.utils.dateparse import parse_datetime
'''
    "Offering_Unit": "FAH",
    "Offering_Department": "CJS",
    "New_code": "JAPN1000",
    "Old_code": "FAH-CJS-JPNB110",
    "courseTitleEng": "PRACTICAL JAPANESE I",
    "courseTitleChi": "實用日語 I",
    "Credits": "6.0",
    "Course_Duration": "Semester"

Offering Unit,Offering Department,Course Code,Course Title,Medium of Instruction,Teacher Information
'''


def import_course(request):
    n = 1
    path = os.path.join(settings.BASE_DIR, 'static')
    path = os.path.join(path, 'Class.csv')
    csvFile = open(path, "r", encoding='utf-8')
    reader = csv.reader(csvFile)
    for item in reader:
        course = models.course_noporf.objects.filter(
            New_code=item[2]
        )
        if len(course) == 0:
            new_course = models.course_noporf(
                Offering_Unit=item[0],
                Offering_Department=item[1],
                New_code=item[2],
                courseTitleEng=item[3],
                Medium_of_Instruction=item[4]
            )
            new_course.save()
    return HttpResponse("success")


def import_prof(request):
    n = 1
    path = os.path.join(settings.BASE_DIR, 'static')
    path = os.path.join(path, 'Class.csv')
    csvFile = open(path, "r", encoding='utf-8')
    reader = csv.reader(csvFile)
    for item in reader:
        prof = models.prof_info.objects.filter(name=item[5])
        if len(prof) == 0:
            new_prof = models.prof_info(
                name=item[5]
            )
            new_prof.save()
    return HttpResponse("success")


def import_prof_course(request):
    n = 1
    path = os.path.join(settings.BASE_DIR, 'static')
    path = os.path.join(path, 'Class.csv')
    csvFile = open(path, "r", encoding='utf-8')
    reader = csv.reader(csvFile)
    for item in reader:
        prof_with_course = models.prof_with_course.objects.filter(
            course=models.course_noporf.objects.filter(
                New_code=item[2]
            ).first(),
            prof=models.prof_info.objects.filter(
                name=item[5]
            ).first()
        )
        if len(prof_with_course) == 0:
            course = models.prof_with_course(
                prof=models.prof_info.objects.filter(
                    name=item[5]
                ).first(),
                course=models.course_noporf.objects.filter(
                    New_code=item[2]
                ).first(),
            )
            course.save()
    return HttpResponse("success")

def importcomment(request):
    num = 1
    path = os.path.join(settings.BASE_DIR, 'static')
    path = os.path.join(path, 'rank.csv')
    csvFile = open(path, "r", encoding='utf-8')
    reader = csv.reader(csvFile)
    for item in reader:
        course = models.prof_with_course.objects.filter(
            prof=models.prof_info.objects.filter(name=item[0]).first(),
            course=models.course_noporf.objects.filter(New_code=item[1]).first()
        )
        if len(course) != 0:
            for i in range(2, 10):
                if item[i] == '':
                    item[i] = '0'
                if item[i] == '每次' or item[i] == '多种' or item[i] == '个人' or item[i] == '多種' or item[i] == '個人':
                    item[i] = '1.0'
                if item[i] == '抽查' or item[i] == '小组' or item[i] == '小組':
                    item[i] = '2.5'
                if item[i] == '不需要':
                    item[i] = '5.0'
                if item[i] == 'null':
                    item[i] = '0.0'
            comment = models.comment(course=course.first(),
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
    d = models.comment.objects.all()
    for i in d:
        n = 7
        # if i.content=='0':
        #     i.content=''
        #     i.save()
        if i.attendance == 0:
            n -= 1
        if i.pre == 0:
            n -= 1
        if i.grade == 0:
            n -= 1
        if i.hard == 0:
            n -= 1
        if i.reward == 0:
            n -= 1
        if i.recommend == 0:
            n -= 1
        if i.assignment == 0:
            n -= 1
        i.result = (i.attendance + i.pre + i.grade + i.hard + i.reward + i.recommend + i.assignment) / n
        i.save()
        print(num)
        num += 1
    return HttpResponse('Success')



def importdata(request):
    n=0
    # path = os.path.join(settings.BASE_DIR, 'static')
    # path = os.path.join(path, 'main_course_course_noporf.csv')
    # csvFile = open(path, "r", encoding='utf-8')
    # reader = csv.reader(csvFile)
    # for item in reader:
    #     new=models.course_noporf(Offering_Unit=item[1],
    #                              Offering_Department=item[2],
    #                              New_code=item[3],
    #                              Old_code=item[4],
    #                              courseTitleEng=item[5],
    #                              courseTitleChi=item[6],
    #                              Course_Duration=item[7],
    #                              Medium_of_Instruction=item[8],
    #                              Credits=item[9],
    #                              temp=item[0])
    #     new.save()
    #     print(n)
    #     n += 1
    # path = os.path.join(settings.BASE_DIR, 'static')
    # path = os.path.join(path, 'main_course_prof_info.csv')
    # csvFile = open(path, "r", encoding='utf-8')
    # reader = csv.reader(csvFile)
    # for item in reader:
    #     print(item[1])
    #     new=models.prof_info(name=item[1],
    #                          temp=item[0])
    #     new.save()
    #     print(n)
    #     n+=1
    # path = os.path.join(settings.BASE_DIR, 'static')
    # path = os.path.join(path, 'main_course_prof_with_course.csv')
    # csvFile = open(path, "r", encoding='utf-8')
    # reader = csv.reader(csvFile)
    # for item in reader:
    #     course=models.course_noporf.objects.filter(temp=item[1])
    #     if len(course)>0:
    #         course=course.first()
    #         prof=models.prof_info.objects.filter(temp=item[2])
    #         if len(prof)>0:
    #             prof=prof.first()
    #             new=models.prof_with_course(
    #                 temp=item[0],
    #                 course=course,
    #                 prof=prof,
    #                 grade=item[3],
    #                 comments=item[4],
    #                 attendance=item[5],
    #                 hard=item[6],
    #                 reward=item[7],
    #                 result=item[8]
    #             )
    #             new.save()
    #             print(n)
    #             n += 1
    path = os.path.join(settings.BASE_DIR, 'static')
    path = os.path.join(path, 'main_course_comment.csv')
    csvFile = open(path, "r", encoding='utf-8')
    reader = csv.reader(csvFile)
    for item in reader:
        course=models.prof_with_course.objects.filter(temp=item[10])
        if len(course)>0:
            try:
                course=course.first()
                new=models.comment(content=item[1],
                                   attendance=item[2],
                                   pre=item[3],
                                   grade=item[4],
                                   hard=item[5],
                                   reward=item[6],
                                   recommend=item[7],
                                   assignment=item[8],
                                   pub_time=parse_datetime(item[9]),
                                   course=course,
                                   result=item[11])
                new.save()
            except:
                continue
            print(n)
            n += 1
    return HttpResponse('Success')








