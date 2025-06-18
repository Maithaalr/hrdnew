
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
        st.markdown("###  التحليلات البصرية")
        col3, _ = st.columns(2)
        with col3:
            if 'الدائرة' in df.columns:
                dept_counts = df['الدائرة'].value_counts()

                # النص داخل الدائرة: فقط اسم الدائرة
                text_values = dept_counts.index

                # النص في الشرح الجانبي (Legend): اسم الدائرة + العدد
                legend_labels = [f"{dept} | {count} موظف" for dept, count in zip(dept_counts.index, dept_counts.values)]

                fig_dept = go.Figure(data=[go.Pie(
                    labels=legend_labels,
                    values=dept_counts.values,
                    hole=0.4,
                    text=text_values,
                    textinfo='text+percent',
                    textposition='outside',
                    insidetextorientation='radial',
                    marker=dict(colors=px.colors.sequential.Blues[::-1])
                )])

                fig_dept.update_layout(
                    title='نسبة الموظفين حسب الدائرة',
                    title_x=0.5,
                    showlegend=True,
                    legend_font_size=12
                )

                st.plotly_chart(fig_dept, use_container_width=True)
