import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
import string
import re
import plotly.graph_objects as go
from joblib import load

# shortcut
sb = st.sidebar

# @st.cache_data
def load_data(path):
    data = pd.read_csv(path, sep=";")
    return data


# @st.cache_data
def load_model(path):
    return load(path)

def preprocess_text(text):
    #pre-processing
    stop_words = set(nltk.corpus.stopwords.words("english"))
    spetial_chars = set(string.printable) - set(string.ascii_letters) - set(" ")
    escaped_chars = [re.escape(c) for c in spetial_chars]
    regex = re.compile(f"({'|'.join(escaped_chars)})")
    stemmer = nltk.stem.porter.PorterStemmer()
    url_regex = re.compile("(?P<url>https?://[^\s]+)")

    # capitalization
    text = text.lower()

    # remove urls
    text = re.sub(url_regex," ",text)
    
    # tokenization
    text = nltk.word_tokenize(text, language='english')
        
    # stop words removal
    text = [word for word in text if word not in stop_words]
    
    # noise removal
    text = [word for word in text if word.isalpha()]
    
    # stemming
    text = [stemmer.stem(word) for word in text]
    
    return ' '.join(text)

def plot_calibration_graphs(model):
    
    #load the calibration file
    calibration = load_model("data/calibration.joblib")

    fig, ax = plt.subplots()
    fig.set_size_inches(5,5)

    calibration[model].plot(ax = ax)

    st.pyplot(fig)


def plot_confusion_matrix(conf_matrix):
    fig = go.Figure(
        data=go.Heatmap(z=conf_matrix, colorscale="Blues", colorbar=dict(title="Count"))
    )

    fig.update_layout(
        xaxis=dict(title="Predicted label"),
        yaxis=dict(title="True label"),
        annotations=[
            dict(
                text=str(conf_matrix[i, j]),
                x=j,
                y=conf_matrix.shape[0] - 1 - i,  # Reverse the row index
                font=dict(color="black"),
                showarrow=False,
            )
            for i in range(conf_matrix.shape[0])
            for j in range(conf_matrix.shape[1])
        ],
    )
    st.plotly_chart(fig)


def display_metrics(metrics):
    # function to display metric with progress bar
    def display_metric_with_progress(name, value):
        st.write(f"{name}: {value:.2f}%")
        st.progress(int(value * 100))

    # change color of progress bar
    st.markdown(
        """
        <style>
            .stProgress > div > div > div > div {
                background-color: white;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Display metrics
    for metric_name, metric_value in metrics.items():
        display_metric_with_progress(metric_name, metric_value)


# Common function to display model information
def display_model_info(model_name, description):
    st.markdown(f"# {model_name}")
    st.write(description)

# Common function to collect model parameters
def collect_model_params():
    kernel = sb.selectbox(
        "Kernel", ["K-Nearest Neighbor (KNN)", "Radial basis function (RBF)"]
    )
    vectorizer = sb.selectbox(
        "Vectorizer",
        [
            "Term Frequency-Inverse Document Frequency (TF-IDF)",
            "Bag of Words (Count Vectorizer)",
        ],
    )
    truncated_svd = sb.checkbox("Truncated SVD")

    params = {
        "kernel": "knn" if kernel == "K-Nearest Neighbor (KNN)" else "rbf",
        "vectorizer": "cv" if vectorizer == "Count" else "tfid",
        "truncated_svd": "_svd" if truncated_svd else "",
    }

    return params
