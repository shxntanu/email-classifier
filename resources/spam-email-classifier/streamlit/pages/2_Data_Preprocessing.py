import numpy as np
import pandas as pd
import nltk
import os
import time
import string
import re
import tqdm

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
import streamlit as st

st.set_page_config(layout="centered", page_title="Data preprocessing",
                   page_icon="📊", initial_sidebar_state="collapsed")

path = os.path.join('.', 'data', 'spam.csv')

if 'steps' not in st.session_state:
    st.session_state.steps = {
        'load_data': False,
        'drop_columns': False,
        'handle_missings': False,
        'rename_columns': False,
        'remove_duplicates': False,
        'extract_features': False,
        'preprocess_text': False,
        'handle_outliers': False,
        'handle_inconsistencies': False,
    }

if 'data' not in st.session_state:
    st.session_state.data = {
        'load_data': pd.DataFrame(),
        'drop_columns': pd.DataFrame(),
        'handle_missings': pd.DataFrame(),
        'rename_columns': pd.DataFrame(),
        'remove_duplicates': pd.DataFrame(),
        'extract_features': pd.DataFrame(),
        'preprocess_text': pd.DataFrame(),
        'handle_outliers': pd.DataFrame(),
        'handle_inconsistencies': pd.DataFrame(),
    }

# if 'features' not in st.session_state:
    # st.session_state.features = {
        # # 'Unnamed: 0': 'unnamed',
        # # 'label': 'label',
        # # 'text': 'text'
    # }

if 'collapsed_status' not in st.session_state:
    st.session_state.collapsed_status = {
        'load_data': True,
        'drop_columns': False,
        'handle_missings': False,
        'rename_columns': False,
        'remove_duplicates': False,
        'extract_features': False,
        'preprocess_text': False,
        'handle_outliers': False,
        'handle_inconsistencies': False,
    }


# @st.cache_data
# def progress_bar():
    # file_size = sum(1 for line in open(path))

    # progress_bar = tqdm.tqdm(total=file_size, desc='Loading data ...')

    # data = pd.read_csv(path, iterator=True, chunksize=1000,
                       # encoding="iso-8859-1")

    # data_list = []
    # for chunk in data:
        # data_list.append(chunk)
        # progress_bar.update(len(chunk))

    # data_df = pd.concat(data_list, ignore_index=True)

    # progress_bar.close()

    # data = data_df

    # return data


with st.expander('load_data', expanded=st.session_state.collapsed_status['load_data']):

    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

    if uploaded_file is not None:

        data = pd.read_csv(uploaded_file)

        st.session_state.data['load_data'] = data
        st.session_state.steps['load_data'] = True
        st.session_state.collapsed_status['load_data'] = False
        st.session_state.collapsed_status['drop_columns'] = True

        st.dataframe(data.head(10), hide_index=True, use_container_width=True)

    else:
        st.error("Please upload a file")

with st.expander('drop_columns', expanded=st.session_state.collapsed_status['drop_columns']):

    if st.button('Skip', type='primary', key='skip-1', use_container_width=True):
        st.session_state.data['drop_columns'] = st.session_state.data['load_data']
        st.session_state.steps['drop_columns'] = True
        st.session_state.collapsed_status['handle_missings'] = True

    if st.session_state.steps['load_data']:

        data = st.session_state.data['load_data']
        columns = st.multiselect(label='Columns', label_visibility='hidden', options=data.columns)

        if st.button('Drop', type='primary', use_container_width=True):

            st.success(f"Columns {columns} dropped")

            st.session_state.data['drop_columns'] = data = data.drop(columns=columns)
            st.session_state.steps['drop_columns'] = True
            st.session_state.collapsed_status['handle_missings'] = True

        if not st.session_state.data['drop_columns'].empty:
            st.dataframe(st.session_state.data['drop_columns'].head(10), hide_index=True, use_container_width=True)
        else:
            st.dataframe(st.session_state.data['load_data'].head(10), hide_index=True, use_container_width=True)

    else:
        st.error("Load data first")

with st.expander('handle_missings', expanded=st.session_state.collapsed_status['handle_missings']):

    if st.button('Skip', type='primary', key='skip-10', use_container_width=True):
        st.session_state.data['handle_missings'] = st.session_state.data['drop_columns']
        st.session_state.steps['handle_missings'] = True
        st.session_state.collapsed_status['rename_columns'] = True

    if st.session_state.steps['drop_columns']:

        data = st.session_state.data['drop_columns']

        if st.button('Show missing values', type='primary', use_container_width=True):

            null_count = data.isnull().sum()

            if null_count.sum() == 0:
                st.info("No missing values")
            else:
                st.warning(f"Missing values in {int(null_count.sum())} rows")
                st.warning("First row with missing values")
                st.write(data[data.isnull().any(axis=1)].head(1))
                data.dropna(axis=0, inplace=True)

            st.session_state.data['handle_missings'] =  data
            st.session_state.steps['handle_missings'] = True
            st.session_state.collapsed_status['rename_columns'] = True

    else:
        st.error("Drop unnecessary columns first")

with st.expander('rename_columns', expanded=st.session_state.collapsed_status['rename_columns']):

    if st.button('Skip', type='primary', key='skip-2', use_container_width=True):
        st.session_state.data['rename_columns'] = st.session_state.data['handle_missings']
        st.session_state.steps['rename_columns'] = True
        st.session_state.collapsed_status['remove_duplicates'] = True

    if st.session_state.steps['handle_missings']:

        data = pd.DataFrame()
        columns = []

        if not st.session_state.data['rename_columns'].empty: data = st.session_state.data['rename_columns']
        else: data = st.session_state.data['handle_missings']

        columns = st.selectbox(label='Columns', label_visibility='hidden', options=data.columns)
        name_new = st.text_input(label='New name')

        if st.button('Rename', type='primary', use_container_width=True):

            if name_new in data.columns:
                st.error(f"Column {name_new} already exists")
            else:
                data.rename(columns={columns: name_new}, inplace=True)
                st.session_state.data['rename_columns'] = data
                st.session_state.steps['rename_columns'] = True
                st.session_state.collapsed_status['remove_duplicates'] = True

                st.success(f"Column {columns} renamed to {name_new}")

        st.dataframe(data.head(10), hide_index=True, use_container_width=True)
    else:
        st.error("handle_missings first")

with st.expander('remove_duplicates', expanded=st.session_state.collapsed_status['remove_duplicates']):

    if st.button('Skip', type='primary', key='skip-3', use_container_width=True):
        st.session_state.data['remove_duplicates'] = st.session_state.data['rename_columns']
        st.session_state.steps['remove_duplicates'] = True
        st.session_state.collapsed_status['extract_features'] = True

    if st.session_state.steps['rename_columns']:

        data = st.session_state.data['rename_columns']
        column = st.selectbox(label='Columns', key=1, label_visibility='hidden', options=data.columns)
        st.warning(f"Number of duplicated rows: {data[column].duplicated().sum()}")

        if st.button('remove_duplicates', type='primary', use_container_width=True):
            columns = data.columns
            data.drop_duplicates(subset=column, inplace=True)
            st.success(f"Number of duplicated rows after removing: {data.duplicated().sum()}")

            st.session_state.data['remove_duplicates'] = data
            st.session_state.steps['remove_duplicates'] = True
            st.session_state.collapsed_status['extract_features'] = True
    else:
        st.error("Rename columns first")

url_regex = re.compile("(?P<url>https?://[^\s]+)")
digits_regex = re.compile("[0-9]+")
curr_symbols = re.compile(r'[€$£¥]')


def get_urls_count(txt):
    return len(re.findall(url_regex, txt))


def get_digits_count(txt):
    return len(re.findall(digits_regex, txt))


def contains_curr_symbols(txt):
    return len(re.findall(curr_symbols, txt)) > 0


with st.expander('extract_features', expanded=st.session_state.collapsed_status['extract_features']):

    if st.button('Skip', type='primary', key='skip-4', use_container_width=True):
        st.session_state.data['extract_features'] = st.session_state.data['remove_duplicates']
        st.session_state.steps['extract_features'] = True
        st.session_state.collapsed_status['preprocess_text'] = True

    if st.session_state.steps['remove_duplicates']:

        data = st.session_state.data['remove_duplicates']

        column = st.selectbox(label='Columns', key=99, label_visibility='hidden', options=data.columns)

        options = st.multiselect(label='Features', label_visibility='hidden', options=['urls_count', 'digits_count', 'contains_curr_symbols', 'length'])

        if st.button('Extract features', type='primary', use_container_width=True):

            if len(options) == 0:
                st.warning('Select at least one feature')
            else:
                if 'urls_count' in options:
                    data["urls_count"] = data[str(column)].apply(get_urls_count)
                    # st.session_state.features["urls_count"] = "urls_count"
                else:
                    if "urls_count" in data.columns:
                        data.drop(columns=["urls_count"], inplace=True)
                if 'digits_count' in options:
                    data["digits_count"] = data[str(column)].apply(get_digits_count)
                    # st.session_state.features["digits_count"] = "digits_count"
                else:
                    if "digits_count" in data.columns:
                        data.drop(columns=["digits_count"], inplace=True)
                if 'contains_curr_symbols' in options:
                    data["contains_curr_symbols"] = data[str(
                        column)].apply(contains_curr_symbols)
                    # st.session_state.features["contains_curr_symbols"] = "contains_curr_symbols"
                else:
                    if "contains_curr_symbols" in data.columns:
                        data.drop(columns=["contains_curr_symbols"], inplace=True)
                if 'length' in options:
                    data["length"] = data[str(column)].apply(len)
                    # st.session_state.features["length"] = "length"
                else:
                    if "length" in data.columns:
                        data.drop(columns=["length"], inplace=True)

                st.session_state.data['extract_features'] = data
                st.session_state.steps['extract_features'] = True
                st.session_state.collapsed_status['preprocess_text'] = True

        st.dataframe(data.head(10), hide_index=True, use_container_width=True)

    else:
        st.error("remove_duplicates first")

stop_words = set(nltk.corpus.stopwords.words("english"))
special_chars = set(string.printable) - set(string.ascii_letters) - set(" ")
escaped_chars = [re.escape(c) for c in special_chars]
regex = re.compile(f"({'|'.join(escaped_chars)})")
stemmer = nltk.stem.porter.PorterStemmer()


def transform(text):

    # lowercase
    text = text.lower()

    # remove urls
    text = re.sub(url_regex, " ", text)

    # tokenization
    text = nltk.word_tokenize(text, language='english')

    # stop words removal
    text = [word for word in text if word not in stop_words]

    # noise removal
    text = [word for word in text if word.isalpha()]

    # stemming
    text = [stemmer.stem(word) for word in text]

    return ' '.join(text)


with st.expander('Text cleaning', expanded=st.session_state.collapsed_status['preprocess_text']):

    if st.button('Skip', type='primary', key='skip-5', use_container_width=True):
        st.session_state.data['preprocess_text'] = st.session_state.data['extract_features']
        st.session_state.steps['preprocess_text'] = True
        st.session_state.collapsed_status['preprocess_text'] = True

    if st.session_state.steps['extract_features']:

        data = st.session_state.data['extract_features']

        column = st.selectbox(label='Columns', key=98, label_visibility='hidden', options=data.columns)

        if st.button('Clean text', type='primary', use_container_width=True):

            data[str(column)] = data[str(column)].apply(transform)

            st.session_state.data['preprocess_text'] = data
            st.session_state.steps['preprocess_text'] = True
            st.session_state.collapsed_status['preprocess_text'] = False

        st.dataframe(data.head(10), hide_index=True, use_container_width=True)

    else:

        st.error("Extract features first")

with st.expander('handle_outliers', expanded=st.session_state.collapsed_status['handle_outliers']):

    if st.button('Skip', type='primary', key='skip-6', use_container_width=True):
        st.session_state.data['handle_outliers'] = st.session_state.data['preprocess_text']
        st.session_state.steps['handle_outliers'] = True
        st.session_state.collapsed_status['handle_inconsistencies'] = True

    if st.session_state.steps['preprocess_text']:

        data = st.session_state.data['preprocess_text']
        column = st.selectbox(label='Columns', key=97, label_visibility='hidden',options=data.columns)

        if st.button('Handle outliers', type='primary', use_container_width=True):

            model = Pipeline(steps=[
                ("feature extraction", CountVectorizer()),
                ("estimator", IsolationForest())
            ])

            model.fit(data[column])

            predictions = model.predict(data[column])

            values, counts = np.unique(np.concatenate(
                [predictions, [1, -1]]), return_counts=True)
            counts = counts - 1
            n = counts[values == -1][0]

            if n != 0:
                st.warning(f"Number of outliers: {n}")
            else:
                st.success("No outliers found")

        st.session_state.data['handle_outliers'] = data
        st.session_state.steps['handle_outliers'] = True
        st.session_state.collapsed_status['handle_inconsistencies'] = True

        st.dataframe(data.head(10), hide_index=True, use_container_width=True)

    else:
        st.error("Clean text first")

# with st.expander('handle_inconsistencies'):
    # if st.session_state.steps['handle_inconsistencies']:
        # column = st.selectbox(label='Columns', key=97, label_visibility='hidden',
                              # options=st.session_state.data_transformed.columns)
        # # columns = st.multiselect(label='Columns', key=96, label_visibility='hidden', options=st.session_state.data_transformed.columns)
        # rows = st.session_state.data_transformed[column].unique()
        # rows_new = rows.copy()

        # for row, index in rows:
            # rows_new[index] = st.text_input(
                # label=f"Replace inconsistenties in {column} with", key=index+10, value=rows[index])

        # if st.button('Replace inconsistenties', type='primary', use_container_width=True):
            # st.session_state.data_transformed[column] = st.session_state.data_transformed[column].map(
                # lambda x: rows_new[rows == x][0])

with st.expander('handle_inconsistencies', expanded=st.session_state.collapsed_status['handle_inconsistencies']):
    if st.button('Skip', type='primary', key='skip-7', use_container_width=True):
        st.session_state.data['handle_inconsistencies'] = st.session_state.data['handle_outliers']
        st.session_state.steps['handle_inconsistencies'] = True
        csv_data = st.session_state.data['handle_inconsistencies'].to_csv(index=False).encode('utf-8')
        st.download_button(label='Download CSV', data=csv_data, file_name='my_data.csv', mime='text/csv', type='secondary', help='Download the data as a CSV file', use_container_width=True)

    if st.session_state.steps['handle_outliers']:

        data = st.session_state.data['handle_outliers']
        column = st.selectbox(label='Columns', key=112, label_visibility='hidden', options=data.columns)

        rows = data[column].unique()
        rows_new = {}

        for index, row in enumerate(rows):
            new_value = st.text_input(label=f"Replace inconsistency '{row}' in {column} with", key=index+20, value=row)
            rows_new[row] = new_value

        if st.button('Replace inconsistenties', type='primary', use_container_width=True):
            data[column] = data[column].map(lambda x: rows_new.get(x, x))

            st.session_state.data_transformed = data
            st.session_state.steps['handle_inconsistencies'] = True

            st.dataframe(data.head(10), hide_index=True, use_container_width=True)

            csv_data = data.to_csv(index=False).encode('utf-8')
            st.download_button(label='Download CSV', data=csv_data, file_name='my_data.csv', mime='text/csv', type='primary', help='Download the data as a CSV file', use_container_width=True)
    else:
        st.error("Handle outliers first")
