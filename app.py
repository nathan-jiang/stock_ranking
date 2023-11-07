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
no_of_stocks = ['top 100', 'top 200', 'top 300', 'top 400', 'top 500']

zip_url = 'https://github.com/nathan-jiang/stock_ranking_web_app/blob/main/data.zip'
response = requests.get(zip_url)

if response.status_code == 200:
    with zipfile.ZipFile(io.BytesIO(response.content), "r") as zip_ref:
        file_list = zip_ref.namelist()
        for file_name in file_list:
            with zip_ref.open(file_name) as csv_file:
                file_contents = csv_file.read()
                globals()['ranking_%s' % file_name] = pd.read_csv(io.BytesIO(file_contents))
                globals()['ranking_%s' % file_name].set_index(globals()['ranking_%s' % file_name].columns[0], inplace=True)  
else:
    print("Failed to download the ZIP archive.")

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
                    if sector_selected == "All":
                        df = st.dataframe(
                            globals()['ranking_%s%s' %
                                      (year_selected,
                                       months_dict[month_selected])])
                    else:
                        df = st.dataframe(
                            globals()['ranking_%s%s' %
                                      (year_selected,
                                       months_dict[month_selected])]
                            [globals()['ranking_%s%s' %
                                       (year_selected,
                                        months_dict[month_selected])]
                             ['ICB Industry name'] == sector_selected])
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
                    df = globals()['ranking_%s%s' %
                                   (year_selected,
                                    months_dict[month_selected])]
                    value_counts = df['ICB Industry name'][:int(
                        number_selected[-3:])].value_counts()

                    empty_labels = [''] * len(value_counts)
                    fig, ax = plt.subplots()
                    plt.figure(figsize=(8,
                                        8))  # Set the figure size (optional)
                    pie = ax.pie(value_counts,
                                 labels=empty_labels,
                                 autopct='%1.0f%%',
                                 textprops={
                                     'fontsize': 12,
                                     'color': 'black'
                                 },
                                 startangle=90)
                    ax.axis('equal')
                    ax.legend(pie[0],
                              value_counts.index,
                              title='Sector Breakdown (%s)' % number_selected,
                              loc="center left",
                              bbox_to_anchor=(1, 0, 0.5, 1))
                    st.pyplot(fig)
                    comment = "Some comment"

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
