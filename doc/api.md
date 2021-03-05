## API
```
    url="https://test.com"
```

### 课程信息
#### request GET
> url/course_info?New_code=xxx 

查询时请将字母大写
#### 返回内容
```
    {
            "course_info":{
                "New_code":" ", // 课程编号
                "Old_code":" " ,// if old code doesn't exit, return "" 旧的课程编号，已弃用
                "Offering_Unit":" ", // 课程提供部门
                "Offering_Department":" ", //课程提供专业
                "courseTitleEng":" ",   //课程的中文名
                "courseTitleChi":" ", //课程的英文名
                "Credits":" ",  //对应学分
                "Medium_of_Instruction":" ", //
            }, 
            "prof_info":[
                {   
                    //此处源码部分注释未更新
                    "name": "", //教授
                    "result":"", //课程总评 
                    "grade": "", //给分
                    "attendance": "", //签到
                    "hard": "", //难易
                    "reward": "", //收获
                    "num":"",  //评价总数
                }，
                {},{},{}...
            ]
        }
```
#### 編號錯誤時的返回内容
```json
    {
        "course_info":"Error Code",
        "msg":"Course doesn't exist",
        "prof_info":[]
    }
```
### 评价信息
#### request GET
> url/comment_info/?New_code=xxx&prof_name=xxx

查询时请将字母大写(/course_info?New_code=xxx 返回的均为大写，可直接引用)
#### 返回内容
```
    {
            "course_info":{
                "New_code":" ",
                "Old_code":" " ,# if old code doesn't exist, return ""
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
            // 以上部分于 /course_info?New_code=xxx 相同

            // 具体评论
            // 由于只用于展示 评论(返回信息中的content)内容 ， 故如若评价(comments)中 评论(content) 为 空：""，本条评价将不会包含在数组返回
            "comments":[
                {
                    "content":" ", //具体评价内容
                    //以下与 "course_info" 相同
                    "grade":" ",
                    "attendance":" ",
                    "hard":" ",
                    "reward":" ",
                    "pre":" ",
                    "recommend":" ",
                    "assignment":" ",
                    "pub_time" : " ",
                }
                {},{},{}...
            ]
        }
```

#### 編號錯誤時的返回内容

```json
{
    "content":"No comment yet",
    "grade":" 0",
    "attendance":"0 ",
    "hard":" 0",
    "reward":"0 ",
    "pre":" 0",
    "recommend":"0 ",
    "assignment":" 0"
}
```
### 提交评论
#### request POST
> url/submit_comment/
```
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
```

#### 返回内容
```
{
    "code": "1", 
    "msg": "Your comment has been submitted successfully"
}
```
or
```json
{
  "code":"0",
  "msg":"Some unknown errors have occurred"
}
```
### 教授信息
#### request GET
> url/prof_info?name=xxx

字母全大写

#### 返回内容

```
    {
        "prof_info":{
            "name":"", //教授
        }
        // 教授所教授的全部课程
        "course":[
            {
                //课程信息
                "course_info":{
                    "New_code":" ",
                    "Old_code":" " ,// if old code doesn't exist, return ""
                    "Offering_Unit":" ",
                    "Offering_Department":" ",
                    "courseTitleEng":" ",
                    "courseTitleChi":" ",
                    "Credits":" ",
                    "Medium_of_Instruction":" ",
                    },
                
                // 本课程中教授信息
                // 懒得改代码了，与上文信息重复 😁
                "prof_info":{
                    "name":" ",
                    "grade":" ", //给分
                    "attendance":" ", // 签到
                    "hard":" ", //难易
                    "reward":" ", //收获
                    "num":,  //评论数量
                }
            },
            {},{},{}...
        ],
    }
```
#### 編號錯誤時的返回内容
```json
{
            "prof_info": {
                "name": "Error NAME",
            },
            "course":[]
```


### fuzzy search
```
url/fuzzy_search?text=Test&type=course/prof/title
```

### 请求统计数据
```
url/get_stat
```
直接上结果
```
{
    "course_num": 1643, 
    "prof_num": 907, 
    "comment_num": 4381, 
    "faculty_detail": {
        "FAH": {
            "course": 373, 
            "comment": 1408
        }, 
        "FBA": {
            "course": 255, 
            "comment": 1254
        }, 
        "FED": {
            "course": 216, 
            "comment": 262
        }, 
        "FHS": {
            "course": 32, 
            "comment": 48
        }, 
        "FLL": {
            "course": 130, 
            "comment": 35
        }, 
        "FSS": {
            "course": 333, 
            "comment": 689
        }, 
        "FST": {
            "course": 275, 
            "comment": 436
        }
    }
}
```
