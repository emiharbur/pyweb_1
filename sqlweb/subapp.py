from django.contrib.auth.models import Group
from .models import subjecttable,application,paybill,itemtable

class subjectpay():
    def __init__(self, name, sum,persum,realsum):
        self.name = name
        self.sum = sum
        self.persum = persum
        self.realsum = realsum


def perdict():
    subli = subjecttable.objects.filter(lvhua=0).filter(statment__in=["施工中","维修","结算中"])
    obl=[]
    for i in subli:
        payl=paybill.objects.filter(applicationID__itemID__subject_id=i)
        realsum=0
        for j in payl:
            realsum += j.sum_m
        itl=itemtable.objects.filter(subject_id=i)
        persum = 0
        for k in itl:
            persum += k.sum_m

        ob=subjectpay(i.subjectshortname,i.subjectsum,persum-realsum,realsum)
        obl.append(ob)




    return obl


def baseinfo(request):
    user_l=request.user
    username = user_l.username
    current_group_set = Group.objects.get(user=user_l)
    groupname=current_group_set.name
    userinfo = {'username':username,"groupname":groupname}
    if groupname == "采购":
        worklist=[
            ["添加管理费用物料单", "http://chinashunlin.com:8001/additem/2/"],
            ["添加绿化物料单", "http://chinashunlin.com:8001/additem/1/"],
            ["添加园建亮化水电物料单", "http://chinashunlin.com:8001/additem/0/"],
            ["管理物料单","http://chinashunlin.com:8001/item/"],
            ["查看申请","http://chinashunlin.com:8001/viewapplication/"],
        ]
        landlist=[]

    elif groupname == "文员":
        worklist=[
            ["添加管理费用物料单", "http://chinashunlin.com:8001/additem/2/"],
            ["添加绿化物料单", "http://chinashunlin.com:8001/additem/1/"],
            ["添加园建亮化水电物料单", "http://chinashunlin.com:8001/additem/0/"],
            ["管理物料单","http://chinashunlin.com:8001/item/"],
            ["查看申请","http://chinashunlin.com:8001/viewapplication"],
        ]
        landlist=[]

    elif groupname in ["会计"]:
        worklist = [
            ["添加管理费用物料单", "http://chinashunlin.com:8001/additem/2/"],
            ["添加绿化物料单", "http://chinashunlin.com:8001/additem/1/"],
            ["添加园建亮化水电物料单", "http://chinashunlin.com:8001/additem/0/"],
            ["管理物料单", "http://chinashunlin.com:8001/item/"],
            ["查看申请", "http://chinashunlin.com:8001/viewapplication"],
        ]
        landlist=[]

    elif groupname in ["综合","审计"]:
        worklist = [
            ["添加管理费用物料单", "http://chinashunlin.com:8001/additem/2/"],
            ["添加绿化物料单", "http://chinashunlin.com:8001/additem/1/"],
            ["添加园建亮化水电物料单", "http://chinashunlin.com:8001/additem/0/"],
            ["管理物料单", "http://chinashunlin.com:8001/item/"],
            ["查看申请", "http://chinashunlin.com:8001/viewapplication"],
        ]
        landlist=[]

    elif groupname in ["总经理"]:
        worklist = [
            ["查看申请", "http://chinashunlin.com:8001/viewapplication"],
        ]
        app_c= application.objects.filter(statment="审核中").exclude(account_suggest__exact="").exclude(audit_suggest__exact='').count()
        app_anp = application.objects.filter(statment="批准").count()

        landlist =[
            ["其余部门已给意见的审批单" , app_c,"http://chinashunlin.com:8001/viewapplication/?ceo=3"],
            ["已批准但尚未转账", app_anp, "http://chinashunlin.com:8001/viewapplication/?ceo=anp"],


                    ]


    elif groupname in ["财务"]:
        worklist=[
            ["物料转账","http://chinashunlin.com:8001/payview"]
        ]
        landlist=[]

    elif groupname == "预算" and username !="李咏欣":
        worklist=[
            ["添加项目", "http://chinashunlin.com:8001/addsubject"],
            ["项目管理","http://chinashunlin.com:8001/subjecttable"],

        ]
        landlist=[]

    if groupname == "主管经理":
        worklist=[
            ["添加物料单","http://chinashunlin.com:8001/additem/"],
            ["管理物料单","http://chinashunlin.com:8001/item/"],
            ["查看申请","http://chinashunlin.com:8001/viewapplication"],
        ]
        landlist=[]





    subjectlist=subjecttable.objects.all()
    subject_l={"subjectlist_b":subjectlist}

    userinfo.update({"worklist":worklist})
    userinfo.update(subject_l)
    userinfo.update({"landlist":landlist})
    payd=perdict()
    userinfo.update({"obl":payd})

    return userinfo


def sortlist(x):
    if x == 0:
        sort_L = ["水泥", "混凝土", "钢筋", "石子、粉", "模板木方", "砖", "沙", "机械台班", "灯具", "电线", "管材", "设备", "工具材料", "人工", "交通运费",
                    "食宿", "其他", "税费"]
    elif x == 2:
        sort_L = ["工资","工会经费","保障医疗","税费","办公费用","快递运费","旅差费","路油修车","食宿费","伙食费","办公室租金","办公室水电","宿舍租金","宿舍水电","设备设施","其他"]

    else:
        sort_L=["交通费","路、油费","机械费用","肥料","农药","工用具","零星材料","食宿","人工","运费","其他"]
    return sort_L

def subjectnamelist(x):
    if x == 0:

        subjectlist=subjecttable.objects.filter(lvhua=0).filter(statment__in=["施工中","维修","结算中"])
        namelist=[]
        for i in subjectlist:
            namelist.append(i.subjectshortname)
    elif x == 2:
        namelist = ["管理费用"]

    else:

        subjectlist = subjecttable.objects.filter(lvhua=1).filter(statment__in=["施工中","维修","结算中"])
        namelist = []
        for i in subjectlist:
            namelist.append(i.subjectshortname)
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
            subject_a.begintime = str(sheet.cell(r, 11).value).replace(".", "-")
        if str(sheet.cell(r, 12).value) != "":
            subject_a.endtime = str(sheet.cell(r, 12).value).replace(".", "-")
        subject_a.statment = sheet.cell(r, 13).value
        subject_a.subjectnote = sheet.cell(r, 12).value

        subject_a.save()


def subjectctldetail(x):
    subject_a= subjecttable.objects.get(subjectshortname=x)
    sortL=sortlist(0)
    subjectctl=[]
    for sort in sortL:
        payl=paybill.objects.filter(applicationID__itemID__subject_id=subject_a).filter(applicationID__itemID__sort=sort)
        rsum = 0
        for j in payl:
            rsum += j.sum_m
        psum = 0
        iteml=itemtable.objects.filter(subject_id=subject_a).filter(sort=sort)
        for k in iteml:
            psum += k.sum_m
        subjectctl.append([sort,rsum,psum-rsum])
    return subjectctl
