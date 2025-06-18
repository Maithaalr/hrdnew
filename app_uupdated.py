
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
from matplotlib import cm
import numpy as np

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

    with tab1:
        st.markdown("###  نظرة عامة للموظفين المواطنين فقط")
        df_citizens = df[df['الجنسية'] == 'إماراتية'].copy()
        total = df_citizens.shape[0]
        excluded_cols = ['رقم الأقامة', 'الكفيل', 'تاريخ اصدار اللإقامة', 'تاريخ انتهاء اللإقامة']
        df_citizens_checked = df_citizens.drop(columns=[col for col in excluded_cols if col in df_citizens.columns])
        complete = df_citizens_checked.dropna().shape[0]
        missing_total = total - complete
        complete_pct = round((complete / total) * 100, 1) if total else 0
        missing_pct = round((missing_total / total) * 100, 1) if total else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='metric-box' style='background-color:#1e3d59;'><h4> عدد المواطنين</h4><h2>{total}</h2></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-box' style='background-color:#2a4d6f;'><h4> السجلات المكتملة</h4><h2>{complete} ({complete_pct}%)</h2></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric-box' style='background-color:#4a7ca8;'><h4> السجلات الناقصة</h4><h2>{missing_total} ({missing_pct}%)</h2></div>", unsafe_allow_html=True)

        st.markdown("###  نظرة عامة للموظفين الوافدين فقط")
        df_non_citizens = df[df['الجنسية'] != 'إماراتية'].copy()
        total_non = df_non_citizens.shape[0]
        required_cols = ['رقم الأقامة', 'الكفيل', 'تاريخ اصدار اللإقامة', 'تاريخ انتهاء اللإقامة']
        present_required_cols = [col for col in required_cols if col in df_non_citizens.columns]
        is_complete = df_non_citizens[present_required_cols].notnull().all(axis=1)
        complete_non = is_complete.sum()
        missing_non = total_non - complete_non
        complete_non_pct = round((complete_non / total_non) * 100, 1) if total_non else 0
        missing_non_pct = round((missing_non / total_non) * 100, 1) if total_non else 0

        col4, col5, col6 = st.columns(3)
        with col4:
            st.markdown(f"<div class='metric-box' style='background-color:#1e3d59;'><h4> عدد الوافدين</h4><h2>{total_non}</h2></div>", unsafe_allow_html=True)
        with col5:
            st.markdown(f"<div class='metric-box' style='background-color:#2a4d6f;'><h4> السجلات المكتملة</h4><h2>{complete_non} ({complete_non_pct}%)</h2></div>", unsafe_allow_html=True)
        with col6:
            st.markdown(f"<div class='metric-box' style='background-color:#4a7ca8;'><h4> السجلات الناقصة</h4><h2>{missing_non} ({missing_non_pct}%)</h2></div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("###  التحليلات البصرية")
        col1, col2 = st.columns(2)
        with col1:
            if 'الجنس' in df.columns:
                gender_counts = df['الجنس'].value_counts().reset_index()
                gender_counts.columns = ['الجنس', 'العدد']
                fig_gender = px.bar(gender_counts, x='الجنس', y='العدد',
                                    color='الجنس',
                                    color_discrete_sequence=['#2F4156', '#567C8D'])
                fig_gender.update_layout(title='توزيع الموظفين حسب الجنس', title_x=0.5)
                st.plotly_chart(fig_gender, use_container_width=True)

        with col2:
            if 'الديانة' in df.columns:
                religion_counts = df['الديانة'].value_counts().reset_index()
                religion_counts.columns = ['الديانة', 'العدد']
                fig_religion = px.bar(religion_counts, x='الديانة', y='العدد',
                                      color='الديانة',
                                      color_discrete_sequence=['#2F4156', '#567C8D'])
                fig_religion.update_layout(title='توزيع الموظفين حسب الديانة', title_x=0.5)
                st.plotly_chart(fig_religion, use_container_width=True)

        col3, _ = st.columns(2)
        with col3:
            if 'الدائرة' in df.columns:
                dept_counts = df['الدائرة'].value_counts()
                sorted_depts = dept_counts.sort_values()
                normalized = (sorted_depts - sorted_depts.min()) / (sorted_depts.max() - sorted_depts.min())

                color_scale = cm.get_cmap('Blues')
                colors_custom = [
                    f"rgb{tuple((np.array(color_scale(val)[:3]) * 255).astype(int))}"
                    for val in normalized
                ]

                labels = [f"{dept} | {count} موظف" for dept, count in zip(sorted_depts.index, sorted_depts.values)]

                fig_dept = go.Figure(data=[go.Pie(
                    labels=labels,
                    values=sorted_depts.values,
                    hole=0.4,
                    marker=dict(colors=colors_custom),
                    textinfo='label+percent',
                    textposition='inside'
                )])
                fig_dept.update_layout(title='نسبة الموظفين حسب الدائرة', title_x=0.5)
                st.plotly_chart(fig_dept, use_container_width=True)
