# Install necessary libraries
# pip install transformers streamlit

import streamlit as st
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load pre-trained T5 model and tokenizer
@st.cache_resource
def load_model():
    model_name = "t5-small"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()


# Function to summarize text
def summarize_text(text, max_length, num_beams, length_penalty):
    input_text = "summarize: " + text
    input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(
        input_ids,
        max_length=max_length,
        num_beams=num_beams,
        length_penalty=length_penalty,
        early_stopping=True,
    )
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# Streamlit UI
st.title("Text Summarization with T5")
st.write("Enter text below to get a summarized version.")

# Text input
text = st.text_area("Input Text", height=200)

with st.sidebar.expander("Model Parameters", expanded=True):
    max_length = st.slider("Max Summary Length", 10, 100, 50)
    num_beams = st.slider("Beam Search (Number of Beams)", 2, 10, 4)
    length_penalty = st.slider("Length Penalty", 0.5, 3.0, 2.0, step=0.1)

# Summarize button
if st.button("Summarize"):
    if text.strip():
        with st.spinner("Summarizing..."):
            summary = summarize_text(text, max_length, num_beams, length_penalty)
        st.subheader("Summary:")
        st.write(summary)
        # Option to download summary
        st.download_button("Download Summary", summary, file_name="summary.txt")
    else:
        st.warning("Please enter text to summarize.")

# Footer
st.markdown("""
---
Made by Ayush
""")
