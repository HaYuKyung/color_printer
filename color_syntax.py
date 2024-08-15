{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 47,
   "id": "125fc8db-18e6-4cbb-8fba-d325b4061176",
   "metadata": {},
   "outputs": [
    {
     "name": "stdin",
     "output_type": "stream",
     "text": [
      "새로운 색채어를 입력하세요:  노르스름한 저녁 너울이\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "가장 유사한 단어쌍: 노르스름 - 누르스름, 유사도: 0.75\n",
      "Category: 노란계열\n",
      "Hex value: #c9c734\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<div style=\"width: 100px; height: 100px; background-color: #c9c734;\"></div>"
      ],
      "text/plain": [
       "<IPython.core.display.HTML object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "import pandas as pd\n",
    "import pandas as pd\n",
    "from IPython.display import HTML\n",
    "from difflib import get_close_matches\n",
    "from difflib import SequenceMatcher\n",
    "from konlpy.tag import Okt\n",
    "\n",
    "\n",
    "df = pd.read_csv('color-adjective.csv')\n",
    "\n",
    "def remove_stopwords(sentence):\n",
    "    stopwords = ['하다', '다','게','이','를','을','가']\n",
    "    okt=Okt()\n",
    "    words = okt.morphs(sentence)\n",
    "    words = [word for word in words if word not in stopwords]\n",
    "    #print(words)\n",
    "    return words\n",
    "\n",
    "def preprocess_color_words(color_words):\n",
    "    preprocessed_words = []\n",
    "    for word in color_words:\n",
    "        #print(word)\n",
    "        cleaned_word = ''.join(remove_stopwords(word))\n",
    "        preprocessed_words.append(cleaned_word)\n",
    "    return preprocessed_words\n",
    "\n",
    "def similarity_ratio(s1, s2):\n",
    "    return SequenceMatcher(None, s1, s2).ratio()\n",
    "\n",
    "def set_initial_value(user_input, color_words):\n",
    "    best_match = (\"\",\"\", 0)\n",
    "    for user_word in user_input:\n",
    "        for data_word in color_words:\n",
    "            similarity = similarity_ratio(user_word, data_word)\n",
    "            #print(f\"유사한 단어쌍: {user_word} - {data_word}, 유사도: {similarity}\")\n",
    "            if similarity > best_match[2]:\n",
    "                best_match = (user_word, data_word, similarity)\n",
    "    return best_match\n",
    "\n",
    "def color_square(hex_code):\n",
    "  html_code= f'<div style=\"width: 100px; height: 100px; background-color: {hex_code};\"></div>'\n",
    "  return html_code\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "###데이터 입력 및 전처리\n",
    "user_input = input(\"새로운 색채어를 입력하세요: \")\n",
    "user_input = remove_stopwords(user_input)\n",
    "color_words = df['color'].tolist()\n",
    "color_words = preprocess_color_words(color_words)\n",
    "#print(color_words)\n",
    "\n",
    "### 컬러 초기값 세팅\n",
    "best_match = set_initial_value(user_input, color_words)\n",
    "\n",
    "print(f\"가장 유사한 단어쌍: {best_match[0]} - {best_match[1]}, 유사도: {best_match[2]}\")\n",
    "\n",
    "color_words_row = df[df['color'] == best_match[1]]\n",
    "input_category = color_words_row['category'].values[0]\n",
    "input_hex = color_words_row['hex'].values[0]\n",
    "\n",
    "print(f\"Category: {input_category}\")\n",
    "print(f\"Hex value: {input_hex}\")\n",
    "display(HTML(color_square(input_hex)))"
   ]
  },
  {
   "cell_type": "raw",
   "id": "db122128-32f2-4269-b32a-fd226b6c10c4",
   "metadata": {},
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
