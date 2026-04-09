import random
import re
import streamlit as st


def extract_words(text):
    return re.findall(r"\S+", text)


def make_dadaist_text(words, min_words_per_line=1, max_words_per_line=8, seed=None):
    if seed is not None:
        random.seed(seed)

    shuffled_words = words[:]
    random.shuffle(shuffled_words)

    lines = []
    i = 0
    while i < len(shuffled_words):
        line_length = random.randint(min_words_per_line, max_words_per_line)
        line_words = shuffled_words[i:i + line_length]
        lines.append(" ".join(line_words))
        i += line_length

    return "\n".join(lines)


st.title("Dada Text Generator")
st.write("Upload a text file and generate a Dadaist version of it.")

uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

min_words = st.slider("Minimum words per line", 1, 10, 1)
max_words = st.slider("Maximum words per line", 1, 15, 8)
seed_input = st.text_input("Optional seed for repeatable output", "")

if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")
    words = extract_words(text)

    if words:
        seed = int(seed_input) if seed_input.strip().isdigit() else None
        dada_text = make_dadaist_text(words, min_words, max_words, seed)

        st.subheader("Generated Dada Text")
        st.text(dada_text)

        st.download_button(
            label="Download Dada Text",
            data=dada_text,
            file_name="dada_output.txt",
            mime="text/plain"
        )
    else:
        st.error("The uploaded file has no readable words.")