from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.conf import settings
from sqlalchemy import create_engine
from Roaster.settings import MEDIA_URL
from .models import FilesUpload
from .models import Table
from .models import seatingplan
from .models import Faculty
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import pandas as pd
from datetime import date, timedelta
import random
from django.contrib import messages
from django.contrib.auth.models import User,auth
import os
from django.db import connection
import numpy as np
import datetime
import io

table={}
def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User = auth.authenticate(username=username,password=password)

        if User is not None:
            auth.login(request,User)
            if request.user.is_superuser:
                return redirect("/home")
            else:
                return redirect("/view")

        else:
            messages.info(request,"Invalid Credentials")
            return redirect('/')
    else:
        return render(request,'login.html')

# Create your views here.
def say_hello(request, *args, **kwargs):
    if request.user.is_authenticated:
        print('yes the user is logged-in')
    else:
        return redirect('/')
    tab=None
    tab1=None
    if request.method=="POST":
        file1=request.FILES['faculty_data']
        file2=request.FILES['resources']
        title=request.POST['title']
        titl = title.replace(" ", "")
        time=datetime.datetime.now()
        titl=titl+str(time)
        table["Ali"]=1
        Table.objects.create(table_name=titl)
        fs=FileSystemStorage()
        first_file1=fs.save(file1.name,file1)
        first_file2=fs.save(file2.name,file2)
        fl=fs.url(first_file1)
        fl1=fs.url(first_file2)
        print(fl1)
        sd = pd.read_csv(fl1.strip("/"), usecols = ['Date'])
        total_duties=pd.read_csv(fl1.strip("/"), usecols = ['Total Duties'])
        i=sd.values.flat[0] 
        print(i)
        print(list(i))
        # j=ed.values.flat[0]
        # startyear, startmonth, startday = map(int, i.split('-'))
        # endyear, endmonth, endday = map(int, j.split('-'))
        # start_date = date(startyear,startmonth,startday)
        # end_date = date(endyear,endmonth,endday)
        sd = sd.dropna()
        print(sd)
        dates=sd.Date.tolist()
        print(dates)
        fac = pd.read_csv(fl.strip("/"),usecols = ['Faculty Name','Designation'])
        print(fac)

        faculty =dict(fac.values)
        print(faculty)
        Associate_Prf=0
        Assistant_Prf=0
        Lecturer=0
        Lab_engineer=0
        for k in faculty:
            if(faculty[k]=="Associate Professor"):
                Associate_Prf=Associate_Prf+1
            elif(faculty[k]=="Assistant Professor"):
                Assistant_Prf=Assistant_Prf+1
            elif(faculty[k]=="Lecturer"):
                Lecturer=Lecturer+1
            elif(faculty[k]=="Lab Engineer"):
                Lab_engineer=Lab_engineer+1
        aso_dut=5*Associate_Prf
        ass_dut=6*Assistant_Prf
        lect_dut=8*Lecturer
        labeng_dut=10*Lab_engineer
        total_dut_ass=aso_dut+ass_dut+lect_dut+labeng_dut
        total_dut_remaining=0
        total_dut_remaining=total_duties.values.flat[0]-total_dut_ass
        print(total_dut_ass)
        print(total_dut_remaining)
        while(total_dut_remaining>0):
            flag=0
            if(total_dut_remaining>(Lab_engineer*1)):
                labeng_dut=labeng_dut+(1*Lab_engineer)
                total_dut_remaining=total_dut_remaining-(1*Lab_engineer)
                flag=flag+1
            if(total_dut_remaining>(Lecturer*1)):
                lect_dut=lect_dut+(1*Lecturer)
                total_dut_remaining=total_dut_remaining-(1*Lecturer)
                flag=flag+1
            if(total_dut_remaining>(Lecturer*1)):
                ass_dut=ass_dut+(1*Assistant_Prf)
                total_dut_remaining=total_dut_remaining-(1*Assistant_Prf)
                flag=flag+1
            if(total_dut_remaining>(Lecturer*1)):
                aso_dut=aso_dut+(1*Associate_Prf)
                total_dut_remaining=total_dut_remaining-(1*Associate_Prf)
                flag=flag+1
            if(total_dut_remaining>0 and flag<4):
                labeng_dut=labeng_dut+1
                total_dut_remaining=total_dut_remaining-1
            if(total_dut_remaining>0 and flag<4):
                lect_dut=lect_dut+1
                total_dut_remaining=total_dut_remaining-1
            if(total_dut_remaining>0 and flag<4):
                ass_dut=ass_dut+1
                total_dut_remaining=total_dut_remaining-1
            if(total_dut_remaining>0 and flag<4):
                aso_dut=aso_dut+1
                total_dut_remaining=total_dut_remaining-1

        print(labeng_dut,lect_dut,ass_dut,aso_dut)
        copyfac=faculty
        for k in faculty:
            cal_dut=0
            lst=[]
            if(faculty[k]=="Associate Professor"):
                cal_dut=int(aso_dut/Associate_Prf)
                lst.append(faculty[k])
                lst.append(cal_dut)
                lst.append(0)
                faculty[k]=lst
            elif(faculty[k]=="Assistant Professor"):
                cal_dut=int(ass_dut/Assistant_Prf)
                lst.append(faculty[k])
                lst.append(cal_dut)
                lst.append(0)
                faculty[k]=lst
            elif(faculty[k]=="Lecturer"):
                cal_dut=int(lect_dut/Lecturer)
                lst.append(faculty[k])
                lst.append(cal_dut)
                lst.append(0)
                faculty[k]=lst
            elif(faculty[k]=="Lab Engineer"):
                cal_dut=int(labeng_dut/Lab_engineer)
                lst.append(faculty[k])
                lst.append(cal_dut)
                lst.append(0)
                faculty[k]=lst

        if ((aso_dut%Associate_Prf)>0):
            for i in range(aso_dut%Associate_Prf):
                d = dict((k, v) for k, v in faculty.items() if v[0] == "Associate Professor")
                randomfac,dut=random.choice(list(d.items()))
                print(randomfac)
                faculty[randomfac][1]+=1
        if ((ass_dut%Assistant_Prf)>0):
            for i in range(ass_dut%Assistant_Prf):
                d = dict((k, v) for k, v in faculty.items() if v[0] == "Assistant Professor")
                randomfac,dut=random.choice(list(d.items()))
                print(randomfac)
                faculty[randomfac][1]+=1
        if ((lect_dut%Lecturer)>0):
            for i in range(lect_dut%Lecturer):
                d = dict((k, v) for k, v in faculty.items() if v[0] == "Lecturer")
                randomfac,dut=random.choice(list(d.items()))
                print(randomfac)
                faculty[randomfac][1]+=1
        if ((labeng_dut%Lab_engineer)>0):
            for i in range(labeng_dut%Lab_engineer):
                d = dict((k, v) for k, v in faculty.items() if v[0] == "Lab Engineer")
                randomfac,dut=random.choice(list(d.items()))
                print(randomfac)
                faculty[randomfac][1]+=1
        print(faculty)
            
        rooms = pd.read_csv(fl1.strip("/"), usecols = ['Index','Room','Total','Date','Shift'])
        rsc=rooms.set_index('Index').T.to_dict('list')

        print(rsc)
        # room=[]
        # room=rooms.values.flatten()
        # name,duties=random.choice(list(faculty.items()))
        # rows,cols=(room.size,len(dates))
        # duts={}
        # for shif in range(shift):
        #     duts["duty"+str(shif)] = [[0 for i in range(cols)] for j in range(rows)]
        # locals().update(duts)
        # fac=""
        # total=0
        # no=0
        for key,values in rsc.items():
            d_list=[]
            d_list=values
            d_list.append('')
            rsc[key]=d_list
        print(rsc)
        for key,values in rsc.items():
            chk=2
            if(values[1]>40):
                chk=3
            for i in range(chk):
                while(True):
                    randomfac,dut=random.choice(list(faculty.items()))
                    duties=int(dut[1])
                    find=0
                    if duties>0:
                        newdict=rsc
                        for skey,svalues in rsc.items():
                            if(values[2]==svalues[2] and values[3]==svalues[3]):
                                if(randomfac in svalues[4]):
                                    print(randomfac,svalues[4])
                                    find=1
                                    break
                        if find==1:
                            continue
                        else:
                            values[4]=values[4]+" "+randomfac
                            break
                    else:
                        continue
        print(rsc)
        # for shifts in range(shift):
        #     for dt in range(cols):
        #         for rm in range(rows):
        #             no=0
        #             while(True):
        #                 local_list=[]
        #                 randomfac,dut=random.choice(list(faculty.items()))
        #                 duties=int(dut[1])
        #                 find=0
        #                 if duties>0:
        #                     for i in range(rows):
        #                         if isinstance(duts["duty"+str(shifts)][i][dt], str)==True:
        #                             if randomfac in duts["duty"+str(shifts)][i][dt]:
        #                                 find=1
        #                                 break
        #                     if find==1:
        #                         continue
        #                     else:
        #                         faculty[randomfac][2]+=1
        #                         duts["duty"+str(shifts)][rm][dt]=randomfac+" ("+str(faculty[randomfac][2])+")"
        #                         faculty[randomfac][1]=duties-1
        #                         break
        #                 else:
        #                     continue
        #     print()
        # disp={}
        # html={}
        # tab={}
        # count=1
        engine = create_engine('postgresql+psycopg2://postgres:khubi123@localhost/Roaster')
        datafrm=pd.DataFrame.from_dict(rsc, orient ='index')
        datafrm.to_sql(titl, engine)
        # for shif in range(shift):
        #     disp["disp"+str(shif)]=pd.DataFrame(duts["duty"+str(shif)],columns=dates)
        #     print(disp["disp"+str(shif)])
        #     disp["disp"+str(shif)].index=room
        #     disp["disp"+str(shif)].to_sql(titl+str(count), engine)
        #     html["html"+str(shif)]=disp["disp"+str(shif)].to_html()
        #     tab["tab"+str(shif)]=html["html"+str(shif)]
        #     count+=1
        disp=rsc
        # print(disp)
        # html=disp.to_html()
        # tab=html
        # print(tab)
        messages.success(request, 'Roaster Generated Successfully')
        return render(request,'roster.html',{'tab': disp})
    return render(request,'roster.html')
def gen_roaster(request, *args, **kwargs):
    if request.user.is_authenticated:
        print('yes the user is logged-in')
    else:
        return redirect('/')
    engine = create_engine('postgresql+psycopg2://postgres:khubi123@localhost/Roaster')
    query_res = seatingplan.objects.all()
    print(query_res)
    for item in query_res:
        name='playground_seatingplan'
        df = pd.read_sql_query('select * from "{}"'.format(name),con=engine)
    print(df)

    # sd = pd.read_csv(fl1.strip("/"), usecols = ['Date'])
    total_duties=600
    # i=sd.values.flat[0] 
    # print(i)
    # print(list(i))
    # sd = sd.dropna()
    # print(sd)
    # dates=sd.Date.tolist()
    # print(dates)
    query_res = Faculty.objects.all()
    print(query_res)
    for item in query_res:
        name='playground_faculty'
        df_fac = pd.read_sql_query('select * from "{}"'.format(name),con=engine)
    print(df_fac)
    # fac = pd.read_csv(fl.strip("/"),usecols = ['Faculty Name','Designation'])
    # print(df_fac)
    df_fac = df_fac.drop(columns="id")
    faculty=df_fac.set_index('Name').T.to_dict('list')
    print(faculty)
    # print(fact_dict)
    # faculty =dict(fac.values)
    # print(faculty)
    Associate_Prf=0
    Assistant_Prf=0
    Lecturer=0
    Lab_engineer=0

    for k in faculty:
        if(faculty[k][0]=="Associate Professor"):
            Associate_Prf=Associate_Prf+1
        elif(faculty[k][0]=="Assistant Professor"):
            Assistant_Prf=Assistant_Prf+1
        elif(faculty[k][0]=="Lecturer"):
            Lecturer=Lecturer+1
        elif(faculty[k][0]=="Lab Engineer"):
            Lab_engineer=Lab_engineer+1
    aso_dut=5*Associate_Prf
    ass_dut=6*Assistant_Prf
    lect_dut=8*Lecturer
    labeng_dut=10*Lab_engineer
    total_dut_ass=aso_dut+ass_dut+lect_dut+labeng_dut
    total_dut_remaining=0
    total_dut_remaining=total_duties-total_dut_ass
    print(total_dut_ass)
    print(total_dut_remaining)
    while(total_dut_remaining>0):
        flag=0
        if(total_dut_remaining>(Lab_engineer*1)):
            labeng_dut=labeng_dut+(1*Lab_engineer)
            total_dut_remaining=total_dut_remaining-(1*Lab_engineer)
            flag=flag+1
        if(total_dut_remaining>(Lecturer*1)):
            lect_dut=lect_dut+(1*Lecturer)
            total_dut_remaining=total_dut_remaining-(1*Lecturer)
            flag=flag+1
        if(total_dut_remaining>(Lecturer*1)):
            ass_dut=ass_dut+(1*Assistant_Prf)
            total_dut_remaining=total_dut_remaining-(1*Assistant_Prf)
            flag=flag+1
        if(total_dut_remaining>(Lecturer*1)):
            aso_dut=aso_dut+(1*Associate_Prf)
            total_dut_remaining=total_dut_remaining-(1*Associate_Prf)
            flag=flag+1
        if(total_dut_remaining>0 and flag<4):
            labeng_dut=labeng_dut+1
            total_dut_remaining=total_dut_remaining-1
        if(total_dut_remaining>0 and flag<4):
            lect_dut=lect_dut+1
            total_dut_remaining=total_dut_remaining-1
        if(total_dut_remaining>0 and flag<4):
            ass_dut=ass_dut+1
            total_dut_remaining=total_dut_remaining-1
        if(total_dut_remaining>0 and flag<4):
            aso_dut=aso_dut+1
            total_dut_remaining=total_dut_remaining-1

    print(labeng_dut,lect_dut,ass_dut,aso_dut)
    copyfac=faculty
    for k in faculty:
        cal_dut=0
        lst=[]
        if(faculty[k][0]=="Associate Professor"):
            cal_dut=int(aso_dut/Associate_Prf)
            lst.append(faculty[k])
            lst.append(cal_dut)
            lst.append(0)
            faculty[k]=lst
        elif(faculty[k][0]=="Assistant Professor"):
            cal_dut=int(ass_dut/Assistant_Prf)
            lst.append(faculty[k])
            lst.append(cal_dut)
            lst.append(0)
            faculty[k]=lst
        elif(faculty[k][0]=="Lecturer"):
            cal_dut=int(lect_dut/Lecturer)
            lst.append(faculty[k])
            lst.append(cal_dut)
            lst.append(0)
            faculty[k]=lst
        elif(faculty[k][0]=="Lab Engineer"):
            cal_dut=int(labeng_dut/Lab_engineer)
            lst.append(faculty[k])
            lst.append(cal_dut)
            lst.append(0)
            faculty[k]=lst
    print(faculty)
    if ((aso_dut%Associate_Prf)>0):
        for i in range(aso_dut%Associate_Prf):
            d = dict((k, v) for k, v in faculty.items() if v[0][0] == "Associate Professor")
            randomfac,dut=random.choice(list(d.items()))
            print(randomfac)
            faculty[randomfac][1]+=1
    if ((ass_dut%Assistant_Prf)>0):
        for i in range(ass_dut%Assistant_Prf):
            d = dict((k, v) for k, v in faculty.items() if v[0][0] == "Assistant Professor")
            randomfac,dut=random.choice(list(d.items()))
            print(randomfac)
            faculty[randomfac][1]+=1
    if ((lect_dut%Lecturer)>0):
        for i in range(lect_dut%Lecturer):
            d = dict((k, v) for k, v in faculty.items() if v[0][0] == "Lecturer")
            randomfac,dut=random.choice(list(d.items()))
            print(randomfac)
            faculty[randomfac][1]+=1
    if ((labeng_dut%Lab_engineer)>0):
        for i in range(labeng_dut%Lab_engineer):
            d = dict((k, v) for k, v in faculty.items() if v[0][0] == "Lab Engineer")
            randomfac,dut=random.choice(list(d.items()))
            print(randomfac)
            faculty[randomfac][1]+=1
    print(faculty)
    rsc=df.set_index('id').T.to_dict('list')
    print(rsc)
    for key,values in rsc.items():
        d_list=[]
        d_list=values
        d_list.append('')
        rsc[key]=d_list
    print(rsc)
    for key,values in rsc.items():
        chk=1
        if(values[1]>20):
            chk=2
        if(values[1]>40):
            chk=3
        for i in range(chk):
            while(True):
                randomfac,dut=random.choice(list(faculty.items()))
                duties=int(dut[1])
                find=0
                if duties>0:
                    newdict=rsc
                    for skey,svalues in rsc.items():
                        if(values[2]==svalues[2] and values[3]==svalues[3]):
                            if(randomfac in svalues[4]):
                                print(randomfac,svalues[4])
                                find=1
                                break
                    if find==1:
                        continue
                    else:
                        values[4]=values[4]+" "+randomfac
                        break
                else:
                    continue
    print(rsc)
    time=datetime.datetime.now()
    titl=str(time)
    Table.objects.create(table_name=titl)
    engine = create_engine('postgresql+psycopg2://postgres:khubi123@localhost/Roaster')
    datafrm=pd.DataFrame.from_dict(rsc, orient ='index')
    datafrm.to_sql(titl, engine)
    disp=rsc
    messages.success(request, 'Roaster Generated Successfully')
    return render(request,'roasterdisplay.html',{'tab': disp})
def seatingplangen(request, *args, **kwargs):
    if request.user.is_authenticated:
        print('yes the user is logged-in')
    else:
        return redirect('/')
    tab=None
    tab1=None
    if request.method=="POST":
        file1=request.FILES['course_data']
        file2=request.FILES['datesheet']
        title=request.POST['title']
        titl = title.replace(" ", "")
        time=datetime.datetime.now()
        titl=titl+str(time)
        fs=FileSystemStorage()
        first_file1=fs.save(file1.name,file1)
        first_file2=fs.save(file2.name,file2)
        fl=fs.url(first_file1)
        fl1=fs.url(first_file2)
        crs = pd.read_csv(fl.strip("/"), usecols = ['Course','Total Students'])
        course_dict=crs.set_index('Course').T.to_dict('list')
        datesheet = pd.read_csv(fl1.strip("/"),usecols = ['Date','Timings','Paper'])
        dts=datesheet.to_dict('index')
        rooms = pd.read_csv(fl1.strip("/"), usecols = ['Rooms Available'])
        rooms=rooms.dropna()
        rm = rooms['Rooms Available'].tolist()
        plan={}
        crs_lst={}
        for ky,val in dts.items():
            plan.update({val['Date']:{}})
            crs_lst.update({val['Date']:{}})
        for key,values in dts.items():
            course_lst=values['Paper'].split(",")
            crs_lst.update()
            local_dict={}
            room_dict={}
            for rms in rm:
               room_dict.update({rms:0}) 
               local_dict.update({rms:{}})
            for room in rm:
                for lst in course_lst:
                    if lst in course_dict:
                        if room_dict[room]<36:
                            nlst={}
                            if course_dict[lst][0]>0:
                                if course_dict[lst][0]>=18:
                                    if room_dict[room]+18<=36:
                                        nlst.update({lst:18})
                                        room_dict[room]+=18
                                        course_dict[lst][0]-=18
                                    else:
                                        req=36-room_dict[room]
                                        room_dict[room]+=req
                                        nlst.update({lst:req})
                                        course_dict[lst][0]-=req
                                else:
                                    req=36-room_dict[room]
                                    if(req<=course_dict[lst][0]):
                                        room_dict[room]+=req
                                        nlst.update({lst:req})
                                        course_dict[lst][0]-=req
                                    else:
                                        room_dict[room]+=course_dict[lst][0]
                                        nlst.update({lst:course_dict[lst][0]})
                                        course_dict[lst][0]=0
                                local_dict[room].update(nlst)
            for chkroom in rm:
                if room_dict[chkroom]>0 and room_dict[chkroom]<=5:
                    cpy=local_dict[chkroom]
                    local_dict[chkroom]={}
                    while(True):
                        randroom,std_list=random.choice(list(local_dict.items())) 
                        if(room_dict[randroom]>5):
                            room_dict[randroom]+=room_dict[chkroom]
                            room_dict[chkroom]=0
                            for key,val in cpy.items():
                                if key in local_dict[randroom]:
                                    local_dict[randroom][key]+=val
                                else:
                                    local_dict[randroom].update(cpy)

                            break
            dt=values['Date']
            plan[dt].update({values['Timings']:{}})
            plan[dt][values['Timings']]=local_dict
            crs_lst[dt][values['Timings']]=course_lst
        seatingplan.objects.all().delete()
        for plan_key,plan_value in plan.items():
            for plan_key2,plan_value2 in plan_value.items():
                for plan_key3,plan_value3 in plan_value2.items():
                    sum_val=0
                    for plan_key4,plan_value4 in plan_value3.items():
                        print(plan_value4)
                        sum_val+=plan_value4
                    if(sum_val>0):
                        plan[plan_key][plan_key2][plan_key3].update({'Total':sum_val})
                        st = seatingplan(Room=plan_key3,Total=sum_val,Date=plan_key,Shift=plan_key2)
                        # seatingplan.Room=plan_key3
                        # seatingplan.Total=sum_val
                        # seatingplan.Date=plan_key
                        # seatingplan.Shift=plan_key2
                        st.save()

        messages.success(request, 'Roaster Generated Successfully')
        return render(request,'seating.html',{'Plan':plan,'course':crs_lst})
    return render(request,'seating.html')
def view(request):
    if request.user.is_authenticated:
        print('yes the user is logged-in')
        fullname = request.user.get_full_name()
    else:
        return redirect('/')
    tab={}
    engine = create_engine('postgresql+psycopg2://postgres:khubi123@localhost/Roaster')
    query_results = Table.objects.all()
    for item in query_results:
        name=item.table_name
        df = pd.read_sql_query('select * from "{}"'.format(name),con=engine)
        new=df.set_index('index').T.to_dict('list')
        html=df.to_html()
        tab=html

    return render(request,'view.html',{"tab":new})
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)
def logout(request):
    auth.logout(request)
    return render(request,'login.html')
def home(request):
    if request.user.is_authenticated:
        print('yes the user is logged-in')
    else:
        return redirect('/')
    return render(request,'home.html')
# fac = pd.read_csv('media/faculty.csv',usecols = ['Faculty Name','Designation'])
# fact_dict=fac.set_index('Faculty Name').T.to_dict('list')
# print(fact_dict)
# Faculty.objects.all().delete()
# for key,value in fact_dict.items():
#     for lst in value:
#         fact=Faculty(Name=key,Post=lst)
#     fact.save()