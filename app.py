import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Olympic Medal Analysis Dashboard",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 10px;
    }
    h2 {
        color: #2c3e50;
        padding-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data():
    """Load the Olympic dataset"""
    # You'll need to provide the path to your CSV file
    # For now, creating a sample data structure
    # Replace this with: df = pd.read_csv('your_olympic_data.csv')
    
    # Sample data structure (replace with actual file loading)
    st.warning("⚠️ Please upload your Olympic dataset CSV file or update the file path in the code.")
    return None

# Data processing functions
def prepare_data(df):
    """Prepare and clean the data"""
    if df is None:
        return None
    
    # Rename Total to Total_Medals if needed
    if 'Total' in df.columns and 'Total_Medals' not in df.columns:
        df = df.rename(columns={'Total': 'Total_Medals'})
    
    return df

def get_medal_summary(df):
    """Get overall medal summary statistics"""
    total_medals = df['Total_Medals'].sum()
    total_gold = df['Gold'].sum()
    total_silver = df['Silver'].sum()
    total_bronze = df['Bronze'].sum()
    total_athletes = df['Athlete'].nunique()
    total_countries = df['Country'].nunique()
    
    return {
        'total_medals': total_medals,
        'total_gold': total_gold,
        'total_silver': total_silver,
        'total_bronze': total_bronze,
        'total_athletes': total_athletes,
        'total_countries': total_countries
    }

def get_top_countries(df, n=10):
    """Get top countries by total medals"""
    return df.groupby('Country')['Total_Medals'].sum().sort_values(ascending=False).head(n)

def get_top_athletes(df, n=10):
    """Get top athletes by total medals"""
    return df.groupby('Athlete').agg({
        'Total_Medals': 'sum',
        'Gold': 'sum',
        'Silver': 'sum',
        'Bronze': 'sum',
        'Country': 'first',
        'Sport': 'first'
    }).sort_values('Total_Medals', ascending=False).head(n)

def get_medals_by_sport(df):
    """Get medal distribution by sport"""
    return df.groupby('Sport')['Total_Medals'].sum().sort_values(ascending=False)

def get_gold_proportion(df):
    """Calculate proportion of gold medals per country"""
    gold_total = df.groupby('Country')['Gold'].sum()
    total_medals = df.groupby('Country')['Total_Medals'].sum()
    return (gold_total / total_medals).sort_values(ascending=False)

def get_athletes_per_country(df):
    """Get number of unique athletes per country"""
    return df.groupby('Country')['Athlete'].nunique().sort_values(ascending=False)

def get_year_medals(df, year):
    """Get medals by country for a specific year"""
    return df[df['Year'] == year].groupby('Country')['Total_Medals'].sum().sort_values(ascending=False)

def calculate_improvement(df):
    """Calculate countries with greatest improvement"""
    country_year = df.groupby(['Country', 'Year'], as_index=False)['Total_Medals'].sum()
    country_year = country_year.sort_values(['Country', 'Year'])
    country_year['Delta'] = country_year.groupby('Country')['Total_Medals'].diff()
    improvement = country_year.loc[country_year.groupby('Country')['Delta'].idxmax()]
    return improvement.sort_values('Delta', ascending=False)

# Main app
def main():
    # Title and description
    st.title("🏅 Olympic Medal Analysis Dashboard")
    st.markdown("### Comprehensive analysis of Olympic medal winners and performance statistics")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your Olympic dataset (CSV)", type=['csv'])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df = prepare_data(df)
        
        # Sidebar filters
        st.sidebar.header("🔍 Filters")
        
        # Year filter
        years = sorted(df['Year'].unique())
        selected_years = st.sidebar.multiselect(
            "Select Years",
            options=years,
            default=years
        )
        
        # Country filter
        countries = sorted(df['Country'].unique())
        selected_countries = st.sidebar.multiselect(
            "Select Countries",
            options=countries,
            default=[]
        )
        
        # Sport filter
        sports = sorted(df['Sport'].unique())
        selected_sports = st.sidebar.multiselect(
            "Select Sports",
            options=sports,
            default=[]
        )
        
        # Apply filters
        filtered_df = df[df['Year'].isin(selected_years)]
        if selected_countries:
            filtered_df = filtered_df[filtered_df['Country'].isin(selected_countries)]
        if selected_sports:
            filtered_df = filtered_df[filtered_df['Sport'].isin(selected_sports)]
        
        # Display metrics
        st.markdown("---")
        summary = get_medal_summary(filtered_df)
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.metric("Total Medals", f"{summary['total_medals']:,}")
        with col2:
            st.metric("🥇 Gold", f"{summary['total_gold']:,}")
        with col3:
            st.metric("🥈 Silver", f"{summary['total_silver']:,}")
        with col4:
            st.metric("🥉 Bronze", f"{summary['total_bronze']:,}")
        with col5:
            st.metric("Athletes", f"{summary['total_athletes']:,}")
        with col6:
            st.metric("Countries", f"{summary['total_countries']:,}")
        
        st.markdown("---")
        
        # Create tabs for different analyses
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🌍 Countries", 
            "🏃 Athletes", 
            "⚽ Sports", 
            "📊 Year Analysis",
            "📈 Trends"
        ])
        
        with tab1:
            st.header("Country Medal Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Top Countries by Total Medals")
                top_countries = get_top_countries(filtered_df, 15)
                
                fig = px.bar(
                    x=top_countries.values,
                    y=top_countries.index,
                    orientation='h',
                    labels={'x': 'Total Medals', 'y': 'Country'},
                    color=top_countries.values,
                    color_continuous_scale='Blues'
                )
                fig.update_layout(showlegend=False, height=500)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Medal Distribution by Type")
                medal_dist = filtered_df.groupby('Country')[['Gold', 'Silver', 'Bronze']].sum()
                top_10_countries = get_top_countries(filtered_df, 10).index
                medal_dist = medal_dist.loc[top_10_countries]
                
                fig = go.Figure()
                fig.add_trace(go.Bar(name='Gold', x=medal_dist.index, y=medal_dist['Gold'], marker_color='gold'))
                fig.add_trace(go.Bar(name='Silver', x=medal_dist.index, y=medal_dist['Silver'], marker_color='silver'))
                fig.add_trace(go.Bar(name='Bronze', x=medal_dist.index, y=medal_dist['Bronze'], marker_color='#CD7F32'))
                
                fig.update_layout(
                    barmode='stack',
                    xaxis_title="Country",
                    yaxis_title="Number of Medals",
                    height=500,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Gold Medal Proportion by Country")
            gold_prop = get_gold_proportion(filtered_df).head(20)
            
            fig = px.bar(
                x=gold_prop.index,
                y=gold_prop.values,
                labels={'x': 'Country', 'y': 'Proportion of Gold Medals'},
                color=gold_prop.values,
                color_continuous_scale='YlOrRd'
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Number of Athletes per Country")
            athletes_country = get_athletes_per_country(filtered_df).head(20)
            
            fig = px.treemap(
                names=athletes_country.index,
                parents=[""] * len(athletes_country),
                values=athletes_country.values,
                color=athletes_country.values,
                color_continuous_scale='Greens'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.header("Top Athletes Analysis")
            
            top_athletes = get_top_athletes(filtered_df, 20)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("Top 20 Athletes by Total Medals")
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    name='Gold',
                    y=top_athletes.index,
                    x=top_athletes['Gold'],
                    orientation='h',
                    marker_color='gold'
                ))
                fig.add_trace(go.Bar(
                    name='Silver',
                    y=top_athletes.index,
                    x=top_athletes['Silver'],
                    orientation='h',
                    marker_color='silver'
                ))
                fig.add_trace(go.Bar(
                    name='Bronze',
                    y=top_athletes.index,
                    x=top_athletes['Bronze'],
                    orientation='h',
                    marker_color='#CD7F32'
                ))
                
                fig.update_layout(
                    barmode='stack',
                    xaxis_title="Number of Medals",
                    yaxis_title="Athlete",
                    height=600,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Top Athletes Details")
                display_athletes = top_athletes.reset_index()[['Athlete', 'Country', 'Sport', 'Total_Medals', 'Gold', 'Silver', 'Bronze']]
                st.dataframe(display_athletes, height=600, use_container_width=True)
        
        with tab3:
            st.header("Sports Analysis")
            
            medals_by_sport = get_medals_by_sport(filtered_df)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Total Medals by Sport")
                
                fig = px.pie(
                    values=medals_by_sport.values[:10],
                    names=medals_by_sport.index[:10],
                    hole=0.4
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Medal Distribution by Sport (Top 15)")
                
                sport_medal_dist = filtered_df.groupby('Sport')[['Gold', 'Silver', 'Bronze']].sum()
                top_sports = medals_by_sport.head(15).index
                sport_medal_dist = sport_medal_dist.loc[top_sports]
                
                fig = go.Figure()
                fig.add_trace(go.Bar(name='Gold', x=sport_medal_dist.index, y=sport_medal_dist['Gold'], marker_color='gold'))
                fig.add_trace(go.Bar(name='Silver', x=sport_medal_dist.index, y=sport_medal_dist['Silver'], marker_color='silver'))
                fig.add_trace(go.Bar(name='Bronze', x=sport_medal_dist.index, y=sport_medal_dist['Bronze'], marker_color='#CD7F32'))
                
                fig.update_layout(
                    barmode='group',
                    xaxis_title="Sport",
                    yaxis_title="Number of Medals",
                    height=500,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("All Sports Medal Count")
            st.dataframe(
                medals_by_sport.to_frame('Total Medals').reset_index(),
                height=400,
                use_container_width=True
            )
        
        with tab4:
            st.header("Year-by-Year Analysis")
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                selected_year = st.selectbox("Select Year for Analysis", years)
            
            with col2:
                st.subheader(f"Medal Distribution in {selected_year}")
            
            year_medals = get_year_medals(filtered_df, selected_year)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(
                    x=year_medals.index[:15],
                    y=year_medals.values[:15],
                    labels={'x': 'Country', 'y': 'Total Medals'},
                    color=year_medals.values[:15],
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(showlegend=False, height=400)
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.pie(
                    values=year_medals.values[:10],
                    names=year_medals.index[:10],
                    hole=0.4
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            st.subheader(f"Complete Rankings for {selected_year}")
            st.dataframe(
                year_medals.to_frame('Total Medals').reset_index(),
                height=400,
                use_container_width=True
            )
        
        with tab5:
            st.header("Performance Trends")
            
            st.subheader("Countries with Greatest Improvement")
            
            try:
                improvement = calculate_improvement(filtered_df)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    top_improvement = improvement.head(15)
                    
                    fig = px.bar(
                        x=top_improvement['Country'],
                        y=top_improvement['Delta'],
                        labels={'x': 'Country', 'y': 'Medal Increase'},
                        color=top_improvement['Delta'],
                        color_continuous_scale='Greens'
                    )
                    fig.update_layout(showlegend=False, height=400)
                    fig.update_xaxes(tickangle=45)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.dataframe(
                        improvement[['Country', 'Year', 'Total_Medals', 'Delta']].head(20),
                        height=400,
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Could not calculate improvement trends: {e}")
            
            st.subheader("Medal Count Over Years")
            
            # Select countries for trend analysis
            trend_countries = st.multiselect(
                "Select countries to compare",
                options=sorted(df['Country'].unique()),
                default=list(get_top_countries(df, 5).index)
            )
            
            if trend_countries:
                country_year_data = df[df['Country'].isin(trend_countries)].groupby(['Country', 'Year'])['Total_Medals'].sum().reset_index()
                
                fig = px.line(
                    country_year_data,
                    x='Year',
                    y='Total_Medals',
                    color='Country',
                    markers=True,
                    labels={'Total_Medals': 'Total Medals', 'Year': 'Olympic Year'}
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
        
        # Download section
        st.markdown("---")
        st.subheader("📥 Download Filtered Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name="olympic_filtered_data.csv",
                mime="text/csv"
            )
        
        with col2:
            summary_data = pd.DataFrame([summary])
            summary_csv = summary_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Summary",
                data=summary_csv,
                file_name="olympic_summary.csv",
                mime="text/csv"
            )
    
    else:
        st.info("👆 Please upload your Olympic dataset CSV file to begin the analysis.")
        st.markdown("""
        ### Expected Data Format
        Your CSV file should contain the following columns:
        - **Athlete**: Name of the athlete
        - **Age**: Age of the athlete
        - **Country**: Country represented
        - **Year**: Olympic year
        - **Date**: Date of the event
        - **Sport**: Type of sport
        - **Gold**: Number of gold medals
        - **Silver**: Number of silver medals
        - **Bronze**: Number of bronze medals
        - **Total**: Total medals (will be renamed to Total_Medals)
        """)

if __name__ == "__main__":
    main()
