import streamlit as st
import requests
from cryptography.fernet import Fernet
import json

heirarchy = json.loads(open('data/bigrag.json').read())

def encrypt_text(key, text):
    cipher_suite = Fernet(key)
    encrypted_text = cipher_suite.encrypt(text.encode())
    return encrypted_text.decode()


st.title('📥 Email Classifier -- Yarn Dev')
st.write('Enter the email and body of your email, and you will get the Deparment ID of where the email should be routed.')

body = st.text_area('Email Content')

if st.button('Submit'):
    st.session_state['body'] = body
    st.write(body)

    data = {
        "content": st.session_state['body']
    }

    headers = {
        'Content-Type': 'application/json'
    }

    url = 'http://192.168.45.165:9000/bigclassify'

    response = requests.post('http://192.168.45.165:9000/bigc÷lassify', data={"content" : st.session_state['body']}, headers={"Content-Type": "application/json"})
    response = requests.post(url, data = json.dumps(data), headers=headers)
    st.write(response.status_code)
    d = response.json()
    print("D: ", d)
    val = 0
    for node in heirarchy["nodes"]:
        if "id" in node and node["id"] == d["team"]:
            val = node["name"]

    st.text_area('Response', value=val, height=200)
    print(response.text)

    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_text = cipher_suite.encrypt(response.text.encode())
    st.text_area('Encrypted Text', value=encrypted_text.decode(), height=200)

    # encrypted_text =   # Replace this with your encryption logic
    # st.text_area('Encrypted Text', value=encrypted_text, height=200)
    # st.text_area('Decrypted Text', value=encrypt_text(encrypted_text), height=200)
