from html import escape
from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# 기본 설정
# ============================================================

st.set_page_config(
    page_title="유통점 업무 인수인계",
    page_icon="📊",
    layout="wide",
)

PURPLE = "#5E2BB8"
MINT = "#08D1D9"

# app.py와 같은 폴더에 있는 엑셀 파일을 읽습니다.
WORKBOOK = Path(__file__).with_name("통합문서1.xlsx")

BUDGET_URL = (
    "https://hanatour0.sharepoint.com/:x:/r/sites/msteams_f947dd/"
    "_layouts/15/Doc.aspx?"
    "sourcedoc=%7BC3059D9E-98E5-44F2-AE9C-708373259FA7%7D"
    "&file=%25uc720%25ud1b5%25uc810%20"
    "%25uc608%25uc0b0%25ud604%25uc669.xlsx"
    "&action=default&mobileredirect=true"
)


# ============================================================
# 디자인
# ============================================================

st.markdown(
    f"""
    <style>
    .block-container {{
        max-width: 1440px;
        padding-top: 1.4rem;
        padding-bottom: 2rem;
    }}

    .hero {{
        border-left: 6px solid {PURPLE};
        padding: 1rem 1.25rem;
        border-radius: 12px;
        background: rgba(94, 43, 184, 0.06);
        margin-bottom: 1rem;
    }}

    .hero h1 {{
        margin: 0;
    }}

    .hero p {{
        margin: 0.35rem 0 0;
        color: #596273;
    }}

    div[data-testid="stMetric"] {{
        border: 1px solid rgba(94, 43, 184, 0.18);
        border-top: 3px solid {MINT};
        border-radius: 12px;
        padding: 0.8rem 1rem;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.35rem;
    }}

    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px 8px 0 0;
    }}

    .table-wrap {{
        width: 100%;
        max-height: 520px;
        overflow: auto;
        border: 1px solid #e4e7ec;
        border-radius: 8px;
    }}

    .handover-table {{
        border-collapse: collapse;
        width: 100%;
        min-width: 700px;
        font-size: 13px;
    }}

    .handover-table th {{
        position: sticky;
        top: 0;
        z-index: 1;
        background: #f3effb;
        color: #35205f;
        font-weight: 700;
        text-align: center;
        white-space: nowrap;
        border: 1px solid #e4e7ec;
        padding: 10px;
    }}

    .handover-table td {{
        border: 1px solid #e4e7ec;
        padding: 9px 10px;
        text-align: left;
        vertical-align: top;
        white-space: pre-wrap;
        min-width: 90px;
    }}

    .handover-table tr:nth-child(even) td {{
        background: #faf9fd;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 엑셀 파일 확인
# ============================================================

if not WORKBOOK.exists():
    st.error(f"엑셀 파일을 찾을 수 없습니다: {WORKBOOK.name}")
    st.info(
        "app.py와 통합문서1.xlsx를 같은 폴더에 넣어주세요. "
        "파일명과 공백도 정확하게 일치해야 합니다."
    )
    st.stop()

try:
    excel = pd.ExcelFile(WORKBOOK, engine="openpyxl")
    all_sheets = excel.sheet_names
except Exception as exc:
    st.error(f"엑셀 파일을 열 수 없습니다: {exc}")
    st.stop()


# ============================================================
# 공통 함수
# ============================================================

def read_sheet(name, header=0):
    """지정한 시트를 읽고 완전히 빈 행과 열을 제거합니다."""
    if name not in all_sheets:
        return pd.DataFrame()

    try:
        df = pd.read_excel(
            excel,
            sheet_name=name,
            header=header,
        )

        df = df.dropna(how="all")
        df = df.dropna(axis=1, how="all")

        return df.reset_index(drop=True)

    except Exception as exc:
        st.error(f"'{name}' 시트를 읽지 못했습니다: {exc}")
        return pd.DataFrame()


def clean_unnamed_columns(df):
    """제목이 없는 빈 열을 제거합니다."""
    if df is None or df.empty:
        return pd.DataFrame()

    result = df.copy()

    # 제목이 없는 열이라도 실제 내용이 있으면 삭제하지 않습니다.
    columns_to_drop = []

    for col in result.columns:
        if str(col).startswith("Unnamed:") and result[col].isna().all():
            columns_to_drop.append(col)

    if columns_to_drop:
        result = result.drop(columns=columns_to_drop)

    return result


def format_value(value):
    """표에 표시할 값을 읽기 쉬운 문자열로 변환합니다."""
    if pd.isna(value):
        return ""

    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d")

    if isinstance(value, float):
        if value.is_integer():
            return f"{int(value):,}"
        return f"{value:,.2f}".rstrip("0").rstrip(".")

    if isinstance(value, int):
        return f"{value:,}"

    return str(value)


def show_table(df, key=None, searchable=False):
    """
    엑셀 데이터를 HTML 표로 표시합니다.

    HTML 표를 사용해 제목과 본문 정렬을 고정합니다.
    엑셀 내용은 HTML로 해석되지 않도록 이스케이프합니다.
    """
    if df is None or df.empty:
        st.info("표시할 내역이 없습니다.")
        return

    result = df.copy()

    if searchable:
        query = st.text_input(
            "점포명 또는 키워드 검색",
            key=key,
            placeholder="검색어를 입력하세요",
        )

        if query.strip():
            mask = (
                result.fillna("")
                .astype(str)
                .apply(
                    lambda col: col.str.contains(
                        query.strip(),
                        case=False,
                        regex=False,
                        na=False,
                    )
                )
                .any(axis=1)
            )

            result = result.loc[mask].copy()

    st.caption(f"표시 건수: {len(result):,}건")

    if result.empty:
        st.info("검색 결과가 없습니다.")
        return

    display_df = result.copy()

    for col in display_df.columns:
        display_df[col] = display_df[col].map(format_value)

    display_df.columns = [
        "" if str(col).startswith("Unnamed:") else str(col)
        for col in display_df.columns
    ]

    table_html = display_df.to_html(
        index=False,
        escape=True,
        classes="handover-table",
        border=0,
    )

    st.markdown(
        f'<div class="table-wrap">{table_html}</div>',
        unsafe_allow_html=True,
    )


def show_sheet(name, search_key):
    """시트 내용을 검색 가능한 표로 표시합니다."""
    if name not in all_sheets:
        st.info(f"엑셀에 '{name}' 시트가 없습니다.")
        return

    df = read_sheet(name)
    df = clean_unnamed_columns(df)

    if df.empty:
        st.info(f"'{name}' 시트에 입력된 내용이 없습니다.")
        return

    # AK 시트의 채널구분은 엑셀에서 병합되어 있습니다.
    # 해당 열만 빈 값을 위 행의 값으로 채웁니다.
    if name == "AK" and "채널구분" in df.columns:
        df["채널구분"] = df["채널구분"].ffill()

    st.caption(f"엑셀 시트: {name}")
    show_table(
        df,
        key=search_key,
        searchable=True,
    )


def show_channel_stores(channel, search_key):
    """전체 유통점 리스트에서 선택한 채널의 점포를 표시합니다."""
    stores = read_sheet("전체 유통점 리스트")

    if stores.empty:
        st.info("전체 유통점 리스트에 표시할 내용이 없습니다.")
        return

    if "채널구분" not in stores.columns:
        st.info("전체 유통점 리스트에서 '채널구분' 열을 찾지 못했습니다.")
        return

    mask = (
        stores["채널구분"]
        .fillna("")
        .astype(str)
        .str.contains(channel, case=False, regex=False)
    )

    filtered = stores.loc[mask].copy()

    if filtered.empty:
        st.info(f"전체 유통점 리스트에서 '{channel}' 점포를 찾지 못했습니다.")
        return

    st.caption("출처: 전체 유통점 리스트 시트")
    show_table(
        filtered,
        key=search_key,
        searchable=True,
    )


# ============================================================
# 첫 페이지: 외부지원금
# ============================================================

def show_overview():
    """유통채널관리 시트 상단의 잔액을 표시합니다."""
    raw = read_sheet("유통채널관리", header=None)

    if raw.empty or len(raw) < 3:
        st.warning("유통채널관리 시트에서 잔액 정보를 찾지 못했습니다.")
        return

    partners = []

    # 첫 번째 행: 채널명
    # 두 번째 행: 잔액
    for col in range(1, raw.shape[1]):
        name = raw.iat[0, col]
        value = raw.iat[1, col]

        if pd.isna(name) or pd.isna(value):
            continue

        try:
            amount = int(float(value))
        except (TypeError, ValueError):
            continue

        partners.append((str(name).strip(), amount))

    if not partners:
        st.warning("채널별 잔액을 읽지 못했습니다.")
        return

    # 세 번째 행의 총합계를 우선 사용합니다.
    try:
        total = int(float(raw.iat[2, 1]))
    except (TypeError, ValueError, IndexError):
        total = sum(amount for _, amount in partners)

    st.subheader("외부지원금 잔액")

    boxes = st.columns(len(partners) + 1)

    boxes[0].metric(
        "총 잔액",
        f"{total:,}원",
    )

    for box, (name, amount) in zip(boxes[1:], partners):
        box.metric(
            name,
            f"{amount:,}원",
        )

        if total > 0 and amount >= 0:
            ratio = amount / total
            box.progress(
                min(ratio, 1.0),
                text=f"전체 잔액의 {ratio * 100:.1f}%",
            )

    st.caption("통합문서1.xlsx의 유통채널관리 시트 기준입니다.")

    st.link_button(
        "유통점 예산현황 상세 확인",
        BUDGET_URL,
    )

    with st.expander("유통채널관리 시트 상세 보기"):
        st.caption(
            "엑셀 원본의 행과 열을 그대로 표시합니다. "
            "병합된 셀의 빈칸은 그대로 보일 수 있습니다."
        )

        detail = raw.copy()
        detail.columns = [f"열 {i + 1}" for i in range(len(detail.columns))]

        show_table(detail)

    with st.expander("전체 유통점 리스트 보기"):
        st.caption("전체 유통점 리스트 시트 기준입니다.")

        stores = read_sheet("전체 유통점 리스트")

        show_table(
            stores,
            key="all_stores_search",
            searchable=True,
        )


# ============================================================
# 홈플러스 외부지원금
# ============================================================

def support_data():
    """
    홈플러스 시트의 A:E 영역에서 연도별 외부지원금 내역을 읽습니다.

    엑셀에 반복되는 제목 행과 합계 행은 제외합니다.
    """
    raw = read_sheet("홈플러스", header=None)

    if raw.empty:
        return pd.DataFrame()

    # A:E 열이 없더라도 오류가 나지 않도록 보정합니다.
    raw = raw.reindex(columns=range(max(5, raw.shape[1])))

    rows = []
    current_year = None

    for values in raw.iloc[:, :5].itertuples(index=False, name=None):
        year, item, amount, document, deposit = values

        if pd.isna(item):
            continue

        year_text = "" if pd.isna(year) else str(year).strip()

        if year_text in {"년도", "연도"}:
            continue

        if year_text.endswith(".0"):
            year_text = year_text[:-2]

        if year_text.isdigit() and len(year_text) == 4:
            current_year = year_text

        label = str(item).strip()

        if not label:
            continue

        if "총액" in label or "합계" in label:
            continue

        rows.append(
            [
                current_year,
                label,
                amount,
                document,
                deposit,
            ]
        )

    return pd.DataFrame(
        rows,
        columns=[
            "년도",
            "항목",
            "입금금액",
            "문서번호",
            "입금번호",
        ],
    )


def show_homeplus_notes():
    """홈플러스 시트의 G:H 참고 내용을 표시합니다."""
    raw = read_sheet("홈플러스", header=None)

    if raw.empty or raw.shape[1] < 7:
        return

    notes = raw.reindex(columns=[6, 7]).copy()
    notes = notes.dropna(how="all")

    if notes.empty:
        return

    notes.columns = ["참고 항목", "비고"]

    with st.expander("홈플러스 시트 참고 내용"):
        show_table(notes)


# ============================================================
# 홈플러스 매출수수료
# ============================================================

def show_commission(year):
    """선택한 연도의 매출수수료 데이터를 표시합니다."""
    sheet_name = "홈플러스 매출수수료 현황"
    df = read_sheet(sheet_name, header=1)

    if df.empty:
        st.info(
            "홈플러스 매출수수료 현황 시트를 찾지 못했거나 "
            "표시할 내용이 없습니다."
        )
        return

    # 첨부된 엑셀은 두 번째 행에 '2026 계약매출'처럼
    # 연도가 포함된 열 제목이 있습니다.
    year_columns = [
        col for col in df.columns
        if year in str(col)
    ]

    if not year_columns:
        st.info(
            f"현재 엑셀의 매출수수료 현황 시트에서 "
            f"{year}년 데이터 열을 확인할 수 없습니다."
        )
        return

    df = clean_unnamed_columns(df)

    st.caption(
        f"{year}년 내역 · 엑셀 시트: {sheet_name} "
        "· 합계 행은 엑셀 원본 기준입니다."
    )

    show_table(df)


# ============================================================
# 화면 구성
# ============================================================

st.markdown(
    """
    <div class="hero">
        <h1>유통점 업무 인수인계</h1>
        <p>유통채널별 지원금과 업무 현황을 한곳에서 확인합니다.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

names = [
    "외부지원금",
    "홈플러스",
    "롯데백화점",
    "롯데마트",
    "AK",
    "NC",
    "기타",
    "직계약 대리점",
]

tabs = st.tabs(names)


# ------------------------------------------------------------
# 외부지원금
# ------------------------------------------------------------

with tabs[0]:
    show_overview()


# ------------------------------------------------------------
# 홈플러스
# ------------------------------------------------------------

with tabs[1]:
    st.subheader("홈플러스")

    menu = st.radio(
        "홈플러스 메뉴",
        [
            "외부지원금",
            "매출수수료",
            "매출순위",
        ],
        horizontal=True,
        key="hp_menu",
    )

    if menu == "외부지원금":
        category = st.radio(
            "외부지원금 구분",
            [
                "등급커미션",
                "기타",
            ],
            horizontal=True,
            key="hp_category",
        )

        df = support_data()

        if not df.empty:
            normalized = (
                df["항목"]
                .astype(str)
                .str.replace(" ", "", regex=False)
            )

            commission_mask = normalized.str.contains(
                "등급커미션",
                regex=False,
            )

            if category == "등급커미션":
                df = df.loc[commission_mask].copy()
            else:
                df = df.loc[~commission_mask].copy()

        st.caption(
            "홈플러스 시트의 항목명으로 구분합니다. "
            "합계 행은 제외합니다."
        )

        show_table(
            df,
            key="hp_support_search",
            searchable=True,
        )

        show_homeplus_notes()

    elif menu == "매출수수료":
        year = st.radio(
            "매출수수료 연도",
            [
                "2024",
                "2025",
                "2026",
            ],
            horizontal=True,
            key="hp_year",
        )

        show_commission(year)

    else:
        st.caption("엑셀 시트: 홈플러스 매출순위")

        rank = read_sheet("홈플러스 매출순위")

        show_table(
            rank,
            key="hp_rank_search",
            searchable=True,
        )


# ------------------------------------------------------------
# 롯데백화점
# ------------------------------------------------------------

with tabs[2]:
    st.subheader("롯데백화점")
    show_sheet(
        "롯데백화점",
        search_key="lotte_department_search",
    )


# ------------------------------------------------------------
# 롯데마트
# ------------------------------------------------------------

with tabs[3]:
    st.subheader("롯데마트")

    mart_df = read_sheet("롯데마트")

    if mart_df.empty:
        st.info(
            "롯데마트 시트가 비어 있어 전체 유통점 리스트에서 "
            "롯데마트 점포를 표시합니다."
        )
        show_channel_stores(
            "롯데마트",
            search_key="lotte_mart_stores_search",
        )
    else:
        show_sheet(
            "롯데마트",
            search_key="lotte_mart_search",
        )

        with st.expander("전체 유통점 리스트에서 롯데마트 보기"):
            show_channel_stores(
                "롯데마트",
                search_key="lotte_mart_extra_search",
            )


# ------------------------------------------------------------
# AK
# ------------------------------------------------------------

with tabs[4]:
    st.subheader("AK")
    show_sheet(
        "AK",
        search_key="ak_search",
    )


# ------------------------------------------------------------
# NC
# ------------------------------------------------------------

with tabs[5]:
    st.subheader("NC")

    nc_df = read_sheet("NC")

    if nc_df.empty:
        st.info(
            "NC 시트가 비어 있어 전체 유통점 리스트에서 "
            "NC 점포를 표시합니다."
        )
        show_channel_stores(
            "NC",
            search_key="nc_stores_search",
        )
    else:
        show_sheet(
            "NC",
            search_key="nc_search",
        )

        with st.expander("전체 유통점 리스트에서 NC 보기"):
            show_channel_stores(
                "NC",
                search_key="nc_extra_search",
            )


# ------------------------------------------------------------
# 기타
# ------------------------------------------------------------

with tabs[6]:
    st.subheader("기타")

    st.warning(
        "기타 시트는 민감정보가 포함될 가능성이 있어 표시하지 않습니다. "
        "화면에서 숨겨도 엑셀 원본의 정보가 삭제되지는 않습니다."
    )

    st.info(
        "대시보드에 올릴 엑셀 복사본에서 계정·비밀번호 등 "
        "민감정보를 제거한 뒤 업로드해 주세요."
    )


# ------------------------------------------------------------
# 직계약 대리점
# ------------------------------------------------------------

with tabs[7]:
    st.subheader("직계약 대리점")

    show_sheet(
        "직계약 대리점",
        search_key="direct_agency_search",
    )


# ============================================================
# 하단 안내
# ============================================================

st.divider()

st.caption(
    "엑셀을 수정한 뒤 대시보드에 연결된 GitHub 저장소에 반영하면 "
    "업데이트된 내용을 확인할 수 있습니다."
)
