# UM_Course_Helper_Server
#### The 2.0 backend of miniprogram '澳大选咩课'.🤐

---
## 框架

本项目是使用Django开发的

## 数据库模型

[models.py](/course/models.py)

- course_noporf
    - 课程相关的数据
    ```python
    class course_noporf(models.Model):
        Offering_Unit=models.CharField(max_length=100,default='') #学院
        Offering_Department=models.CharField(max_length=100,default='') #院系
        New_code=models.CharField(max_length=100,default='') #新的课程编号，在对数据库检索时主要使用这一数据
        Old_code=models.CharField(max_length=100,default='') # 旧的课程编号，新添加的课可能没用
        courseTitleEng=models.CharField(max_length=100,default='') #课程的英文名
        courseTitleChi=models.CharField(max_length=100,default='') #课程的中文名
        Credits=models.CharField(max_length=100,default='') #对应学分
        Course_Duration=models.CharField(max_length=100,default='') #课时？（大概）
        Medium_of_Instruction=models.CharField(max_length=100,default='') #授课语言
        
        def info(self): #调用本函数将会返回课程相关信息（无对应教师）
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
    ```

- prof_info
    - 教师相关信息
    ```python
    class prof_info(models.Model):
        name=models.CharField(max_length=100)

        def info(self): #调用本函数将会返回教师相关信息
            content={
                "name":self.name
            }
            return content
    ```
   
- prof_with_course
    - 课程对应教师
    ```python
        class prof_with_course(models.Model):
            prof=models.ForeignKey(prof_info,on_delete=models.CASCADE) #指向prof_info中的教师实例
            course=models.ForeignKey(course_noporf,on_delete=models.CASCADE) #指向course_noporf中的课程实例
            result=models.FloatField(default=0) # 本课程的综合评价
            comments=models.IntegerField(default=0) # 学生提交的评论总数
            attendance=models.FloatField(default=0.0) # 本课程的签到情况
            grade = models.FloatField(default=0.0) # 本课程的给分情况
            hard = models.FloatField(default=0.0) # 本课程的难易情况
            reward = models.FloatField(default=0.0) # 本课程的收获

            def info(self): #调用本函数将会返回课程相关信息（有对应教师）
                content={
                "name": self.prof.name,
                "result":self.result,
                "grade": self.grade,
                "attendance": self.attendance,
                "hard": self.hard,
                "reward": self.reward,
                "num":self.comments,
                }
                return content
    ```

- comment
    -单次评价
    ```python
        class comment(models.Model):
            course=models.ForeignKey(prof_with_course,on_delete=models.CASCADE) #指向prof_with_course中的课程实例
            content=models.TextField() # 评价内容
            attendance=models.FloatField()# 本课程的签到情况
            pre=models.FloatField()#pre情况
            grade=models.FloatField()# 本课程的给分情况
            hard=models.FloatField()# 本课程的难易情况
            reward=models.FloatField()# 本课程的收获
            recommend=models.FloatField()# 是否推荐
            assignment=models.FloatField()# 作业情况
            result=models.FloatField(default=0) # 本次评价的综合得分
            pub_time=models.DateTimeField(default=timezone.now)# 提交时间

            def info(self): #调用本函数将会返回本次评价的相关信息
                content={
                    "content": self.content,
                    "grade": self.grade,
                    "attendance": self.attendance,
                    "hard": self.hard,
                    "reward": self.reward,
                    "pre": self.pre,
                    "recommand": self.recommend,
                    "assignment": self.assignment,
                }
                return content
    ```