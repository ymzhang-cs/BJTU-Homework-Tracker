# BJTU-Homework-Tracker

北京交通大学智慧课程平台作业抓取

## 技术原理

### 1. 获取课程列表

http://123.121.147.7:88/ve/back/coursePlatform/course.shtml?method=getCourseList&pagesize=100&page=1&xqCode=2024202501

**Response:**

```json
{
    "courseList": [
        {
            "id": 112261,
            "name": "计算机类专业导论",
            "course_num": "M202001B",
            "pic": null,
            "teacher_id": 1491,
            "teacher_name": "侯亚欣",
            "begin_date": "2024-09-02 00:00:00",
            "end_date": "2025-01-12 00:00:00",
            "type": 0,
            "selective_course_id": null,
            "fz_id": "2024-2025-1-2M202001B02",
            "xq_code": "2024202501",
            "boy": "1"
        },
        {...},
        {...},
        ...
    ],
    "STATUS": "0",
    "message": "成功",
    "rows": 100,
    "page": 1,
    "currentRows": 已删除,
    "total": 已删除,
    "totalPage": 1
}
```

### 2. 获取作业列表

http://123.121.147.7:88/ve/back/coursePlatform/homeWork.shtml?method=getHomeWorkList&cId=112261&subType=1&page=1&pagesize=10

cID 为课程 ID
subType 为作业类型，0、1、2分别对应作业、课程报告、实验


```json
{
    "courseNoteList": [
        {
            "id": 90030,
            "create_date": "2024-09-12 12:57:58",
            "course_id": 112261,
            "course_sched_id": 0,
            "course_name": "计算机类专业导论",
            "comment_num": 0,
            "content": "<p>请按照附件要求完成。<\/p><p>不允许重逢提交。<\/p>",
            "title": "期末大作业",
            "user_id": 1491,
            "praise_num": 0,
            "is_fz": 0,
            "content_type": 0,
            "calendar_id": null,
            "end_time": "2024-11-04 00:00",
            "open_date": "2024-10-08 00:00",
            "score": "100",
            "moudel_id": 0,
            "isOpen": 2,
            "status": "1",
            "submitCount": 0,
            "allCount": 98,
            "excellentCount": 0,
            "is_publish_answer": null,
            "review_method": {
                "type": "0"
            },
            "makeup_flag": "0",
            "is_repeat": 0,
            "makeup_time": "",
            "snId": null,
            "scoreId": null,
            "subTime": null,
            "subStatus": "未提交",
            "return_flag": null,
            "return_num": 0,
            "is_excellent": "0",
            "stu_score": "未公布成绩",
            "refAnswer": "未公布答案",
            "pg_user_id": null,
            "pg_user_name": null,
            "returnContent": null,
            "lastScore": "未公布成绩"
        }
    ],
    "page": 1,
    "size": 10,
    "currentRow": 1,
    "total": 1,
    "totalPage": 1,
    "STATUS": "0",
    "message": "成功"
}
```