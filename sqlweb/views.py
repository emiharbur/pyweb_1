from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import itemtable,application,subjecttable,itemimage,Bankaccount,paybill
from .subapp import baseinfo ,subjectnamelist,sortlist,subjectctldetail

@login_required(login_url='/login/')
def index(request):
    userinfo=baseinfo(request)
    return render(request,'zhuye.html',userinfo)


def login_v(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['user'], password=request.POST['password'])
        if user is None:
            return render(request,'登陆页面.html',{'错误':'登陆失败：用户名或密码错误'})
        else:
            login(request,user)
            return redirect("http://chinashunlin.com:8001")
    else:
        return render(request,'登陆页面.html')


def logout_v(request):
    logout(request)
    return redirect("http://chinashunlin.com:8001")


#===================================================
#采购操作
import datetime
from django.db.models import Max


@login_required(login_url='/login/')
def additem(request,sort):
    userinfo = baseinfo(request)

    today=datetime.date.today()
    b=str(today).replace('-','')+'00'
    a= itemtable.objects.filter(itemID__gt=b).count()
    if a==0:
        itemid=str(int(b)+1)
    else:
        maxo=itemtable.objects.aggregate(maxid=Max('itemID'))
        itemid=str(int(maxo["maxid"])+1)
    user_l=request.user
    username = user_l.username
    forminfo={"id":itemid,"申请人":username}

    sortl = sortlist(int(sort))
    namel=subjectnamelist(int(sort))

    userinfo.update(forminfo)

    userinfo.update({"namelist":namel})

    userinfo.update({"sortlist":sortl})

    return render(request,"表格.html",userinfo)


@login_required(login_url='/login/')
def itemsave(request):
    userinfo = baseinfo(request)

    if request.method=='POST':
        #下面是创建物料
        if itemtable.objects.filter(itemID=request.POST.get("itemID")).count()==0:
            item=itemtable(itemID=request.POST.get("itemID"))
            #item.itemID=request.POST.get("itemID")
            item.proposer=request.POST.get("staff")
            item.sort= request.POST.get("classify")
            item.subject=subjecttable.objects.get(subjectshortname=request.POST.get("subject"))
            if Bankaccount.objects.filter(accountnumber=request.POST.get('account')).count()==0:
                bankacc = Bankaccount(accountnumber=request.POST.get('account'))
                bankacc.accountname = request.POST.get("accountname")
                bankacc.bankname = request.POST.get("bankname")
                bankacc.accountstyle = request.POST.get("accountstype")
                bankacc.save()
            else:
                bankacc=Bankaccount.objects.get(accountnumber=request.POST.get('account'))
                bankacc.accountname = request.POST.get("accountname")
                bankacc.bankname = request.POST.get("bankname")
                bankacc.accountstyle = request.POST.get("accountstype")
                bankacc.save()
            item.benefi_acc=bankacc
            item.sum_m=float(request.POST.get("sum"))
            print(item.sum_m)
            if request.POST.get('havebill') == '1':
                item.haverbill=1
            else:
                item.haverbill=0
            item.detail=request.POST.get('detail')
            item.statment="已保存"
            files = request.FILES.getlist("image")
            item.save()
            i=1
            for file in files :
                ext = file.name.split('.')[-1]
                itemimage_a=itemimage(item=itemtable.objects.get(itemID=request.POST.get("itemID")))
                file.name = '{}.{}'.format(request.POST.get("itemID") + str(i), ext)
                itemimage_a.image=file
                itemimage_a.save()
                i=i+1
            userinfo.update({"result":"创建新的物料成功"})
            return render(request,"result.html",userinfo)

        #下面是修改条目
        else:
            item = itemtable.objects.get(itemID=request.POST.get("itemID"))
            if item.statment=="已保存" or item.statment=="申请款项中"and userinfo["groupname"] in ["文员"]:
                # item.itemID=request.POST.get("itemID")
                item.proposer = request.POST.get("staff")
                item.sort = request.POST.get("classify")
                item.subject = subjecttable.objects.get(subjectshortname=request.POST.get("subject"))
                if Bankaccount.objects.filter(accountnumber=request.POST.get('account')).count() == 0:
                    bankacc = Bankaccount(accountnumber=request.POST.get('account'))
                    bankacc.accountname = request.POST.get("accountname")
                    bankacc.bankname = request.POST.get("bankname")
                    bankacc.accountstyle = request.POST.get("accountstype")
                    bankacc.save()
                else:
                    bankacc = Bankaccount.objects.get(accountnumber=request.POST.get('account'))
                    bankacc.accountname = request.POST.get("accountname")
                    bankacc.bankname = request.POST.get("bankname")
                    bankacc.accountstyle = request.POST.get("accountstype")
                    bankacc.save()
                item.benefi_acc=bankacc
                item.sum_m = float(request.POST.get("sum"))
                print(item.sum_m)
                if request.POST.get('havebill') == '1':
                    item.haverbill = 1
                else:
                    item.haverbill = 0
                item.detail = request.POST.get('detail')
                files = request.FILES.getlist("image")
                i = 1
                for file in files:
                    ext = file.name.split('.')[-1]
                    itemimage_a = itemimage(item=itemtable.objects.get(itemID=request.POST.get("itemID")))
                    file.name = '{}.{}'.format(request.POST.get("itemID") + str(i), ext)
                    itemimage_a.image = file
                    itemimage_a.save()
                    i = i + 1
                item.save()
                userinfo.update({"result":"修改并保存物料成功"})
                return render(request,"result.html",userinfo)
            else:
                res="修改失败，当前物料状态"+item.statment+"，无权限修改。"
                userinfo.update({"result":res})
                return render(request,"result.html",userinfo)

@login_required(login_url='/login/')
def item_v(request):
    userinfo = baseinfo(request)

    if userinfo["groupname"]=="采购":
        itemlist=itemtable.objects.filter(proposer=userinfo["username"]).filter(statment__in=["已保存","部分转账"])

    elif userinfo["groupname"]== "文员":
        if userinfo["username"] == "李詠仪":
            itemlist = itemtable.objects.filter(statment__in=["已保存","部分转账"]).filter(subject__lvhua__in=[0])
        else:
            itemlist = itemtable.objects.filter(statment__in=["已保存", "部分转账"]).filter(subject__lvhua__in=[1])

    elif userinfo["groupname"] in ["项目经理","会计","综合","审计","总经理"]:
        itemlist = itemtable.objects.filter(statment__in=["已保存","部分转账"])

    else:
        itemlist={}

    userinfo.update({"itemlist":itemlist})

    return render(request,"item_v.html",userinfo)


@login_required(login_url='/login/')
def applicationsave(request):
    userinfo = baseinfo(request)

    if request.method=="POST":
        if application.objects.filter(applicationID=request.POST.get('applicationid')).count()==0:
            application_a=application(applicationID=request.POST.get("applicationid"))
            application_a.itemID=itemtable.objects.get(itemID=request.POST.get("A_itemID"))
            item_d=itemtable.objects.get(itemID=request.POST.get("A_itemID"))
            if item_d.statment != "部分转账":
                item_d.statment = "申请款项中"
                item_d.save()
            application_a.S_pay_name=request.POST.get("S_account")
            application_a.S_pay_accounnt_type=request.POST.get("S_acc_t")
            application_a.final_sum=0
            application_a.statment="审核中"

            application_a.save()
            userinfo.update({"result":"创建新申请成功"})
            return render(request,"result.html",userinfo)
        else:
            if userinfo["groupname"] in ["文员","会计","综合","审计","总经理"]:
                application_a=application.objects.get(applicationID=request.POST.get("applicationid"))
                application_a.S_pay_name = request.POST.get("S_pay_name")
                application_a.S_pay_accounnt_type = request.POST.get("S_acc_t")
                application_a.account_suggest = request.POST.get("account_suggest")
                application_a.multiple_suggest = request.POST.get("multiple_suggest")
                application_a.audit_suggest = request.POST.get("audit_suggest")
                application_a.final_sum = request.POST.get("final_sum")
                application_a.ceo_suggest = request.POST.get("ceo_suggest")
                application_a.statment = "审核中"
                application_a.save()
                userinfo.update({"result": "添加或修改审核意见成功"})
                return render(request, "result.html", userinfo)



@login_required(login_url='/login/')
def item_detail(request,itemid):
    userinfo = baseinfo(request)

    item_d=itemtable.objects.get(itemID=itemid)
    userinfo.update({"item_d":item_d})

    today=datetime.date.today()
    b="7"+str(today).replace('-','')+'00'
    a= application.objects.filter(applicationID__gt=b).count()
    if a==0:
        applicationID=str(int(b)+1)
    else:
        maxo=application.objects.aggregate(maxid=Max('applicationID'))
        applicationID=str(int(maxo["maxid"])+1)
    if item_d.subject.subjectshortname== "管理费用" :
        namel=subjectnamelist(2)
        sortL=sortlist(2)
    else:
        namel=subjectnamelist(item_d.subject.lvhua)
        sortL = sortlist(item_d.subject.lvhua)
    photol=itemimage.objects.filter(item=item_d)
    userinfo.update({"photo":photol})
    userinfo.update({"申请ID":applicationID})
    userinfo.update({"namelist":namel})


    userinfo.update({"sortlist":sortL})
    if item_d.statment == "部分转账":
        app_a = application.objects.filter(itemID=item_d)
        sum=0
        for app in app_a:
            sum = sum + app.final_sum

        dispay = item_d.sum_m-sum

        userinfo.update({"apppay":sum})
        userinfo.update({"dispay":dispay})


    return render(request,"物料编辑.html",userinfo)

@login_required(login_url='/login/')
def viewapplication(request):
    userinfo = baseinfo(request)
    if userinfo["groupname"]=="采购":
        application_D=application.objects.filter(statment="审核中").filter(itemID__proposer=userinfo['username'])

    elif request.GET.get('statment')== '3':
        application_D = application.objects.filter(statment="批准")

    elif userinfo["groupname"] == "总经理":
        if request.GET.get('ceo') == '3':
            application_D=application.objects.filter(statment="审核中").exclude(account_suggest__exact="").exclude(audit_suggest__exact="")
        elif request.GET.get('ceo') == 'anp' :
            application_D=application.objects.filter(statment="批准")
        else:
            application_D = application.objects.filter(statment="审核中")


    else:
        application_D=application.objects.filter(statment="审核中")

    userinfo.update({"application_d":application_D})



    return render(request,"application_v.html",userinfo)


@login_required(login_url='/login/')
def application_detail(request,applicationid):
    userinfo = baseinfo(request)


    application_d=application.objects.get(applicationID=applicationid)
    if application_d.itemID.subject.subjectshortname == "管理费用":
        sortL=sortlist(2)
        namel=subjectnamelist(2)
    else:
        sortL = sortlist(application_d.itemID.subject.lvhua)
        namel = subjectnamelist(application_d.itemID.subject.lvhua)
    userinfo.update({"application_d":application_d})
    userinfo.update({"namelist":namel})
    photol=itemimage.objects.filter(item__application=application_d)
    userinfo.update({"photo":photol})
    userinfo.update({"sortlist": sortL})

    if application_d.itemID.statment == "部分转账":
        app_a=application.objects.filter(itemID=application_d.itemID)
        sum=0
        for app in app_a:
            sum = sum + app.final_sum
        dissum=application_d.itemID.sum_m-sum
        userinfo.update({"paysum":sum})
        userinfo.update({"dissum":dissum })




    return render(request,"applicationdetail.html",userinfo)



@login_required(login_url='/login/')
def applicationreject(request):
    userinfo = baseinfo(request)
    if request.method == "POST":
        if userinfo("groupname") == "总经理":
            application_a = application.objects.get(applicationID=request.POST.get("applicationid"))
            application_a.S_pay_name = request.POST.get("S_pay_name")
            application_a.S_pay_accounnt_type = request.POST.get("S_acc_t")
            application_a.account_suggest = request.POST.get("account_suggest")
            application_a.multiple_suggest = request.POST.get("multiple_suggest")
            application_a.audit_suggest = request.POST.get("audit_suggest")
            application_a.final_sum = request.POST.get("final_sum")
            application_a.ceo_suggest = request.POST.get("ceo_suggest")
            application_a.statment = "不批准"

            application_a.save()
            userinfo.update({"result": "否决申请成功"})
            return render(request, "result.html", userinfo)
    else:
        userinfo.update({"result": "操作失败，错误操作或无权限操作"})
        return render(request, "result.html", userinfo)

@login_required(login_url='/login/')
def applicationapprove(request):
    userinfo = baseinfo(request)
    if request.method == "POST":
        if userinfo["groupname"] == "总经理":
            application_a = application.objects.get(applicationID=request.POST.get("applicationid"))
            application_a.S_pay_name = request.POST.get("S_pay_name")
            application_a.S_pay_accounnt_type = request.POST.get("S_acc_t")
            application_a.account_suggest = request.POST.get("account_suggest")
            application_a.multiple_suggest = request.POST.get("multiple_suggest")
            application_a.audit_suggest = request.POST.get("audit_suggest")
            application_a.final_sum = request.POST.get("final_sum")
            application_a.ceo_suggest = request.POST.get("ceo_suggest")
            application_a.statment = "批准"

            application_a.save()
            userinfo.update({"result": "批准申请成功"})
            return render(request, "result.html", userinfo)
    else:
        userinfo.update({"result": "操作失败，错误操作或无权限操作"})
        return render(request, "result.html", userinfo)

from .models import subjecttable

@login_required(login_url='/login/')
def subject_v(request):
    userinfo = baseinfo(request)

    subjectlist = subjecttable.objects.all()
    sortlist=[]
    for i in subjectlist:
        sort=""
        if i.lvhua == 1:
            sort=sort+" 绿化"
        if i.yuanjian == 1:
            sort=sort+" 园建"
        if i.shuidian == 1:
            sort=sort+" 水电"
        if i.light == 1:
            sort=sort+" 绿化"
        sortlist.append(sort)

    a={"subjectlist":subjectlist}
    userinfo.update({"sortlist":sortlist})
    userinfo.update(a)




    return  render(request,"subject_v.html",userinfo)
from .subapp import excel

@login_required(login_url='/login/')
def addsubject(request):

    userinfo = baseinfo(request)
    return render(request,"subjectdetail.html",userinfo)


@login_required(login_url='/login/')
def subjectsave(request):
    userinfo = baseinfo(request)
    if request.method=="POST":
        if request.POST.get("subjectID") == "":
            subject_a = subjecttable(subjectname=request.POST.get("subjectname"))
            subject_a.subjectshortname =  request.POST.get("subjectshortname")
            subject_a.contractnunber= request.POST.get("contractnunber")
            subject_a.subjectsum = request.POST.get("subjectsum")
            subject_a.jia = request.POST.get("jia")
            subject_a.yi = request.POST.get("yi")
            subject_a.subjectmanager = request.POST.get("subjectmanager")
            if request.POST.get("lvhua") != None:
                subject_a.lvhua = request.POST.get("lvhua")
            if request.POST.get("yuanjian") != None:
                subject_a.yuanjian = request.POST.get("yuanjian")
            if request.POST.get("lvlighthua") != None:
                subject_a.light = request.POST.get("light")
            if request.POST.get("shuidian") != None:
                subject_a.shuidian = request.POST.get("shuidian")
            if request.POST.get("begintime") != "":
                subject_a.begintime = request.POST.get("begintime")
            if request.POST.get("endtime") != "":
                subject_a.endtime = request.POST.get("endtime")
            subject_a.statment = request.POST.get("statment")
            subject_a.subjectnote = request.POST.get("subjectnote")
            if request.POST.get("percentage") != "":
                subject_a.percentage = request.POST.get("percentage")
            subject_a.save()
            userinfo.update({"result":"新项目创建成功"})
            return render(request,"result.html",userinfo)
        else:
            subject_a = subjecttable.objects.get(subjectID=request.POST.get("subjectID"))
            subject_a.subjectname = request.POST.get("subjectname")
            subject_a.subjectshortname = request.POST.get("subjectshortname")
            subject_a.contractnunber = request.POST.get("contractnunber")
            subject_a.subjectsum = request.POST.get("subjectsum")
            subject_a.jia = request.POST.get("jia")
            subject_a.yi = request.POST.get("yi")
            subject_a.subjectmanager = request.POST.get("subjectmanager")
            if request.POST.get("lvhua") != None:
                subject_a.lvhua = request.POST.get("lvhua")
            if request.POST.get("yuanjian") != None:
                subject_a.yuanjian = request.POST.get("yuanjian")
            if request.POST.get("lvlighthua") != None:
                subject_a.light = request.POST.get("light")
            if request.POST.get("shuidian") != None:
                subject_a.shuidian = request.POST.get("shuidian")
            if request.POST.get("begintime") != "":
                subject_a.begintime = request.POST.get("begintime")
            if request.POST.get("endtime") != "":
                subject_a.endtime = request.POST.get("endtime")
            subject_a.statment = request.POST.get("statment")
            subject_a.subjectnote = request.POST.get("subjectnote")
            if request.POST.get("percentage") != "":
                subject_a.percentage = request.POST.get("percentage")
            subject_a.save()
            userinfo.update({"result": "保存项目成功"})
            return render(request, "result.html", userinfo)
    else:
        return HttpResponse("请求不是post")


@login_required(login_url='/login/')
def subjectdetail(request,subjectid):
    userinfo = baseinfo(request)
    subject_a=subjecttable.objects.get(subjectID=subjectid)
    userinfo.update({'subject_a':subject_a})

    return render(request,"subjectdetail.html",userinfo)

@login_required(login_url='/login/')
def payview(request):
    userinfo=baseinfo(request)

    if userinfo["username"] == "陈燕兴":
        application_D = application.objects.filter(statment="批准").filter(S_pay_accounnt_type="私人账户")
    else:
        application_D = application.objects.filter(statment="批准").filter(S_pay_accounnt_type="公司账户")




    userinfo.update({"application_d":application_D})
    return render(request,"pay_v.html",userinfo)


@login_required(login_url='/login/')
def paydetail(request,appid):

    userinfo = baseinfo(request)
    application_d=application.objects.get(applicationID=appid)
    userinfo.update({"application_d":application_d})

    return render(request,"pay_detail.html",userinfo)



@login_required(login_url='/login/')
def paycheck (request,appid):
    userinfo=baseinfo(request)
    application_d= application.objects.get(applicationID=appid)
    application_d.statment="已转账"
    application_d.save()

    payment = paybill(applicationID=application_d)
    payment.pay_name = application_d.S_pay_name
    payment.pay_accounnt_type = application_d.S_pay_accounnt_type
    payment.accountnunber = application_d.itemID.benefi_acc
    payment.sum_m = application_d.final_sum
    payment.save()

    app_a=application.objects.filter(itemID=application_d.itemID)
    sum = 0
    for app in app_a:
        sum = sum + app.final_sum

    item_d = itemtable.objects.get(itemID=application_d.itemID.itemID)
    if sum == item_d.sum_m:
        item_d.statment="待还单"
    elif sum < item_d.sum_m:
        item_d.statment="部分转账"
    else :
        item_d.statment="出错"
    item_d.save()
    userinfo.update({"result":"转账保存成功"})
    return render(request,'result.html',userinfo)


def subjectctl(request):
    userinfo = baseinfo(request)
    if request.method == "GET":
        dicttmp=subjectctldetail(request.GET.get("subject"))
        maxsum = 0
        for i,j,k in dicttmp:
            z=j+k
            if z>=maxsum:
                maxsum=z


        subject_d = subjecttable.objects.get(subjectshortname=request.GET.get("subject"))


        userinfo.update({"sortL":dicttmp})
        userinfo.update({"maxsum": maxsum})

        userinfo.update({"subject_d":subject_d})

        return render(request,"subjectctl.html",userinfo)




    pass




# Create your views here.
