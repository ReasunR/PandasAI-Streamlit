import pandas as pd
import streamlit as st
from sql_example import get_list_of_tables_from_sql_db, get_df_from_table, ask, get_log_content, get_code_to_run, \
    get_agent, explain

st.set_page_config(layout="wide")
LIST_OF_TABLES = get_list_of_tables_from_sql_db()
st.markdown("<h1 style='text-align: center;'>Ask your data anything! 🧙‍</h1>", unsafe_allow_html=True)


def add_table():
    selected_table = st.session_state.selected_table
    if selected_table not in st.session_state.list_of_all_added_tables:
        st.session_state.list_of_all_added_tables.append(selected_table)


def remove_table(idx):
    st.session_state.list_of_all_added_tables.pop(idx)


def create_agent(list_of_dfs):
    st.session_state.agent = get_agent(list_of_dfs)


if 'list_of_all_added_tables' not in st.session_state:
    st.session_state.list_of_all_added_tables = []
if 'ask_result' not in st.session_state:
    st.session_state.ask_result = None
if 'explain_result' not in st.session_state:
    st.session_state.explain_result = None
if 'agent' not in st.session_state:
    st.session_state.agent = None

left, middle, right = st.columns([1, 2, 1])

with left:
    st.write("### Select Tables from SQL")
    table = st.selectbox('Available tables:', ['Select a table'] + LIST_OF_TABLES, key='selected_table')

    if table != 'Select a table':
        if st.checkbox('Show table head'):
            st.write(get_df_from_table(table).head())
        st.button('Add', on_click=add_table)

    st.divider()

    st.write("Selected tables:")
    if st.session_state.list_of_all_added_tables:
        for idx, added_table in enumerate(st.session_state.list_of_all_added_tables):
            col1, col2 = st.columns([3, 1])
            col1.write(added_table)
            col2.button(f'Remove', key=f'remove_{idx}', on_click=remove_table, args=(idx,))

    list_of_dfs = [get_df_from_table(table_name) for table_name in st.session_state.list_of_all_added_tables]
    st.button("Confirm", on_click=create_agent, args=(list_of_dfs,))

with middle:
    st.write("### Chat")
    user_input = st.text_input('Ask your data anything:', 'What is the average sepal length?')

    if st.button('Ask'):
        response = ask(user_input, st.session_state.agent)
        print(f'flag response: {response}\n')
        st.session_state.ask_result = response
        st.session_state.image_path = '/Users/checkito950/PycharmProjects/Streamlit_PandasAI/exports/charts/temp_chart.png'

    if isinstance(st.session_state.ask_result, pd.DataFrame) or st.session_state.ask_result:
        st.write(st.session_state.ask_result)
    if not isinstance(st.session_state.ask_result, pd.DataFrame) and len(
            str(st.session_state.ask_result)) > 13 and st.session_state.ask_result[-14:] == "temp_chart.png":
        st.image(st.session_state.image_path, caption='Your Image Caption', use_column_width=True)

    if st.button('Explain'):
        st.session_state.explain_result = explain(st.session_state.agent)

    if st.session_state.explain_result:
        st.write(st.session_state.explain_result)

with right:
    logs = get_log_content()
    code_to_run = get_code_to_run(user_input)

    st.write("Code to run:")
    if isinstance(st.session_state.ask_result, pd.DataFrame) or st.session_state.ask_result:
        st.code(code_to_run, language='python')
    else:
        st.write("No code to run yet.")

    st.divider()

    st.write("Logs:")
    if isinstance(st.session_state.ask_result, pd.DataFrame) or st.session_state.ask_result:
        st.write(logs, unsafe_allow_html=True)
    else:
        st.write("No logs to show yet.")
