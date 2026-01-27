# olampic_dataset
# Olympic Medal Analysis Dashboard 🏅

A comprehensive Streamlit dashboard for analyzing Olympic medal data with interactive visualizations and filtering capabilities.

## Features

### 📊 Dashboard Components

1. **Overview Metrics**
   - Total medals, gold, silver, bronze counts
   - Total athletes and countries represented

2. **Country Analysis**
   - Top countries by total medals
   - Medal distribution (Gold, Silver, Bronze) stacked bar charts
   - Gold medal proportion analysis
   - Number of athletes per country (treemap visualization)

3. **Athletes Analysis**
   - Top 20 athletes by total medals
   - Medal breakdown for each athlete
   - Detailed athlete statistics table

4. **Sports Analysis**
   - Total medals by sport (pie chart)
   - Medal distribution across different sports
   - Complete sports ranking table

5. **Year-by-Year Analysis**
   - Medal distribution for selected year
   - Country rankings by year
   - Interactive year selector

6. **Performance Trends**
   - Countries with greatest improvement
   - Medal count trends over years
   - Multi-country comparison

### 🎛️ Interactive Filters

- **Year Filter**: Select specific Olympic years
- **Country Filter**: Focus on specific countries
- **Sport Filter**: Analyze specific sports

## Installation

1. **Install Python** (3.8 or higher)

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install packages individually:
   ```bash
   pip install streamlit pandas plotly
   ```

## Usage

### Running the Dashboard

1. **Basic run** (without data):
   ```bash
   streamlit run olympic_dashboard.py
   ```
   This will open the app with an upload interface.

2. **With your Olympic data CSV**:
   - Launch the app using the command above
   - Use the file uploader in the web interface to upload your CSV file
   - The dashboard will automatically load and analyze your data

### Data Format

Your CSV file should contain the following columns:

| Column  | Description              |
|---------|--------------------------|
| Athlete | Name of the athlete      |
| Age     | Age of the athlete       |
| Country | Country represented      |
| Year    | Olympic year             |
| Date    | Date of the event        |
| Sport   | Type of sport            |
| Gold    | Number of gold medals    |
| Silver  | Number of silver medals  |
| Bronze  | Number of bronze medals  |
| Total   | Total medals won         |

**Example data row:**
```csv
Athlete,Age,Country,Year,Date,Sport,Gold,Silver,Bronze,Total
Michael Phelps,23.0,United States,2008,08-24-08,Swimming,8,0,0,8
```

## Features Overview

### 1. Country Analysis Tab
- View top performing countries
- Analyze medal distribution by type
- Compare gold medal proportions
- Visualize athlete representation by country

### 2. Athletes Tab
- Discover top medal-winning athletes
- View detailed medal breakdowns
- Filter by country, year, or sport

### 3. Sports Tab
- Analyze medal distribution across sports
- Compare sports popularity
- View complete sport rankings

### 4. Year Analysis Tab
- Select specific Olympic years
- View country rankings for that year
- Analyze year-specific trends

### 5. Trends Tab
- Identify countries with greatest improvements
- Compare performance trends over time
- Visualize medal counts across multiple years

## Advanced Usage

### Filtering Data

Use the sidebar filters to:
- Select multiple years for comparison
- Focus on specific countries
- Analyze particular sports

### Downloading Results

- Download filtered dataset as CSV
- Export summary statistics
- Save visualizations (right-click on charts)

## Customization

To customize the dashboard:

1. **Modify colors**: Edit the color schemes in the `plotly` chart definitions
2. **Add new metrics**: Add calculations in the data processing functions
3. **Change layout**: Modify the column layouts using `st.columns()`
4. **Add new visualizations**: Use additional plotly chart types

## Troubleshooting

### Common Issues

1. **"Module not found" error**:
   ```bash
   pip install --upgrade streamlit pandas plotly
   ```

2. **CSV upload issues**:
   - Ensure CSV is properly formatted
   - Check that all required columns are present
   - Verify there are no special characters in column names

3. **Visualization not displaying**:
   - Check that your data contains valid values
   - Ensure there are no NaN values in key columns

4. **Performance issues with large datasets**:
   - The app uses `@st.cache_data` for optimization
   - Clear cache: `streamlit cache clear`

## Tips for Best Results

1. **Data Quality**: Ensure your data is clean with no missing values in critical columns
2. **Year Range**: Include multiple years for better trend analysis
3. **Filters**: Use filters to focus on specific insights
4. **Comparisons**: Select 3-5 countries for trend comparison for best visualization

## Technical Details

- **Framework**: Streamlit
- **Visualizations**: Plotly Express and Plotly Graph Objects
- **Data Processing**: Pandas
- **Caching**: Built-in Streamlit caching for performance

## Requirements

- Python 3.8+
- streamlit 1.31.0+
- pandas 2.1.4+
- plotly 5.18.0+

## License

This dashboard is provided as-is for analysis purposes.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify your data format matches the expected structure
3. Ensure all dependencies are correctly installed
