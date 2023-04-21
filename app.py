import streamlit as st
import gspread as gs
import pandas as pd 
import altair as alt 

 

def get_all_columns_title(data):
    ret = []
    for k, v in data.items():
        for i in range(len(v)):
            ret.append(k+': '+v[i]) 
    return ret 

def get_x_axis(k,data_header,df): 
    
    for r, v in data_header.items():
        if r in st.session_state:
            if r==k:
                selected_value = st.session_state[k]         
                draw_chart(k+": "+selected_value,df)
            else:     
                st.session_state[r] = "Select "+r
             
def filter_show_select_option():
    if "filter_select_option" in st.session_state: 
        selected_value = st.session_state["filter_select_option"]

def draw_chart(x_axis,df):
    if x_axis != '':
        c = alt.Chart(df.reset_index()).mark_bar().encode(
            x=alt.X(  x_axis + ':Q',scale=alt.Scale(domain=[0, 100]) ),
            y=alt.Y('index:N', title="Answer" ),
            color=alt.Color('index:N',title="Answer")
        )
        st.altair_chart(c,theme=None, use_container_width=True)
    else:
        st.write("Please select a column to draw chart")
        
        
          
def main():
    st.set_page_config(layout="wide")
    
    
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;display:none!important;}
                footer {visibility: hidden;display:none!important;}
                header {visibility: hidden;display:none!important;}
                .viewerBadge_container__1QSob,a[rel="noopener noreferrer"]{visibility: hidden;display:none!important;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)
      
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

    df = pd.DataFrame( new_data ).T 
    df.columns = get_all_columns_title(data_header)
    layout_col = st.columns(2)
    
    with layout_col[0]:
        filter = st.selectbox("Select a Filter", data_header.keys() ,key = "filter_select_option", index=0,  on_change=filter_show_select_option)
    
    with layout_col[1]:
        if filter in data_header:
            v = data_header[filter];
            v.insert(0, "Select "+filter)
            st.selectbox(filter, v ,key =filter, index=0,  on_change=get_x_axis,args=(filter,data_header,df))     
   
    
if __name__ == '__main__':
    main()
