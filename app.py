import streamlit as st
from color_context import remove_stopwords
from color_context import categorize_color_context
from color_context import saturation_context
from color_context import brightness_context
from color_context import categorize_color_adjective
from color_context import color_square
from color_context import context_main
from color_syntax import remove_stopwords
from color_syntax import preprocess_color_words
from color_syntax import similarity_ratio
from color_syntax import set_initial_value
from color_syntax import color_square
from color_syntax import syntax_main



st. header('언어의 감성 융프팀입니다')

tab1, tab2 = st.tabs(['syntax_color', 'context_color'])

with tab1:
    #st.subheader("문법적 특성으로 결정되는 색채어의 색을 알아보세요!")
    syntax_main()

with tab2:
    #st.subheader("맥락을 반영한 문장의 색을 알아보세요!")
    context_main()
