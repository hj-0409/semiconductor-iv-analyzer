import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("⚡ MOSFET I-V Characterization Analyzer")
st.write("CSV 파일을 업로드하여 I-V 커브를 확인하세요.")

uploaded_file = st.file_uploader("I-V 데이터 CSV 업로드", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head())
    
    fig, ax = plt.subplots()
    ax.plot(df.iloc[:, 0], df.iloc[:, 1], marker='o')
    ax.set_xlabel("Vgs")
    ax.set_ylabel("Id")
    st.pyplot(fig)