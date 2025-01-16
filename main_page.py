import streamlit as st
from functions import *
import json
from openai import OpenAI
with st.sidebar:
    api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    if api_key:
        client = OpenAI(api_key=api_key)

uploaded_file = st.file_uploader("Upload a Word Document", type=["docx"])
# text_input = st.text_area('Or use JSON string as input',key="text_input")
if uploaded_file:
    submit = st.button('Send prompt')
    if submit:
        contents = convert_docx_to_text(uploaded_file)
        if not api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
        response = askGPT_fine_turned(contents,client)
        st.subheader("Response:", divider=True)
        st.code(json.dumps(response),language="json")
        st.title('Demo survey created from JSON')
        questions = response['pages'][0]['questions']
        with st.form("form",border = False):
            for idx,question in enumerate(questions):
                with st.container(border = True):
                    st.write(question['question'])
                    options = question['options']
                    if question['type'] == "checkbox":
                        num = 0
                        for i in options:
                            st.checkbox(i,key="check_box_" + str(idx) + "_" + str(num))
                            num += 1
                    elif "radio" in question['type']:
                        st.radio('',options,key="radio_" + str(idx))
                    elif question['type'] == "number":
                        st.number_input('',min_value = question['min'] or 0, max_value= question['max'] or 99)
                    elif question['type'] == "text":
                        st.text_input('',key = "text_input_"+ str(idx))
            st.form_submit_button()


# if text_input:
#     submit = st.button('Send prompt',key='submit_2')
#     if submit:
#         response = json.loads(text_input)
#         questions = response['pages'][0]['questions']

#         with st.form("form",border = False):
#             for idx,question in enumerate(questions):
#                 with st.container(border = True):
#                     st.write(question['question'])
#                     options = question['options']
#                     if question['type'] == "checkbox":
#                         num = 0
#                         for i in options:
#                             st.checkbox(i,key="check_box_" + str(idx) + "_" + str(num))
#                             num += 1
#                     elif "radio" in question['type']:
#                         st.radio('',options,key="radio_" + str(idx))
#                     elif question['type'] == "number":
#                         st.number_input('',min_value = question['min'] or 0, max_value= question['max'] or 99)
#                     elif question['type'] == "text":
#                         st.text_input('',key = "text_input_"+ str(idx))

#             st.form_submit_button()