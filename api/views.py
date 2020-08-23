from django.http import JsonResponse
from django.shortcuts import HttpResponse
from course import models as course_modle
import json

def course_info(request):
    '''
        :param request:
            /course_info?New_code=xxx
        :return
        {
            "course_info":{
                "New_code":" ",
                "Old_code":" " ,// if old code doesn't exit, return ""
                "Offering_Unit":" ",
                "Offering_Department":" ",
                "courseTitleEng":" ",
                "courseTitleChi":" ",
                "Credits":" ",
                "Medium_of_Instruction":" ",
            },
            "prof_info":[
                {
                    "name":" "
                }，
                {},{},{}...
            ]
        }
        '''
    context={
        "course_info": {},
        "prof_info": []
    }
    New_code=request.GET.get('New_code')
    course=course_modle.course_noporf.objects.filter(New_code=New_code).first()
    context['course_info']=course.info()
    prof_course_list=course_modle.prof_with_course.objects.filter(course=course)
    for prof_course in prof_course_list:
        prof=prof_course.prof
        context['prof_info'].append(prof.info())
    return HttpResponse(json.dumps(context),content_type="application/json")

def comment_info(request):
    '''
        :param request:
            /comment_info/?New_code=xxx&prof_name=xxx
        :return:
        {
            "course_info":{
                "New_code":" ",
                "Old_code":" " ,// if old code doesn't exist, return ""
                "Offering_Unit":" ",
                "Offering_Department":" ",
                "courseTitleEng":" ",
                "courseTitleChi":" ",
                "Credits":" ",
                "Medium_of_Instruction":" ",
            }
            "prof_info":{
                "name":" ",
                "grade":" ",
                "attendance":" ",
                "hard":" ",
                "reward":" ",
                "num":,
            }
            "comments":[
                {
                    "content":" ",
                    "grade":" ",
                    "attendance":" ",
                    "hard":" ",
                    "reward":" ",
                    "pre":" ",
                    "recommend":" ",
                    "assignment":" ",
                }
                {},{},{}...
            ]
        }
    '''
    context = {
        "course_info": {},
        "prof_info": {},
        "comments": [],
    }
    New_code=request.GET.get("New_code")
    course=course_modle.course_noporf.objects.filter(New_code=New_code).first()
    prof_name=request.GET.get("prof_name")
    prof=course_modle.prof_info.objects.filter(name=prof_name).first()
    course_prof=course_modle.prof_with_course.objects.filter(prof=prof,course=course).first()
    context["course_info"]=course.info()
    context["prof_info"]=course_prof.info()
    comments=course_modle.comment.objects.filter(course=course_prof)
    for comment in comments:
        context["comments"].append(comment.info())
    return HttpResponse(json.dumps(context), content_type="application/json")

def submit_comment(request):
    '''

    :param request:

        data:{
            "New_code":xxx,
            "prof_name":xxx,
            "content":zzzzzzzz,
            "grade":,
            "attendance":,
            "hard":,
            "reward":,
            "pre":,
            "recommend":,
            "assignment":,
        }
    :return:
        {
            "code":"Success"/"Error",
            "msg":"",
        }
    '''
    New_code=request.POST["New_code"]
    prof_name=request.POST["prof_name"]
    content=request.POST["content"]
    grade=float(request.POST["grade"])
    attendance=float(request.POST["attendance"])
    hard=float(request.POST["hard"])
    reward=float(request.POST["reward"])
    pre=float(request.POST["pre"])
    recommend=float(request.POST["recommend"])
    assignment=float(request.POST["assignment"])

    course_noprof=course_modle.course_noporf.objects.filter(New_code=New_code).first()
    prof=course_modle.prof_info.objects.filter(name=prof_name).first()
    course=course_modle.prof_with_course.objects.filter(course=course_noprof,prof=prof)

    if len(course)>0:
        course=course.first()
        comment=course_modle.comment(
            course=course,
            content=content,
            grade=grade,
            attendance=attendance,
            hard=hard,
            reward=reward,
            pre=pre,
            recommend=recommend,
            assignment=assignment
        )
        comment.save()
        comment.result=comment.cal_result()
        comment.save()
        course.comments+=1
        course.attendance=(course.attendance*(course.comments-1)+comment.attendance)/course.comments
        course.grade=(course.grade*(course.comments-1)+comment.grade)/course.comments
        course.hard=(course.hard*(course.comments-1)+comment.hard)/course.comments
        course.reward=(course.reward*(course.comments-1)+comment.reward)/course.comments
        course.result = (course.result * (course.comments - 1) + comment.result) / course.comments
        course.save()
        return JsonResponse({"code": "Success", "msg": ""})
    else:
        return JsonResponse({"code":"Error","msg":"Course doesn't exist"})