from django.http.response import HttpResponse
from django.shortcuts import render
from django.conf import settings

from Roaster.settings import MEDIA_URL
from .models import FilesUpload
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import pandas as pd
from datetime import date, timedelta
import random
from django.contrib import messages
import os

# Create your views here.
def say_hello(request, *args, **kwargs):
    tab=None
    tab1=None
    if request.method=="POST":
        file1=request.FILES['faculty']
        file2=request.FILES['resources']
        higlight=request.POST['high']
        print(higlight)
        fs=FileSystemStorage()
        fs.save(file1.name,file1)
        fs.save(file2.name,file2)
        print("File: ",file1)
        fl="media/{}".format(file1)
        fl1="media/{}".format(file2)
        print(fl1)
        sd = pd.read_csv(fl1, usecols = ['Start Date'])
        ed = pd.read_csv(fl1, usecols = ['End Date'])
        total_duties=pd.read_csv(fl1, usecols = ['Total Duties'])
        i=sd.values.flat[0]
        j=ed.values.flat[0]
        startyear, startmonth, startday = map(int, i.split('-'))
        endyear, endmonth, endday = map(int, j.split('-'))
        start_date = date(startyear,startmonth,startday)
        end_date = date(endyear,endmonth,endday)
        dates=[]
        for single_date in daterange(start_date, end_date):
            dates.append(single_date.strftime("%Y-%m-%d"))

        print(dates)
        fac = pd.read_csv(fl,usecols = ['Faculty Members','Duties'])
        print(fac)
        faculty =dict(fac.values)
        print(faculty)
        Associate_Prf=0
        Assistant_Prf=0
        Lecturer=0
        Lab_engineer=0
        for k in faculty:
            if(faculty[k]=="Associate Proffesor"):
                Associate_Prf=Associate_Prf+1
            elif(faculty[k]=="Assistant Proffesor"):
                Assistant_Prf=Assistant_Prf+1
            elif(faculty[k]=="Lecturer"):
                Lecturer=Lecturer+1
            elif(faculty[k]=="Lab Engineer"):
                Lab_engineer=Lab_engineer+1
        td=total_duties.values.flat[0]
        Aso=(td/100)*5
        Ass=(td/100)*20
        lect=(td/100)*35
        labeng=(td/100)*40
        remain=0
        if(Aso%Associate_Prf!=0):
            remain=remain+(Aso%Associate_Prf)
            Associate_Prf=Associate_Prf-(Aso%Associate_Prf)
        if(Ass%Assistant_Prf!=0):
            remain=remain+(Ass%Assistant_Prf)
            Assistant_Prf=Assistant_Prf-(Aso%Assistant_Prf)
        if(lect%Lecturer!=0):
            remain=remain+(lect%Lecturer)
            Lecturer=Lecturer-(lect%Lecturer)
        if(labeng%Lab_engineer!=0):
            remain=remain+(labeng%Lab_engineer)
            Lab_engineer=Lab_engineer-(labeng%Lab_engineer)
        for k in faculty:
            cal_dut=0
            if(faculty[k]=="Associate Proffesor"):
                cal_dut=int(Aso/Associate_Prf)
                faculty[k]=cal_dut
            elif(faculty[k]=="Assistant Proffesor"):
                cal_dut=int(Ass/Assistant_Prf)
                faculty[k]=cal_dut
            elif(faculty[k]=="Lecturer"):
                cal_dut=int(lect/Lecturer)
                faculty[k]=cal_dut
            elif(faculty[k]=="Lab Engineer"):
                cal_dut=int(labeng/Lab_engineer)
                faculty[k]=cal_dut
        print(faculty)
        rooms = pd.read_csv(fl1, usecols = ['Rooms'])
        room=[]
        room=rooms.values.flatten()
        name,duties=random.choice(list(faculty.items()))

        rows,cols=(room.size,len(dates))
        duty = [[0 for i in range(cols)] for j in range(rows)]
        rows,cols=(room.size,len(dates))
        duty1 = [[0 for i in range(cols)] for j in range(rows)]
        fac=""
        total=0
        no=0
        for shift in range(2):
            for dt in range(cols):
                for rm in range(rows):
                    no=0
                    while(True):
                        randomfac,dut=random.choice(list(faculty.items()))
                        duties=int(dut)
                        find=0
                        if duties>0:
                            for i in range(rows):
                                if shift==0:
                                    if randomfac ==duty[i][dt]:
                                        find=1
                                        break
                                else:
                                    if randomfac ==duty1[i][dt]:
                                        find=1
                                        break
                            if find==1:
                                continue
                            else:
                                if(shift==0):
                                    duty[rm][dt]=randomfac
                                else:
                                    duty1[rm][dt]=randomfac
                                faculty[randomfac]=duties-1
                                break
                        else:
                            continue
            print()
        disp1=pd.DataFrame(duty,columns=dates)
        disp1.index=room
        disp=pd.DataFrame(duty1,columns=dates)
        disp.index=room
        a=1
        if higlight!="":
            print("Shift 1: ")
            disp1=disp1[disp1.eq(higlight).any(1)]
            disp1=disp1.style.applymap(lambda x: "background-color: red;color: white" if x==higlight else "background-color: white")
            disp=disp[disp.eq(higlight).any(1)]
            disp=disp.style.applymap(lambda x: "background-color: red;color: white" if x==higlight else "background-color: white")
        html=disp1.to_html()
        html1=disp.to_html()
        tab=html
        tab1=html1
        messages.success(request, 'Roaster Generated Successfully')
    return render(request,'roster.html',{"table":tab,"table1":tab1})
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)
