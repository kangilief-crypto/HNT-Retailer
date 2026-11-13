import html
import re
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import streamlit as st


# =========================================================
# 1. 페이지 기본 설정
# =========================================================

st.set_page_config(
    page_title="유통점 업무 인수인계",
    page_icon="🛍️",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent

MAIN_FILE = BASE_DIR / "통합문서1.xlsx"
HOMEPLUS_FILE = BASE_DIR / "홈플러스 기업회생 절차.xlsx"

PURPLE = "#5E2BB8"
MINT = "#08D1D9"


# =========================================================
# 2. 화면 디자인
# =========================================================

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 1500px;
        }

        .dashboard-header {
            background: #5E2BB8;
            border-radius: 12px;
            padding: 26px 30px;
            color: white;
            margin-bottom: 22px;
        }

        .dashboard-header h1 {
            color: white !important;
            margin: 0 !important;
            font-size: 28px !important;
            font-weight: 800 !important;
        }

        .dashboard-header p {
            color: #E8DFFF !important;
            margin: 8px 0 0 0 !important;
            font-size: 13px !important;
        }

        .section-title {
            border-left: 5px solid #08D1D9;
            padding-left: 12px;
            margin: 24px 0 12px 0;
            font-size: 19px;
            font-weight: 800;
            color: #252135;
        }

        .info-box {
            background: #F5F1FF;
            border-left: 4px solid #5E2BB8;
            border-radius: 6px;
            padding: 14px 18px;
            margin: 10px 0 18px 0;
            color: #373047;
            line-height: 1.7;
            font-size: 14px;
        }

        .step-box {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 10px;
            padding: 18px 20px;
            margin-bottom: 12px;
        }

        .step-box h4 {
            color: #5E2BB8;
            margin: 0 0 10px 0;
        }

        .step-box ol {
            margin: 0;
            padding-left: 20px;
            line-height: 1.9;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 5px;
            background: #F3F4F6;
            padding: 6px;
            border-radius: 10px;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 6px;
            padding: 10px 14px;
        }

        .stTabs [aria-selected="true"] {
            background: #5E2BB8 !important;
        }

        .stTabs [aria-selected="true"] p {
            color: white !important;
            font-weight: 700 !important;
        }

        .table-scroll {
            width: 100%;
            overflow-x: auto;
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            margin: 10px 0 18px 0;
        }

        .hana-table {
            border-collapse: collapse;
            width: 100%;
            min-width: 700px;
            font-size: 13px;
            background: white;
        }

        .hana-table th {
            background: #F4F0FB;
            color: #342250;
            font-weight: 700;
            text-align: center;
            padding: 10px 12px;
            border: 1px solid #E5E7EB;
            white-space: nowrap;
        }

        .hana-table td {
            padding: 9px 12px;
            border: 1px solid #E5E7EB;
            vertical-align: top;
            line-height: 1.6;
            white-space: pre-wrap;
            overflow-wrap: anywhere;
            color: #242424;
        }

        .hana-table td.text {
            text-align: left;
        }

        .hana-table td.number {
            text-align: right;
            white-space: nowrap;
        }

        .hana-table tr:nth-child(even) td {
            background: #FAFAFC;
        }

        .footer-note {
            border-top: 1px solid #E5E7EB;
            margin-top: 30px;
            padding-top: 12px;
            color: #777777;
            font-size: 12px;
            text-align: right;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 3. 공통 함수
# =========================================================

def section_title(title):
    """섹션 제목을 표시합니다."""
    safe_title = html.escape(str(title))
    st.markdown(
        f'<div class="section-title">{safe_title}</div>',
        unsafe_allow_html=True,
    )


def info_box(message):
    """안내 문구를 표시합니다."""
    safe_message = html.escape(str(message)).replace("\n", "<br>")
    st.markdown(
        f'<div class="info-box">{safe_message}</div>',
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def read_excel_sheet(file_path, sheet_name, header_row, modified_time):
    """
    엑셀 시트를 읽습니다.

    modified_time을 함께 전달하여 파일이 수정되면
    캐시를 다시 읽도록 합니다.
    """
    return pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        header=header_row,
        engine="openpyxl",
    )


def load_sheet(file_path, sheet_name, header_row=0):
    """파일과 시트가 존재하는지 확인한 후 읽습니다."""
    if not file_path.exists():
        st.warning(
            f"파일을 찾을 수 없습니다: {file_path.name}\n\n"
            "app.py와 같은 위치에 파일을 넣어주세요."
        )
        return None

    try:
        modified_time = file_path.stat().st_mtime_ns

        df = read_excel_sheet(
            str(file_path),
            sheet_name,
            header_row,
            modified_time,
        )

        return df

    except ImportError:
        st.error(
            "엑셀을 읽는 데 필요한 openpyxl을 불러오지 못했습니다. "
            "requirements.txt에 openpyxl이 있는지 확인해주세요."
        )
        return None

    except ValueError as exc:
        st.error(
            f"'{file_path.name}'에서 '{sheet_name}' 시트를 "
            f"읽지 못했습니다. 시트 이름을 확인해주세요.\n\n{exc}"
        )
        return None

    except Exception as exc:
        st.error(
            f"'{file_path.name}' 파일을 읽는 중 오류가 발생했습니다.\n\n"
            f"{type(exc).__name__}: {exc}"
        )
        return None


def clean_dataframe(df):
    """
    완전히 비어 있는 행과 열을 제거하고,
    이름 없는 열은 화면에서 알아보기 쉽게 표시합니다.
    """
    if df is None:
        return None

    df = df.copy()

    # 내용이 없는 문자열도 빈 값으로 처리합니다.
    df = df.replace(r"^\s*$", pd.NA, regex=True)
    df = df.dropna(how="all").dropna(axis=1, how="all")

    if df.empty:
        return df

    renamed_columns = []
    used_names = {}

    for index, column in enumerate(df.columns):
        name = str(column).strip()

        if not name or name.startswith("Unnamed:"):
            name = f"항목 {index + 1}"

        # 엑셀에 같은 열 이름이 있을 때 구분합니다.
        count = used_names.get(name, 0) + 1
        used_names[name] = count

        if count > 1:
            name = f"{name} ({count})"

        renamed_columns.append(name)

    df.columns = renamed_columns

    return df


def format_cell(value):
    """표 안의 값을 읽기 쉽게 변환합니다."""
    if value is None or pd.isna(value):
        return "", "text"

    if isinstance(value, (datetime, date, pd.Timestamp)):
        return value.strftime("%Y-%m-%d"), "text"

    if isinstance(value, bool):
        return str(value), "text"

    if isinstance(value, int):
        return f"{value:,}", "number"

    if isinstance(value, float):
        if value.is_integer():
            return f"{int(value):,}", "number"

        return f"{value:,.2f}".rstrip("0").rstrip("."), "number"

    return str(value), "text"


def show_html_table(df):
    """
    HTML 표로 표시합니다.

    텍스트는 왼쪽, 숫자는 오른쪽으로 정렬합니다.
    엑셀의 문자열은 HTML로 해석되지 않도록 이스케이프합니다.
    """
    if df is None or df.empty:
        st.info("표시할 데이터가 없습니다.")
        return

    header_html = "".join(
        f"<th>{html.escape(str(column))}</th>"
        for column in df.columns
    )

    rows_html = []

    for row in df.itertuples(index=False, name=None):
        cells = []

        for value in row:
            text, css_class = format_cell(value)
            safe_text = html.escape(text).replace("\n", "<br>")

            cells.append(
                f'<td class="{css_class}">{safe_text}</td>'
            )

        rows_html.append(
            "<tr>" + "".join(cells) + "</tr>"
        )

    table_html = (
        '<div class="table-scroll">'
        '<table class="hana-table">'
        f"<thead><tr>{header_html}</tr></thead>"
        f"<tbody>{''.join(rows_html)}</tbody>"
        "</table>"
        "</div>"
    )

    st.markdown(table_html, unsafe_allow_html=True)


def filter_dataframe(df, keyword):
    """모든 열을 대상으로 키워드 검색을 수행합니다."""
    if df is None or df.empty or not keyword.strip():
        return df

    keyword = keyword.strip()

    matched = df.astype(str).apply(
        lambda column: column.str.contains(
            keyword,
            case=False,
            na=False,
            regex=False,
        )
    )

    return df[matched.any(axis=1)]


def show_sheet(
    file_path,
    sheet_name,
    header_row,
    search_key,
    title=None,
    selected_columns=None,
    forward_fill_columns=None,
):
    """시트를 불러와 검색창과 HTML 표를 표시합니다."""
    if title:
        section_title(title)

    df = load_sheet(
        file_path=file_path,
        sheet_name=sheet_name,
        header_row=header_row,
    )

    if df is None:
        return

    df = clean_dataframe(df)

    if df is None or df.empty:
        st.info("이 시트에는 표시할 내용이 없습니다.")
        return

    # 병합 셀로 인해 비어 있는 값 중 지정한 열만 채웁니다.
    if forward_fill_columns:
        for column in forward_fill_columns:
            if column in df.columns:
                df[column] = df[column].ffill()

    if selected_columns:
        existing_columns = [
            column
            for column in selected_columns
            if column in df.columns
        ]

        if existing_columns:
            df = df[existing_columns]

    keyword = st.text_input(
        "키워드 검색",
        placeholder="점포명, 대리점명, 업무 내용 등을 입력하세요.",
        key=search_key,
    )

    filtered = filter_dataframe(df, keyword)

    st.caption(f"표시 중: {len(filtered):,}개 행")

    if filtered.empty:
        st.info("검색 결과가 없습니다.")
        return

    show_html_table(filtered)


def show_raw_sheet(
    file_path,
    sheet_name,
    search_key,
    title=None,
):
    """
    여러 행으로 구성된 표는 제목행을 임의 지정하지 않고
    엑셀의 행과 열 구조에 가깝게 표시합니다.
    """
    if title:
        section_title(title)

    df = load_sheet(
        file_path=file_path,
        sheet_name=sheet_name,
        header_row=None,
    )

    if df is None:
        return

    df = df.replace(r"^\s*$", pd.NA, regex=True)
    df = df.dropna(how="all").dropna(axis=1, how="all")

    if df.empty:
        st.info("이 시트에는 표시할 내용이 없습니다.")
        return

    df.columns = [
        f"열 {number}"
        for number in range(1, len(df.columns) + 1)
    ]

    keyword = st.text_input(
        "키워드 검색",
        placeholder="검색할 단어를 입력하세요.",
        key=search_key,
    )

    filtered = filter_dataframe(df, keyword)

    st.caption(
        "복합 표의 원본 행을 표시합니다. "
        "병합 셀이나 수식 결과는 엑셀 원본과 다르게 보일 수 있습니다."
    )
    st.caption(f"표시 중: {len(filtered):,}개 행")

    if filtered.empty:
        st.info("검색 결과가 없습니다.")
        return

    show_html_table(filtered)


def show_empty_channel(channel):
    """비어 있는 채널 시트를 안내합니다."""
    section_title(f"{channel} 점포별 업무")

    df = load_sheet(
        file_path=MAIN_FILE,
        sheet_name=channel,
        header_row=None,
    )

    if df is None:
        return

    cleaned = df.replace(r"^\s*$", pd.NA, regex=True)
    cleaned = cleaned.dropna(how="all").dropna(axis=1, how="all")

    if cleaned.empty:
        st.info(
            f"현재 엑셀의 '{channel}' 시트가 비어 있습니다. "
            "엑셀에 내용을 추가하면 표시할 수 있습니다."
        )
        return

    show_sheet(
        file_path=MAIN_FILE,
        sheet_name=channel,
        header_row=0,
        search_key=f"channel_{channel}",
    )


# =========================================================
# 4. 상단 헤더
# =========================================================

st.markdown(
    """
    <div class="dashboard-header">
        <h1>유통점 업무 인수인계</h1>
        <p>유통채널별 운영 현황 · 점포별 업무 · 홈플러스 기업회생</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if not MAIN_FILE.exists() or not HOMEPLUS_FILE.exists():
    st.warning(
        "엑셀 파일이 모두 확인되지 않았습니다. "
        "app.py와 같은 위치에 아래 파일을 넣어주세요.\n\n"
        "- 통합문서1.xlsx\n"
        "- 홈플러스 기업회생 절차.xlsx"
    )


# =========================================================
# 5. 상단 메뉴
# =========================================================

tab_labels = [
    "신규입점",
    "외부지원금",
    "홈플러스",
    "롯데백화점",
    "롯데마트",
    "AK",
    "NC",
    "기타",
    "직계약 대리점",
]

tabs = st.tabs(tab_labels)


# =========================================================
# 6. 신규입점
# =========================================================

with tabs[0]:
    section_title("유통점 신규입점 안내")

    info_box(
        "아래 절차는 이전에 작업한 대시보드 내용을 참고한 안내입니다. "
        "실제 진행 시 최신 내부 규정과 채널별 조건을 확인해주세요."
    )

    st.markdown(
        """
        <div class="step-box">
            <h4>1. 문의부터 선정까지</h4>
            <ol>
                <li>유통점 모집공고와 입점 조건을 확인합니다.</li>
                <li>입점 희망 대리점과 사전 협의합니다.</li>
                <li>입점제안서를 작성해 영업전략팀에 전달합니다.</li>
                <li>복수 지원 시 내부 평가를 진행하고 대리점을 선정합니다.</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)

    with left:
        st.markdown(
            """
            <div class="step-box">
                <h4>2-A. 공식인증예약센터</h4>
                <ol>
                    <li>유통점 입점 품의를 진행합니다.</li>
                    <li>채널별 인테리어 규정을 확인합니다.</li>
                    <li>전자계약을 체결합니다.</li>
                    <li>사업자 및 관광사업자 등록 주소 변경을 진행합니다.</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            """
            <div class="step-box">
                <h4>2-B. 일반대리점</h4>
                <ol>
                    <li>공식인증 개설 관련 서류와 신용정보를 확인합니다.</li>
                    <li>유통점 입점 품의를 진행합니다.</li>
                    <li>채널별 인테리어 규정을 확인합니다.</li>
                    <li>전자계약과 사업자 주소 변경을 진행합니다.</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )

    section_title("유통점 운영 시 확인사항")

    st.markdown(
        """
        - 영업시간과 휴무일은 해당 유통채널의 계약 및 운영 규정을 확인합니다.
        - 부재 시에는 안내문을 설치하고 점포 담당자와 소통합니다.
        - 집기, 간판 및 인테리어는 해당 유통채널의 승인 기준을 확인합니다.
        - 권리금 및 계약 조건은 관련 계약서와 내부 규정을 확인합니다.
        """
    )


# =========================================================
# 7. 외부지원금
# =========================================================

with tabs[1]:
    section_title("외부지원금")

    support_tab_1, support_tab_2 = st.tabs(
        ["유통채널관리 현황", "홈플러스 연도별 청구 내역"]
    )

    with support_tab_1:
        info_box(
            "통합문서의 '유통채널관리' 시트를 기준으로 표시합니다. "
            "여러 줄로 구성된 원본 표이므로 가로 스크롤로 확인해주세요."
        )

        show_raw_sheet(
            file_path=MAIN_FILE,
            sheet_name="유통채널관리",
            search_key="support_raw_search",
            title="외부지원금 현황",
        )

    with support_tab_2:
        info_box(
            "통합문서의 '홈플러스' 시트에서 연도별 외부지원금 "
            "청구 내역을 표시합니다."
        )

        show_sheet(
            file_path=MAIN_FILE,
            sheet_name="홈플러스",
            header_row=4,
            search_key="support_homeplus_search",
            title="홈플러스 연도별 외부지원금 청구 내역",
            selected_columns=[
                "년도",
                "항목",
                "입금금액",
                "문서번호",
                "입금번호",
            ],
            forward_fill_columns=["년도"],
        )


# =========================================================
# 8. 홈플러스
# =========================================================

with tabs[2]:
    section_title("홈플러스 업무 현황")

    info_box(
        "홈플러스 관련 자료를 두 엑셀 파일에서 불러옵니다. "
        "퇴점 여부, 금액, 일정은 엑셀에 기록된 내용을 기준으로 표시합니다."
    )

    home_tabs = st.tabs(
        [
            "기업회생 점포 현황",
            "기업회생 타임라인",
            "매출수수료",
            "점포별 계약매출",
            "전년대비 매출",
            "매출순위",
            "점포별 이슈",
        ]
    )

    with home_tabs[0]:
        show_sheet(
            file_path=HOMEPLUS_FILE,
            sheet_name="홈플러스 기업회생",
            header_row=1,
            search_key="home_recovery_stores",
            title="기업회생 관련 점포 현황",
        )

    with home_tabs[1]:
        st.caption(
            "정리된 타임라인은 'Sheet1'을 기준으로 표시합니다."
        )

        show_sheet(
            file_path=HOMEPLUS_FILE,
            sheet_name="Sheet1",
            header_row=1,
            search_key="home_timeline",
            title="기업회생 업무 타임라인",
        )

        with st.expander("원본 타임라인 보기"):
            show_sheet(
                file_path=HOMEPLUS_FILE,
                sheet_name="홈플러스 기업회생 타임라인",
                header_row=1,
                search_key="home_original_timeline",
            )

    with home_tabs[2]:
        show_sheet(
            file_path=MAIN_FILE,
            sheet_name="홈플러스 매출수수료 현황",
            header_row=1,
            search_key="home_commission",
            title="홈플러스 월별 매출수수료 현황",
        )

    with home_tabs[3]:
        show_sheet(
            file_path=HOMEPLUS_FILE,
            sheet_name="홈플러스 점포별 계약매출",
            header_row=1,
            search_key="home_contract_sales",
            title="홈플러스 점포별 계약매출",
        )

    with home_tabs[4]:
        st.caption(
            "엑셀의 두 번째 행을 제목으로 사용합니다. "
            "연도 구분과 중복 월 표기는 엑셀 원본도 함께 확인해주세요."
        )

        show_sheet(
            file_path=HOMEPLUS_FILE,
            sheet_name="홈플러스 전년대비 매출",
            header_row=1,
            search_key="home_year_comparison",
            title="홈플러스 전년대비 매출",
        )

    with home_tabs[5]:
        show_sheet(
            file_path=MAIN_FILE,
            sheet_name="홈플러스 매출순위",
            header_row=0,
            search_key="home_sales_ranking",
            title="홈플러스 매출순위",
        )

    with home_tabs[6]:
        st.caption(
            "점포별 이슈 시트는 일반적인 표 형식이 아니어서 "
            "원본 행을 기준으로 표시합니다."
        )

        show_raw_sheet(
            file_path=HOMEPLUS_FILE,
            sheet_name="홈플러스 점포별 이슈",
            search_key="home_store_issues",
            title="홈플러스 점포별 이슈",
        )


# =========================================================
# 9. 롯데백화점
# =========================================================

with tabs[3]:
    show_sheet(
        file_path=MAIN_FILE,
        sheet_name="롯데백화점",
        header_row=0,
        search_key="lotte_department_search",
        title="롯데백화점 점포별 업무",
    )


# =========================================================
# 10. 롯데마트
# =========================================================

with tabs[4]:
    show_empty_channel("롯데마트")


# =========================================================
# 11. AK
# =========================================================

with tabs[5]:
    show_sheet(
        file_path=MAIN_FILE,
        sheet_name="AK",
        header_row=0,
        search_key="ak_search",
        title="AK 점포별 업무",
    )


# =========================================================
# 12. NC
# =========================================================

with tabs[6]:
    show_empty_channel("NC")


# =========================================================
# 13. 기타
# =========================================================

with tabs[7]:
    section_title("기타 채널")

    st.warning(
        "제공받은 엑셀의 '기타' 시트에는 계정 및 비밀번호가 "
        "포함되어 있어 이 화면에 표시하지 않습니다."
    )

    st.info(
        "민감정보를 삭제한 별도의 안전한 시트를 준비한 후 "
        "필요한 업무 내용만 연결해주세요."
    )


# =========================================================
# 14. 직계약 대리점
# =========================================================

with tabs[8]:
    show_sheet(
        file_path=MAIN_FILE,
        sheet_name="직계약 대리점",
        header_row=0,
        search_key="direct_agency_search",
        title="직계약 대리점 현황",
    )

    with st.expander("전체 유통점 리스트 보기"):
        show_sheet(
            file_path=MAIN_FILE,
            sheet_name="전체 유통점 리스트",
            header_row=0,
            search_key="all_stores_search",
            title="전체 유통점 리스트",
        )


# =========================================================
# 15. 하단 안내
# =========================================================

st.markdown(
    """
    <div class="footer-note">
        엑셀 파일을 수정한 후 대시보드에 연결된 저장소의 파일을 교체하면
        변경 내용을 확인할 수 있습니다.
    </div>
    """,
    unsafe_allow_html=True,
)
