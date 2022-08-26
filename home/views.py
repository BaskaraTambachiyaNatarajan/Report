import json
from django.shortcuts import  render
from django.conf import settings
from django.core.files.storage import FileSystemStorage 
from django.http import HttpResponse
from django.contrib import messages
import pandas as pd
import numpy as np



# Create your views here.

def home(request):
    return render(request,'home.html')

def upload_file(request):
    if request.method=='POST':
        uploaded_file=request.FILES['doc']
        f=FileSystemStorage()
        name=f.save(uploaded_file.name,uploaded_file)
        url=settings.MEDIA_ROOT.replace("/","\\")
        #print(url+"\\"+name)
        p=url+"\\"+name
        if 'csv' in p:
            df=pd.read_csv(p)
        elif 'json' in p:
            df=pd.read_json(p)
        elif 'xlsx' in p:
            df=pd.read_excel(p)
        else:
            context={"msg":"not valid"}
            return render(request,'home.html',context)
        l=[]
        
        #print(df)
        for i in df.index:
            s=str(i+1)
            l.append(s)
        df.insert(loc=0, column='SNO', value=l)
        df['PortCode']=df['PortCode'].apply(portcodecheck,d=df)
        df.dropna(subset=['ID','Name','PortCode','UnctadPortCode','Country','Latitude','Longitude'],inplace=True)
        #print(df)
        name=df['Name'].to_list()
        PortCode=df['PortCode'].to_list()
        df['MainPortName']=df['MainPortCode'].apply(mainport,y=name,z=PortCode)
        df["Longitude"]=df["Longitude"].apply(rep)
        df["Latitude"]=df["Latitude"].apply(rep)
        df['ID']=df['ID'].apply(str)
        df['Map'] = df.apply(lambda row: "https://www.google.com/maps/search/?api=1&query="+row.Latitude+"%2C"+row.Longitude, axis = 1)
        df_copy=df.drop(['SNO'], axis=1)
        head=df_copy.columns
        df_copy=df_copy.to_json(orient="index")
        json_df_copy=json.loads(df_copy)
        #columns=json_df['columns']
        #indexes=json_df['index']
        #data=json_df['data']
        context={"all":json_df_copy,"head":head}
        df.to_json('E:\\Private\\New folder\\port.json', orient='index')
        return render(request,'file.html',context)
    elif request.method == 'GET':
        return HttpResponse("Success!")

def portcodecheck(x,d):
    temp = d['PortCode'].str.contains(x, case=False)
    df=d[temp]
    w=df['UnctadPortCode'].loc[df.index[0]]
    if len(x)==5:
        if x[2:]==w:
            return x
    else:
        return np.nan

def mainport(x,y,z):
    if x in z:
        p=z.index(x)
        x=y[p]
    return x

def rep(x):
    return str(x).replace(',','.')
    
def search(request):
    word=request.POST.get('keyword')
    d=pd.read_json('E:\\Private\\New folder\\port.json', orient='index')
    #print(d)
    d['ID']=d['ID'].apply(str)
    mask1 = d['PortCode'].str.contains(word, case=False)
    mask2 = d['Name'].str.contains(word, case=False)
    mask3 = d['ID'].str.contains(word, case=False)
    df=d[mask1 | mask2 | mask3]
    df_copy=df.drop(['SNO'], axis=1)
    head=df_copy.columns
    df_copy=df_copy.to_json(orient="index")
    json_df=json.loads(df_copy)
    if len(json_df)>0:
        context={"all":json_df,"head":head}
    else:
        context={"nodata":"No data available"}
    return render(request,'file.html',context)


def to_edit(request):
    portcode=request.POST.get('portcode')
    d=pd.read_json('E:\\Private\\New folder\\port.json', orient='index')
    mask3 = d['PortCode'].str.contains(portcode, case=False)
    df=d[mask3].drop(['Map','MainPortName'], axis=1)
    head=df.columns
    df_copy=df.to_json(orient="index")
    json_df=json.loads(df_copy)
    context={"all":json_df,"head":head}
    return render(request,'edit.html',context)

def edit(request):
    if request.method=='POST':
        sno=str(request.POST.get('SNO'))
        id=request.POST.get('ID')
        Name=request.POST.get('Name')
        PortCode=request.POST.get('PortCode')
        UnctadPortCode=request.POST.get('UnctadPortCode')
        Country=request.POST.get('Country')
        Latitude=request.POST.get('Latitude')
        Longitude=request.POST.get('Longitude')
        Url=request.POST.get('Url')
        MainPortCode=request.POST.get('MainPortCode')
        df=pd.read_json('E:\\Private\\New folder\\port.json', orient='index')
        df['SNO']=df['SNO'].apply(str)
        mask3 = df['SNO'].str.contains(sno, case=False)
        d=df[mask3]
        if id=='' or Name=='' or PortCode=='' or UnctadPortCode=='' or Country=='' or Latitude=='' or Longitude=='' or MainPortCode=='':
            if PortCode[2:]==UnctadPortCode and len(PortCode)==5:
                df=d[mask3].drop(['Map','MainPortName'], axis=1)
                print(df)
                head=df.columns
                df_copy=df.to_json(orient="index")
                json_df=json.loads(df_copy)
                messages.error(request,"Hi buddy")
                context={"all":json_df,"head":head}
                return render(request,'edit.html',context)
        w=d.index[0]
        df.at[w,'ID']=id
        df.at[w,'Name']=Name
        df.at[w,'PortCode']=PortCode
        df.at[w,'UnctadPortCode']=UnctadPortCode
        df.at[w,'Country']=Country
        df.at[w,'Latitude']=Latitude
        df.at[w,'Longitude']=Longitude
        df.at[w,'Url']=Url
        df.at[w,'MainPortCode']=MainPortCode
        df.at[w,'Map']="https://www.google.com/maps/search/?api=1&query="+Latitude+"%2C"+Longitude
        df_copy=df.drop(['SNO'], axis=1)
        head=df_copy.columns
        df_copy=df_copy.to_json(orient="index")
        json_df_copy=json.loads(df_copy)
        #columns=json_df['columns']
        #indexes=json_df['index']
        #data=json_df['data']
        context={"all":json_df_copy,"head":head}
        df.to_json('E:\\Private\\New folder\\port.json', orient='index')
        return render(request,'file.html',context)
    elif request.method == 'GET':
        return HttpResponse("Success!")

def delete(request):
    portcode=request.POST.get('portcode')
    d=pd.read_json('E:\\Private\\New folder\\port.json', orient='index')
    mask3 = d['PortCode'].str.contains(portcode, case=False)
    df=d[mask3]
    w=df.index[0]
    d=d.drop(w)
    d=d.drop(['SNO'],axis=1)
    l=[]
    for i in d.index:
        s=str(i)
        l.append(s)
    d.insert(loc=0, column='SNO', value=l)
    df_copy=d.drop(['SNO'], axis=1)
    head=df_copy.columns
    df_copy=df_copy.to_json(orient="index")
    json_df_copy=json.loads(df_copy)
    context={"all":json_df_copy,"head":head}
    d.to_json('E:\\Private\\New folder\\port.json', orient='index')
    return render(request,'file.html',context)