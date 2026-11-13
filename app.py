import streamlit as st
import base64
import csv
import io
import html
import pandas as pd
from datetime import date, datetime
from numbers import Number
from pathlib import Path


# ─────────────────────────────────────────────────────
# 페이지 기본 설정
# ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="유통점 업무 인수인계",
    page_icon="🛍️",
    layout="wide",
)


# ─────────────────────────────────────────────────────
# 컬러 토큰
# ─────────────────────────────────────────────────────
PURPLE = "#5E2BB8"
MINT = "#08D1D9"
BLACK = "#111111"
GRAY_50 = "#F9FAFB"
GRAY_100 = "#F3F4F6"
GRAY_200 = "#E5E7EB"
GRAY_500 = "#6B7280"
GRAY_700 = "#374151"


# ─────────────────────────────────────────────────────
# 파일 경로
# ─────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"
MAIN_EXCEL = BASE_DIR / "통합문서1.xlsx"
HOME_EXCEL = BASE_DIR / "홈플러스 기업회생 절차.xlsx"
PROPOSAL_FILE = ASSETS / "유통점_입점제안서_양식.pptx"


# ─────────────────────────────────────────────────────
# 채널 데이터
# ─────────────────────────────────────────────────────
CHANNELS = {
    "외부지원금": {
        "logo": None,
        "subtitle": "외부지원금 안내",
        "status": "운영중",
    },
    "홈플러스": {
        "logo": "homeplus.png",
        "subtitle": "HOMEPLUS · 대형마트",
        "status": "운영중",
    },
    "롯데마트": {
        "logo": "lottemart.png",
        "subtitle": "LOTTE MART · 대형마트",
        "status": "준비중",
    },
    "롯데백화점": {
        "logo": "lottedept.png",
        "subtitle": "LOTTE DEPT · 백화점",
        "status": "준비중",
    },
    "AK": {
        "logo": "ak.png",
        "subtitle": "AK · 백화점",
        "status": "준비중",
    },
    "NC": {
        "logo": "nc.png",
        "subtitle": "NC · 쇼핑몰",
        "status": "준비중",
    },
    "기타": {
        "logo": None,
        "subtitle": "GS리테일 · 세이브존 등",
        "status": "운영중",
    },
    "직계약 대리점": {
        "logo": None,
        "subtitle": "직계약 대리점 안내",
        "status": "준비중",
    },
}


# ─────────────────────────────────────────────────────
# 통합 문의·입점 절차 데이터
# ─────────────────────────────────────────────────────
INQUIRY_PROCESS = [
    (
        "모집공고 확인",
        "유통점 모집공고 페이지에서 조건 확인",
    ),
    (
        "대리점 소통",
        "입점 희망 대리점과 사전 협의 진행",
    ),
    (
        "입점제안서 작성",
        "양식 다운로드 후 작성",
    ),
    (
        "영업전략팀 전달",
        "담당자에게 쪽지로 제안서 전달",
    ),
    (
        "내부 평가 · 선정",
        "동일 점포 복수 지원 시 평가지표 기반 선정",
    ),
]

ENTRY_OFFICIAL = [
    (
        "유통점 입점 품의",
        "영업전략팀 상신",
    ),
    (
        "인테리어 작업 준비",
        "인테리어 규정은 유통채널별로 상이, "
        "자세한 규정은 각 채널 탭 확인",
    ),
    (
        "전자계약 체결",
        "글로싸인 발송",
    ),
    (
        "사업자/관광사업자 등록증 주소변경 진행",
        "전대차계약서 혹은 사용승인 공문 증빙",
    ),
]

ENTRY_GENERAL = [
    (
        "공식인증 개설 신청 관련서류 게시판 등록 및 신용정보조회",
        "개설 품의 작성 제외 — 영업전략팀 선정 품의로 갈음",
    ),
    (
        "유통점 입점 품의",
        "영업전략팀 상신",
    ),
    (
        "인테리어 작업 준비",
        "인테리어 규정은 유통채널별로 상이, "
        "자세한 규정은 각 채널 탭 확인",
    ),
    (
        "전자계약 체결",
        "글로싸인 발송",
    ),
    (
        "사업자/관광사업자 등록증 주소변경 진행",
        "전대차계약서 혹은 사용승인 공문 증빙",
    ),
]


# ─────────────────────────────────────────────────────
# 커스텀 CSS
# ─────────────────────────────────────────────────────
st.markdown(
    f"""
<style>
    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }}

    header[data-testid="stHeader"] {{
        display: none;
    }}

    [data-testid="stSidebar"] {{
        display: none;
    }}

    /* 상단 헤더 */
    .top-header {{
        background: linear-gradient(
            135deg,
            {PURPLE} 0%,
            {MINT} 180%
        );
        border-radius: 12px;
        padding: 28px 32px;
        color: white;
        height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
        box-sizing: border-box;
        overflow: hidden;
    }}

    .top-header-text {{
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}

    .top-header-text h1 {{
        font-size: 28px !important;
        font-weight: 800 !important;
        margin: 0 !important;
        color: white !important;
        letter-spacing: -0.3px;
        line-height: 1.25;
    }}

    .top-header-text p {{
        font-size: 13px !important;
        margin: 10px 0 0 0 !important;
        color: rgba(255, 255, 255, 0.92) !important;
        line-height: 1.4;
    }}

    /* 탭 디자인 */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 4px;
        background: {GRAY_100};
        padding: 6px;
        border-radius: 10px;
        margin-bottom: 20px;
    }}

    .stTabs [data-baseweb="tab"] {{
        background: transparent;
        border-radius: 6px;
        padding: 10px 18px;
        color: {BLACK};
        border: none;
    }}

    .stTabs [data-baseweb="tab"] p {{
        font-weight: 700 !important;
        font-size: 14px !important;
        letter-spacing: -0.2px;
    }}

    .stTabs [aria-selected="true"] {{
        background: {PURPLE} !important;
    }}

    .stTabs [aria-selected="true"] p {{
        color: white !important;
        font-weight: 800 !important;
    }}

    .stTabs [data-baseweb="tab-panel"] {{
        padding-top: 8px;
    }}

    /* 섹션 제목 */
    .section-wrap {{
        margin: 24px 0 14px 0;
    }}

    .section-num {{
        display: inline-block;
        background: {PURPLE};
        color: white;
        width: 24px;
        height: 24px;
        text-align: center;
        line-height: 24px;
        font-size: 12px;
        font-weight: 700;
        border-radius: 6px;
        margin-right: 10px;
        vertical-align: middle;
    }}

    .section-title {{
        display: inline-block;
        font-size: 17px;
        font-weight: 700;
        color: {BLACK};
        vertical-align: middle;
    }}

    .section-accent {{
        display: inline-block;
        width: 4px;
        height: 18px;
        background: {MINT};
        vertical-align: middle;
        margin: 0 8px 0 4px;
        border-radius: 2px;
    }}

    /* 안내 배너 */
    .info-banner {{
        background: #f5f1ff;
        border-left: 4px solid {PURPLE};
        border-radius: 6px;
        padding: 16px 20px;
        font-size: 13.5px;
        color: {GRAY_700};
        line-height: 1.8;
    }}

    .info-banner b {{
        color: {PURPLE};
    }}

    /* 다운로드 버튼 */
    .stDownloadButton button {{
        background: {PURPLE} !important;
        color: white !important;
        border: none !important;
        font-weight: 700 !important;
    }}

    .stDownloadButton button:hover {{
        background: #4b22a0 !important;
        color: white !important;
    }}

    /* 카드 */
    .card {{
        border: 1px solid {GRAY_200};
        border-radius: 10px;
        padding: 20px 22px;
        background: white;
        height: 100%;
    }}

    .card-title {{
        font-size: 14px;
        font-weight: 700;
        color: {BLACK};
        margin-bottom: 14px;
        padding-bottom: 12px;
        border-bottom: 1px solid {GRAY_200};
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    .card-count {{
        font-size: 11px;
        color: {GRAY_500};
        font-weight: 500;
    }}

    /* 단계 */
    .step-item {{
        display: flex;
        align-items: flex-start;
        padding: 12px 0;
        border-bottom: 1px dashed {GRAY_200};
    }}

    .step-item:last-child {{
        border-bottom: none;
        padding-bottom: 0;
    }}

    .step-circle {{
        background: {PURPLE};
        color: white;
        width: 26px;
        height: 26px;
        text-align: center;
        line-height: 26px;
        font-size: 12px;
        font-weight: 700;
        border-radius: 50%;
        margin-right: 12px;
        flex-shrink: 0;
    }}

    .step-text {{
        flex: 1;
    }}

    .step-title {{
        font-size: 13.5px;
        font-weight: 600;
        color: {BLACK};
    }}

    .step-sub {{
        font-size: 12px;
        color: {GRAY_500};
        margin-top: 3px;
        line-height: 1.5;
    }}

    /* 분기 표시 */
    .branch-marker {{
        margin: 20px 0 12px 0;
        text-align: center;
        position: relative;
    }}

    .branch-marker-line {{
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        height: 1px;
        background: {GRAY_200};
        z-index: 0;
    }}

    .branch-marker-text {{
        position: relative;
        display: inline-block;
        background: white;
        padding: 6px 18px;
        border: 1.5px solid {PURPLE};
        color: {PURPLE};
        font-size: 13px;
        font-weight: 700;
        border-radius: 20px;
        z-index: 1;
    }}

    .branch-down-arrow {{
        text-align: center;
        color: {PURPLE};
        font-size: 18px;
        margin: 4px 0 8px 0;
        font-weight: 700;
    }}

    /* 상태 배지 */
    .status-badge {{
        display: inline-block;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 4px;
    }}

    .status-active {{
        background: {MINT};
        color: {BLACK};
    }}

    .status-prep {{
        background: {GRAY_100};
        color: {GRAY_500};
    }}

    /* 알림 박스 */
    .alert-purple {{
        background: #f5f1ff;
        border-left: 4px solid {PURPLE};
        border-radius: 6px;
        padding: 14px 18px;
    }}

    .alert-mint {{
        background: #e6fcfd;
        border-left: 4px solid {MINT};
        border-radius: 6px;
        padding: 14px 18px;
    }}

    .alert-title {{
        font-size: 13px;
        font-weight: 700;
        color: {BLACK};
        margin-bottom: 6px;
    }}

    .alert-body {{
        font-size: 13px;
        color: {GRAY_700};
        line-height: 1.6;
    }}

    /* 준비 중 화면 */
    .empty-state {{
        border: 2px dashed {GRAY_200};
        border-radius: 10px;
        padding: 48px 20px;
        text-align: center;
        color: {GRAY_500};
        font-size: 14px;
        background: {GRAY_50};
    }}

    /* 임대·관리비 카드 */
    .metric-card {{
        border: 1px solid {GRAY_200};
        border-radius: 10px;
        padding: 20px 22px;
        background: white;
    }}

    .metric-label {{
        font-size: 12px;
        color: {GRAY_500};
        font-weight: 500;
        margin-bottom: 10px;
    }}

    .metric-value {{
        font-size: 26px;
        font-weight: 700;
        color: {BLACK};
    }}

    .metric-accent {{
        color: {PURPLE};
    }}

    /* 하단 안내 */
    .footer-note {{
        text-align: right;
        font-size: 11px;
        color: {GRAY_500};
        margin-top: 32px;
        padding-top: 16px;
        border-top: 1px solid {GRAY_200};
    }}

    /* 공통 표: 내용에 맞춘 간격, 긴 표는 가로 스크롤 */
    .table-wrap {{ width:100%; overflow-x:auto; border:1px solid {GRAY_200}; border-radius:8px; }}
    table.report {{ border-collapse:collapse; width:max-content; min-width:100%; table-layout:auto; font-size:13px; line-height:1.45; letter-spacing:normal; background:white; color:{BLACK}; }}
    table.report th, table.report td {{ border-bottom:1px solid {GRAY_200}; padding:6px 9px; height:auto; vertical-align:middle; text-align:left; }}
    table.report th {{ background:{GRAY_100}; color:{BLACK}; font-weight:700; white-space:nowrap; }}
    table.report td {{ max-width:320px; white-space:normal; overflow-wrap:anywhere; }}
    table.report td.number, table.report th.number {{ text-align:right; white-space:nowrap; }}
    table.report td.center, table.report th.center {{ text-align:center; white-space:nowrap; }}
    table.report tbody tr:last-child td {{ border-bottom:none; }}
    table.report tbody tr:nth-child(even) {{ background:{GRAY_50}; }}
    .timeline-wrap {{ max-width:100%; overflow-x:auto; }}
    table.timeline-report {{ table-layout:auto; }}
    table.timeline-report th:nth-child(1), table.timeline-report td:nth-child(1),
    table.timeline-report th:nth-child(2), table.timeline-report td:nth-child(2),
    table.timeline-report th:nth-child(4), table.timeline-report td:nth-child(4) {{ white-space:nowrap; }}
    table.timeline-report td:nth-child(3) {{ max-width:320px; white-space:normal; }}
    .inline-detail summary {{ cursor:pointer; color:{PURPLE}; font-weight:700; white-space:normal; }}
    .inline-detail-label {{ color:{PURPLE}; font-size:12px; font-weight:700; margin:9px 0 3px; }}
    .inline-detail-body {{ white-space:normal; min-width:220px; max-width:540px; line-height:1.55; overflow-wrap:anywhere; color:{GRAY_700}; }}
    /* 표의 긴 설명을 별도 영역으로 분리 */
    .detail-item {{ border:1px solid {GRAY_200}; border-left:3px solid {PURPLE}; border-radius:6px; padding:10px 12px; margin:8px 0; background:white; }}
    .detail-heading {{ font-size:13px; font-weight:700; color:{BLACK}; margin-bottom:5px; }}
    .detail-label {{ font-size:12px; font-weight:700; color:{PURPLE}; margin:7px 0 3px; }}
    .detail-body {{ font-size:13px; line-height:1.55; color:{GRAY_700}; overflow-wrap:anywhere; }}

</style>
""",
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────
# 헬퍼 함수
# ─────────────────────────────────────────────────────
def section_header(num: int, title: str):
    """번호가 있는 섹션 제목을 표시합니다."""
    st.markdown(
        f'<div class="section-wrap">'
        f'<span class="section-num">{num}</span>'
        f'<span class="section-accent"></span>'
        f'<span class="section-title">{title}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_steps_html(steps, start_num=1):
    """입점 절차를 단계별 HTML로 변환합니다."""
    items = ""

    for i, (title, sub) in enumerate(steps, start_num):
        sub_html = (
            f'<div class="step-sub">{sub}</div>'
            if sub
            else ""
        )

        items += (
            f'<div class="step-item">'
            f'<div class="step-circle">{i}</div>'
            f'<div class="step-text">'
            f'<div class="step-title">{title}</div>'
            f'{sub_html}'
            f'</div>'
            f'</div>'
        )

    return items


def load_logo(filename):
    """로고 파일이 있으면 파일 경로를 반환합니다."""
    if not filename:
        return None

    path = ASSETS / filename

    return str(path) if path.exists() else None


def logo_to_base64(filename):
    """로고 파일을 HTML 표시용으로 인코딩합니다."""
    if not filename:
        return None

    path = ASSETS / filename

    if not path.exists():
        return None

    with open(path, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()

    return f"data:image/png;base64,{encoded}"


def load_proposal_file():
    """입점제안서 양식 파일을 읽어 반환합니다."""
    if PROPOSAL_FILE.exists():
        with open(PROPOSAL_FILE, "rb") as file:
            return file.read()

    return None


# ─────────────────────────────────────────────────────
# 상단 헤더
# ─────────────────────────────────────────────────────
hanatour_logo_b64 = logo_to_base64("hanatour.png")

header_left, header_right = st.columns(
    [1.3, 8],
    gap="small",
)

with header_left:
    if hanatour_logo_b64:
        st.markdown(
            f'<div style="'
            f'background:white; '
            f'border:1px solid #E5E7EB; '
            f'border-radius:12px; '
            f'height:130px; '
            f'box-sizing:border-box; '
            f'display:flex; '
            f'align-items:center; '
            f'justify-content:center; '
            f'padding:14px 18px; '
            f'overflow:hidden;">'
            f'<img src="{hanatour_logo_b64}" '
            f'style="'
            f'max-height:95px; '
            f'max-width:100%; '
            f'width:auto; '
            f'height:auto; '
            f'object-fit:contain; '
            f'display:block;" />'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div style="'
            f'background:white; '
            f'border:1px solid #E5E7EB; '
            f'border-radius:12px; '
            f'height:130px; '
            f'box-sizing:border-box; '
            f'display:flex; '
            f'align-items:center; '
            f'justify-content:center; '
            f'font-weight:800; '
            f'color:{PURPLE}; '
            f'font-size:18px;">'
            f'HANATOUR'
            f'</div>',
            unsafe_allow_html=True,
        )

with header_right:
    st.markdown(
        '<div class="top-header">'
        '<div class="top-header-text">'
        '<h1>유통점 업무 인수인계</h1>'
        
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────
# 메뉴 탭 구성
# ─────────────────────────────────────────────────────
tab_labels = [
    "신규입점",
    "외부지원금",
    "홈플러스",
    "롯데마트",
    "롯데백화점",
    "AK",
    "NC",
    "기타",
    "직계약 대리점",
]

tabs = st.tabs(tab_labels)


# ═════════════════════════════════════════════════════
# 탭 0: 신규입점
# ═════════════════════════════════════════════════════
with tabs[0]:

    # ── 1. 안내사항 ──
    section_header(1, "안내사항")

    st.markdown(
        f'<div class="info-banner">'
        f'<b>[유통점 모집공고]</b> 사이트를 통해 '
        f'입점 조건 확인 부탁드리겠습니다.<br>'
        f'동일 점포에 복수 지원 시 내부 평가지표에 근거하여 '
        f'평가 진행 후 선정합니다.<br>'
        f'세부 조건은 <b>영업전략팀</b>으로 '
        f'문의 부탁드리겠습니다.'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="height: 12px;"></div>',
        unsafe_allow_html=True,
    )

    button_1, button_2, _ = st.columns([1, 1, 2])

    with button_1:
        st.link_button(
            "유통점 모집공고",
            "https://app.notion.com/p/"
            "e95a5614ef634ab5bd48e6c9df5f4bbf?pvs=21",
            use_container_width=True,
        )

    with button_2:
        proposal_bytes = load_proposal_file()

        if proposal_bytes:
            st.download_button(
                label="입점제안서 양식 다운로드",
                data=proposal_bytes,
                file_name="유통점_입점제안서_양식.pptx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "presentationml.presentation"
                ),
                use_container_width=True,
                type="primary",
            )
        else:
            st.link_button(
                "입점제안서 양식 다운로드 (파일 없음)",
                "#",
                type="primary",
                use_container_width=True,
                disabled=True,
            )

    # ── 2. 유통점 입점 절차 ──
    section_header(2, "유통점 입점 절차")

    # 공통 1~5단계
    st.markdown(
        f'<div class="card">'
        f'<div class="card-title">'
        f'<span>문의 → 선정 프로세스</span>'
        f'<span class="card-count">'
        f'총 {len(INQUIRY_PROCESS)}단계'
        f'</span>'
        f'</div>'
        f'{render_steps_html(INQUIRY_PROCESS)}'
        f'</div>',
        unsafe_allow_html=True,
    )

    # 분기 마커
    st.markdown(
        f'<div class="branch-marker">'
        f'<span class="branch-marker-line"></span>'
        f'<span class="branch-marker-text">'
        f'대리점 선정 및 입점 확정'
        f'</span>'
        f'</div>'
        f'<div class="branch-down-arrow">▼</div>',
        unsafe_allow_html=True,
    )

    # 공식인증예약센터 / 일반대리점
    column_official, column_general = st.columns(2)

    with column_official:
        st.markdown(
            f'<div class="card">'
            f'<div class="card-title">'
            f'<span>A. 공식인증예약센터일 경우</span>'
            f'<span class="card-count">'
            f'총 {len(ENTRY_OFFICIAL)}단계 (6~9)'
            f'</span>'
            f'</div>'
            f'{render_steps_html(ENTRY_OFFICIAL, start_num=6)}'
            f'</div>',
            unsafe_allow_html=True,
        )

    with column_general:
        st.markdown(
            f'<div class="card">'
            f'<div class="card-title">'
            f'<span>B. 일반대리점일 경우</span>'
            f'<span class="card-count">'
            f'총 {len(ENTRY_GENERAL)}단계 (6~10)'
            f'</span>'
            f'</div>'
            f'{render_steps_html(ENTRY_GENERAL, start_num=6)}'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── 3. 중요 안내사항 ──
    section_header(3, "유통점 중요 안내사항")

    st.markdown(
        f'<div class="card">'

        f'<div class="card-title">'
        f'<span>유통점 운영 시 반드시 확인해주세요</span>'
        f'</div>'

        f'<div class="step-item">'
        f'<div class="step-circle">1</div>'
        f'<div class="step-text">'
        f'<div class="step-title">권리금 관련 효력 불인정</div>'
        f'<div class="step-sub">'
        f'유통점 내 입점 공간에 대해 '
        f'<b>권리금과 관련한 어떠한 계약상 효력도 '
        f'인정하지 않음.</b>'
        f'</div>'
        f'</div>'
        f'</div>'

        f'<div class="step-item">'
        f'<div class="step-circle">2</div>'
        f'<div class="step-text">'
        f'<div class="step-title">영업시간 · 휴무일 준수</div>'
        f'<div class="step-sub">'
        f'영업시간 및 휴무일은 입점 시 체결한 계약서에 따라 '
        f'<b>각 유통채널 영업규정에 따름.</b>'
        f'</div>'
        f'</div>'
        f'</div>'

        f'<div class="step-item">'
        f'<div class="step-circle">3</div>'
        f'<div class="step-text">'
        f'<div class="step-title">부재 시 응대 원칙</div>'
        f'<div class="step-sub">'
        f'출장·공항 미팅 등 부재 시 '
        f'<b>부재 중 팻말 설치 및 점포 담당자와 소통 필수.</b>'
        f'</div>'
        f'</div>'
        f'</div>'

        f'<div class="step-item">'
        f'<div class="step-circle">4</div>'
        f'<div class="step-text">'
        f'<div class="step-title">집기 사용 기준</div>'
        f'<div class="step-sub">'
        f'유통점 내 사용 집기는 '
        f'<b>방재 / 방염 검수 완료된 집기만 사용.</b>'
        f'</div>'
        f'</div>'
        f'</div>'

        f'<div class="step-item">'
        f'<div class="step-circle">5</div>'
        f'<div class="step-text">'
        f'<div class="step-title">간판 제작 규정</div>'
        f'<div class="step-sub">'
        f'유통점 간판 제작 시 '
        f'<b>하나투어 브랜드 단독 노출.</b> '
        f'(여행사 이름, 전화번호 노출 X)'
        f'</div>'
        f'</div>'
        f'</div>'

        f'</div>',
        unsafe_allow_html=True,
    )


# ═════════════════════════════════════════════════════
# 채널별 상세 화면
# ═════════════════════════════════════════════════════


# ── 엑셀 연동: 기존 대시보드 데이터는 그대로 유지 ──
@st.cache_data(show_spinner=False)
def read_excel_linked(path, sheet, header, modified_ns):
    return pd.read_excel(path, sheet_name=sheet, header=header, engine="openpyxl")


def format_excel_value(value):
    if pd.isna(value):
        return ""
    if isinstance(value, (datetime, date, pd.Timestamp)):
        return value.strftime("%Y-%m-%d")
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, Number):
        if float(value).is_integer():
            return f"{int(value):,}"
        return str(value)
    return str(value)


# ── 외부지원금 및 홈플러스 상세 데이터 ──
BUDGET_URL = "https://hanatour0.sharepoint.com/:x:/r/sites/msteams_f947dd/_layouts/15/Doc.aspx?sourcedoc={C3059D9E-98E5-44F2-AE9C-708373259FA7}&file=%25uc720%25ud1b5%25uc810%20%25uc608%25uc0b0%25ud604%25ud669.xlsx&action=default&mobileredirect=true"


def esc(value):
    return html.escape(str(value), quote=True)


def report_table(headers, rows, numeric=(), centered=(), timeline=False, inside_expander=False):
    """표는 간결하게 표시하고, 설명 열은 표 아래 별도 영역에 보존합니다."""
    detail_names = {"내용", "상세내용", "회신내용"}
    detail_indices = [i for i, header in enumerate(headers) if str(header).strip() in detail_names]
    display_rows = []
    details = []
    for row in rows:
        shown = list(row)
        parts = []
        for i in detail_indices:
            if i < len(row) and str(row[i]).strip():
                parts.append((str(headers[i]), str(row[i])))
        if parts:
            detail_no = len(details) + 1
            for i in detail_indices:
                if i < len(row) and str(row[i]).strip():
                    shown[i] = f"상세 {detail_no}"
            # 행의 앞쪽 식별 정보는 내용과 분리한 설명의 제목으로 사용합니다.
            identity = [str(v) for i, v in enumerate(row)
                        if i not in detail_indices and str(v).strip()][:3]
            details.append((detail_no, identity, parts))
        display_rows.append(shown)

    def cell(value, index, tag):
        cls = ' class="number"' if index in numeric else (' class="center"' if index in centered else '')
        return f'<{tag}{cls}>{esc(value).replace(chr(10), "<br>")}</{tag}>'

    head = ''.join(cell(v, i, 'th') for i, v in enumerate(headers))
    body = ''.join('<tr>' + ''.join(cell(v, i, 'td') for i, v in enumerate(row)) + '</tr>' for row in display_rows)
    wrap_class = "table-wrap timeline-wrap" if timeline else "table-wrap"
    table_class = "report timeline-report" if timeline else "report"
    st.markdown(f'<div class="{wrap_class}"><table class="{table_class}"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>', unsafe_allow_html=True)

    if details:
        # 엑셀 영역은 이미 expander 안에 있으므로 expander를 중첩하지 않습니다.
        detail_area = st.container() if inside_expander else st.expander(
            f"표와 연결된 상세내용 ({len(details)}건)", expanded=len(details) <= 5
        )
        with detail_area:
            if inside_expander:
                st.markdown(f"**표와 연결된 상세내용 ({len(details)}건)**")
            st.caption("표의 상세 번호와 아래 번호가 연결됩니다. 검색 중에는 검색 결과의 상세내용만 표시됩니다.")
            for number, identity, parts in details:
                title = f"상세 {number}" + (" · " + " · ".join(identity) if identity else "")
                content = ''.join(
                    f'<div class="detail-label">{esc(label)}</div>'
                    f'<div class="detail-body">{esc(value).replace(chr(10), "<br>")}</div>'
                    for label, value in parts
                )
                st.markdown(f'<div class="detail-item"><div class="detail-heading">{esc(title)}</div>{content}</div>', unsafe_allow_html=True)



def inline_detail_table(headers, rows, trigger_index, detail_indices, numeric=(), centered=(), timeline=False):
    """주제 또는 대리점명을 클릭하면 해당 행의 상세 내용이 셀 안에서 펼쳐집니다."""
    visible = [i for i in range(len(headers)) if i not in detail_indices]
    head = ''.join(f'<th>{esc(headers[i])}</th>' for i in visible)
    body = []
    for row in rows:
        parts = [(str(headers[i]), str(row[i])) for i in detail_indices
                 if i < len(row) and str(row[i]).strip()]
        cells = []
        for i in visible:
            value = str(row[i]) if i < len(row) else ''
            cls = ' class="number"' if i in numeric else (' class="center"' if i in centered else '')
            content = esc(value).replace('\n', '<br>')
            if i == trigger_index and parts:
                label = content or '상세 보기'
                detail = ''.join(
                    f'<div class="inline-detail-label">{esc(name)}</div>'
                    f'<div class="inline-detail-body">{esc(text).replace(chr(10), "<br>")}</div>'
                    for name, text in parts
                )
                content = f'<details class="inline-detail"><summary>{label}</summary>{detail}</details>'
            cells.append(f'<td{cls}>{content}</td>')
        body.append('<tr>' + ''.join(cells) + '</tr>')
    table_class = 'report timeline-report' if timeline else 'report'
    st.markdown(
        f'<div class="table-wrap"><table class="{table_class}">'
        f'<thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>',
        unsafe_allow_html=True,
    )


def format_lotte_number(value):
    """롯데백화점 번호: 쉼표 제거 후 숫자 네 자리 뒤에 하이픈을 넣습니다."""
    if pd.isna(value):
        return ''
    if isinstance(value, Number) and not isinstance(value, bool):
        if float(value).is_integer():
            value = str(int(value))
        else:
            return str(value).replace(',', '')
    value = str(value).strip().replace(',', '')
    digits = value.replace('-', '').replace(' ', '')
    if digits.isdigit():
        return digits[:4] + '-' + digits[4:] if len(digits) > 4 else digits
    return value


def render_agency_sheet(channel_name):
    """롯데백화점과 AK 원본 표를 본문에 표시하며 상세는 대리점명에서 펼칩니다."""
    st.subheader(f'{channel_name} 점포별 업무')
    if not MAIN_EXCEL.exists():
        st.warning(f'{MAIN_EXCEL.name} 파일을 app.py와 같은 폴더에 넣어주세요.')
        return
    try:
        df = read_excel_linked(str(MAIN_EXCEL), channel_name, 0, MAIN_EXCEL.stat().st_mtime_ns)
        # 기존 설정(첫 행 제목)을 우선 유지하되, 첫 행이 제목이 아니면 둘째 행을 확인합니다.
        def has_agency(columns):
            return any('대리점' in str(c).replace(' ', '') and
                       ('명' in str(c).replace(' ', '') or str(c).replace(' ', '') == '대리점')
                       for c in columns)
        if not has_agency(df.columns):
            second = read_excel_linked(str(MAIN_EXCEL), channel_name, 1, MAIN_EXCEL.stat().st_mtime_ns)
            if has_agency(second.columns):
                df = second
    except Exception as exc:
        st.error(f'{channel_name} 시트를 읽을 수 없습니다. 파일과 시트 이름을 확인해 주세요. ({type(exc).__name__}: {exc})')
        return
    df = df.replace(r'^\s*$', pd.NA, regex=True).dropna(how='all').dropna(axis=1, how='all')
    if df.empty:
        st.info('표시할 데이터가 없습니다.')
        return
    headers = [f'항목 {i + 1}' if str(c).startswith('Unnamed:') else str(c).strip()
               for i, c in enumerate(df.columns)]
    agency_indices = [i for i, h in enumerate(headers) if '대리점' in h.replace(' ', '') and
                      ('명' in h.replace(' ', '') or h.replace(' ', '') == '대리점')]
    detail_indices = [i for i, h in enumerate(headers)
                      if h.replace(' ', '') in {'내용', '상세', '상세내용', '회신내용'}]
    search = st.text_input('점포명·대리점명·내용 검색', key=f'agency_search_{channel_name}').strip()
    if search:
        df = df[df.astype(str).apply(lambda col: col.str.contains(search, case=False, regex=False, na=False)).any(axis=1)]
    st.caption(f'표시: {len(df):,}개 행')
    if df.empty:
        st.info('검색 결과가 없습니다.')
        return
    number_indices = [i for i, h in enumerate(headers) if h.replace(' ', '') == '번호'] if channel_name == '롯데백화점' else []
    rows = [[format_lotte_number(v) if i in number_indices else format_excel_value(v)
             for i, v in enumerate(row)] for row in df.itertuples(index=False, name=None)]
    numeric = tuple(i for i in range(len(headers)) if i not in number_indices and pd.api.types.is_numeric_dtype(df.iloc[:, i]))
    if not agency_indices:
        st.warning('대리점명 열을 찾지 못해 원본 표로 표시합니다. 시트의 열 이름을 확인해 주세요.')
        # 자동 분리하지 않고 모든 내용을 보존합니다.
        inline_detail_table(headers, rows, -1, [], numeric=numeric)
    elif not detail_indices:
        st.caption('별도 상세내용 열을 찾지 못해 원본 열을 그대로 표시합니다.')
        inline_detail_table(headers, rows, agency_indices[0], [], numeric=numeric)
    else:
        st.caption('대리점명을 클릭하면 해당 행의 상세내용을 확인할 수 있습니다.')
        inline_detail_table(headers, rows, agency_indices[0], detail_indices, numeric=numeric)

def parse_rows(text, expected):
    rows = list(csv.reader(io.StringIO(text.strip()), delimiter='|'))
    for i, row in enumerate(rows, 1):
        if len(row) != expected:
            raise ValueError(f'데이터 행 {i}: {len(row)}개 항목 (필요 {expected}개)')
    return [[x.strip() for x in row] for row in rows]


def show_steps(title, steps, start=1):
    items = []
    for n, (name, detail) in enumerate(steps, start):
        items.append(f'<div class="step-item"><div class="step-circle">{n}</div><div><div class="step-title">{esc(name)}</div><div class="step-sub">{esc(detail)}</div></div></div>')
    st.markdown(f'<div class="card"><div class="card-title">{esc(title)}</div>{"".join(items)}</div>', unsafe_allow_html=True)


CLAIMS = parse_rows("""
2024|2분기 등급 커미션|26,664,483|E25011018843|B2409301240834
2024|3분기 등급 커미션|33,053,280|E25010711887|B2412021353758
2024|유통점 프로모션|7,743,044|E25010711887|B2412021353758
2024|4분기 등급커미션|25,521,849|E25050218255|B2504091564828
2024|홈플러스 창립기념일|14,080,000|E25022862736|B2504091564828
2024|홈플러스 동계 상품권|20,000,000|E24112569356|B2504091564828
2025|1분기 등급커미션|35,625,600|E25073000082|B2506301672991
2025|2분기 등급커미션|28,861,934|E25112108923|B2509301809598
2025|3분기 등급커미션|19,246,898|E26012069476|B2601061959325
2025|4분기 등급커미션|16,300,846|E26061508325|B2604072114146
2025|유니폼 제작 비용 지원|1,875,000|E25091142409|B2601191982998
2025|일회용 앞치마|5,073,000|E25122944783|B2603042054844
2026|1분기 등급커미션|28,891,489|E26101915322|B2609232315480
2026|2분기 등급커미션|18,296,094|E26100703083|2026년 11월 30일 입금예정
2026|3분기 등급커미션|8,053,080|E26100703108|미입금
2026|4분기 등급커미션|예정|예정|예정
""", 5)


ADDITIONAL_CLAIMS = parse_rows("""
2025|부천상동점 CTI 지원금 2025년 2분기|1,125,825|E25112108923|B2509301809598 포함
2025|부천상동점 CTI 지원금 2025년 3분기|2,884,283|E26012069476|B2601061959325 포함
2025|부천상동점 CTI 지원금 2025년 4분기|3,997,143|E26061508325|B2604072114146 포함
2026|부천상동점 CTI 지원금 2026년 1분기|2,470,151|E26101915322|B2609232315480 포함
2025|우수점주 지원금|8,250,000|하나투어 본사수익 귀속|B2604282138538
""", 5)


FEES = parse_rows("""
1월|217,161,669|253,512,753|218,333,021
2월|197,036,427|218,501,808|162,512,202
3월|192,745,998|219,952,344|178,041,363
4월|200,899,413|212,010,490|207,346,487
5월|185,698,653|217,651,396|167,892,161
6월|140,043,768|157,954,153|91,884,630
7월|156,078,646|143,227,478|76,304,042
8월|128,443,225|98,576,899|61,037,206
9월|215,307,145|163,572,943|60,517,930
10월|246,904,127|350,874,321|99,869,516
11월|199,750,059|212,452,806|60,190,417
12월|182,856,569|173,984,767|26,388,660
총 합|2,262,925,699|2,422,272,158|1,410,317,635
""", 4)


STORES = parse_rows("""
1|월드컵점|A9M9R|하나여행[홈플러스 월드컵점]|영업1실||||
2|방학점|PH05080|라호투어[홈플러스 방학점]|영업1실||||
3|원주점|A9NZ3|홈앤투어[홈플러스 원주점]|영업1실||||
4|서울상봉점|A6648|인터팩투어[홈플러스 서울상봉점]|영업1실||||
5|의정부점|PH03909|투어리즘[홈플러스 의정부점]|영업1실||||
6|남양주진접점|PH03821|하랑여행사[홈플러스 진접점]|영업1실|260731|퇴점완료|E26072942040|재택 후 로드샵
7|월곡점|PH05488|(주)와이티투어[홈플러스 월곡점]|영업1실||||
8|면목점|A9MQW|연우투어[홈플러스 면목점]|영업1실|260630|퇴점완료|E26062312662|유통점(NC천호점)
9|춘천점|PH02793|브리즈투어[홈플러스 춘천점]|영업1실|260831|퇴점완료|E26082566798|유통점(롯데슈퍼 춘천점)
10|파주운정점|A9EJR|나라여행[홈플러스 운정점]|영업1실|260901|퇴점완료|E26090172790|로드샵
11|강동점|A9KOP|케이엘트래블[홈플러스 강동점]|영업1실|260901|퇴점완료|E26090375436|로드샵
12|킨텍스점|A9L73|투어에프씨[홈플러스 킨텍스점]|영업1실|260731|퇴점완료|E26072942042|로드샵
13|중계점|PH01088|가람T&C[홈플러스 중계점]|영업1실|260731|퇴점완료|E26072942049|공유오피스
14|신내점|PH06513|탄탄투어 주식회사[홈플러스 신내점]|영업1실|260731|퇴점완료|E26072942089|홈플러스 남현점
15|경기하남점|A9MZF|와이앤제이[홈플러스 경기하남점]|영업1실|260731|퇴점완료|E26072942051|로드샵
16|합정점|PH04176|미라클[홈플러스 합정점]|영업1실||||
17|고양터미널점|PH05424|마이컴퍼니[홈플러스 고양터미널점]|영업1실|260731|퇴점완료|E26072942121|로드샵
18|서수원점|A9L57|그랜드여행사 하나비엔티[홈플러스 서수원점]|영업2실|260630|퇴점완료|E26060295997|로드샵
19|북수원점|A9JL2|미래투어 주식회사[홈플러스 북수원점]|영업2실||||
20|인하점|A9IAO|클럽모조[홈플러스 인하점]|영업2실||||
21|평촌점|PH04004|웰빙트래블[홈플러스 평촌점]|영업2실||||
22|신도림점|PH03613|허니투어[홈플러스 신도림점]|영업2실||||
23|영통점|A9K6Y|레몬투어[홈플러스 영통점]|영업2실||||
24|인천송도점|PH03889|제이에스투어[홈플러스 송도점]|영업2실|260731|퇴점완료|E26072942125|로드샵
25|영등포점|A9GDN|한나여행사[홈플러스 영등포점]|영업2실|260710|퇴점완료|E26060598867|유통점(스타필드 운정점)
26|구월점|PH02526|하늬투어[홈플러스 구월점]|영업2실|260814|퇴점완료|E26080651195|로드샵
27|인천연수점|PH03777|투어그린[홈플러스 연수점]|영업2실|260731|퇴점완료|E26072942103|로드샵
28|간석점|A9KEG|트루일[홈플러스 간석점]|영업2실|260730|퇴점완료|E26072841677|로드샵
29|김포점|A9JYH|성보여행사[홈플러스 김포점]|영업2실||||
30|부천여월점|PH07518|투어유니버스[홈플러스 부천여월점]|영업2실|260731|퇴점완료|E26072035872|로드샵
31|병점점|PH03908|(주)티앤투어여행사[홈플러스 병점점]|영업2실|260831|퇴점완료|E26081961433|공식인증해지
32|가좌점|PH03815|미소여행사[홈플러스 가좌점]|영업2실|260609|퇴점완료|E26060295993|로드샵
33|분당오리점|PH08198|온드림 여행사[홈플러스 분당오리점]|영업2실|260731|퇴점완료|E26072942821|유통점(하나로마트 분당)
34|금천점|PH00480|(주)다나트립[홈플러스 금천점]|영업2실|261015|퇴점완료|E26100198480|AK금정점
35|작전점|PH05760|주식회사 하나둘투어[홈플러스 작전점]|영업2실|260918|퇴점완료|E26091688499|지역이전 로드샵(대구)
36|강서점|PH05979|다니엘투어[홈플러스 강서점]|영업2실||||
37|동수원점|PH05631|정투어[홈플러스 동수원점]|영업2실|260729|퇴점완료|E26072740676|유통점(롯데마트 권선점)
38|인천청라점|A9KG6|티아이엠코리아[홈플러스 청라점]|영업2실||||
39|인천논현점|PH03842|해피투어[홈플러스 인천논현점]|영업2실|260731|퇴점완료|E26072942129|재택 후 로드샵
40|잠실점|PH03792|유유 T&W[홈플러스 잠실점]|영업2실|260731|퇴점완료|E26072841855|사업자폐업
41|화성향남점|PH03841|홈플러스 투어클럽[홈플러스 화성향남점]|영업2실|260131|퇴점완료|E26012372585|로드샵
42|울산동구점|A9I2T|나침반여행사[홈플러스 울산동구점]|지방영업1실||||
43|센텀시티점|PH04840|데이제로컴퍼니[홈플러스 센텀시티점]|지방영업1실|260731|퇴점완료|E26072942110|로드샵(호텔)
44|아시아드점|PH01163|한빛투어[홈플러스 아시아드점]|지방영업1실||||
45|김해점|PH04062|글로벌원투어[홈플러스 김해점]|지방영업1실|260728|퇴점완료|E26072942099|유통점(하나로마트 김해점)
46|성서점|PH03938|여행예약센터[홈플러스 대구성서점]|지방영업1실||||
47|창원점|A3367|가든여행사[홈플러스 창원점]|지방영업1실||||
48|칠곡점|PH03843|칠곡홈플투어[홈플러스 칠곡점]|지방영업1실||||
49|울산점|A9DYP|여행사랑[홈플러스 울산중구점]|지방영업1실||||
50|대전가오점|A9KNU|비발디투어[홈플러스 대전가오점]|지방영업2실||||
51|오창점|PH05606|주식회사 오성투어[홈플러스 오창점]|지방영업2실|260714|퇴점완료|E26071431726|이마트 서북점
52|청주점|A9K4J|라온투어[홈플러스 청주점]|지방영업2실|260710|퇴점완료|E26070826741|로드샵
53|문화점|A9KBT|디어트래블[홈플러스 문화점]|지방영업2실|260118|퇴점완료|E26011667436|로드샵
54|동광주점|PH02173|바른여행[홈플러스 동광주점]|지방영업2실||||
55|광양점|PH03686|미소투어[홈플러스 광양점]|지방영업2실||||
56|전주효자점|A9O2E|함께하는여행[홈플러스 전주효자점]|지방영업2실|260716|퇴점완료|E26070929281|공식인증해지
57|세종점|PH03907|올림투어[홈플러스 세종점]|지방영업2실|260830|퇴점완료|E26081961438|로드샵
""", 9)


TIMELINE = parse_rows("""
2025-03-04|기업회생절차|홈플러스|하나투어|홈플러스 기업회생절차 신청|홈플러스 기업회생절차 최초 신청일자 공유
2025-03-07|기업회생절차|홈플러스|하나투어|기업회생절차 신청 배경 및 향후 운영계획 공유|신용등급 하락에 따른 단기 자금 문제에 선제적으로 대응하기 위해 회생절차를 신청하였음을 설명. 부동산 자산 약 4.7조 원 및 금융부채 약 2조 원을 근거로 회생절차 조기 종료 가능성을 전망함. 전 부문의 정상 운영이 가능하며, 기존 계약 및 승인 건은 차질 없이 진행될 예정임을 전달. 다만 법정관리로 인한 비용 집행의 어려움 및 인력 구조조정 등 운영 효율화 가능성을 공유함.
2025-03-07|기업회생절차|하나투어|내부|기업회생절차 관련 거래 유지 및 고객 대응방안 검토|하나투어는 POS 결제 및 상품권 취급이 없어 대금 결제 관련 직접적인 이슈가 없음을 확인. 고객 대금 전액 하나투어 입금 구조를 유지하고 고객 안내를 강화하기로 함. 홈플러스 신규 입점은 보류하며, 고객센터를 통해 홈플러스 정상 영업 및 하나투어 예약 관련 이상이 없음을 안내하도록 대응함.
2025-03-13|점포폐점|홈플러스|하나투어|홈플러스 폐점 예정 9개 점포 공유|내당점, 부천소사점, 부산반여점, 순천풍덕점, 신내점, 부천상동점, 안산선부점, 동청주점, 동대문점 등 폐점 예정 9개 점포 리스트 공유 및 퇴점 준비 요청.
2025-04-15|기업회생절차|하나투어|홈플러스|홈플러스 기업회생 관련 대면미팅|홈플러스 기업회생절차 진행에 따른 거래 및 점포 운영 관련 협의 진행.
2025-05-14|점포폐점|홈플러스|하나투어|임대점포 계약 해지 예정 통보|홈플러스 임대점포 계약 해지 예정 사항 통보.
2025-06-12|점포운영|하나투어|홈플러스|홈플러스 점포 운영 관련 협의|점포 운영 관련 주요 사항 협의.
2025-06-19|점포운영|하나투어|대리점|홈플러스 입점 대리점 운영 관련 안내|홈플러스 점포 운영 및 대리점 관련 사항 안내.
2025-09-03|점포폐점|홈플러스|하나투어|홈플러스 임대점포 계약 해지 관련 협의|임대점포 계약 해지 관련 진행사항 공유 및 협의.
2025-09-04|점포폐점|홈플러스|하나투어|임대점포 계약 해지 확정 및 퇴점 요청|계산점, 울산북구점, 가양점, 시흥점, 일산점, 안산고잔점, 문화점, 울산남구점 등 8개 점포의 계약 해지 확정. 11월 30일 이전까지 퇴점 요청.
2026-01-12|공동마케팅 지원금|하나투어|홈플러스|2025년 4분기 공동마케팅 지원금 청구|2025년 4분기 공동마케팅 지원금 내역 공유 및 관련 인보이스 입금 요청.
2026-02-05|공동마케팅 지원금|하나투어|홈플러스|공동마케팅 지원금 및 점포 퇴점 보상비용 협의|대면미팅을 통해 2025년 4분기 공동마케팅 지원금 및 부천상동점 퇴점 미이행에 따른 보상비용 처리방안 논의. 당시 확정 전이었던 하림의 홈플러스 익스프레스 인수 관련 내용을 공유받고, 향후 현금흐름 개선 및 추가 비용 송금 가능성 확인.
2026-02-06|공동마케팅 지원금|하나투어|홈플러스|2025년 4분기 공동마케팅 지원금 입금 재요청|2025년 4분기 공동마케팅 지원금 인보이스 입금 재요청.
2026-04-07|공동마케팅 지원금|홈플러스|하나투어|2025년 4분기 공동마케팅 지원금 입금 완료|홈플러스 내부 규정에 따라 발행 요청일 기준 90일 이내 입금 처리. 2025년 4분기 공동마케팅 지원금 16,300,846원 전액 입금 완료.
2026-05-08|점포운영 축소|홈플러스|하나투어|홈플러스 하이퍼사업부문 축소 운영 확정|김해점, 동수원점, 센텀시티점, 가좌점, 신내점, 잠실점, 분당오리점, 남양주진접점, 인천논현점, 일산킨텍스점, 경기하남점, 고양터미널점, 인천연수점, 인천송도점, 면목점, 중계점 등 16개 점포의 하이퍼사업부문 축소 운영 확정.
2026-05-19|공동마케팅 지원금|하나투어|홈플러스|2026년 1분기 공동마케팅 지원금 청구|2026년 1분기 공동마케팅 지원금 내역 공유 및 관련 인보이스 입금 요청.
2026-06-04|점포폐점|홈플러스|하나투어|홈플러스 비핵심 점포 37개 폐점 결정|홈플러스 비핵심 점포 37개점 폐점 결정 및 관련 사항 공유.
2026-07-03|기업회생절차|홈플러스|하나투어|홈플러스 기업회생절차 폐지 결정|홈플러스 기업회생절차 폐지 결정에 따른 관련 사항 공유.
2026-07-13|점포운영 중단|홈플러스|하나투어|전국 홈플러스 마트 영업 휴업 안내|전국 홈플러스 마트 영업 휴업 관련 안내.
2026-07-22|공동마케팅 지원금|하나투어|홈플러스|2026년 1분기 공동마케팅 지원금 지급계획 확인|2026년 1분기 공동마케팅 지원금 지급 여부 및 입금계획 확인 요청.
2026-07-22|판매수수료|하나투어|홈플러스|홈플러스 마트 휴업에 따른 판매수수료 면제 요청|홈플러스 마트 휴업에 따른 판매수수료 면제 요청 공문 발송(E26072440178).
2026-08-18|공동마케팅 지원금|하나투어|홈플러스|공동마케팅 지원금 입금 전 매출수수료 송금 보류 통보|2026년 1분기 공동마케팅 지원금 입금 전까지 6월분 매출수수료 송금을 보류한다는 공문 발송(E26080754085).
2026-08-19|판매수수료|하나투어|홈플러스|판매수수료 면제 요청 관련 2차 회신 요청|판매수수료 면제 요청에 대한 홈플러스의 공식 회신 재요청.
2026-08-19|판매수수료|홈플러스|하나투어|판매수수료 면제 검토 관련 회신|홈플러스 정상화 시점 이후인 9월부터 판매수수료 면제 검토가 가능하다는 회신 수령.
2026-08-21|공동마케팅 지원금|홈플러스|하나투어|공동마케팅 지원금 공익채권 등록 및 상환계획 동의 요청|홈플러스는 하나투어 공동마케팅 지원금을 공익채권으로 등록하고, 회생계획안에 따른 상환계획 동의 요청서를 등기 발송. 2029년 2월 28일까지 지급하는 내용에 대해 하나투어의 서명 요청.
2026-08-24|판매수수료|하나투어|홈플러스|매출수수료 감면안 수용 불가 및 2% 감면 재검토 요청|홈플러스의 상환계획에 동의할 수 없으며 2026년 이내로 입금할 것을 요청함과 동시에 매출수수료 2% 감면안 재검토 요청.
2026-08-24|판매수수료|홈플러스|하나투어|매출수수료 2% 감면안 재검토 불가 회신|홈플러스 측에서 2% 매출수수료 감면안 재검토 불가 회신 및 1% 감면으로 협의 요청.
2026-08-24|판매수수료|하나투어|홈플러스|매출수수료 감면 협의 및 추가 감면 요청|홈플러스의 매출수수료 1% 제안에 대한 거절 및 추가 감면 요청과 함께 홈플러스 채널의 매출 급감 데이터 전달.
2026-08-24|판매수수료|홈플러스|하나투어|매출수수료 감면 1.25% 제안|하나투어의 매출수수료 감면 요청에 대해 홈플러스 측에서 1.25% 감면안 제시.
2026-08-25|판매수수료|영업본부|예산관리팀|홈플러스 매출수수료 감면 협의 진행상황 공유|홈플러스 VI 78,329,206원 중 매출수수료 감면 협의를 진행하고 있으며, 8월 중 합의 예정임을 공유.
2026-08-26|판매수수료|하나투어|홈플러스|매출수수료 감면 4차 요청 및 관련 자료 전달|홈플러스 요청 자료 전달 및 매출수수료 감면 4차 요청.
2026-09-04|판매수수료|홈플러스|하나투어|매출수수료 감면 요청 검토 결과 회신|하나투어의 4차 감면 요청에 대해 불가 회신 및 1.25% 감면안 검토 결과 회신.
2026-09-04|판매수수료|하나투어|홈플러스|매출수수료 협의|7월~8월 매출수수료 2.75%로 최종 합의 및 재계약 시 계약 조건 변경 예정임을 고지.
2026-09-09|공동마케팅 지원금|하나투어|홈플러스|공동마케팅 지원금 지급 시기 및 합의서 작성 협의|홈플러스 본사 대면미팅을 통해 공익채권 등록 동의서에 서명하지 않고 공동마케팅 지원금을 2026년 내 지급하는 방향으로 재요청. 기존 공익채권 상환계획 대신 2026년 지급을 전제로 잔여 금액을 이월 처리하는 양사 합의서 작성 제안. 별도로 홈플러스 점포 퇴점으로 인해 2026년 등급커미션 청구 액이 연 1억원을 넘지 않을 것으로 예상되어 추가 공동마케팅 진행을 제안.
2026-09-14|공동마케팅|홈플러스|하나투어|홈플러스 공동마케팅 진행 불가 통보|홈플러스 측에서 공동마케팅 진행 불가 회신.
2026-09-17|판매수수료|하나투어|홈플러스|7~8월 매출 마감자료 및 세금계산서 발행 방식 확인|7~8월 마감 매출 파일 공유 및 세금계산서 발행 방식 확인 요청.
2026-09-18|판매수수료|홈플러스|하나투어|매출수수료 세금계산서 발행 일정 확인|세금계산서를 9월자로 각각 발행 예정임을 확인 및 공유.
2026-09-21|공동마케팅 지원금|홈플러스|하나투어|공동마케팅 지원금 지급 및 매출수수료 송금 요청|홈플러스는 2026년 1분기 공동마케팅 지원금 전액을 9월 내 입금할 예정임을 전달. 이에 따라 하나투어에서 송금 보류 중인 매출수수료를 9월 내 정상 송금해 줄 것을 요청.
2026-09-23|공동마케팅 지원금|홈플러스|하나투어|공동마케팅 지원금 입금|공동마케팅 지원금 입금 완료(B2609232315480).
2026-10-06|공동마케팅 지원금|하나투어|홈플러스|입금 관련 내용 공문발송 요청|공문발송 요청.
2026-10-12|공동마케팅 지원금|하나투어|홈플러스|입금 관련 내용 공문발송 요청|공문발송 2차 요청.
2026-10-16|공동마케팅 지원금|하나투어|홈플러스|입금 관련 내용 공문발송 요청|공문발송 3차 요청.
2026-10-16|공동마케팅 지원금|홈플러스|하나투어|하나투어 내부 문서 상신|공문 회신 및 기타수익협조문 상신을 통해 영업지원팀 수익으로 귀속(E26101915322).
2026-10-20|재계약|하나투어|홈플러스|2027년 전략적 제휴계약 조건 협의|하나투어는 2027년 전략적 제휴계약과 관련하여 매출수수료 1% 적용, 임대(갑) 계약 전환 또는 계약 해지까지 고려하고 있음을 구두로 전달.
""", 6)


def render_external_details():
    section_header(1, "외부지원금 · 유통점 예산현황")
    st.link_button("유통점 예산현황 파일 열기", BUDGET_URL, use_container_width=True)
    st.caption("SharePoint 접근 권한이 필요할 수 있습니다.")
    st.markdown("""
- 유통점 외부지원금은 현대드림투어 및 홈플러스를 대상으로 각각 임대차계약서에 명시된 기준 및 금액에 따라 청구하고 있습니다.
- 홈플러스 부속합의서에 의거하여 하나투어는 홈플러스에 마케팅 비용의 **50%**를 청구할 수 있으며, 연간 청구 한도는 최대 **1억 원**입니다.
- 하나투어는 매 분기 홈플러스 대리점에 지급한 등급커미션 비용의 **50%**를 홈플러스에 청구하고 있습니다.
- 지원금 입금 확인 후 기타수익협조문을 통해 영업지원팀 수익으로 귀속 처리하며, 외부지원금 관리 장표에 해당 내역을 기재하여 관련 비용을 관리하고 있습니다.
- 외부지원금은 입금일로부터 **1년 이내** 사용 가능하며, 사용 기한 경과 시 미사용 잔액은 하나투어 본사 수익으로 귀속됩니다.
""")
    section_header(2, "외부지원금 분기이월 요건")
    st.markdown('<div class="alert-purple">세금계산서 발행 또는 입금일자로부터 1년 내 마케팅예산 내 전용하여 사용 가능.</div>', unsafe_allow_html=True)
    show_steps("분기이월 시 확인사항", [
        ("발생 시점(=수익) 기준 1년 이내", ""),
        ("최초 계약과 동일한 명목", "타 사업으로 전용 불가"),
        ("품의 갱신 및 분기 이월 계획 기재", "경영관리부 합의 추가"),
    ])
    st.caption("사용기한의 기산점은 위 제공 문구에 따라 함께 표시했습니다. 실제 적용 기준은 관련 부서에 확인해 주세요.")

def render_homeplus_details():
    section_header(3, "홈플러스 상세 현황")
    t1, t2, t3, t4, t5 = st.tabs(["① 공동마케팅 청구", "② 매출수수료", "③ 퇴점 점포", "④ 기업회생 타임라인", "⑤ 점포별 특이사항"])
    with t1:
        st.subheader("2024년 ~ 2026년 홈플러스 공동마케팅(외부지원금) 청구 내역")
        st.caption("금액 단위: 원. 연도는 제공된 청구 내역의 분류 기준이며 입금 연도와 다를 수 있습니다.")
        for year in ("2024", "2025", "2026"):
            st.markdown(f'#### {year}년')
            year_rows = [r for r in CLAIMS if r[0] == year]
            report_table(["년도", "항목", "입금금액 / 청구금액", "문서번호", "입금번호 / 상태"], year_rows, numeric=(2,), centered=(0,))
            if year == "2024":
                st.markdown("**2024년 입금 총액: 127,062,656원**")
            elif year == "2025":
                st.markdown("**2025년 입금 총액: 106,983,278원**")
            else:
                st.caption("2026년 2·3분기는 입금예정 또는 미입금이며 4분기는 예정입니다. 위 금액을 모두 입금액으로 합산하지 않습니다.")
        st.markdown("#### 부천상동점 CTI 및 우수점주 지원금")
        report_table(["년도", "항목", "금액", "문서번호 / 비고", "입금번호 / 상태"], ADDITIONAL_CLAIMS, numeric=(2,), centered=(0,))
        st.markdown("**제공된 별도 내역 총액: 18,727,402원**")
        st.caption("CTI 항목은 해당 입금번호에 포함된 금액으로 표시되어 있습니다. 기존 내역과 중복 합산하지 않도록 확인해 주세요.")
    with t2:
        st.subheader("2024년 ~ 2026년 매출수수료 송금 비용")
        st.markdown("- 2026년 **11월~12월은 예측비용**입니다.\n- 2026년 7월~8월 매출수수료는 **4% → 2.75%**로 인하되었습니다.")
        st.caption("금액 단위: 원. 제공된 합계와 월별 수치를 그대로 표시하며, 2026년 합계에는 예측치가 포함됩니다.")
        report_table(["월", "2024년", "2025년", "2026년"], FEES, numeric=(1,2,3), centered=(0,))
    with t3:
        st.subheader("홈플러스 퇴점 점포")
        st.markdown("""**퇴점 점포 지급 내역**
1. 2026년 7월 ~ 9월 임대료 면제.
2. 대리점 퇴점 이후 3개월 간 웰컴 프로모션 제공 (E26073043443).
3. 공식인증예약센터 등급제 등급 즉시 원복.
""")
        st.markdown("#### 홈플러스 퇴점점포 리스트")
        st.caption("담당부서는 제공해 주신 점포 번호 기준으로 표시했습니다. 그 외 빈 항목은 미기재이며, 퇴점 여부 미기재는 퇴점 여부 미확인입니다.")
        search = st.text_input("점포명·대리점명·코드 검색", key="store_search")
        state = st.selectbox("퇴점 여부", ["전체", "퇴점완료", "미기재"], key="store_state")
        filtered = [r for r in STORES if (not search or search.lower() in ' '.join(r).lower()) and (state == "전체" or (state == "퇴점완료" and r[6] == "퇴점완료") or (state == "미기재" and not r[6]))]
        st.caption(f"표시: {len(filtered)}개 / 전체 {len(STORES)}개")
        report_table(["번호", "점포명", "대리점코드", "대리점명", "담당부서", "퇴점일자", "퇴점여부", "문서번호", "이전확정"], filtered, centered=(0,2,5,6))
    with t4:
        st.subheader("홈플러스 기업회생 타임라인")
        st.caption("제공된 자료를 발생일 기준으로 정리했습니다. 협의 내용과 전망은 해당 시점의 기록입니다.")

        filter_year, filter_keyword, filter_search = st.columns([1, 1.4, 2])
        with filter_year:
            years = ["전체"] + sorted({row[0][:4] for row in TIMELINE})
            selected_year = st.selectbox("연도", years, key="timeline_year")
        with filter_keyword:
            keywords = ["전체"] + sorted({row[1] for row in TIMELINE})
            selected_keyword = st.selectbox("키워드", keywords, key="timeline_filter")
        with filter_search:
            search_text = st.text_input("내용 검색", placeholder="점포명, 주제, 문서번호 등", key="timeline_search").strip().lower()

        rows = [
            row for row in TIMELINE
            if (selected_year == "전체" or row[0][:4] == selected_year)
            and (selected_keyword == "전체" or row[1] == selected_keyword)
            and (not search_text or search_text in " ".join(row).lower())
        ]
        # 날짜순 정렬은 안정 정렬이므로 같은 날짜의 원래 순서는 유지됩니다.
        rows = sorted(rows, key=lambda row: row[0])
        st.caption(f"표시: {len(rows)}건 / 전체 {len(TIMELINE)}건 · 오래된 순 · 주제를 클릭하면 상세내용이 펼쳐집니다.")

        if not rows:
            st.info("선택한 조건에 해당하는 내역이 없습니다.")
        else:
            # 연도별 표에서 날짜, 주제, 발신·수신 및 상세내용을 한 번에 확인합니다.
            for year in sorted({row[0][:4] for row in rows}):
                year_rows = [row for row in rows if row[0][:4] == year]
                st.markdown(f"#### {year}년")
                inline_detail_table(
                    ["일자", "키워드", "주제", "발신 → 수신", "상세내용"],
                    [[date, keyword, title, f"{sender} → {receiver}", detail]
                     for date, keyword, sender, receiver, title, detail in year_rows],
                    trigger_index=2,
                    detail_indices=(4,),
                    centered=(0,),
                    timeline=True,
                )
    with t5:
        st.subheader("기타 점포별 특이사항")
        with st.expander("강릉점 · 관광사업체 인허가", expanded=True):
            st.markdown("**요청사항:** 홈플러스 강릉점에 여행사 관광사업체 인허가 요청.\n\n**강릉시청 답변:** 건축법상 용도가 잘못 되어 있어 여행사 입점 불가.")
            report_table(["강릉시청 담당자", "회신내용"], [
                ["관광정책과 관광산업팀 최형일 주무관", "관광진흥법상 문제 없지만 건축법상 용도가 사무실로 되어 있어야 하는데 홈플러스 강릉점은 판매시설(쇼핑센터)로 신고되어 있어 허가 불가. 건축과 통해 표시변경 신고를 한 뒤에 다시 요청해야 함."],
                ["건축과 건축허가팀", "건축허가팀은 이견 없고 관광정책과에서만 승인하면 문제 없음."],
                ["건축과 건축물대장팀", "건축 대장상에 표시 변경 요청을 하면 신청은 받지만 홈플러스 도면이 호수로 구분되어 있는 것이 아닌, 통으로 되어 있어 호실별로 구분이 되지 않기 때문에 표시변경이 불가함. 이와 별개로 관광정책과와 조율이 안 되면 불가함. 관광정책과에서 승인을 받아야 함."],
            ])
            st.markdown("""
- **하나투어 법무준법팀 및 홈플러스 법무팀:** 강릉시청 주무관의 잘못된 법해석으로 보이며 법적으로 문제 없다는 의견.
- **2024년 7월:** 양사 법무팀을 통해 법적 문제 없는 점을 확인하여 강릉시청에 민원 제기하며 입점을 추진하고자 하였으나, 강릉점 임대인에게 피해가 갈 수 있어 홈플러스 측에서 진행 보류 요청.
- 이후 국토교통부에 관련 법령 해석과 행정행위 절차에 대해 민원을 요청하였으며, 강릉점 점포 내부에 포함된 근린생활시설을 판매시설로 봐야 한다는 답변을 받음. (044-201-3764)
- 이는 관광산업팀 최형일 주무관의 주장과 상반된 답변으로, 강릉점에 여행사가 입점해도 무방할 것으로 보임. **제공된 자료상 최종 입점 가능으로 정리 완료.**
""")
            st.caption("실제 인허가 및 현재 적용 여부는 관련 기관 확인이 필요합니다.")
        with st.expander("부천상동점 · CTI 지원금", expanded=True):
            st.markdown("""
- 부천상동점 퇴점 이후 **4월 1일부로 CTI 대리점 선정**. (E25032583539)
- CTI 지급으로 인한 예상 비용 약 **5,000만원의 50%인 2,500만원**을 홈플러스 측에 요청. (월 200만원, 24개월 예상 기준)
- 홈플러스에서 일시불 비용 송금은 어려울 것으로 판단하고 있어 분할 송금으로 확인 중이며 지급 근거 자료를 요청함.
- 하나투어 - 대리점 간 퇴점 합의서: **E25020537608**
- 홈플러스 - 하나투어 간 퇴점 합의서: **E25022055509**
""")



# 보내주신 이미지에 보이는 직계약 대리점 목록 (17행)
DIRECT_AGENCIES = parse_rows("""
1|AK프라자|분당점|A3473|대한여행사[AK 분당점]|영업2부|영업9팀|경기 성남시 분당구 황새울로360번길 42 AK플라자 2층
2|NC|강서점|A9HSC|아름다운여행사[NC 강서점]|영업2부|영업8팀|서울 강서구 강서로56길 17 nc백화점 8층
3|NC|광명점|A0667|초원여행|영업2부|영업11팀|경기도 광명시 하안로 287번길 8, 6층 초원여행 (하안동,뉴코아아울렛)
4|NC|부산대학교점|PH04152|내일여행㈜|영남영업부|부산2팀|부산광역시 금정구 부산대학로63번길 2, 2층(장전동, NC백화점) 하나투어
5|NC|인천점|A8710|가자여행사[뉴코아 인천점]|영업2부|영업11팀|인천 남동구 인하로 485, 11층 (뉴코아아울렛)
6|롯데마트|대덕점|PH05795|(주)여행의온|충청영업부|충청1팀|대전광역시 유성구 테크노중앙로 14 1층(롯데마트대덕테크노밸리점)
7|롯데백화점|대전점|A2816|알프스투어&골프|충청영업부|충청1팀|대전광역시 서구 계룡로 598, 9층 (괴정동, 롯데백화점)
8|비트플렉스몰|왕십리점|A9LKH|온투어세상|영남영업부|영업1팀|왕십리역 비트플렉스몰 3층
9|탑마트|서진주점|PH04776|글로벌교육문화교류원|영남영업부|경남팀|경남 진주시 새평거로 136
10|하나로마트|퇴계점|A9IVD|아타여행사|영업1부|영업5팀|강원도 춘천시 지석로11 별관1층 103호 (퇴계동, 하나로마트)
11|하나로마트|김포농협점|A9LN2|세계로투어|영업2부|영업11팀|경기 김포시 홍도평로 20, 2층 하나투어
12|하나로마트|연무농협점|PH07123|라이언여행사(주) 연무대지점|충청영업부|충청1팀|충청남도 논산시 안심로 33, 1층
13|하나로마트|청주점|A9D60|투어뱅크[청주]|충청영업부|충청2팀|충북 청주시 상당구 무농정로 32 1층
14|하나로마트|고양점|A9L6R|(주)하나여행[하나로마트 고양점]|영업1부|영업1팀|경기도 고양시 일산서구 대화로 362, 1층
15|하나로마트|삼송점|PH06648|(주)삼송나비투어[하나로마트 삼송점]|영업1부|영업1팀|경기도 고양시 덕양구 동송로 20, 1층
16|메가마트|동래점|A7234|토성관광[메가마트 동래점]|영남영업부|부산2팀|부산광역시 동래구 충렬대로 197, 2층 여행사코너
17|하나로마트|성남점|PH08198|온드림 여행사[하나로마트 성남점]|영업2부|영업9팀|경기 성남시 분당구 성남대로43번길 11 농협하나로마트 1층 식자재 매장옆 하나투어
""", 8)


def render_direct_agencies():
    section_header(1, "직계약 대리점 현황")
    st.caption("제공된 이미지에서 확인되는 17개 행을 표시합니다. 엑셀 자동 연동 데이터가 아닙니다.")
    query = st.text_input(
        "직계약 대리점 검색", key="direct_agency_search",
        placeholder="채널, 점포명, 대리점명, 코드 또는 주소를 입력하세요.",
    ).strip().casefold()
    rows = [row for row in DIRECT_AGENCIES if not query or query in " ".join(row).casefold()]
    st.caption(f"표시: {len(rows)}개 / 전체 {len(DIRECT_AGENCIES)}개")
    if rows:
        report_table(["번호", "채널구분", "점포명", "대리점코드", "대리점명", "담당부서", "담당팀", "주소"], rows, centered=(0, 1, 2, 3, 5, 6))
    else:
        st.info("검색 결과가 없습니다.")


def render_channel_tab(channel_name: str, info: dict):
    """각 메뉴의 상세 화면을 표시합니다."""

    logo_path = load_logo(info["logo"])

    column_logo, column_title = st.columns([1, 6])

    with column_logo:
        if logo_path:
            st.image(logo_path, width=90)
        else:
            st.markdown(
                f'<div style="'
                f'width:90px;'
                f'height:90px;'
                f'background:{GRAY_100};'
                f'border-radius:12px;'
                f'display:flex;'
                f'align-items:center;'
                f'justify-content:center;'
                f'text-align:center;'
                f'padding:6px;'
                f'color:{GRAY_500};'
                f'font-weight:700;'
                f'font-size:14px;">'
                f'{channel_name}'
                f'</div>',
                unsafe_allow_html=True,
            )

    with column_title:
        status_cls = (
            "status-active"
            if info["status"] == "운영중"
            else "status-prep"
        )

        st.markdown(
            f'<div style="padding-top:14px;">'
            f'<div style="'
            f'font-size:22px; '
            f'font-weight:700; '
            f'color:{BLACK};">'
            f'{channel_name}'
            f'</div>'
            f'<div style="'
            f'font-size:13px; '
            f'color:{GRAY_500}; '
            f'margin:4px 0 8px 0;">'
            f'{info["subtitle"]}'
            f'</div>'
            f'<span class="status-badge {status_cls}">'
            f'기존 안내'
            f'</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div style="height: 8px;"></div>',
        unsafe_allow_html=True,
    )

    # ── 홈플러스 상세 내용 ──
    if channel_name == "홈플러스":

        section_header(1, "임대 · 관리비")

        column_1, column_2, column_3 = st.columns(3)

        with column_1:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-label">보증금</div>'
                f'<div class="metric-value">없음</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        with column_2:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-label">'
                f'임대료 (계약관계 기준)'
                f'</div>'
                f'<div class="metric-value">'
                f'<span class="metric-accent">70</span>'
                f'<span style="'
                f'font-size:15px; '
                f'color:{GRAY_500};">만원</span>'
                f'<span style="'
                f'color:{GRAY_200}; '
                f'margin:0 6px;"> / </span>'
                f'<span class="metric-accent">80</span>'
                f'<span style="'
                f'font-size:15px; '
                f'color:{GRAY_500};">만원</span>'
                f'</div>'
                f'<div style="'
                f'font-size:12px; '
                f'color:{GRAY_500}; '
                f'margin-top:8px;">'
                f'듀얼 70만원 · 단독 80만원'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        with column_3:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-label">관리비</div>'
                f'<div class="metric-value">없음</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        section_header(2, "특이사항 · 퇴점 안내")

        column_special, column_exit = st.columns(2)

        with column_special:
            st.markdown(
                f'<div class="alert-purple">'
                f'<div class="alert-title">특이사항</div>'
                f'<div class="alert-body">'
                f'홈플러스 입점 대리점은 '
                f'<b>등급커미션 −1단계</b> 적용.'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        with column_exit:
            st.markdown(
                f'<div class="alert-mint">'
                f'<div class="alert-title">퇴점 내용</div>'
                f'<div class="alert-body">'
                f'하나투어 → 홈플러스 공문 발송일 기준 '
                f'<b>최소 30일 전 퇴점 내용 공유</b> '
                f'조건으로 중도퇴점 패널티 면제.'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        # 기존 임대·관리비와 퇴점 안내는 유지하고 세부 탭을 추가합니다.
        render_homeplus_details()

    # ── 외부지원금 상세 내용 ──
    elif channel_name == "외부지원금":
        render_external_details()

    # ── 롯데백화점과 AK: 대리점명을 눌러 상세내용 확인 ──
    elif channel_name in ("롯데백화점", "AK"):
        render_agency_sheet(channel_name)

    # ── 직계약 대리점 목록 ──
    elif channel_name == "직계약 대리점":
        render_direct_agencies()

    # ── 그 외 메뉴 ──
    else:
        st.markdown(
            f'<div class="empty-state">'
            f'<div style="'
            f'font-size:32px; '
            f'margin-bottom:8px;">📋</div>'
            f'<div style="'
            f'font-weight:600; '
            f'color:{BLACK}; '
            f'margin-bottom:4px;">'
            f'{channel_name} 기존 안내'
            f'</div>'
            f'<div>'
            f'관련 내용이 업데이트될 예정입니다.'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────
# 메뉴와 상세 화면 연결
# ─────────────────────────────────────────────────────
channel_tab_names = [
    "외부지원금",
    "홈플러스",
    "롯데마트",
    "롯데백화점",
    "AK",
    "NC",
    "기타",
    "직계약 대리점",
]

for tab_idx, channel_name in enumerate(
    channel_tab_names,
    start=1,
):
    with tabs[tab_idx]:
        render_channel_tab(
            channel_name,
            CHANNELS[channel_name],
        )


# ─────────────────────────────────────────────────────
# 하단 안내 문구
# ─────────────────────────────────────────────────────
st.markdown(
    '<div class="footer-note">'
    '본 안내는 신규입점 가이드용이며, '
    '세부 조건은 영업전략팀 확인을 권장합니다.'
    '</div>',
    unsafe_allow_html=True,
)
