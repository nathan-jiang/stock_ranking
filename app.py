import requests
import streamlit as st
import pandas as pd
import datetime
import io
import plotly.express as px
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import calendar

st.write('#')
# Streamlit page config
st.set_page_config(page_title="Ranking Algo on Stocks",
                   page_icon=":tada:",
                   layout="wide")

# Load Lottie animation
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Local CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style/style.css")

# Load assets
lottie_stock = load_lottieurl("https://lottie.host/befbdacd-2c16-4004-b618-52438922978b/TZkcNE0Uvq.json")

# Caching data to avoid repeated requests
@st.cache_data
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        csv_content = io.BytesIO(response.content)
        return pd.read_csv(csv_content)
    return None

# ---- HEADER SECTION ----
def header_section():
    with st.container():
        st.subheader("Stock Ranking with Combinatorial Fusion")
        st.title("A Comprehensive Ranking Algo on US Stocks")
        st.write("""
            This ranking algorithm ranks all US stocks with a market cap of over $250 million on a monthly basis for the period of April 2020 - June 2024. 
            A fixed pool of machine learning base models is employed, and predictions are optimized through the 'Combinatorial Fusion Analysis' framework.
        """)
        st.write("[Find more on Github>](https://github.com/nathan-jiang/Equity-Ranking-with-SD-and-CFA)")

# ---- SETTINGS ----
def get_settings():
    current_year = datetime.date.today().year
    years = [current_year, current_year - 1, current_year - 2, current_year - 3]
    months = list(calendar.month_name[1:])
    sectors = ["All", "Basic Materials", "Consumer Discretionary", "Consumer Staples",
               "Energy", "Financials", "Health Care", "Industrials", "Real Estate",
               "Technology", "Telecommunications", "Utilities"]
    no_of_stocks = ['top 100', 'top 200', 'top 300', 'top 400', 'top 500']
    
    months_dict = {month: str(index).zfill(2) for index, month in enumerate(calendar.month_name) if month}
    
    return years, months, sectors, no_of_stocks, months_dict

# ---- Ranking Generator ----
def ranking_generator(result_placeholder, years, months, sectors, months_dict, base_url):
    st.header("Ranking Generator")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        month_selected = col1.selectbox("Select Month:", months)
        year_selected = col2.selectbox("Select Year:", years)
        sector_selected = col3.selectbox("Select Sector:", sectors)
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            with st.spinner("Fetching and processing data..."):
                st.write(f"Ranking for {month_selected}, {year_selected}, {sector_selected}")
                data_url = f'{base_url}{year_selected}{months_dict[month_selected]}.csv'
                df = fetch_data(data_url)

                if df is not None:
                    df.set_index(df.columns[0], inplace=True)
                    if sector_selected == "All":
                        result_placeholder.dataframe(df, use_container_width=True)
                    else:
                        result_placeholder.dataframe(df[df['ICB Industry name'] == sector_selected], use_container_width=True)
                else:
                    st.error("Failed to load data")
                    
    # Clear Results button
    if st.button("Clear Results"):
        result_placeholder.empty()

# ---- Data Visualization ----
def data_visualization(years, months, no_of_stocks, months_dict, base_url):
    st.header("Data Visualization")
    with st.form("saved_no_of_stocks"):
        col1, col2, col3 = st.columns(3)
        month_selected = col1.selectbox("Select Month:", months)
        year_selected = col2.selectbox("Select Year:", years)
        number_selected = col3.selectbox("Select Number of Stocks", no_of_stocks)
        submitted = st.form_submit_button("Plot Sector Breakdown")
        
        if submitted:
            with st.spinner("Loading and processing data..."):
                data_url = f'{base_url}{year_selected}{months_dict[month_selected]}.csv'
                df = fetch_data(data_url)
                
                if df is not None:
                    df.set_index(df.columns[0], inplace=True)
                    value_counts = df['ICB Industry name'][:int(number_selected[-3:])].value_counts()

                    fig = px.pie(names=value_counts.index, values=value_counts,
                                 title=f'Sector Breakdown ({number_selected})',
                                 labels={'label': 'Sector'},
                                 template='plotly', hole=0.4)

                    st.plotly_chart(fig, use_container_width=True)

# ---- MAIN APP ----
def main():
    header_section()
    result_placeholder = st.empty()
    base_url = 'https://raw.githubusercontent.com/nathan-jiang/stock_ranking_web_app/main/data/'
    years, months, sectors, no_of_stocks, months_dict = get_settings()
    
    # Option Menu
    selected = option_menu(None, ["Ranking Generator", "Data Visualization"],
                           icons=["list-ol", "pie-chart-fill"], orientation="horizontal")
    
    if selected == "Ranking Generator":
        ranking_generator(result_placeholder, years, months, sectors, months_dict, base_url)
    
    elif selected == "Data Visualization":
        data_visualization(years, months, no_of_stocks, months_dict, base_url)

    with st.sidebar:
        st_lottie(lottie_stock, height=300, key="stock")

# Run the app
if __name__ == "__main__":
    main()

# ---- CONTACT ----
with st.container():
    st.write("---")
    st.header("Get In Touch With Me!")
    st.write("##")

    contact_form = """
    <form action="https://formsubmit.co/njiang3@fordham.edu" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="You email" required>
        <textarea name="message" placeholder="Your message here" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()


