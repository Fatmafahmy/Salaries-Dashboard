#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st

# page size
st.set_page_config(layout="wide")

# data load
df = pd.read_csv("ds_salaries.csv")

# clean
df.columns = df.columns.str.strip()

# title
st.title("Data Science Salaries Dashboard")

# sidebar filter
st.sidebar.header("Filters")


experience = st.sidebar.selectbox(
    "Select Experience Level",
    ["All"] + list(df['experience_level'].dropna().unique())
)

year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + list(df['work_year'].dropna().unique())
)


filtered = df.copy()

if experience != "All":
    filtered = filtered[filtered["experience_level"] == experience]

if year != "All":
    filtered = filtered[filtered["work_year"] == year]

# KPI
col1, col2, col3, col4 = st.columns(4)

col1.metric("Average Salary (USD)", f"{filtered['salary_in_usd'].mean():,.0f}")
col2.metric("Max Salary (USD)", f"{filtered['salary_in_usd'].max():,.0f}")
col3.metric("Min Salary (USD)", f"{filtered['salary_in_usd'].min():,.0f}")
col4.metric("Total Salary (USD)", f"{filtered['salary_in_usd'].sum():,.0f}")

# chart 1
fig1 = px.bar(
    filtered,
    x='job_title',
    y='salary_in_usd',
    title="Salary by Job Title"
)
st.plotly_chart(fig1)

st.divider()

colleft, colright = st.columns(2)

# chart 2
with colleft:
    st.subheader("Salary by Country")
    salary_country = (
        filtered.groupby('company_location')['salary_in_usd']
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )
    fig, ax = plt.subplots()
    salary_country.plot(kind='bar', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# chart 3
with colright:
    st.subheader("Salary Distribution")
    fig2, ax2 = plt.subplots()
    ax2.hist(filtered['salary_in_usd'], bins=30)
    st.pyplot(fig2)