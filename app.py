import requests
import streamlit as st
import streamlit_lottie
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import calendar
import datetime
import pandas as pd
import calendar
import io
import seaborn as sns
import plotly.express as px

sns.set()
import matplotlib.pyplot as plt
import zipfile

# find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Ranking Algo on Stocks",
                   page_icon=":tada:",
                   layout="wide")


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")
# ---- LOAD ASSETS ----
lottie_stock = load_lottieurl(
    "https://lottie.host/befbdacd-2c16-4004-b618-52438922978b/TZkcNE0Uvq.json")

# ---- HEADER SECTION ----
with st.container():

    st.subheader("Stock Ranking with Combinatorial Fusion")
    st.title("A Comprehensive Ranking Algo on US Stocks")
    st.write(
        "This ranking algorithm aims at ranking all the US stocks with a market cap of over $250 millions on a monthly basis for the period of April 2020 - September 2023. A fixed pool of machine learning base models are employed, and their predictions are further optimized and enhanced through model fusion technique called 'Combinatorial Fusion Analysis', a generative AI framework for pre-training, generating, evaluating, and optimizing diverse models."
    )
    st.write(
        "[Find more on Github>](https://github.com/nathan-jiang/Equity-Ranking-with-SD-and-CFA)"
    )

# ---- SETTINGS ----
years = [
    datetime.date.today().year,
    datetime.date.today().year - 1,
    datetime.date.today().year - 2,
    datetime.date.today().year - 3
]
end = datetime.date(2023, 9, 30)
start = datetime.date(2020, 4, 1)
dates = pd.date_range(start, end, freq='BMS')
dates = dates.strftime('%Y%m')
months = list(calendar.month_name[1:])
months_dict = dict((month, str(index).zfill(2))
                   for index, month in enumerate(calendar.month_name) if month)
sectors = [
    "All", "Basic Materials", "Consumer Discretionary", "Consumer Staples",
    "Energy", "Financials", "Health Care", "Industrials", "Real Estate",
    "Technology", "Telecommunications", "Utilities"
]
no_of_stocks = ['top 100', 'top 200', 'top 300', 'top 400', 'top 500']

base_url = 'https://raw.githubusercontent.com/nathan-jiang/stock_ranking_web_app/main/data/'

# ---- SOMETHING MORE ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        # ---- NAVIGATION MENU ----
        selected = option_menu(
            menu_title=None,
            options=["Ranking Generator", "Data Visualization"],
            icons=["list-ol",
                   "pie-chart-fill"],  #https://icons.getbootstrap.com/
            orientation="horizontal",
        )
        
        if selected == "Ranking Generator":
            st.header("Ranking Generator")
            # ---- INPUT & SAVE PERIODS ----
            with st.form("entry_form", clear_on_submit=True):
                col1, col2, col3 = st.columns(3)
                month_selected = col1.selectbox("Select Month:", months)
                year_selected = col2.selectbox("Select Year:", years)
                sector_selected = col3.selectbox("Select Sector:", sectors)
                submitted = st.form_submit_button("Submit")
                if submitted:
                    st.write(
                        f"Ranking for {month_selected}, {year_selected}, {sector_selected}"
                    )
                    response = requests.get(
                        f'{base_url}{year_selected}{months_dict[month_selected]}.csv'
                    )
                    if sector_selected == "All":
                        if response.status_code == 200:
                            csv_content = io.BytesIO(response.content)
                            df = pd.read_csv(csv_content)
                            df.set_index(df.columns[0], inplace=True)
                            df = st.dataframe(df)
                    else:
                        if response.status_code == 200:
                            csv_content = io.BytesIO(response.content)
                            df = pd.read_csv(csv_content)
                            df.set_index(df.columns[0], inplace=True)
                            df = st.dataframe(
                                df[df['ICB Industry name'] == sector_selected])
                "---"
                with st.expander("Comment"):
                    comment = st.text_area(
                        "", placeholder="Enter a comment here ...")
                "---"
                submitted = st.form_submit_button("Save Data")
                if submitted:
                    period = str(st.session_state["year"]) + "_" + str(
                        st.session_state["month"])
                    sector = str(st.session_state["sector"])
                    #data = conn.read(spreadsheet=url, worksheet=gids[0])
                    #st.dataframe(data)

                    # TODO: Insert values into database
                    #st.write(f"sectors: {sectors}")
                    st.success("Data saved!")
        if selected == "Data Visualization":
            st.header("Data Visualization")
            with st.form("saved_no_of_stocks"):
                col1, col2, col3 = st.columns(3)
                month_selected = col1.selectbox("Select Month:", months)
                year_selected = col2.selectbox("Select Year:", years)
                number_selected = col3.selectbox("Select Number of Stocks",
                                                 no_of_stocks)
                submitted = st.form_submit_button("Plot Sector Breakdown")
                if submitted:
                    response = requests.get(
                        f'{base_url}{year_selected}{months_dict[month_selected]}.csv'
                    )
                    month_str = months_dict[month_selected]
                    month_int = int(month_str) - 1
                    formatted_month = f'{month_int:02d}'
                    if month_selected == 'January':
                        response_prev = requests.get(
                            f'{base_url}{year_selected-1}' + '12.csv')
                    else:
                        response_prev = requests.get(
                            f'{base_url}{year_selected}{formatted_month}.csv')
                    if response.status_code == 200 and response_prev.status_code == 200:
                        csv_content = io.BytesIO(response.content)
                        df = pd.read_csv(csv_content)
                        df.set_index(df.columns[0], inplace=True)
                        value_counts = df['ICB Industry name'][:int(
                            number_selected[-3:])].value_counts()

                        csv_content_prev = io.BytesIO(response_prev.content)
                        df_prev = pd.read_csv(csv_content_prev)
                        df_prev.set_index(df_prev.columns[0], inplace=True)
                        value_counts_prev = df_prev['ICB Industry name'][:int(
                            number_selected[-3:])].value_counts()

                        fig = px.pie(names=value_counts.index,
                                     values=value_counts,
                                     title='Sector Breakdown (%s)' %
                                     number_selected,
                                     labels={'label': sectors},
                                     template='plotly',
                                     hole=0.4)

                        fig.update_traces(
                            textinfo='percent+label',
                            hoverinfo='label+percent',
                            textfont_size=12,
                            textposition='outside',
                        )

                        fig.update_layout(
                            showlegend=True,
                            legend_title_text='ICB Industry Name',
                            legend=dict(orientation='h',
                                        yanchor='middle',
                                        xanchor='left',
                                        x=1.8,
                                        y=0.6),
                        )

                        st.plotly_chart(fig, use_container_width=True)

                        weight_change_diff = (value_counts - value_counts_prev
                                              ) / int(number_selected[-3:])
                        colors = [
                            'red' if diff < 0 else 'green'
                            for diff in weight_change_diff
                        ]

                        # Create a bar chart using Plotly Express
                        fig_bar = px.bar(
                            x=weight_change_diff.index,
                            y=weight_change_diff,
                            title=
                            'Sector Weight Change (Current Month - Previous Month)',
                            labels={
                                'y': 'Weight Change',
                                'x': 'Sector'
                            },
                            template='plotly',
                            color=colors,
                            text=(weight_change_diff *
                                  100).round(1).astype(str) + '%',
                        )

                        # Update layout and show the legend
                        fig_bar.update_layout(
                            showlegend=False,
                            legend_title_text='ICB Industry Name',
                            legend=dict(orientation='h',
                                        yanchor='middle',
                                        xanchor='left',
                                        x=1.8,
                                        y=1.0),
                            xaxis_title='ICB Industry Name',
                            yaxis_title='Weight Change',
                            xaxis=dict(tickangle=90))

                        # Show the bar chart
                        st.plotly_chart(fig_bar, use_container_width=True)

    with right_column:
        st_lottie(lottie_stock, height=300, key="stock")

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
