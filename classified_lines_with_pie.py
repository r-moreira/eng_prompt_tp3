import streamlit as st
import pandas as pd
import plotly.express as px

# Title of the app
st.title("Classified Lines Viewer with Pie Chart")

# Filepath
file_path = "data/classified_lines.csv"

# Read the CSV file
try:
    df = pd.read_csv(file_path, sep="|")

    # Display the dataframe
    st.subheader("CSV File Contents:")
    st.dataframe(df)

    # Summary of classifications
    st.subheader("Classification Summary:")
    classification_counts = df["Classification"].value_counts()

    # Pie chart of classifications
    st.subheader("Pie Chart of Classification Proportions:")
    pie_fig = px.pie(
        classification_counts,
        values=classification_counts.values,
        names=classification_counts.index,
        title="Proportion of Each Classification",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(pie_fig)

    # Filter lines by classification
    st.subheader("Filter by Classification:")
    classification_filter = st.selectbox(
        "Select Classification", ["All"] + df["Classification"].unique().tolist()
    )

    if classification_filter != "All":
        filtered_df = df[df["Classification"] == classification_filter]
        st.write(f"Lines with {classification_filter} classification:")
        st.dataframe(filtered_df)
    else:
        st.write("Showing all lines:")
        st.dataframe(df)
except FileNotFoundError:
    st.error(f"File not found: {file_path}. Please ensure the file exists.")
except Exception as e:
    st.error(f"An error occurred: {e}")
