import streamlit as st
import gspread as gs
import pandas as pd
import base64
import altair as alt
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")

gc = gs.service_account(filename='service_account.json')

sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/13d66R8p25S3wvjaSkivAIplxGmEc7KE4BXilvbYh6WI/edit')

 
ind = sh.worksheet('Index').get_all_values()
q = []
 
for i in range(len(ind)):
    q.append(ind[i][0])

qs = st.selectbox( "Select the Question",  q , index=0)

ws = sh.worksheet(qs)

new_data = {}
data = ws.get_all_values()

del data[0]
for i in range(len(data)):
    new_data[data[i][0]] = []
    for j in range(1,len(data[i]),1):
        data[i][j] = data[i][j].replace('%','')
        if data[i][j] == '':
            data[i][j] = 0
        else:
            data[i][j] = float(data[i][j])
        
        new_data[data[i][0]].append(data[i][j] )


data_header = { "Generation":["Total", "Gen Z", "Younger Millennial", "Older Millennial", "Gen X", "Boomer",]  , "Gender":["Male", "Female"] , "Employment Status":["Full Time", "Part Time", "Self-Employed", "Looking"]   
               ,"Job Title":["C Level","VP", "Director", "Manager", "Employee"]  ,"Role":["Management", "Employee"] ,"Company Size": ["1-49",  "50-99", "100-499", "500-999", "1000-4999", "5000-9999", "10000+"] ,
                "HHI": ["<$20K", "$20K-$34k", "$35K-$49K", "$50K-$74K", "$75K-$99K", "100K-$149K", "150K-$199K", "$200K+" ] ,
                "Education":["Some High School or <", "High School Graduated", "Some College", "Professional School Graduated", "Assoc. Degree", "Bachelor Degree", "Grand Degree"] 
                 ,"Region":["Urban", "Sub-Urban", "Rural"] }


def get_all_columns_title(data_header):
    ret = []
    for k, v in data_header.items():
        for i in range(len(v)):
            ret.append(k+': '+v[i]) 
    return ret


df = pd.DataFrame( new_data ).T 
df.columns = get_all_columns_title(data_header)
 

def get_x_axis(k): 
    for r, v in data_header.items():
        if r in st.session_state:
            if r==k:
                selected_value = st.session_state[k]         
                draw_chart(k+": "+selected_value)
            else:     
                st.session_state[r] = "Select "+r
             

layout_col = st.columns(len(data_header))
i=0
for k, v in data_header.items():
    v.insert(0, "Select "+k)
    with layout_col[i]:
        st.selectbox(k, v ,key =k, index=0, on_change=get_x_axis,args=(k,)) 
    i = i +1

def draw_chart(x_axis):
    if x_axis != '':
        c = alt.Chart(df.reset_index()).mark_bar().encode(
            x=alt.X(  x_axis + ':Q',scale=alt.Scale(domain=[0, 100]) ),
            y=alt.Y('index:N', title="Answer" ),
            color=alt.Color('index:N',title="Answer")
        )
        st.altair_chart(c,theme=None, use_container_width=True)
    else:
        st.write("Please select a column to draw chart")
        
        
          
