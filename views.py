from flask import flash, redirect, render_template, url_for,request,send_file,jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc
from werkzeug.utils import secure_filename
import os
from datetime import datetime

from . import sales

import pandas as pd

def getdata(by):
    fl='d:/글로벌/실적분석/곰스_2002.xlsx'
    df= pd.read_excel(fl,header=0)
    df['계약일자']=pd.to_datetime(df.계약일자,format='%Y-%m-%d')
   
    
    import datetime
    fr=pd.to_datetime('2020-02-01',format='%Y-%m-%d')
    to=pd.to_datetime('2020-02-29',format='%Y-%m-%d')
    cond2= (df.계약일자 >= fr) & (df.계약일자 <= to)
    if by=='brh':
        df2=pd.DataFrame(df[cond2].groupby(['지점'])['초회보험료'].agg('sum'))
    elif by=='day':
        df['계약일자']=df.계약일자.dt.strftime('%m-%d')
        df2=pd.DataFrame(df[cond2].groupby(['계약일자'])['초회보험료'].agg('sum'))
   
    else: return 'err'

    df2=df2.reset_index()
    return df2

labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

@sales.route("/line_chart")
@login_required
def line_chart():
    title="지점별실적"
    legend = 'sales'
    df=getdata('day')
    values=df.초회보험료
    labels=df.계약일자
    
    return render_template('sales/line_chart.html', values=values, labels=labels, legend=legend,title=title)


@sales.route('/bar_chart')
@login_required
def bar_chart():
    df=getdata('brh')
    legend = 'sales'
    bar_labels=df.지점
    bar_values=df.초회보험료
    print("len=",len(bar_values))
    return render_template('sales/bar_chart.html', title='sales by branch',max=17000,labels=bar_labels, values=bar_values,legend=legend)


@sales.route('/pie_chart')
@login_required
def pie_chart():
    pie_labels = labels
    pie_values = values
    return render_template('sales/pie_chart.html', title='sales per branch',max=17000, values=pie_values, labels=pie_labels, colors=colors)