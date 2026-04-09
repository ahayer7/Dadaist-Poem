import random
import re
import streamlit as st


def extract_words(text):
    return re.findall(r"\S+", text)


def make_dadaist_text(
    words,
    min_words_per_line=1,
    max_words_per_line=8,
    randomize_range=False,
    absolute_max_random_line=20
):
    shuffled_words = words[:]
    random.shuffle(shuffled_words)

    if randomize_range:
        min_words_per_line = random.randint(1, max(1, min(10, len(shuffled_words))))
        max_upper_bound = max(min_words_per_line, min(absolute_max_random_line, len(shuffled_words)))
        max_words_per_line = random.randint(min_words_per_line, max_upper_bound)

    lines = []
    i = 0

    while i < len(shuffled_words):
        if randomize_range:
            current_min = random.randint(1, max(1, min(10, len(shuffled_words))))
            current_max = random.randint(
                current_min,
                max(current_min, min(absolute_max_random_line, len(shuffled_words)))
            )
            line_length = random.randint(current_min, current_max)
        else:
            line_length = random.randint(min_words_per_line, max_words_per_line)

        line_words = shuffled_words[i:i + line_length]
        lines.append(" ".join(line_words))
        i += line_length

    return "\n".join(lines)


st.title("Dada Text Generator")
st.write("Upload a text file and generate a Dadaist version of it.")

uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

randomize_range = st.checkbox("Fully randomize line lengths in Dada mode", value=True)

if not randomize_range:
    min_words = st.slider("Minimum words per line", 1, 10, 1)
    max_words = st.slider("Maximum words per line", min_words, 20, 8)
else:
    st.write("Line lengths will be randomized as much as possible for each generated poem.")
    min_words = 1
    max_words = 20

if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")
    words = extract_words(text)

    if words:
        dada_text = make_dadaist_text(
            words,
            min_words_per_line=min_words,
            max_words_per_line=max_words,
            randomize_range=randomize_range,
            absolute_max_random_line=20
        )

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