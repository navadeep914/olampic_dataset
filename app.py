import streamlit as st
import pandas as pd

# Set the page title
st.set_page_config(page_title="Olympic Medal Improvement Analysis")

st.title("🏅 Olympic Medal Improvement Analysis")
st.write("Upload your Olympic data CSV to analyze which countries have shown the greatest improvement in medal counts.")

# Step 1: File Uploader
uploaded_file = st.file_uploader("Upload 'olympic_data.csv'", type=['csv', 'txt'])

if uploaded_file is not None:
    try:
        # Step 2: Read the data
        # Using sep='\t' because the data is tab-separated
        df = pd.read_csv(uploaded_file, sep='\t')
        
        # Display raw data preview
        with st.expander("View Raw Data"):
            st.dataframe(df.head())

        # Step 3: Data Preprocessing
        # Ensure column names match the notebook's logic (Standardizing headers)
        df.columns = df.columns.str.strip().str.title() 
        
        # Rename 'Athelete' to 'Athlete' if misspelled in source, and ensure 'Total' exists
        rename_map = {'Athelete': 'Athlete', 'Total': 'Total_Medals'}
        df = df.rename(columns=rename_map)
        
        # Verify required columns exist
        if 'Country' in df.columns and 'Year' in df.columns and 'Total_Medals' in df.columns:
            
            # --- NOTEBOOK LOGIC START ---
            
            # Group by Country and Year to get total medals per country per Olympics
            country_year = df.groupby(['Country', 'Year'], as_index=False)['Total_Medals'].sum()

            # Sort by Country and Year to ensure chronological order for diff()
            country_year = country_year.sort_values(['Country', 'Year'])

            # Find the change from the previous Olympics
            # We group by country again so the diff calculation doesn't spill over between different countries
            country_year['Delta'] = country_year.groupby('Country')['Total_Medals'].diff()

            # Find the year with the greatest improvement for each country
            # We look for the maximum 'Delta' value
            idx_improvement = country_year.groupby('Country')['Delta'].idxmax()
            
            # Filter out countries that might result in NaN (e.g., only participated once)
            idx_improvement = idx_improvement.dropna()
            
            # Select the rows corresponding to max improvement
            improvement = country_year.loc[idx_improvement]

            # Sort by improvement value (highest improvement first)
            improvement = improvement.sort_values('Delta', ascending=False)

            # --- NOTEBOOK LOGIC END ---

            # Step 4: Display Results
            st.subheader("🏆 Top 10 Countries with Greatest Improvement")
            st.write("This table shows the year a country achieved its highest increase in medals compared to its previous appearance.")
            
            # Formatting for cleaner display
            display_df = improvement.head(10).copy()
            display_df['Year'] = display_df['Year'].astype(str) # Remove commas from years
            display_df['Delta'] = display_df['Delta'].astype(int) # Remove decimals
            display_df['Total_Medals'] = display_df['Total_Medals'].astype(int)

            st.table(display_df[['Country', 'Year', 'Total_Medals', 'Delta']])
            
            # Optional: Bar Chart
            st.bar_chart(data=display_df.set_index('Country')['Delta'])

        else:
            st.error(f"The CSV file must contain columns: 'Country', 'Year', and 'Total' (or 'Total_Medals'). Found: {list(df.columns)}")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
