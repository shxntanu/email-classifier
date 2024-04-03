import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import numpy as np
import nltk
import os
import zipfile
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer

st.session_state['toggle'] = 0
st.session_state['download'] = 0
st.session_state['slider'] = 0
# st.session_state['df'] = pd.DataFrame()

st.title("Exploratory Data Analysis")

st.markdown("### Data Loading")

# buffer = None

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame()

with st.expander('load_data', expanded=True):

    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.session_state.data = data
        st.dataframe(data.head(10), hide_index=True, use_container_width=True)
    else:
        st.error("Please upload a file")

st.markdown("### Basic EDA")

with st.expander("Examine the top & the tail of the dataframe", expanded=False):

    data = st.session_state.data

    if not data.empty:
        st.dataframe(data.head(10), hide_index=True, use_container_width=True)
        st.dataframe(data.tail(10), hide_index=True, use_container_width=True)
    else:
        st.error("Please upload a file")

with st.expander("Examine the dimensions of the dataset", expanded=False):
    data = st.session_state.data
    if not data.empty:
        st.info(f"The number of columns is : {data.shape[1]}")
        st.info(f"The number of data points is : {data.shape[0]}")
    else:
        st.error("Please upload a file")

with st.expander("Examine data types and missing values", expanded=False):
    data = st.session_state.data
    if not data.empty:
        info = pd.DataFrame()
        info["Column"] = data.columns
        info["Non-Null Count"] = (~data.isna()).sum().apply(lambda x: str(x) + ' non-null').values
        info["Dtype"] = data.dtypes.values
        st.dataframe(info, hide_index=True, use_container_width=True)
    else:
        st.error("Please upload a file")

with st.expander("Examine basic statistics about the dataset", expanded=False):
    data = st.session_state.data
    if not data.empty:
        st.dataframe(data.describe(), hide_index=True, use_container_width=True)
        st.dataframe(data.select_dtypes(bool).describe(), hide_index=True, use_container_width=True)

st.markdown("### Visualization")

figures = {}

def fig_download_button(fig: plt.Figure, name: str):
    download = st.session_state['download']
    st.session_state['download'] += 1
    bytes = io.BytesIO()
    fig.savefig(fname=bytes)
    st.download_button(
        label="Export as png",
        data=bytes,
        file_name=f"{name}.png",
        mime="image/png",
        key=f"btn{download}",
        use_container_width=True
    )
    return bytes


with st.expander("Labels distribution", expanded=False):

    data = st.session_state.data

    if not data.empty:
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)

        # fig.set_size_inches()

        column = st.selectbox("Select the column to visualize", data.columns)
        unique_values = data[column].unique()

        sns.countplot(data=data, x=column, ax=ax1)
        data[column].value_counts().plot.pie(labels=unique_values, autopct="%0.2f", ax=ax2)

        ax1.set_title("class counts by label (Bar plot)")
        ax2.set_title("class counts by label (Pie plot)")

        st.pyplot(fig=fig)

        figures["Labels_distribution"] = fig_download_button(fig, name="lables_distribution")

        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
        # fig.set_size_inches(15, 7.5)

        sns.countplot(data=data, x=column, ax=ax1)
        data[column].value_counts().plot.pie(labels=unique_values, autopct="%0.2f", ax=ax2)

        ax1.set_title("class counts by label (Bar plot)")
        ax2.set_title("class counts by label (Pie plot)")

        st.pyplot(fig=fig)

        figures["Labels_distribution"] = fig_download_button(fig, name="lables_distribution")
    else:
        st.error("Please upload a file")

with st.expander("Unlabled vs labeled", expanded=False):
    if not data.empty:

        column = st.selectbox("Select the column to visualize", key='unlabled', options=data.columns)

        is_labeled = (data[column] == -1).map({
            True: "unlabled",
            False: "labeled"
        })

        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
        # fig.set_size_inches(15, 7.5)

        sns.countplot(x=is_labeled, ax=ax1)
        is_labeled.value_counts().plot.pie(
            labels=["unlabled", "labled"], autopct="%0.2f", ax=ax2)

        ax1.set_title("Unalebed vs labled (Bar plot)")
        ax2.set_title("Unalebed vs labled (Pie plot)")

        st.pyplot(fig=fig)

        figures["unlabled_vs_labled"] = fig_download_button(
            fig, name="unlabled_vs_labled")
    else:
        st.error("Please upload a file")

# labled_df = df[df["class"] != -1]

with st.expander("Ham vs Spam", expanded=False):
    labled_df = data[data["class"] != -1]
    data = st.session_state.data
    if not data.empty:
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
        # fig.set_size_inches(15, 7.5)
        # column = st.selectbox("Select the column to visualize", key='ham_spam', options=data.columns)
        column = data.columns[0]

        sns.countplot(data=labled_df, x="class", ax=ax1)
        labled_df[column].value_counts().plot.pie(labels=["ham", "spam"], autopct="%0.2f", ax=ax2)

        ax1.set_title("class counts by label (Bar plot)")
        ax2.set_title("class counts by label (Pie plot)")

        st.pyplot(fig=fig)

        figures["class_counts_lables_bar_plot"] = fig_download_button(fig, name="class_counts_lables_bar_plot")
    else:
        st.error("Please upload a file")

# def hist_plot(label: str, column: str, fig_name: str):
    # with st.expander(label, expanded=False):
        # data = st.session_state.data
        # if not data.empty:

            # selectbox = st.session_state['toggle']
            # slider = st.session_state['slider']

            # st.session_state['toggle'] += 1
            # st.session_state['slider'] += 1

            # log_scale = st.toggle(
                # label="Log Scale",
                # key=f"toggle{selectbox}",
                # value=False
            # )

            # eps = 0

            # if log_scale and data[column].min() <= 0:
                # st.warning(
                    # "Can not scale when data contains element with value less or equal to 0")
                # eps = st.slider("Specify a value for Epsilon",
                                # min_value=10e-10,
                                # max_value=1.,
                                # value=10e-1,
                                # key=f"slider{slider}"
                                # )

            # fig, ax = plt.subplots()

            # try:
                # sns.histplot(
                    # x=data[column] + eps,
                    # hue=data["class"],
                    # kde=True,
                    # ax=ax,
                    # stat="density",
                    # common_norm=False,
                    # log_scale=log_scale
                # )

                # # fig.set_size_inches(5, 5)
                # st.pyplot(fig=fig)

                # figures[fig_name] = fig_download_button(fig, name=fig_name)
            # except np.linalg.LinAlgError as error:
                # st.error(
                    # f"Log scaling has failed due to the following error : {error}")
        # else:
            # st.error("Please upload a file")


# for column in data.columns:
    # hist_plot(label=column, column=column, fig_name=column)
# hist_plot(label="Urls Count", column="Number of urls", fig_name="urls_count")
# hist_plot(label="Digits Count", column="Number of digit strings", fig_name="digits_count")
# hist_plot(label="Length", column="Length", fig_name="length")


st.markdown("### Word frequency analysis")

# with st.expander("Word frequency analysis", expanded=False):
    # if not data.empty:
        # column = st.selectbox("Select the column to visualize", key='word_frequency', options=data.columns)

        # fig, ax = plt.subplots(nrows=1, ncols=1)
        # # fig.set_size_inches(15, 7.5)

        # sns.countplot(data=data, x=column, ax=ax)

        # st.pyplot(fig=fig)

        # figures["Word_frequency_analysis"] = fig_download_button(fig, name="word_frequency_analysis")
    # else:
        # st.error("Please upload a file")


# with st.expander("Top k most frequent words", expanded=False):
    # if not data.empty:
        # column = st.selectbox("Select the column to visualize", key='top_k', options=data.columns)

        # fig, ax = plt.subplots(nrows=1, ncols=1)
        # # fig.set_size_inches(15, 7.5)

        # sns.countplot(data=data, x=column, ax=ax)

        # st.pyplot(fig=fig)

        # figures["top_k_most_frequent_words"] = fig_download_button(fig, name="top_k_most_frequent_words")
    # else:
        # st.error("Please upload a file")
        
with st.expander("Top k most frequent words", expanded=False):
    if not data.empty:
        column = st.selectbox("Select the column to visualize", key='top_k', options=data.columns)

        # Use CountVectorizer to transform text data
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(data[column])

        # Get the total count for each word
        word_counts = X.sum(axis=0)

        # Get the feature names (words)
        feature_names = vectorizer.get_feature_names_out()

        # Create a dictionary mapping words to their counts
        word_count_dict = dict(zip(feature_names, word_counts.A1))

        # Sort the dictionary by counts in descending order
        sorted_word_count_dict = dict(sorted(word_count_dict.items(), key=lambda item: item[1], reverse=True))

        # Select the top k most frequent words
        k = 10  # Change k to the desired number of top words
        top_k_words = list(sorted_word_count_dict.keys())[:k]
        top_k_counts = list(sorted_word_count_dict.values())[:k]

        # Visualize the frequency of top k words using a count plot
        fig, ax = plt.subplots()
        sns.barplot(x=top_k_words, y=top_k_counts, ax=ax)
        ax.set_title(f"Top {k} Most Frequent Words in {column}")
        ax.set_xlabel("Words")
        ax.set_ylabel("Frequency")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        figures["top_k_most_frequent_words"] = fig_download_button(fig, name="top_k_most_frequent_words")
    else:
        st.error("Please upload a file")



# def plot_topk_results(dist, ax, k=20):
    # most_common = dist.most_common(k)
    # tokens = np.array([word for word, count in most_common])
    # counts = np.array([count for word, count in most_common])
    # sns.barplot(x=tokens, y=counts, ax=ax)
    # ax.set_xticklabels(ax.get_xticklabels(), rotation=80)


# def top_k():
    # with st.expander("Top k most frequent words"):
        # fig, (ax1, ax2) = plt.subplots(ncols=2, nrows=1)

        # k = st.number_input(label="K", min_value=5, max_value=50, value=20)

        # fig.set_size_inches(15, 7.5)

        # plot_topk_results(grouped_df["frequencies"].loc[0], ax=ax1, k=k)
        # plot_topk_results(grouped_df["frequencies"].loc[1], ax=ax2, k=k)

        # ax1.set_title(f"Top {k} most frequent words in ham emails")
        # ax2.set_title(f"Top {k} most frequent words in spam emails")

        # st.pyplot(fig=fig)

        # figures["top_k"] = fig_download_button(fig, name="top_k")


# def word_clouds():
    # with st.expander("Wordclouds", expanded=False):
        # wc1, wc2 = WordCloud(), WordCloud()

        # im1 = wc1.generate(grouped_df["content"].loc[0])
        # im2 = wc2.generate(grouped_df["content"].loc[1])

        # fig, (ax1, ax2) = plt.subplots(ncols=2, nrows=1)

        # fig.set_size_inches(15, 7.5)

        # ax1.imshow(im1)
        # ax2.imshow(im2)

        # st.pyplot(fig=fig)

        # figures["word_clouds"] = fig_download_button(fig, name="word_clouds")


# if buffer:

    # grouped_df = labled_df[["class", "content"]
                           # ].groupby(by="class").agg(" ".join)
    # grouped_df["tokens"] = grouped_df["content"].apply(nltk.word_tokenize)
    # grouped_df["frequencies"] = grouped_df["tokens"].apply(
        # nltk.probability.FreqDist)

    # top_k()
    # word_clouds()

# st.markdown("### Correlations analysis")


# def heatmap():
    # with st.expander("Heatmap", expanded=False):
        # method = st.selectbox("Pick heatmap type", options=[
                              # 'pearson', 'kendall', 'spearman'])
        # data = labled_df.select_dtypes(
            # include=np.number).corr(method=method).abs()
        # data.fillna(0, inplace=True)
        # fig, ax = plt.subplots()
        # sns.heatmap(data=data, vmin=0, vmax=1, annot=True, ax=ax)
        # fig.set_size_inches(8, 8)
        # st.pyplot(fig=fig)

        # figures["heatmap"] = fig_download_button(fig, name="heatmap")


# heatmap()
