import pandas as pd
import difflib
import pandas as pd
from konlpy.tag import Okt
import streamlit as st


#알고리즘 순서
# 1. 색채어 데이터와 입력문장의 단어들 간의 유사도 비교 -> 유사도 가장 높은 단어 쌍의 유사도가 0.5 이상이면 있다고 판단
#  1-1 색채어가 있을 경우, 바로 계열 확정 및 초기컬러 세팅
#  1-2 색채어가 없을 경우, 색을 연상시키는 단어 목록과 입력문장의 단어들 간의 의미적 유사도 비교 
#  1-3 색의 계열 확정 및 초기컬러 세팅
# 2. 이후, 명도/채도의 의미를 가질 수 있는 단어들과 입력문장 단어들 간의 의미적 유사도 비교 -> 기본 값에서 명도 조정


df_context_category = pd.read_csv('csv/color-context.csv')
df_color_adjective= pd.read_csv('csv/b-s-color-setting_value.csv')
df_saturation = pd.read_csv('csv/saturation.csv')
df_brightness = pd.read_csv('csv/brightness.csv')


def remove_stopwords(sentence):
    stopwords = ['하다', '다','게','이','를','을','가']
    okt=Okt()
    words = okt.morphs(sentence)
    words = [word for word in words if word not in stopwords]
    #print(words)
    return words

def categorize_color_context(user_input):
    #print("<문맥에 대한 색분류 모델>")
    best_match = ("","","",0)
    for user_word in user_input:
        for rows in df_context_category.itertuples():
            similarity = difflib.SequenceMatcher(None, user_word, rows.color).ratio()
            #if similarity > 0 :print(f"유사한 단어쌍: '{user_word}'-'{rows.color}'  색계열: '{rows.category}'  유사도: '{similarity}'")
            if similarity > best_match[3]:
                best_match = (user_word, rows.color, rows.category, similarity)
    return best_match

def saturation_context(user_input):
    #print("<문맥에 대한 채도 판단 모델>")
    best_match = ("","",0,0)
    for user_word in user_input:
        for rows in df_saturation.itertuples():
            similarity = difflib.SequenceMatcher(None, user_word, rows.word).ratio()
            #if similarity > 0 :print(f"유사한 단어쌍: '{user_word}'-'{rows.word}'  채도: '{rows.saturation}'  유사도: '{similarity}'")
            if similarity > best_match[3]:
                best_match = (user_word, rows.word, rows.saturation, similarity)
    return best_match

def brightness_context(user_input):
    #print("<문맥에 대한 명도 판단 모델>")
    best_match = ("","",0,0)
    for user_word in user_input:
        for rows in df_brightness.itertuples():
            similarity = difflib.SequenceMatcher(None, user_word, rows.word).ratio()
            #if similarity > 0 :print(f"유사한 단어쌍: '{user_word}'-'{rows.word}'  명도: '{rows.brightness}'  유사도: '{similarity}'")
            if similarity > best_match[3]:
                best_match = (user_word, rows.word, rows.brightness, similarity)
    return best_match  

def categorize_color_adjective(user_input):
    #print("<색채어에 대한 색분류 모델>")
    best_match = ("","","",0,0,0)
    for user_word in user_input:
        for rows in df_color_adjective.itertuples():
            similarity = difflib.SequenceMatcher(None, user_word, rows.color).ratio()
            #if similarity > 0 : print(f"유사한 단어쌍: '{user_word}'-'{rows.color}'  색계열: '{rows.category}'   유사도: '{similarity}'")
            if similarity > best_match[3]:
                best_match = (user_word, rows.color, rows.category, similarity, rows.saturation, rows.brightness)
    return best_match

def color_square(red, green, blue):
  html_code= f'<div style="width: 300px; height: 300px; background-color: rgb({red}, {green}, {blue});"></div>'
  return html_code


def context_main():
    ###################### 사용자 입력
    user_input = st.text_input("색을 연상시키는 문장을 입력해주세요: ")
    user_input = remove_stopwords(user_input)

    ###################### 입력 문장의 1차 색계열 분류(색채어가 없을 경우를 대비하여)
    best_match = categorize_color_context(user_input)
    #print(f"가장 유사한 단어쌍-전체: {best_match[0]} - {best_match[1]} 색의 계열: {best_match[2]} 유사도: {best_match[3]}")
    best_match_s = saturation_context(user_input)
    best_match_b = brightness_context(user_input)
    #print(f"가장 유사한 명도쌍: {best_match_s[0]} - {best_match_s[1]} 색의 계열: {best_match_s[2]} 유사도: {best_match_s[3]}")
    #print(f"가장 유사한 채도쌍: {best_match_b[0]} - {best_match_b[1]} 색의 계열: {best_match_b[2]} 유사도: {best_match_b[3]}")

    ###################### 입력 문장의 2차 색계열 분류(색채어가 있을 경우 색계열에 영향을 더 많이 끼치므로)
    best_match_color = categorize_color_adjective(user_input)
    #print(f"가장 유사한 단어쌍-색채어: {best_match_color[0]} - {best_match_color[1]} 색의 계열: {best_match_color[2]} 유사도: {best_match_color[3]}")
    
    if best_match_color[3] >= 0.5:
        input_category = best_match_color[2]
        brightness = best_match_color[4]
        saturation = best_match_color[5]
        #print(f"최종 명도: {brightness}")
        #print(f"최종 채도: {saturation}")
        if saturation < brightness:
            saturation = 0
        else:
            brightness = 0
    else:
        input_category = best_match[2]
        brightness = best_match_s[2]
        saturation = best_match_b[2]

    ########################### 계열, 명도, 채도 통합한 색 출력
    r = 0
    g = 0
    b = 0

    if input_category == '빨간계열':
        r = 255 - brightness
        g = saturation
        b = saturation
        #print(f"RGB({r},{g},{b})")
        if g < r:
            st.markdown(color_square(r, g, b), unsafe_allow_html=True)

        else:
            st.markdown(color_square(r, 0, 0), unsafe_allow_html=True)

    if input_category == '파란계열':
        r = saturation
        g = saturation
        b = 255 - brightness
        #print(f"RGB({r},{g},{b})")
        if g < b:
            st.markdown(color_square(r, g, b), unsafe_allow_html=True)
        else:
            st.markdown(color_square(0, 0, b), unsafe_allow_html=True)

    if input_category == '노란계열':
        r = 255 - brightness
        g = 238 - brightness
        b = saturation
        #print(f"RGB({r},{g},{b})")
        if b < g:
            st.markdown(color_square(r, g, 0), unsafe_allow_html=True)
