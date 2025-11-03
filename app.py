import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

#  Streamlit Page Config 
st.set_page_config(page_title="SATYA CSV-V", layout="wide")
st.title(" CSV Data Visualizer")
st.markdown("Upload a CSV file to explore and visualize your dataset with clear, responsive charts. Supports both numerical and categorical data.")

#  Upload CSV 
uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

# Create folder for plots
os.makedirs("plots", exist_ok=True)
plot_counter = 1  # For saving plots sequentially

#  When CSV is Uploaded 
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 🔹 Show full dataset
    st.subheader(" Full Dataset")
    st.dataframe(df)  # Scrollable full data table

    # Dataset info
    st.markdown("###  Dataset Info")
    st.write(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")
    st.write("**Columns:**", ", ".join(df.columns))

    # Handle missing values
    df = df.fillna(df.mean(numeric_only=True))

    # Identify column types
    num_cols = df.select_dtypes(include=np.number).columns
    cat_cols = df.select_dtypes(include=['object']).columns

    #  NUMERICAL VISUALIZATIONS 
    if len(num_cols) > 0:
        st.header(" Numerical Data Visualizations (All Data)")

        # Histogram
        for col in num_cols:
            st.subheader(f"Histogram - {col}")
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.histplot(df[col], kde=True, color="royalblue", ax=ax)
            ax.set_title(f"Distribution of {col}")
            ax.set_xlabel(col)
            ax.set_ylabel("Frequency")
            plt.tight_layout()
            st.pyplot(fig)
            fig.savefig(f"plots/plot{plot_counter}.png", dpi=120, bbox_inches="tight")
            plot_counter += 1
            plt.close(fig)

        # Box Plot
        st.subheader(" Box Plot - Numeric Columns")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.boxplot(data=df[num_cols], ax=ax) 
        ax.set_title("Box Plot of Numeric Columns")
        plt.tight_layout()
        st.pyplot(fig)
        fig.savefig(f"plots/plot{plot_counter}.png", dpi=120, bbox_inches="tight")
        plot_counter += 1
        plt.close(fig)

        # Correlation Heatmap
        if len(num_cols) > 1:
            st.subheader(" Correlation Heatmap")
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(df[num_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
            ax.set_title("Correlation Heatmap")
            plt.tight_layout()
            st.pyplot(fig)
            fig.savefig(f"plots/plot{plot_counter}.png", dpi=120, bbox_inches="tight")
            plot_counter += 1
            plt.close(fig)

        # Scatter Plot (first two numeric columns)
        if len(num_cols) >= 2:
            st.subheader(" Scatter Plot - First Two Numeric Columns")
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.scatterplot(x=df[num_cols[0]], y=df[num_cols[1]], color="orange", ax=ax)
            ax.set_title(f"{num_cols[0]} vs {num_cols[1]}")
            plt.tight_layout()
            st.pyplot(fig)
            fig.savefig(f"plots/plot{plot_counter}.png", dpi=120, bbox_inches="tight")
            plot_counter += 1
            plt.close(fig)

        # Area Chart
        st.subheader(" Area Chart - Numeric Columns")
        st.area_chart(df[num_cols])  # Streamlit’s built-in chart (not saved)

    #  CATEGORICAL VISUALIZATIONS 
    if len(cat_cols) > 0:
        st.header(" Categorical Data Visualizations (All Data)")

        for col in cat_cols:
            st.subheader(f"Bar Chart - {col}")
            top_values = df[col].value_counts().nlargest(10)
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(x=top_values.values, y=top_values.index, color='seagreen', ax=ax)
            ax.set_title(f"Top 10 Categories in {col}")
            ax.set_xlabel("Count")
            ax.set_ylabel(col)
            plt.tight_layout()
            st.pyplot(fig)
            fig.savefig(f"plots/plot{plot_counter}.png", dpi=120, bbox_inches="tight")
            plot_counter += 1
            plt.close(fig)

            # Pie Chart
            if len(top_values) <= 10:
                st.subheader(f" Pie Chart - {col}")
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.pie(top_values.values, labels=top_values.index, autopct="%1.1f%%", startangle=90)
                ax.set_title(f"Category Proportions - {col}")
                plt.tight_layout()
                st.pyplot(fig)
                fig.savefig(f"plots/plot{plot_counter}.png", dpi=120, bbox_inches="tight")
                plot_counter += 1
                plt.close(fig)

    #  TIME-SERIES VISUALIZATION 
    st.header("⏳ Time-Series Visualization")
    date_cols = df.select_dtypes(include=["datetime64"]).columns

    # Auto-detect datetime columns
    if len(date_cols) == 0:
        for col in df.columns:
            try:
                df[col] = pd.to_datetime(df[col])
                date_cols = date_cols.append(pd.Index([col]))
            except:
                pass

    if len(date_cols) > 0 and len(num_cols) > 0:
        time_col = date_cols[0]
        st.subheader(f" Line Chart over Time - {time_col}")
        df_sorted = df.sort_values(by=time_col)
        fig, ax = plt.subplots(figsize=(10, 4))
        for ncol in num_cols[:3]:
            ax.plot(df_sorted[time_col], df_sorted[ncol], label=ncol)
        ax.legend()
        ax.set_title(f"Trends Over Time - {time_col}")
        plt.tight_layout()
        st.pyplot(fig)
        fig.savefig(f"plots/plot{plot_counter}.png", dpi=120, bbox_inches="tight")
        plot_counter += 1
        plt.close(fig)

    #  Final Message 
    st.success(f" All plots generated and saved successfully in the 'plots' folder ({plot_counter - 1} images).")

else:
    st.info(" Please upload a CSV file to begin visualization.")
