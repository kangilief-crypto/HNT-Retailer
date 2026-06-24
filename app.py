import streamlit as st
import os
from pathlib import Path

# ─────────────────────────────────────────────────────
# 페이지 기본 설정
# ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="유통채널 안내",
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
# 채널 데이터
# ─────────────────────────────────────────────────────
ASSETS = Path("assets")

CHANNELS = {
    "이마트": {
        "logo": "emart.png",
        "subtitle": "EMART · 대형마트",
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
    "현대백화점": {
        "logo": "hyundai.png",
        "subtitle": "HYUNDAI · 백화점",
        "status": "준비중",
    },
    "NC": {
        "logo": "nc.png",
        "subtitle": "NC · 쇼핑몰",
        "status": "준비중",
    },
    "기타": {
        "logo": None,
        "subtitle": "AK · GS리테일 · 세이브존 등",
        "status": "운영중",
    },
}

# ─────────────────────────────────────────────────────
# 통합 문의·입점 절차 데이터
# ─────────────────────────────────────────────────────
INQUIRY_PROCESS = [
    ("모집공고 확인", "유통점 모집공고 페이지에서 조건 확인"),
    ("대리점 소통", "입점 희망 대리점과 사전 협의 진행"),
    ("입점제안서 작성", "양식 다운로드 후 작성"),
    ("영업전략팀 전달", "담당자에게 쪽지로 제안서 전달"),
    ("내부 평가 · 선정", "동일 점포 복수 지원 시 평가지표 기반 선정"),
]

ENTRY_OFFICIAL = [
    ("선정 품의 진행", "영업전략팀 상신"),
    ("인테리어 작업 준비", "인테리어 규정은 유통채널별로 상이, 자세한 규정은 각 채널 탭 확인"),
    ("전자계약 체결", "글로싸인 발송"),
    ("사업자/관광사업자 등록증 주소변경 진행", "전대차계약서 혹은 사용승인 공문 증빙"),
]

ENTRY_GENERAL = [
    ("선정 품의 진행", "영업전략팀 상신"),
    ("공식인증 개설 신청 관련서류 게시판 등록 및 신용정보조회",
     "개설 품의 작성 제외 — 영업전략팀 선정 품의로 갈음"),
    ("인테리어 작업 준비", "인테리어 규정은 유통채널별로 상이, 자세한 규정은 각 채널 탭 확인"),
    ("전자계약 체결", "글로싸인 발송"),
    ("사업자/관광사업자 등록증 주소변경 진행", "전대차계약서 혹은 사용승인 공문 증빙"),
]

# ─────────────────────────────────────────────────────
# 커스텀 CSS
# ─────────────────────────────────────────────────────
st.markdown(f"""
<style>
    .block-container {{ padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1400px; }}
    header[data-testid="stHeader"] {{ display: none; }}
    [data-testid="stSidebar"] {{ display: none; }}

    /* ── 상단 헤더 ── */
    .top-header {{
        background: linear-gradient(135deg, {PURPLE} 0%, {MINT} 180%);
        border-radius: 12px;
        padding: 26px 32px;
        color: white;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 24px;
    }}
    .top-header-logo {{
        background: white;
        border-radius: 10px;
        padding: 10px 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}
    .top-header-text h1 {{
        font-size: 24px;
        font-weight: 800;
        margin: 0;
        color: white;
        letter-spacing: -0.3px;
    }}
    .top-header-text p {{
        font-size: 13px;
        margin: 6px 0 0 0;
        color: rgba(255,255,255,0.9);
    }}
    .top-header-tag {{
        display: inline-block;
        background: rgba(255,255,255,0.18);
        padding: 4px 10px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 1px;
        border-radius: 4px;
        margin-bottom: 8px;
    }}

    /* ── 탭 디자인 (볼드 강화) ── */
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
    .stTabs [data-baseweb="tab-panel"] {{ padding-top: 8px; }}

    /* ── 섹션 헤더 ── */
    .section-wrap {{ margin: 24px 0 14px 0; }}
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

    /* ── 안내 배너 ── */
    .info-banner {{
        background: #f5f1ff;
        border-left: 4px solid {PURPLE};
        border-radius: 6px;
        padding: 16px 20px;
        font-size: 13.5px;
        color: {GRAY_700};
        line-height: 1.8;
    }}
    .info-banner b {{ color: {PURPLE}; }}

    /* ── 카드 ── */
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

    /* ── 단계 아이템 ── */
    .step-item {{
        display: flex;
        align-items: flex-start;
        padding: 12px 0;
        border-bottom: 1px dashed {GRAY_200};
    }}
    .step-item:last-child {{ border-bottom: none; padding-bottom: 0; }}
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
    .step-text {{ flex: 1; }}
    .step-title {{ font-size: 13.5px; font-weight: 600; color: {BLACK}; }}
    .step-sub {{ font-size: 12px; color: {GRAY_500}; margin-top: 3px; line-height: 1.5; }}

    /* ── 분기 안내 박스 ── */
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

    /* ── 채널 카드 ── */
    .channel-card {{
        border: 1px solid {GRAY_200};
        border-radius: 12px;
        padding: 24px;
        background: white;
        text-align: center;
    }}
    .channel-logo-wrap {{
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 12px;
    }}
    .channel-name {{
        font-size: 16px;
        font-weight: 700;
        color: {BLACK};
        margin-bottom: 4px;
    }}
    .channel-sub {{
        font-size: 12px;
        color: {GRAY_500};
        margin-bottom: 10px;
    }}
    .status-badge {{
        display: inline-block;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 4px;
    }}
    .status-active {{ background: {MINT}; color: {BLACK}; }}
    .status-prep {{ background: {GRAY_100}; color: {GRAY_500}; }}

    /* ── 알림 박스 ── */
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

    /* ── 점선 헬프 박스 ── */
    .empty-state {{
        border: 2px dashed {GRAY_200};
        border-radius: 10px;
        padding: 48px 20px;
        text-align: center;
        color: {GRAY_500};
        font-size: 14px;
        background: {GRAY_50};
    }}

    /* ── 메트릭 카드 ── */
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
    .metric-accent {{ color: {PURPLE}; }}

    .footer-note {{
        text-align: right;
        font-size: 11px;
        color: {GRAY_500};
        margin-top: 32px;
        padding-top: 16px;
        border-top: 1px solid {GRAY_200};
    }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# 헬퍼 함수
# ─────────────────────────────────────────────────────
def section_header(num: int, title: str):
    st.markdown(
        f'<div class="section-wrap">'
        f'<span class="section-num">{num}</span>'
        f'<span class="section-accent"></span>'
        f'<span class="section-title">{title}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

def render_steps_html(steps, start_num=1):
    items = ""
    for i, (title, sub) in enumerate(steps, start_num):
        sub_html = f'<div class="step-sub">{sub}</div>' if sub else ""
        items += (
            f'<div class="step-item">'
            f'<div class="step-circle">{i}</div>'
            f'<div class="step-text">'
            f'<div class="step-title">{title}</div>'
            f'{sub_html}'
            f'</div></div>'
        )
    return items


def load_logo(filename):
    if not filename:
        return None
    path = ASSETS / filename
    return str(path) if path.exists() else None

# ─────────────────────────────────────────────────────
# 상단 헤더 (하나투어 로고 + 제목)
# ─────────────────────────────────────────────────────
hanatour_logo = load_logo("hanatour.png")

header_col1, header_col2 = st.columns([1, 8])
with header_col1:
    st.markdown(
        f'<div class="top-header" style="padding:14px; justify-content:center;">',
        unsafe_allow_html=True,
    )
    if hanatour_logo:
        st.image(hanatour_logo, use_container_width=True)
    else:
        st.markdown(
            f'<div style="background:white; border-radius:8px; padding:14px 10px; '
            f'text-align:center; font-weight:800; color:{PURPLE}; font-size:13px;">'
            f'HANATOUR</div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

with header_col2:
    st.markdown(
        f'<div class="top-header" style="margin-left:-8px;">'
        f'<div class="top-header-text">'
        f'<div class="top-header-tag">HANATOUR · RETAILER GUIDE</div>'
        f'<h1>유통채널 안내</h1>'
        f'<p>영업팀 대상 유통채널 관련 내용 안내 드립니다.</p>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────
# 탭 구성
# ─────────────────────────────────────────────────────
tab_labels = [
    "유통점 공통안내",
    "이마트",
    "홈플러스",
    "롯데마트",
    "롯데백화점",
    "현대백화점",
    "NC",
    "기타",
]
tabs = st.tabs(tab_labels)

# ═════════════════════════════════════════════════════
# 탭 0: 유통점 공통안내
# ═════════════════════════════════════════════════════
with tabs[0]:
    # ── 1. 안내사항 ──
    section_header(1, "안내사항")
    st.markdown(
        f'<div class="info-banner">'
        f'<b>[유통점 모집공고]</b> 사이트 통해 입점 조건 확인 부탁드리겠습니다.<br>'
        f'동일 점포에 복수 지원 시 내부 평가지표에 근거하여 평가 진행 후 선정합니다.<br>'
        f'세부 조건은 <b>영업전략팀</b>으로 문의 부탁드리겠습니다.'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True)
    b1, b2, _ = st.columns([1, 1, 2])
    with b1:
        st.link_button(
            "유통점 모집공고",
            "https://app.notion.com/p/e95a5614ef634ab5bd48e6c9df5f4bbf",
            use_container_width=True,
        )
    with b2:
        st.link_button(
            "입점제안서 양식 다운로드",
            "#",
            type="primary",
            use_container_width=True,
        )

    # ── 2. 유통점 문의절차 (선형 5단계 → 분기 → 2갈래) ──
    section_header(2, "유통점 문의 절차")

    # 1~5단계 (선형)
    st.markdown(
        f'<div class="card">'
        f'<div class="card-title">'
        f'<span>문의 → 선정 프로세스</span>'
        f'<span class="card-count">총 {len(INQUIRY_PROCESS)}단계</span>'
        f'</div>'
        f'{render_steps_html(INQUIRY_PROCESS)}'
        f'</div>',
        unsafe_allow_html=True,
    )

    # 분기 마커: "대리점 선정 및 입점 확정"
    st.markdown(
        f'<div class="branch-marker">'
        f'<span class="branch-marker-line"></span>'
        f'<span class="branch-marker-text">대리점 선정 및 입점 확정</span>'
        f'</div>'
        f'<div class="branch-down-arrow">▼</div>',
        unsafe_allow_html=True,
    )

    # 두 갈래 분기: A. 공식인증예약센터 / B. 일반대리점
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f'<div class="card">'
            f'<div class="card-title">'
            f'<span>A. 공식인증예약센터일 경우</span>'
            f'<span class="card-count">총 {len(ENTRY_OFFICIAL)}단계 (6~9)</span>'
            f'</div>'
            f'{render_steps_html(ENTRY_OFFICIAL, start_num=6)}'
            f'</div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="card">'
            f'<div class="card-title">'
            f'<span>B. 일반대리점일 경우</span>'
            f'<span class="card-count">총 {len(ENTRY_GENERAL)}단계 (6~10)</span>'
            f'</div>'
            f'{render_steps_html(ENTRY_GENERAL, start_num=6)}'
            f'</div>',
            unsafe_allow_html=True,
        )


    # ── 3. 지원 방법 · 근무 규정 ──
    section_header(3, "지원 방법 · 근무 규정")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f'<div class="card">'
            f'<div class="card-title"><span>지원 방법</span></div>'
            f'<div style="font-size:13.5px; color:{GRAY_700}; line-height:1.8;">'
            f'• 입점 희망 대리점과 소통하며 <b>입점제안서 작성</b><br>'
            f'• 작성 완료 후 영업전략팀 담당자에게 쪽지 전달'
            f'</div>'
            f'<div style="margin-top:14px; padding:12px 14px; background:{GRAY_50}; '
            f'border-radius:4px; border-left:3px solid {PURPLE};">'
            f'<div style="color:{GRAY_500}; font-size:11px;">영업전략팀 담당자</div>'
            f'<div style="color:{BLACK}; font-weight:600; font-size:13.5px; margin-top:2px;">'
            f'이강일B / 노태성</div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="card">'
            f'<div class="card-title"><span>근무 규정</span></div>'
            f'<div style="font-size:13.5px; color:{GRAY_700}; line-height:1.9;">'
            f'• 근무 시 <b>출입증(명찰) 패용</b> 필수<br>'
            f'• 유통점 매장 영업시간 준수<br>'
            f'• 출장·공항 미팅 등 부득이한 부재 시 <b>부재 중 팻말 설치 및 점포 담당자와 소통</b> 필수'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── 4. 채널별 요약 ──
    section_header(4, "채널별 요약")
    cols = st.columns(4)
    items = list(CHANNELS.items())
    for idx, (name, info) in enumerate(items):
        with cols[idx % 4]:
            st.markdown('<div class="channel-card">', unsafe_allow_html=True)
            st.markdown('<div class="channel-logo-wrap">', unsafe_allow_html=True)
            logo_path = load_logo(info["logo"])
            if logo_path:
                st.image(logo_path, width=64)
            else:
                st.markdown(
                    f'<div style="width:64px;height:64px;background:{GRAY_100};'
                    f'border-radius:8px;display:flex;align-items:center;'
                    f'justify-content:center;color:{GRAY_500};font-weight:700;">기타</div>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)
            status_cls = "status-active" if info["status"] == "운영중" else "status-prep"
            st.markdown(
                f'<div class="channel-name">{name}</div>'
                f'<div class="channel-sub">{info["subtitle"]}</div>'
                f'<span class="status-badge {status_cls}">{info["status"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        if (idx + 1) % 4 == 0 and idx != len(items) - 1:
            cols = st.columns(4)

# ═════════════════════════════════════════════════════
# 탭 1~7: 채널별 상세
# ═════════════════════════════════════════════════════
def render_channel_tab(channel_name: str, info: dict):
    logo_path = load_logo(info["logo"])

    c1, c2 = st.columns([1, 6])
    with c1:
        if logo_path:
            st.image(logo_path, width=90)
        else:
            st.markdown(
                f'<div style="width:90px;height:90px;background:{GRAY_100};'
                f'border-radius:12px;display:flex;align-items:center;'
                f'justify-content:center;color:{GRAY_500};font-weight:700;font-size:14px;">'
                f'기타</div>',
                unsafe_allow_html=True,
            )
    with c2:
        status_cls = "status-active" if info["status"] == "운영중" else "status-prep"
        st.markdown(
            f'<div style="padding-top:14px;">'
            f'<div style="font-size:22px; font-weight:700; color:{BLACK};">{channel_name}</div>'
            f'<div style="font-size:13px; color:{GRAY_500}; margin:4px 0 8px 0;">'
            f'{info["subtitle"]}</div>'
            f'<span class="status-badge {status_cls}">{info["status"]}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)

    if channel_name == "홈플러스":
        section_header(1, "임대 · 관리비")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-label">보증금</div>'
                f'<div class="metric-value">없음</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-label">임대료 (계약관계 기준)</div>'
                f'<div class="metric-value">'
                f'<span class="metric-accent">70</span>'
                f'<span style="font-size:15px; color:{GRAY_500};">만원</span>'
                f'<span style="color:{GRAY_200}; margin:0 6px;"> / </span>'
                f'<span class="metric-accent">80</span>'
                f'<span style="font-size:15px; color:{GRAY_500};">만원</span>'
                f'</div>'
                f'<div style="font-size:12px; color:{GRAY_500}; margin-top:8px;">'
                f'듀얼 70만원 · 단독 80만원</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-label">관리비</div>'
                f'<div class="metric-value">없음</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        section_header(2, "특이사항 · 퇴점 안내")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                f'<div class="alert-purple">'
                f'<div class="alert-title">특이사항</div>'
                f'<div class="alert-body">'
                f'홈플러스 입점 대리점은 <b>등급커미션 −1단계</b> 적용.'
                f'</div></div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f'<div class="alert-mint">'
                f'<div class="alert-title">퇴점 내용</div>'
                f'<div class="alert-body">'
                f'하나투어 → 홈플러스 공문 발송일 기준 <b>최소 30일 전 퇴점 내용 공유</b> '
                f'조건으로 중도퇴점 패널티 면제.'
                f'</div></div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            f'<div class="empty-state">'
            f'<div style="font-size:32px; margin-bottom:8px;">📋</div>'
            f'<div style="font-weight:600; color:{BLACK}; margin-bottom:4px;">'
            f'{channel_name} 채널 정보 준비 중</div>'
            f'<div>임대 조건, 입점 절차, 특이사항 등이 곧 업데이트될 예정입니다.</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

channel_tab_names = ["이마트", "홈플러스", "롯데마트", "롯데백화점", "현대백화점", "NC", "기타"]
for tab_idx, ch_name in enumerate(channel_tab_names, start=1):
    with tabs[tab_idx]:
        render_channel_tab(ch_name, CHANNELS[ch_name])

# ─────────────────────────────────────────────────────
# 푸터
# ─────────────────────────────────────────────────────
st.markdown(
    '<div class="footer-note">'
    '본 안내는 신규입점 가이드용이며, 세부 조건은 영업전략팀 확인을 권장합니다.'
    '</div>',
    unsafe_allow_html=True,
)
