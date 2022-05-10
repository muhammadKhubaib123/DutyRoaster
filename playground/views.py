from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.conf import settings
from sqlalchemy import create_engine
from Roaster.settings import MEDIA_URL
from .models import FilesUpload
from .models import Table
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
                return redirect("/roaster")
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
        # roster_shift=item.shift
        # list_frame=[]
        # for sh in range(roster_shift):
        #     df = pd.read_sql_query('select * from "{}{}"'.format(name,(sh+1)),con=engine)
        #     df=df.style.applymap(lambda x: "background-color: red;color: white" if x==fullname else "")
        #     html=df.to_html()
        #     list_frame.append(html)
        tab=html

    return render(request,'view.html',{"tab":new})
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)
def logout(request):
    auth.logout(request)
    return render(request,'login.html')