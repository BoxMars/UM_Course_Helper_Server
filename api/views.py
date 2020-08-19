from django.shortcuts import render,HttpResponse
from course import models as course_modle
import json

def course_info(request):
    '''
        /course_info?New_code=xxx
        :return
        {
            "course_info":{
                "id":" "
                "New_code":" "
                "Old_code":" " // if old code doesn't exit, return ""
                "Offering_Unit":" "
                "Offering_Department":" "
                "courseTitleEng":" "
                "courseTitleChi":" "
                "Credits":" "
                "Medium_of_Instruction":" "
            },
            "prof_info":[
                {
                    "id":" "
                    "name":" "
                }
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