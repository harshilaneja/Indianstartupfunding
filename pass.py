import pandas as pd
import streamlit as st

email=st.text_input('email')
password=st.text_input('pass')
gender=st.selectbox('select gender',['male','female','others'])

btn=st.button('login kr')

if btn:
    if email=='harshil@gmail.com' and password=='1234':
        st.balloons()
        st.write(gender)

    else:
        st.error('failed')

file=st.file_uploader('upload')

if file is not None:
    df=pd.read_csv(file)
    st.dataframe(df.describe())

import pandas as pd
import streamlit as st
import time
st.title('Stratup Dasboard')
st.header('I am learning Streamlit')
st.subheader('And i am loving that')

st.write('This is a normal text')

st.markdown(""""
### My favorite movies
- race
- housefull
- krish
""")

st.code("""
def foo(input):
    return foo**2
x=foo(2)
""")

st.latex('x^2+y^2+2=0')

df=pd.DataFrame({
    'name':['Nitish','Ankit','Anupam'],
    'marks':[50,60,70],
    'package':[10,20,12]
})
st.dataframe(df)

st.metric('Revenue','Rs  3L','3%' )

st.json({
    'name':['Nitish','Ankit','Anupam'],
    'marks':[50,60,70],
    'package':[10,20,12]
})

st.sidebar.title('side  title')

col1,col2=st.columns(2)

with col1:
    st.write('pro')

with col2:
    st.write('oo')

st.error('failed')

st.success('sucessfull')

st.info('info')

st.warning('warning')

bar=st.progress(0)
for i in range(1,101):
    time.sleep(0.1)
    bar.progress(i)

email=st.text_input('Enter email')
number=st.number_input('Enter age')
date=st.date_input('enter date')
