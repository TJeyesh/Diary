import streamlit as st
from datetime import datetime,time
import sqlite3
st.set_page_config(layout="wide")
conn= sqlite3.connect('database.db')
c=conn.cursor()

def ADD():
    date = st.date_input("Enter the date", value=datetime.today())
    start_time = st.time_input("Enter the Start time")
    end_time = st.time_input("Enter the End time")
    notes=st.text_input('Enter Notes')
    if st.button("Save"):
        c.execute(f"insert into diary values ('{date}','{start_time}','{end_time}','{notes}')")
        conn.commit()

def History():
    def func(li: list):
        li_=['']
        for i in li:
            li_.append(i[0])
        return li_
    def sql(o1,o2,o3):
        sql = ''
        if o1!='':
            if o2!='':
                sql=f" date = '{o1}' and start_time='{o2}'"
            else:
                sql=f" date = '{o1}' "
            if o3!='':
                return sql+f" and end_time='{o3}'"
            else:
                return sql
        elif o2!='':
            if o1!='':
                sql=f" date ='{o1}' and start_time ='{o2}'"
            else:
                sql=f"start_time ='{o2}'diary"
            if o3!='':
                return sql+f" and end_time ='{o3}'"
            else:
                return sql

        else :
            if o1!='':
                sql=f" date = '{o1}' and end_time ='{o3}'"
            else:
                sql=f"end_time ='{o3}'"
            if o2!='':
                return sql+f" and start_time ='{o2}'"
            else:
                return sql
    
    st.text('Filter by')
    col1, col2, col3, col4 = st.columns(4)
# Place selectboxes in each column
    with col1:
        c.execute("select date from diary")
        option1 = st.selectbox("Date", func(c.fetchall()))

    with col2:
        c.execute("select start_time from diary")
        option2 = st.selectbox("Start time", func(c.fetchall()))

    with col3:
        c.execute("select end_time from diary")
        option3 = st.selectbox("End time", func(c.fetchall()))
    with col4:
        option4 = st.selectbox("End time",'')
    if st.button('Filter'):
        if [option1,option2,option3]!=['','','']:
            # st.write(sql(option1,option2,option3))
            c.execute("select * from diary where"+sql(option1,option2,option3)+" order by date,start_time")
            for i in c.fetchall():
                st.text(f"{i[0]}")
                st.text(f"From {i[1]} to {i[2]}")
                st.text(i[3])
        else:
            c.execute("select * from diary order by date,start_time")
            for i in c.fetchall():

                st.markdown(f"## {i[0]}")
                st.markdown(f"* From {i[1]} to {i[2]}")
                st.markdown(i[3])


def home():
    option = st.sidebar.selectbox('Select mode', ['', 'ADD', 'Debit', 'History'],placeholder='Choose an Option')
    if option == 'ADD':
        ADD()
    elif option == 'Debit':
        # Debit()
        pass
    elif option == 'History':
        History()

st.title('Personal Online Diary')

home()

