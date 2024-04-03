import streamlit as st
import reveal_slides as rs

presentationContent = """
    ## Machine Learning Operations (MLOps)
    ---
    ## Introduction
    ---
    ### Introduction
    As a machine learning engineer, you know that building a model is only half the battle. The other half is deploying your model to a production environment, where it can serve predictions to real users or applications. <!-- .element: class="fragment" data-fragment-index="0" -->
    --
    This is not a trivial task, as you need to consider many aspects such as scalability, performance, reliability, integration, monitoring, and cost.
    ---
    ## What is MLOps?
    ---
    ### What is MLOps?
    MLOps stands for Machine Learning Operations. MLOps is a core function of Machine Learning engineering, focused on streamlining the process of taking machine learning models to production, and then maintaining and monitoring them. <!-- .element: class="fragment" data-fragment-index="0" -->
    --
    MLOps is a collaborative function, often comprising data scientists, devops engineers, and IT.
    ---
    ## What is the use of MLOps?
    ---
    ### What is the use of MLOps?
    MLOps is a useful approach for the creation and quality of machine learning and AI solutions. <!-- .element: class="fragment" data-fragment-index="0" -->
    --
    By adopting an MLOps approach, data scientists and machine learning engineers can collaborate and increase the pace of model development and production, by implementing continuous integration and deployment (CI/CD) practices with proper monitoring, validation, and governance of ML models.
    ---
    ## The benefits of MLOps
    ---
    ## Efficiency
    --
    MLOps allows data teams to achieve faster model development, deliver higher quality ML models, and faster deployment and production.
    ---
    ## Scalability
    --
    MLOps also enables vast scalability and management where thousands of models can be overseen, controlled, managed, and monitored for continuous integration, continuous delivery, and continuous deployment.
    ---
    ## Risk reduction
    --
    Machine learning models often need regulatory scrutiny and drift-check, and MLOps enables greater transparency and faster response to such requests and ensures greater compliance with an organization's or industry's policies.
    ---
    ## MLOps tools & frameworks
    ---
    ## TensorFlow Serving
    Tensorflow Serving is a powerful tool for serving high performance and low latency predictions. TensorFlow Serving makes it easy to deploy new algorithms and experiments, while keeping the same server architecture and APIs and it provides out-of-the-box integration with TensorFlow. <!-- .element: class="fragment" data-fragment-index="0" -->
    --
    ### Advantages
    - Seamless integration with TensorFlow models. <!-- .element: class="fragment" data-fragment-index="0" -->
    - Can serve different models or versions at the same time. <!-- .element: class="fragment" data-fragment-index="1" -->
    - Can batch inference requests to use GPU efficiently. <!-- .element: class="fragment" data-fragment-index="2" -->
    --
    ### Disadvantages
    - It is recommended to use Docker or Kubernetes to run in production which might not be compatible with existing platforms or infrastructures. <!-- .element: class="fragment" data-fragment-index="0" -->
    - It lacks support for features such as security, authentication, etc. <!-- .element: class="fragment" data-fragment-index="1" -->
    ---
    ## MLflow
    MLflow is an open source platform for managing the end-to-end machine learning lifecycle, including model development, tracking, deployment, and registry. You can use MLflow to deploy your models to various targets, such as local servers, cloud platforms, or Kubernetes clusters. <!-- .element: class="fragment" data-fragment-index="0" -->
    --
    ### Advantages
    - It supports a standard format for packaging models that can be used in different downstream tools, such as real-time serving through a REST API or batch inference on Apache Spark. <!-- .element: class="fragment" data-fragment-index="0" -->
    - It integrates with the MLflow Model Registry, which allows you to store, organize, and manage multiple versions of your models and promote them to different lifecycle stages, such as Staging and Production. <!-- .element: class="fragment" data-fragment-index="1" -->
    --
    ### Disadvantages
    - It doesn't provide a high-availability and scalable model server out-of-the-box. You need to use other tools or platforms to deploy your models as REST APIs or batch jobs. <!-- .element: class="fragment" data-fragment-index="0" -->
    - It doesn't support adaptive micro-batching, which can improve the throughput and latency of model inference. <!-- .element: class="fragment" data-fragment-index="1" -->
    ---
    ## Azure ML
    Azure ML is a cloud service that provides an enterprise-grade AI platform for the end-to-end machine learning lifecycle. It allows users to build, train, deploy, and manage machine learning models using various tools and frameworks. <!-- .element: class="fragment" data-fragment-index="0" -->
    --
    ### Advantages
    - It supports multiple development tools and frameworks, such as Python, R, PyTorch, TensorFlow, scikit-learn, and ONNX. <!-- .element: class="fragment" data-fragment-index="0" -->
    - It offers automated machine learning for tabular, text, and image models, which can help to create accurate models quickly and easily. <!-- .element: class="fragment" data-fragment-index="1" -->
    - It supports responsible AI to build explainable models using data-driven decisions for transparency and accountability. <!-- .element: class="fragment" data-fragment-index="2" -->
    --
    ### Disadvantages
    - Limited built-in algorithms: Azure ML has a number of algorithms and transformations built-in, but it does not cover all the possible techniques (e.g. XGBoost). <!-- .element: class="fragment" data-fragment-index="0" -->
    - Resource limits: Azure ML and Azure have some resource limits that can affect machine learning workloads, such as the number of endpoints, deployments, compute instances, cores, memory, etc. These limits vary by region, subscription type, etc. <!-- .element: class="fragment" data-fragment-index="1" -->
    ---
    ## Conclusion
    We're at a time when there is a boom in the MLOps industry. Every week you see new development, new startups, and new tools launching to solve the basic problem of converting notebooks into production-ready applications. <!-- .element: class="fragment" data-fragment-index="0" -->
    --
    Even existing tools are expanding the horizon and integrating new features to become super MLOps tools.
    ---
    ## Thank you!
"""

with st.sidebar:
    st.subheader("Slide Configuration")
    content_height = st.number_input("Content Height", value=900)
    content_width = st.number_input("Content Width", value=900)
    scale_range = st.slider("Scale Range", min_value=0.0, max_value=5.0, value=[0.1, 5.0], step=0.1)
    margin = st.slider("Margin", min_value=0.0, max_value=0.8, value=0.0, step=0.05)
    st.subheader("Initial State")
    hslidePos = st.number_input("Horizontal Slide Position", value=0)
    vslidePos = st.number_input("Vertical Slide Position", value=0)
    fragPos = st.number_input("Fragment Position", value=-1)
    overview = st.checkbox("Show Overview", value=False)
    paused = st.checkbox("Pause", value=False)

rs.slides(presentationContent, 
                    height=600, 
                    theme="night", 
                    config={
                            "width": content_width, 
                            "height": content_height, 
                            "minScale": scale_range[0], 
                            "maxScale": scale_range[1], 
                            "margin": margin, 
                            }, 
                    initial_state={
                                    "indexh": hslidePos, 
                                    "indexv": vslidePos, 
                                    "indexf": fragPos, 
                                    "paused": paused, 
                                    "overview": overview 
                                    }, 
                    markdown_props={"data-separator-vertical":"^--$"}, 
                    key="foo")
