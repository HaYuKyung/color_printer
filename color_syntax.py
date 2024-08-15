import os
import pandas as pd
import streamlit as st
from difflib import get_close_matches
from difflib import SequenceMatcher
from konlpy.tag import Okt

st.title("언어의 감성")

file_path = os.path.join(os.path.dirname(__file__), "color-adjective.csv")
df = pd.read_csv(file_path)

def remove_stopwords(sentence):
    stopwords = ['하다', '다','게','이','를','을','가']
    okt=Okt()
    words = okt.morphs(sentence)
    words = [word for word in words if word not in stopwords]
    #print(words)
    return words

def preprocess_color_words(color_words):
    preprocessed_words = []
    for word in color_words:
        #print(word)
        cleaned_word = ''.join(remove_stopwords(word))
        preprocessed_words.append(cleaned_word)
    return preprocessed_words

def similarity_ratio(s1, s2):
    return SequenceMatcher(None, s1, s2).ratio()

def set_initial_value(user_input, color_words):
    best_match = ("","", 0)
    for user_word in user_input:
        for data_word in color_words:
            similarity = similarity_ratio(user_word, data_word)
            #print(f"유사한 단어쌍: {user_word} - {data_word}, 유사도: {similarity}")
            if similarity > best_match[2]:
                best_match = (user_word, data_word, similarity)
    return best_match

def color_square(hex_code):
  html_code = f'''
  <div style="width: 100px; height: 100px; background-color: {hex_code};"></div>
  '''
  return html_code




###데이터 입력 및 전처리
user_input = st.text_input("문장을 입력하세요: ")
user_input = remove_stopwords(user_input)
color_words = df['color'].tolist()
color_words = preprocess_color_words(color_words)
#print(color_words)

### 컬러 초기값 세팅
best_match = set_initial_value(user_input, color_words)

color_words_row = df[df['color'] == best_match[1]]

if not color_words_row.empty:
    input_category = color_words_row['category'].values[0]
    input_hex = color_words_row['hex'].values[0]
    st.write(f"가장 유사한 단어쌍: {best_match[0]} - {best_match[1]}, 유사도: {best_match[2]}")
    st.write(f"Category: {input_category}")
    st.write(f"Hex value: {input_hex}")
    st.markdown(color_square(input_hex), unsafe_allow_html=True)

