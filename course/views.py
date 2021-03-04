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

Offering Unit,Offering Department,Course Code,Course Title,Medium of Instruction,Teacher Information
'''
def import_course(request):
    n = 1
    path = os.path.join(settings.BASE_DIR, 'static')
    path = os.path.join(path, 'Class.csv')
    csvFile = open(path, "r", encoding='utf-8')
    reader = csv.reader(csvFile)
    for item in reader:
        course=models.course_noporf.objects.filter(
            New_code=item[2]
        )
        if len(course) == 0:
            new_course=models.course_noporf(
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
        prof=models.prof_info.objects.filter(name=item[5])
        if len(prof)==0:
            new_prof=models.prof_info(
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
        prof_with_course=models.prof_with_course.objects.filter(
            course=models.course_noporf.objects.filter(
                New_code=item[2]
            ).first(),
            prof=models.prof_info.objects.filter(
                name=item[5]
            ).first()
        )
        if len(prof_with_course) ==  0:
            course=models.prof_with_course(
                prof=models.prof_info.objects.filter(
                    name=item[5]
                ).first(),
                course=models.course_noporf.objects.filter(
                    New_code=item[2]
                ).first(),
            )
            course.save()
    return HttpResponse("success")



def faculty_detail(faculty):
    context={
        "course_num":0,
        "comment_num":0,
    }
    num=0
    courses=course_modle.course_noporf.objects.filter(Offering_Unit=faculty)
    context["course_num"]=len(courses)
    for course in courses:
        course_prof=course_modle.prof_with_course.objects.filter(course=course)
        for i in course_prof:
            comments=course_modle.comment.objects.filter(course=i)
            context["comment_num"]+=len(comments)
    return context

def stat(request):
    '''
        :param request:
        :return:
            {
                "course_num": ;
                "prof_num": ;
                "comment_num" ;

                "faculty_detail":{
                    "FAH": {
                        "course_num": ;
                        "comment_num": ;
                        };
                    "FBA": ;
                    "FED": ;
                    "FHS": ;
                    "FLL": ;
                    "FSS": ;
                    "FST": ;
                    }
            }
        '''

    context = {
        "course_num": 0,
        "prof_num": 0,
        "comment_num": 0,

        "faculty_detail": {
            "FAH": {
                "course_num": 0,
                "comment_num": 0,
            },
            "FBA": {
                "course_num": 0,
                "comment_num": 0,
            },
            "FED": {
                "course_num": 0,
                "comment_num": 0,
            },
            "FHS": {
                "course_num": 0,
                "comment_num": 0,
            },
            "FLL": {
                "course_num": 0,
                "comment_num": 0,
            },
            "FSS": {
                "course_num": 0,
                "comment_num": 0,
            },
            "FST": {
                "course_num": 0,
                "comment_num": 0,
            },
        }
    }

    context["course_num"] = len(course_modle.course_noporf.objects.all())
    context["prof_num"] = len(course_modle.prof_info.objects.all())
    context["comment_num"] = len(course_modle.comment.objects.all())
    context["faculty_detail"]["FAH"] = faculty_detail("FAH")
    context["faculty_detail"]["FBA"] = faculty_detail("FBA")
    context["faculty_detail"]["FED"] = faculty_detail("FED")
    context["faculty_detail"]["FHS"] = faculty_detail("FHS")
    context["faculty_detail"]["FLL"] = faculty_detail("FLL")
    context["faculty_detail"]["FSS"] = faculty_detail("FSS")
    context["faculty_detail"]["FST"] = faculty_detail("FST")

    data=models.statistics(
        name="FAH",
        course_num=context["faculty_detail"]["FAH"]["course_num"],
        comment_num=context["faculty_detail"]["FAH"]["comment_num"]
    )
    data.save()

    data = models.statistics(
        name="FBA",
        course_num=context["faculty_detail"]["FBA"]["course_num"],
        comment_num=context["faculty_detail"]["FBA"]["comment_num"]
    )
    data.save()

    data = models.statistics(
        name="FED",
        course_num=context["faculty_detail"]["FED"]["course_num"],
        comment_num=context["faculty_detail"]["FED"]["comment_num"]
    )
    data.save()

    data = models.statistics(
        name="FHS",
        course_num=context["faculty_detail"]["FHS"]["course_num"],
        comment_num=context["faculty_detail"]["FHS"]["comment_num"]
    )
    data.save()

    data = models.statistics(
        name="FLL",
        course_num=context["faculty_detail"]["FLL"]["course_num"],
        comment_num=context["faculty_detail"]["FLL"]["comment_num"]
    )
    data.save()

    data = models.statistics(
        name="FSS",
        course_num=context["faculty_detail"]["FSS"]["course_num"],
        comment_num=context["faculty_detail"]["FSS"]["comment_num"]
    )
    data.save()

    data = models.statistics(
        name="FST",
        course_num=context["faculty_detail"]["FST"]["course_num"],
        comment_num=context["faculty_detail"]["FST"]["comment_num"]
    )
    data.save()

    return HttpResponse("success")

def test_course(request):
    courses=models.course_noporf.objects.all()
    for course in courses:
        if course.Credits=='':
            course.Credits='0.0'
            course.save()
    return HttpResponse("Success")
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
def delete_test(request):
    prof=models.prof_info.objects.filter(name="TEST").first()
    course=models.prof_with_course.objects.filter(prof=prof).first()
    comments=models.comment.objects.filter(course=course)
    n=0
    for comment in comments:
        comment.delete()
        print(n)
        n+=1
    return HttpResponse('Success')

def cal_neg_comments(request):
    commments=models.comment.objects.all()
    n=0
    m=0
    for commment in commments:
        if  commment.content=='':
            n+=1
            if commment.result<=1:
                m+=1
                commment.delete()
    print(n)
    print(m)
    print(m/n)
    return HttpResponse(m)

def del_same_commets(request):
    courses=models.prof_with_course.objects.all()
    for course in courses:
        comments=models.comment.objects.filter(course=course)
        if len(comments)>0:
            for comment in comments:
                duplicated_comments=models.comment.objects.filter(course=course,content=comment.content)
                if len(duplicated_comments)>1 and comment.content!="":
                    for i in range(1,len(duplicated_comments)):
                        print(duplicated_comments[i].content)
                        duplicated_comments[i].delete()
    return HttpResponse("Success")