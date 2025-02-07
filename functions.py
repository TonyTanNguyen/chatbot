# import subprocess 


# def read_word_with_pandoc(file_path, output_format="plain"):
#     """
#     Reads a Word file using Pandoc and converts it to the specified format.

#     :param file_path: Path to the Word file.
#     :param output_format: Format to convert to (e.g., "markdown", "plain", "json").
#     :return: The converted content as a string.
#     """
#     try:
#         result = subprocess.run(
#             ["pandoc", file_path, "-t", output_format],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )
        
#         if result.returncode != 0:
#             raise Exception(f"Error: {result.stderr}")
        
#         return result.stdout
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None
    
import pypandoc
import json
import streamlit as st
import tempfile
# Load environment variables from .env file
from pypandoc.pandoc_download import download_pandoc
def convert_docx_to_text(file):
    """Convert a docx file to plain text using Pandoc."""
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
        temp_file.write(file.read())
        temp_file_path = temp_file.name

    # Convert the document to plain text using pypandoc
    try:
        converted_text = pypandoc.convert_file(temp_file_path, 'plain')
        return converted_text
    except Exception as e:
        st.error(f"An error occurred while converting the file: {e}")


def askGPT_fine_turned(content,client):
    system_message = "You are survey scripting converter, who can read plain text and convert question/options into JSON format."
    completion = client.chat.completions.create(
    model="ft:gpt-4o-2024-08-06:tgm-research::AqXfZUqf",
    # response_format={"type":"json_object"},
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": content}],
    )
    status = completion.choices[0].finish_reason
    if status == "stop":
        data = completion.choices[0].message.content

        json_obj = json.loads(data)
        return json_obj
    else:
        print('Error! Please re-generate or check your input.')
        return False
    


def checkbox(st,options):
    return [st.checkbox(option) for option in options]

def radio(st,options):
    return st.radio('',options)
