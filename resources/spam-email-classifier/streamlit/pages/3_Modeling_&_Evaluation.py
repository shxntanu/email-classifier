import streamlit as st
import numpy as np
import json
from utils import load_data, load_model, plot_confusion_matrix, plot_calibration_graphs, display_metrics, display_model_info, collect_model_params, preprocess_text


#Shortcut to display items in the sidebar
sb = st.sidebar

# choosing the algorithms
model_choice = sb.radio(
    "Choose a semi-supervised learning algorithm",
    ["Self Training", "Label Propagation", "Label Spreading"],
)

model_name = ""
model = None

# Process model choice
if model_choice == "Label Propagation":
    display_model_info(
        "Label Propagation",
        """
        Label Propagation is a semi-supervised learning algorithm that assigns labels to previously unlabeled data points. It does this by propagating the labels of known data points to unknown data points. The algorithm works by modeling the data as a graph and using the graph to predict the labels of unknown data points.
        
        The algorithm has a few hyperparameters that can be tuned. The kernel hyperparameter is used to determine the similarity between data points. The vectorizer hyperparameter is used to convert the text data into a format that can be used by the algorithm. The truncated svd hyperparameter is used to reduce the dimensionality of the data.
    """,
    )

    params = collect_model_params()
    model_name = (
        f"lp_{params['vectorizer']}_{params['kernel']}{params['truncated_svd']}"
    )
    lp_evaluation = load_data("data/lp_evaluation_df.csv")

elif model_choice == "Label Spreading":
    display_model_info(
        "Label Spreading",
        """
        Label Spreading is a semi-supervised learning algorithm that assigns labels to previously unlabeled data points. It does this by propagating the labels of known data points to unknown data points. The algorithm works by modeling the data as a graph and using the graph to predict the labels of unknown data points.
        
        The algorithm has a few hyperparameters that can be tuned. The kernel hyperparameter is used to determine the similarity between data points. The vectorizer hyperparameter is used to convert the text data into a format that can be used by the algorithm. The truncated svd hyperparameter is used to reduce the dimensionality of the data.
    """,
    )

    params = collect_model_params()
    model_name = (
        f"ls_{params['vectorizer']}_{params['kernel']}{params['truncated_svd']}"
    )
    ls_evaluation = load_data("data/ls_evaluation_df.csv")

elif model_choice == "Self Training":
    display_model_info(
        "Self Training",
        """
        Self Training is a semi-supervised learning algorithm that assigns labels to previously unlabeled data points. It does this by training a supervised learning model on the labeled data and using the model to predict the labels of unknown data points. The algorithm works by modeling the data as a graph and using the graph to predict the labels of unknown data points.
        
        The algorithm has only one hyperparameter that can be tuned. The base estimator hyperparameter is used to determine the supervised learning model that is used to predict the labels of unknown data points. The base estimator can be any supervised learning model, such as logistic regression, support vector machine, or naive bayes.
    """,
    )

    base_estimator = sb.selectbox(
        "Base Estimator",
        ["Logistic Regression", "SGD Classifier", "Naive Bayes", "SVM"],
    )

    param = (
        "lr"
        if base_estimator == "Logistic Regression"
        else (
            "sgd"
            if base_estimator == "SGD Classifier"
            else "nb" if base_estimator == "Naive Bayes" else "svm"
        )
    )

    model_name = f"st_{param}"
    st_evaluation = load_data("data/st_evaluation_df.csv")

# button to evaluate the model
sb.write("Click the button below to train the model")

#store the evaluation button in session state so that streamlit can remember the state of the button
#this is used so that the evaluation button is not reset when the user clicks on the predict button (items in the main page disappear when the user clicks on the predict button)
if "evaluation_button" not in st.session_state:
    st.session_state.evaluation_button = False

def callback():
    st.session_state.evaluation_button = True

if sb.button("Evaluate Model", type="primary", on_click=callback) or st.session_state.evaluation_button:
    # Loading the model
    model = load_model('models/'+model_name+'_model.joblib')
    if model_choice == "Label Propagation":
        evaluation_table = lp_evaluation
    elif model_choice == "Label Spreading":
        evaluation_table = ls_evaluation
    elif model_choice == "Self Training":
        evaluation_table = st_evaluation
        #calibration plot
        st.markdown("## Calibration Plot")
        plot_calibration_graphs(param)

    row = evaluation_table[evaluation_table["Unnamed: 0"] == model_name]
    two_d_array = json.loads(row["Confusion Matrix"].values[0])
    st.markdown("## Confusion Matrix")

    plot_confusion_matrix(np.array(two_d_array))

    metrics = {
        "Accuracy": row["accuracy_score"].values[0],
        "Precision": row["precision_score"].values[0],
        "Recall": row["recall_score"].values[0],
        "F1 Score": row["f1_score"].values[0],
    }

    st.markdown("## Model Metrics")
    display_metrics(metrics)
    #add input for making predictions
    st.markdown("## Make Predictions")
    text = st.text_area("Enter text to make predictions", "Enter the email text here")
    if st.button("Predict"):
        email_text = preprocess_text(text)
        prediction = model.predict([email_text])
        is_spam = bool(prediction[0])
        st.write(f"The email is {'spam' if is_spam else 'not spam'}")