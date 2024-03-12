import streamlit as st
from PIL import Image
from werkzeug.utils import secure_filename
import os
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

# Configuration and Keyword Setup
app_title = 'Document Classification and Verification'
st.set_page_config(page_title=app_title)
upload_folder = 'uploads/'
results_folder = 'results/'
os.makedirs(upload_folder, exist_ok=True)
os.makedirs(results_folder, exist_ok=True)

# Keyword lists (same as in your Flask app)
olevel_keywords = ["ordinary level", "o level"] 
alevel_keywords = ["advanced subsidiary", "advanced Level"]
cnic_keywords = ["national identity card", "nadra", "cnic"]
ielts_keywords = ["international english language testing system", "ielts", "british council"]
sat_keywords = ["sat", "scholastic aptitude test", "college board"]

# Document classification function (same as in Flask)
def classify_document(text):
    text = text.lower()  # Normalize for case-insensitive matching

    if any(word in text for word in olevel_keywords):
        return "O Levels Certificate"
    elif any(word in text for word in alevel_keywords):
        return "A Levels Certificate"
    elif any(word in text for word in cnic_keywords):
        return "CNIC"
    elif any(word in text for word in ielts_keywords):
        return "IELTS Score Certificate"
    elif any(word in text for word in sat_keywords):
        return "SAT Certificate"
    else:
        return "Unknown Document Type"

# OCR Model Setup
model = ocr_predictor(pretrained=True) 

# Streamlit App Structure
st.title(app_title)

# Uploaders for each document type
uploaded_olevels = st.file_uploader("Upload O Levels Certificates", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
uploaded_alevels = st.file_uploader("Upload A Levels Certificates", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
uploaded_ielts = st.file_uploader("Upload IELTS Score Certificate", type=['png', 'jpg', 'jpeg'], accept_multiple_files=False)
uploaded_sat = st.file_uploader("Upload SAT Certificate", type=['png', 'jpg', 'jpeg'], accept_multiple_files=False)
uploaded_cnic = st.file_uploader("Upload CNIC", type=['png', 'jpg', 'jpeg'], accept_multiple_files=False)
uploaded_passport = st.file_uploader("Upload Passport", type=['png', 'jpg', 'jpeg'], accept_multiple_files=False)
name = st.text_input("Enter Name")
cnic = st.text_input("Enter CNIC")
passport_number = st.text_input("Enter Passport Number")

if st.button('Analyze'):
    results = []

    def process_document(uploaded_files, doc_type):
        for file in uploaded_files:
            filename = secure_filename(file.name)
            file_path = os.path.join(upload_folder, filename)

            # Save the image temporarily
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())

            # OCR using doctr
            img = DocumentFile.from_images(file_path)
            result = model(img)
            output = result.export()
            full_text = " ".join([obj3["value"] for obj1 in output['pages'][0]["blocks"] for obj2 in obj1["lines"] for obj3 in obj2["words"]])

            # Verification logic
            name_found = name.lower() in full_text.lower() if name else False
            cnic_found = any(word.lower() in full_text.lower() for word in cnic_keywords) if cnic else False
            passport_number_found = passport_number.lower() in full_text.lower() if passport_number else False
            found = name_found or cnic_found or passport_number_found

            # Results display
            result_info = []
            if name_found:
                result_info.append(f"Name found in:\n- {filename}")
            if cnic_found:
                result_info.append("CNIC found")
            if passport_number_found:
                result_info.append("Passport Number found")

            status = 'found' if found else 'not found'
            document_type = classify_document(full_text)
            results.append((filename, status, result_info, document_type))

        # Process uploaded documents
    if uploaded_olevels:
        process_document(uploaded_olevels, "O Levels Certificate")

    if uploaded_alevels:
        process_document(uploaded_alevels, "A Levels Certificate")

    if uploaded_ielts:
        process_document(uploaded_ielts, "IELTS Score Certificate")

    if uploaded_sat:
        process_document(uploaded_sat, "SAT Certificate")

    if uploaded_cnic:
        process_document(uploaded_cnic, "CNIC")

    if uploaded_passport:
        process_document(uploaded_passport, "Passport")

      # Display the results in Streamlit
    for filename, status, result_info, document_type in results:
        st.subheader(filename)
        st.write("Status:", status)
        st.write("Document Type:", document_type)
        if result_info:
            st.write("Additional Info:")
            for info in result_info:
                st.write(info)
