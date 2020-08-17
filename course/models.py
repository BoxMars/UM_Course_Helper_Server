from django.db import models
import uuid
class course(models.Model):
    uuid=models.UUIDField(primary_key=True, default=uuid.uuid4,unique=True)
    Offering_Unit=models.CharField(max_length=100,default='')
    Offering_Department=models.CharField(max_length=100,default='')
    New_code=models.CharField(max_length=100,default='')
    Old_code=models.CharField(max_length=100,default='')
    courseTitleEng=models.CharField(max_length=100,default='')
    courseTitleChi=models.CharField(max_length=100,default='')
    Credits=models.CharField(max_length=100,default='')
    Course_Duration=models.CharField(max_length=100,default='')
    Medium_of_Instruction=models.CharField(max_length=100,default='')
    Teacher_Information=models.CharField(max_length=100,default='')

class course_noporf(models.Model):
    uuid=models.UUIDField(primary_key=True, default=uuid.uuid4,unique=True)
    Offering_Unit=models.CharField(max_length=100,default='')
    Offering_Department=models.CharField(max_length=100,default='')
    New_code=models.CharField(max_length=100,default='')
    Old_code=models.CharField(max_length=100,default='')
    courseTitleEng=models.CharField(max_length=100,default='')
    courseTitleChi=models.CharField(max_length=100,default='')
    Credits=models.CharField(max_length=100,default='')
    Course_Duration=models.CharField(max_length=100,default='')
    Medium_of_Instruction=models.CharField(max_length=100,default='')


class prof_info(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    name=models.CharField(max_length=100)

class prof_with_course(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    prof=models.ForeignKey(prof_info,on_delete=models.CASCADE)
    course=models.ForeignKey(course_noporf,on_delete=models.CASCADE)

