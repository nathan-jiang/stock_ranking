import requests
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from streamlit_gsheets import GSheetsConnection
import plotly.graph_objects as go
import calendar
import datetime
import pandas as pd
import calendar

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
        "This ranking algorithm aims at ranking all the US stocks with a market cap of over $250 millions on a monthly basis for the period of April 2020 - September 2023. A fixed pool of machine learning base models are employed, and their predictions are further optimized and enhanced through model fusion technique called 'Combinatorial Fusion Analysis', a generative AI framwork for pretraining, generating, evaluating, and optimizing diverse models."
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

ranking_lists = pd.ExcelFile('combined_ranking_new_method.xlsx')
for date in dates:
    globals()['ranking_%s' % date] = pd.read_excel(ranking_lists,
                                                   date,
                                                   index_col=0)

# ---- SOMETHING MORE ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("Ranking Generator")
        # ---- INPUT & SAVE PERIODS ----
        with st.form("entry_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            #col1.selectbox("Select Month:", months, key="month")
            #col2.selectbox("Select Year:", years, key="year")
            #col3.selectbox("Select Sector:", sectors, key="sector")
            month_selected = col1.selectbox("Select Month:", months)
            year_selected = col2.selectbox("Select Year:", years)
            sector_selected = col3.selectbox("Select Sector:", sectors)
            submitted = st.form_submit_button("Submit")
            if submitted:
                st.write(
                    f"Ranking for {month_selected}, {year_selected}, {sector_selected}"
                )
                if sector_selected == "All":
                    df = st.dataframe(
                        globals()['ranking_%s%s' %
                                  (year_selected,
                                   months_dict[month_selected])], )
                else:
                    df = st.dataframe(
                        globals()['ranking_%s%s' %
                                  (year_selected, months_dict[month_selected])]
                        [globals()['ranking_%s%s' %
                                   (year_selected,
                                    months_dict[month_selected])]
                         ['ICB Industry name'] == sector_selected], )
            "---"
            with st.expander("Comment"):
                comment = st.text_area("",
                                       placeholder="Enter a comment here ...")
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
