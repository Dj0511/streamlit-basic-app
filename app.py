import streamlit as st
import pandas as pd
import numpy as np


@st.cache_data
def read_csv(file):
    df = pd.read_csv(file)
    return df

def calculate_avg(row):
    return row[['Science', 'English', 'History', 'Maths']].mean()

def get_grade(avg):
    if avg >= 90:
        return 'A+'
    elif avg >= 75:
        return 'A'
    elif avg >= 60:
        return 'B'
    elif avg >= 40:
        return 'C'
    else:
        return 'F'

# For Icons and Emojis prefer this github repo : https://github.com/ikatyang/emoji-cheat-sheet?tab=readme-ov-file#table-of-contents 

st.title("📊 Student Score Analyzer App")

# File uploader with Dynamic Nature to upload same feature file
uploaded_file = st.file_uploader("Upload Student Marksheet CSV", type=["csv"])
if uploaded_file:
    df = read_csv(uploaded_file)
    # Show raw data
    st.subheader("📄 Raw Data Preview")
    st.dataframe(df.head())

    # Clean missing values
    df.fillna(df.mean(numeric_only=True), inplace=True)

    # Calculate total, average and grade
    df["Total Score"] = df[['Science', 'English', 'History', 'Maths']].sum(axis=1)
    df["Average"] = df.apply(calculate_avg, axis=1)
    df["Grade"] = df["Average"].apply(get_grade)

        
    st.sidebar.title("🎛️ Filters")

    # Streamlit Feature for Filter Dataframe made by various Selections : https://discuss.streamlit.io/t/filter-dataframe-by-selections-made-in-select-box/6627

    filter_type = st.sidebar.selectbox("Filter by", ["None", "Gender", "Section"])
    if filter_type == "Gender":
        selected_gender = st.sidebar.selectbox("Select Gender", df["Gender"].unique())
        df = df[df["Gender"] == selected_gender]
    elif filter_type == "Section":
        selected_section = st.sidebar.selectbox("Select Section", df["Section"].unique())
        df = df[df["Section"] == selected_section]

    # Show only top scorers
    if st.sidebar.checkbox("Show only top scorers (Avg > 80 in all subjects)"):
        df = df[(df["Science"] > 80) & 
                (df["English"] > 80) & 
                (df["History"] > 80) & 
                (df["Maths"] > 80)]

  
    st.subheader("🧾 Student Scores")
    st.dataframe(df[["Name", "Gender", "Section", "Science", "English", "History", "Maths", "Total Score", "Average", "Grade"]])


    st.subheader("📈 Analysis")

    # Class-wise averages
    class_avg = df.groupby("Section")[["Science", "English", "History", "Maths"]].mean()
    st.write("📊 Class-wise Subject Averages")
    st.dataframe(class_avg)

    # Top scorer(s)
    top_scorer = df[df["Total Score"] == df["Total Score"].max()]
    st.write("🏆 Top Scorer(s)")
    st.dataframe(top_scorer[["Name", "Total Score", "Average", "Grade"]])

    # Subject with highest average
    subject_means = df[["Science", "English", "History", "Maths"]].mean()
    st.write(f"📚 Subject with Highest Average: **{subject_means.idxmax()} ({subject_means.max()})**")

    # Students scoring >80 in all subjects
    st.subheader("🎯 Students Scoring >80 in All Subjects")
    top_all_subjects = df[(df["Science"] > 80) & (df["English"] > 80) & (df["History"] > 80) & (df["Maths"] > 80)]

    if not top_all_subjects.empty:
        for _, row in top_all_subjects.iterrows():
            st.write(f"✅ {row['Name']} scored >80 in all subjects.")
    else:
        st.write("❌ No student scored >80 in all subjects.")

    # Group-wise averages
    st.subheader("👥 Group-wise Averages")
    group_by = st.radio("Group by", ["Gender", "Section"])
    group_avg = df.groupby(group_by)[["Science", "English", "History", "Maths", "Total Score"]].mean()
    st.dataframe(group_avg)

    # Sort by total score
    st.subheader("📋 Sorted by Total Score")
    sorted_df = df.sort_values(by="Total Score", ascending=False)
    st.dataframe(sorted_df[["Name", "Total Score", "Average", "Grade"]])