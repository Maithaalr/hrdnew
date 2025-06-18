
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

st.set_page_config(page_title="لوحة معلومات الموارد البشرية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@500;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        background-color: #f5f8fc;
    }
    .metric-box {
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        color: white;
    }
    .section-header {
        font-size: 20px;
        color: #1e3d59;
        margin-top: 20px;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

col_logo, col_upload = st.columns([1, 3])

with col_logo:
    logo = Image.open("logo.png")
    st.image(logo, width=180)

with col_upload:
    st.markdown("<div class='section-header'>يرجى تحميل بيانات الموظفين</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("ارفع الملف", type=["xlsx"])

if uploaded_file:
    all_sheets = pd.read_excel(uploaded_file, sheet_name=None, header=0)
    selected_sheet = st.selectbox("اختر الجهة", list(all_sheets.keys()))
    df = all_sheets[selected_sheet]

    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.duplicated()]

    tab1, tab2, tab3, tab4 = st.tabs([" نظرة عامة", " تحليلات بصرية", " البيانات المفقودة", " عرض البيانات"])

    with tab2:
        st.markdown("### توزيع الموظفين حسب الجنس داخل كل دائرة")

        if 'الدائرة' in df.columns and 'الجنس' in df.columns:
            grouped = df.groupby(['الدائرة', 'الجنس']).size().reset_index(name='عدد')
            total_per_dept = grouped.groupby('الدائرة')['عدد'].transform('sum')
            grouped['النسبة'] = round((grouped['عدد'] / total_per_dept) * 100, 1)
            grouped['label'] = grouped.apply(lambda row: f"{row['عدد']} | {row['النسبة']}%", axis=1)

            fig_gender_per_dept = px.bar(
                grouped,
                x='الدائرة',
                y='عدد',
                color='الجنس',
                text='label',
                barmode='stack',
                color_discrete_sequence=['#2F4156', '#C8D9E6']  # أزرق غامق + أزرق فاتح
            )

            fig_gender_per_dept.update_layout(
                title='توزيع الموظفين حسب الجنس داخل كل دائرة',
                title_x=0.5,
                xaxis_tickangle=-45
            )

            fig_gender_per_dept.update_traces(
                textposition='inside',
                insidetextanchor='middle'
            )

            st.plotly_chart(fig_gender_per_dept, use_container_width=True)
