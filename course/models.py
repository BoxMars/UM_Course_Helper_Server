from django.db import models
from django.utils import timezone
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

    def info(self):
        content={
            "New_code":self.New_code,
            "Offering_Unit":self.Offering_Unit,
            "Old_code":self.Old_code,
            "courseTitleEng":self.courseTitleEng,
            "courseTitleChi":self.courseTitleChi,
            "Credits":float(self.Credits),
            "Medium_of_Instruction":self.Medium_of_Instruction,
            "Offering_Department":self.Offering_Department,
        }
        return content


class prof_info(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    name=models.CharField(max_length=100)

    def info(self):
        content={
            "name":self.name
        }
        return content

class prof_with_course(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    prof=models.ForeignKey(prof_info,on_delete=models.CASCADE)
    course=models.ForeignKey(course_noporf,on_delete=models.CASCADE)
    grade=models.FloatField(default=0)
    comments=models.IntegerField(default=0)

class comment(models.Model):
    uuid=models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    course=models.ForeignKey(prof_with_course,on_delete=models.CASCADE)
    content=models.TextField()
    attendance=models.FloatField()
    pre=models.FloatField()
    grade=models.FloatField()
    hard=models.FloatField()
    reward=models.FloatField()
    recommend=models.FloatField()
    assignment=models.FloatField()
    result=models.FloatField(default=0)
    pub_time=models.DateTimeField(default=timezone.now)
