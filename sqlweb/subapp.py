from django.contrib.auth.models import Group
from .models import subjecttable


def baseinfo(request):
    user_l=request.user
    username = user_l.username
    current_group_set = Group.objects.get(user=user_l)
    groupname=current_group_set.name
    userinfo = {'username':username,"groupname":groupname}
    if groupname == "采购":
        worklist=[
            ["添加绿化物料单", "http://chinashunlin.com:8001/additem/1/"],
            ["添加园建亮化水电物料单", "http://chinashunlin.com:8001/additem/0/"],
            ["管理物料单","http://chinashunlin.com:8001/item/"],
            ["查看申请","http://chinashunlin.com:8001/viewapplication/"],
        ]

    elif groupname == "文员":
        worklist=[
            ["添加绿化物料单", "http://chinashunlin.com:8001/additem/1/"],
            ["添加园建亮化水电物料单", "http://chinashunlin.com:8001/additem/0/"],
            ["管理物料单","http://chinashunlin.com:8001/item/"],
            ["查看申请","http://chinashunlin.com:8001/viewapplication"],
        ]
    elif groupname in ["会计"]:
        worklist = [
            ["添加绿化物料单", "http://chinashunlin.com:8001/additem/1/"],
            ["添加园建亮化水电物料单", "http://chinashunlin.com:8001/additem/0/"],
            ["管理物料单", "http://chinashunlin.com:8001/item/"],
            ["查看申请", "http://chinashunlin.com:8001/viewapplication"],
        ]

    elif groupname in ["综合","审计","总经理"]:
        worklist = [
            ["查看申请", "http://chinashunlin.com:8001/viewapplication"],
        ]

    elif groupname in ["财务"]:
        worklist=[
            ["物料转账","http://chinashunlin.com:8001/payview"]
        ]

    elif groupname == "预算" and username !="李咏欣":
        worklist=[
            ["添加项目", "http://chinashunlin.com:8001/addsubject"],
            ["项目管理","http://chinashunlin.com:8001/subjecttable"],

        ]

    if groupname == "经理主管":
        worklist=[
            ["添加物料单","http://chinashunlin.com:8001/additem/"],
            ["管理物料单","http://chinashunlin.com:8001/item/"],
            ["查看申请","http://chinashunlin.com:8001/viewapplication"],
        ]




    subjectlist=subjecttable.objects.all()
    subject_l={"subjectlist_b":subjectlist}

    userinfo.update({"worklist":worklist})
    userinfo.update(subject_l)
    return userinfo


def sortlist(x):
    if x == 0:
        sort_L = ["水泥", "混凝土", "钢筋", "石子、粉", "模板木方", "砖", "沙", "机械台班", "灯具", "电线", "管材", "设备", "工具材料", "人工", "交通运费",
                    "食宿", "其他", "税费"]
    else:
        sort_L=["交通费","路、油费","机械费用","肥料","农药","工用具","零星材料","食宿","人工","运费","其他"]
    return sort_L

def subjectnamelist(x):
    if x == 0:

        subjectlist=subjecttable.objects.filter(lvhua=0).filter(statment__in=["施工中","维修","结算中"])
        namelist=[]
        for i in subjectlist:
            namelist.append(i.subjectshortname)
    else:
        namelist = []
    return namelist


def excel():
    import xlrd
    from sqlweb.models import subjecttable

    book = xlrd.open_workbook('/root/web/pyweb_1/static/abc.xlsx')
    sheet = book.sheet_by_name("1")

    for r in range(1, sheet.nrows):
        subject_a = subjecttable(subjectname=sheet.cell(r, 1).value)

        subject_a.subjectname = sheet.cell(r, 1).value
        subject_a.subjectshortname = sheet.cell(r, 2).value
        if str(sheet.cell(r, 3).value) != None:
            subject_a.contractnunber = sheet.cell(r, 3).value
        if str(sheet.cell(r, 4).value) != '':
            subject_a.subjectsum = sheet.cell(r, 4).value
        if str(sheet.cell(r, 6).value) != None:
            subject_a.jia = sheet.cell(r, 6).value
        if str(sheet.cell(r, 5).value) != None:
            subject_a.yi = sheet.cell(r, 5).value
        if str(sheet.cell(r, 15).value) != None:
            subject_a.subjectmanager = sheet.cell(r, 15).value
        if str(sheet.cell(r, 8).value) == '1.0':
            subject_a.lvhua = sheet.cell(r, 8).value
        if str(sheet.cell(r, 10).value) == '1.0':
            subject_a.light = sheet.cell(r, 10).value
        if str(sheet.cell(r, 9).value) == '1.0':
            subject_a.yuanjian = sheet.cell(r, 9).value
        if str(sheet.cell(r, 7).value) == '1.0':
            subject_a.shuidian = sheet.cell(r, 7).value

        if str(sheet.cell(r, 11).value) != "" :
            subject_a.begintime = sheet.cell(r, 11).value.replace(".", "-")
        if str(sheet.cell(r, 12).value) != "":
            subject_a.endtime = sheet.cell(r, 12).value.replace(".", "-")
        subject_a.statment = sheet.cell(r, 13).value
        subject_a.subjectnote = sheet.cell(r, 12).value

        subject_a.save()


