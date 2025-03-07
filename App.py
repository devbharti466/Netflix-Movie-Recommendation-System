import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ✅ Load Merged Dataset
df = pd.read_csv("data\\flixpatrol.csv")

# Ensure Premiere is numeric
df["Premiere"] = pd.to_numeric(df["Premiere"], errors='coerce')

df["Watchtime in Million"] = df["Watchtime in Million"].str.replace("M", "").astype(float)  # Convert watchtime to numeric

st.title("Netflix Movie Recommendation System")

# User Inputs
movie_type = st.selectbox("Select Type:", ["Movie", "TV Show"])
genre = st.selectbox("Select Genre:", df["Genre"].unique())
year_range = st.slider("Select Year Range:", 2000, 2023, (2010, 2020))
view_option = st.radio("Select Viewing Preference:", ["Most Viewed", "Least Viewed"])
analysis_option = st.selectbox("Select Analysis Type:", [
    "Netflix Insights",
    "Movie Purchase Recommendation",
    "Customer Complaints & Suggestions"
])

# Filter dataset
filtered_data = df[(df["Type"] == movie_type) & (df["Genre"].str.contains(genre, na=False)) & (df["Premiere"].between(year_range[0], year_range[1], inclusive="both"))]

# Sort based on selected viewing preference
if view_option == "Most Viewed":
    filtered_data = filtered_data.sort_values(by="Watchtime in Million", ascending=False)
else:
    filtered_data = filtered_data.sort_values(by="Watchtime in Million", ascending=True)

# ✅ Display Filtered Data in Proper Order
st.subheader("Filtered Data Table (Sorted by Watchtime)")
st.write(filtered_data[["Title", "Genre", "Premiere", "Watchtime in Million"]].reset_index(drop=True).head(10))

# Perform Analysis Based on User Selection
if analysis_option == "Netflix Insights":
    st.subheader("Insights for Netflix")
    netflix_problems = [
        "Find the most popular genre in different regions.",
        "Analyze trends in movie watchtime over the years.",
        "Identify underperforming movies and genres.",
        "Recommend suitable movie categories for different seasons.",
        "Analyze audience preference for new vs. old movies."
    ]
    st.write("### 5 Key Insights Netflix Can Use:")
    st.write("\n".join([f"- {problem}" for problem in netflix_problems]))

elif analysis_option == "Movie Purchase Recommendation":
    st.subheader("Movie Purchase Recommendation for Netflix")
    if not filtered_data.empty:
        top_movie = filtered_data.iloc[0]
        st.write(f"**Recommendation:** Purchase movies similar to '{top_movie['Title']}' as it has high watchtime in its category.")
    else:
        st.write("No suitable recommendation found based on the current filters.")

elif analysis_option == "Customer Complaints & Suggestions":
    st.subheader("Customer Feedback Based on Data")
    cust_feedback = [
        "More diversity in content with different genres.",
        "Adding more classic movies based on audience interest.",
        "Increasing availability of highly watched but discontinued shows.",
        "Better regional content selection based on viewing trends.",
        "More frequent updates on trending movie lists."
    ]
    st.write("### Customer Complaints & Suggestions:")
    st.write("\n".join([f"- {feedback}" for feedback in cust_feedback]))
