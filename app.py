import streamlit as st
import base64
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
ASSETS = Path("assets")
PROPOSAL_FILE = ASSETS / "유통점_입점제안서_양식.pptx"


# ─────────────────────────────────────────────────────
# 채널 데이터
# ─────────────────────────────────────────────────────
CHANNELS = {
    "외부지원금": {
        "logo": None,
        "subtitle": "외부지원금 안내",
        "status": "준비중",
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
        '<p>영업전략팀 이강일</p>'
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
            f'{info["status"]}'
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
            f'{channel_name} 정보 준비 중'
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
