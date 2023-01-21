import streamlit as st
from streamlit_option_menu import option_menu
import pickle, warnings, numpy as np, os, time, glob
warnings.filterwarnings('ignore')
from gtts import gTTS
from googletrans import Translator

# streamlit run 'C:\Users\91898\Desktop\streamtest\streamenv\stream_main.py'
#  #  pip install googletrans==3.1.0a0
#  ## pip install googletrans==4.0.0-rc1

#  #  Book Recommendation module
popular_df = pickle.load(open(r'E:\Recommendation_App\popular.pkl', 'rb'))
pt = pickle.load(open(r'E:\Recommendation_App\pt.pkl', 'rb'))
books = pickle.load(open(r'E:\Recommendation_App\books.pkl', 'rb'))
similarity_scores = pickle.load(open(r'E:\Recommendation_App\similarity_scores.pkl', 'rb'))

# book_name = list(popular_df['Book-Title'].values)
# author = list(popular_df['Book-Author'].values)
# image = list(popular_df['Image-URL-M'].values)
# votes = list(popular_df['num_ratings'].values)
# rating = list(popular_df['avg_rating'].astype(int).values)

# # loading the save Dengue models with help of pickle
loaded_model = pickle.load(open(r'C:\Users\91898\Documents\jupyter_not_proj\finalized_model.pkl', 'rb'))

with open("whisper_mdl.pkl", "rb") as f:   # pkl model for mp3, mp4, wav to text converter
    wsp_res = pickle.load(f)

with st.sidebar:    # sidebar for navigation
        selected = option_menu('Recommendation & Dengue Disease Prediction System',
    ['Dengue Disease', 'Book Recommend', 'Translation & Mp3_Mp4 To Text '],
        icons=['activity', 'book', 'play'], menu_icon="cast",
        default_index=2)  # orientation="horizontal"

if selected == 'Dengue Disease':     # setup page prediction
    st.title('Dengue Disease Prediction by ML')  # page title
    col1, col2, col3 = st.columns(3)        # columns for input fields
    with col1:
        AGE = st.number_input('Age')         # Getting the data from user input
    with col2:
        Temp = st.number_input('Temperature')
    with col3:
        RBC = st.number_input('RBC')
    with col1:
        Hmgbn = st.number_input('Hemoglobin')
    with col2:
        Leukocyte = st.number_input('Leukocyte_Test')
    with col3:
        Platelet = st.number_input('Platelet_Count')
    with col1:
        SGOT = st.number_input('SGOT_Level')
    with col2:
        SGPT = st.number_input('SGPT_Level')


    dengue_diagnosis = ''
    if st.button('Dengue Patient Result'):     # create button for prediction streamlit
        dengue_prediction = loaded_model.predict([[AGE, Temp, RBC, Hmgbn, Leukocyte, Platelet, SGOT, SGPT]])
        if dengue_prediction[0] == 1:
            dengue_diagnosis = 'The Person have a Dengue.'
        else:
            'The Person have not a Dengue.'
    st.success(dengue_diagnosis)

if selected == 'Book Recommend':
    st.title('Book Recommendation Prediction by ML')  # page title
    st.subheader('Enter Your Book Name Bellow')
    # colourful text
    # success
    col1, col2 = st.columns(2)
    with col1:
        Name = st.text_input('Book Name')
    res = ''
    # create button for prediction streamlit
    if st.button('Search Book Name'):
        user_input = Name   # user_input
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

        data=[]
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            data.append(item)

        bookname = []
        bookrating = []
        for i in similar_items:
            item1 = []
            temp_df1 = books[books['Book-Title'] == pt.index[i[0]]]
            item1.extend(list(temp_df1.drop_duplicates('Book-Title')['Book-Title'].values))
            bookname.append(item1)

        col1, col2 = st.columns(2)
        st.success('Similar BooK Recommended by System')
        with col1:
            st.text_input('BOOK NAME', bookname[0])
        with col2:
            st.text_input('BOOK NAME', bookname[1])
        with col1:
            st.text_input('BOOK NAME', bookname[2])
        with col2:
            st.text_input('BOOK NAME', bookname[3])
        with col1:
            st.text_input('BOOK NAME', bookname[4])
        res = data

        ds = []
        for i in range(0, len(data[0]), 3):
            ds.append(data[0][i])
        for i in range(0, len(data[1]), 3):
            ds.append(data[1][i])
        for i in range(0, len(data[2]), 3):
            ds.append(data[2][i])
        for i in range(0, len(data[3]), 3):
            ds.append(data[3][i])
        for i in range(0, len(data[4]), 3):
            ds.append(data[4][i])
        # Manually Adjust the width of the image as per requirement
        images = [ds[0], ds[1], ds[2], ds[3], ds[4]]
        st.image(images, width=180, caption=['App Recommend Book'] * len(images))  # use_column_width=400
        st.success(res)
    #   book name for test - 1st to Die: A Novel     2nd Chance    4 Blondes

if selected == 'Translation & Mp3_Mp4 To Text ':
    st.title('Translation & Mp3_Mp4 To Text ')  # page title
    try:
        os.mkdir("temp")
    except:
        pass
    # st.title("Text to speech")
    translator = Translator()
    text = st.text_input("Enter text")
    in_lang = st.selectbox("Select your input language",
                           ("English", "Hindi", "Bengali", "korean", "Chinese", "Japanese"),
                           )
    if in_lang == "English":
        input_language = "en"
    elif in_lang == "Hindi":
        input_language = "hi"
    elif in_lang == "Tamil":
        input_language = "ta"
    elif in_lang == "Bengali":
        input_language = "ba"
    elif in_lang == "Chinese":
        input_language = "zh-cn"
    elif in_lang == "Japanese":
        input_language = "ja"

    out_lang = st.selectbox("Select your output language",
                            ("English", "Hindi", "Bengali", "korean", "Chinese", "Japanese"), )
    if out_lang == "English":
        output_language = "en"
    elif out_lang == "Hindi":
        output_language = "hi"
    elif out_lang == "Tamil":
        output_language = "ta"
    elif out_lang == "Bengali":
        output_language = "ba"
    elif out_lang == "Chinese":
        output_language = "zh-cn"
    elif out_lang == "Japanese":
        output_language = "ja"

    display_output_text = st.checkbox("Display output text")

    # if st.button('Play Translate Audio'):
    def text_to_speech(input_language, output_language, text):
        translation = translator.translate(text, src=input_language, dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language, slow=False)
        try:
            my_file_name = text[0:20]
        except:
            my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, trans_text


    if st.button("Translate"):
        result, output_text = text_to_speech(input_language, output_language, text)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.success(f"## Your audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        if display_output_text:
            st.success(f"## Output text:")
            st.write(f" {output_text}")

    def remove_files(n):
        mp3_files = glob.glob("temp/*mp3")
        if len(mp3_files) != 0:
            now = time.time()
            n_days = n * 86400
            for f in mp3_files:
                if os.stat(f).st_mtime < now - n_days:
                    os.remove(f)
                    print("Deleted ", f)

    remove_files(7)
    st.subheader('MP3/VIDEO TO TEXT ')
    col1, col2 = st.columns(2)
    out = ''
    with col1:      # select box
        path_ = st.text_input("Past the File Path Here: ")
        if st.button('Convert As Text'):
            res = wsp_res.transcribe(path_, fp16=False, language='English')
            out = res['text']
            st.success(out)
    with col1:
        f = st.file_uploader("Upload a file", type=(["mp3", "mp4", "wav", 'avi']))
        if f is not None:
            path_in = f.name
        else:
            path_in = None

    if st.button('File Translate As Text'):
        res = wsp_res.transcribe(path_in, fp16=False, language='English')
        out = res['text']
        st.success(out)  # create button for prediction streamlit

