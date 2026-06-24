import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────────────
# 페이지 기본 설정
# ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="유통점 채널 대시보드",
    page_icon="🏬",
    layout="wide",
)

# ─────────────────────────────────────────────────────
# 채널 데이터
# ─────────────────────────────────────────────────────
CHANNELS = {
    "홈플러스": {
        "tag": "HOMEPLUS",
        "tag_color": "#E60012",
        "subtitle": "대리점 신규입점 가이드 · 2026 기준",
        "status": "운영중",
        "deposit": "없음",
        "rent_dual": "70",
        "rent_solo": "80",
        "rent_caption": "듀얼 70만원 · 단독 80만원",
        "mgmt_fee": "없음",
        "notice_url": "https://app.notion.com/p/e95a5614ef634ab5bd48e6c9df5f4bbf",
        "proposal_url": "#",
        "steps_a": [
            ("입점제안서 제출", None),
            ("선정 품의 진행", "영업전략팀 상신"),
            ("전자계약 체결", "글로싸인 발송"),
            ("관광사업자 · 사업자 등록 (주소변경)", "계약서 또는 홈플러스 사용 승인 공문 증빙"),
        ],
        "steps_b": [
            ("입점제안서 제출", None),
            ("공식인증 개설 신청 관련서류 게시판 등록 및 신용정보조회",
             "개설 품의 작성 제외 — 영업전략팀 선정 품의로 갈음"),
            ("선정 품의 진행", "영업전략팀 상신"),
            ("전자계약 체결", "글로싸인 발송"),
            ("관광사업자 · 사업자 등록 (주소변경)", "계약서 또는 홈플러스 사용 승인 공문 증빙"),
        ],
        "support": [
            "입점 희망 대리점과 소통하며 **입점제안서 작성**",
            "작성 완료 후 영업전략팀 담당자에게 쪽지 전달",
        ],
        "contact": "이강일B / 노태성",
        "work_rules": [
            "근무 시 **출입증(명찰) 패용** 필수",
            "홈플러스 매장 영업시간 준수",
            "출장·공항 미팅 등 부득이한 부재 시 **부재 중 팻말 설치 및 점포 담당자와 소통** 필수",
        ],
        "special_notice": "홈플러스 입점 대리점은 <b>등급커미션 −1단계</b> 적용.",
        "exit_condition": "하나투어 → 홈플러스 공문 발송일 기준 <b>최소 30일 전 퇴점 내용 공유</b> 조건으로 중도퇴점 패널티 면제.",
    },
    "이마트": {
        "tag": "EMART",
        "tag_color": "#FFCD00",
        "subtitle": "대리점 신규입점 가이드 · 2026 기준",
        "status": "준비중",
        "deposit": "TBD",
        "rent_dual": "-",
        "rent_solo": "-",
        "rent_caption": "내용 추가 예정",
        "mgmt_fee": "TBD",
        "notice_url": "#",
        "proposal_url": "#",
        "steps_a": [],
        "steps_b": [],
        "support": [],
        "contact": "TBD",
        "work_rules": [],
        "special_notice": "내용 추가 예정",
        "exit_condition": "내용 추가 예정",
    },
}

# ─────────────────────────────────────────────────────
# 커스텀 CSS
# ─────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 2rem; max-width: 1400px; }
    header[data-testid="stHeader"] { display: none; }

    /* 상단 채널 태그 */
    .channel-tag {
        display: inline-block;
        color: white;
        padding: 5px 12px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
        border-radius: 4px;
        margin-right: 12px;
        vertical-align: middle;
    }
    .page-title {
        display: inline-block;
        font-size: 26px;
        font-weight: 700;
        color: #111827;
        vertical-align: middle;
    }
    .page-subtitle {
        color: #6b7280;
        font-size: 13px;
        margin-top: 6px;
    }

    /* 섹션 헤더 */
    .section-num {
        display: inline-block;
        background-color: #1f2937;
        color: white;
        width: 22px;
        height: 22px;
        text-align: center;
        line-height: 22px;
        font-size: 12px;
        font-weight: 700;
        border-radius: 4px;
        margin-right: 8px;
        vertical-align: middle;
    }
    .section-title {
        display: inline-block;
        font-size: 17px;
        font-weight: 700;
        color: #111827;
        vertical-align: middle;
    }
    .section-wrap { margin: 24px 0 12px 0; }

    /* 안내 배너 */
    .info-banner {
        background-color: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 6px;
        padding: 14px 18px;
        font-size: 13px;
        color: #1e3a8a;
        margin: 16px 0 24px 0;
    }
    .info-banner a { color: #1d4ed8; font-weight: 600; }

    /* 카드 공통 */
    .card {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 22px 24px;
        background: white;
    }

    /* 메트릭 카드 */
    .metric-label {
        font-size: 13px;
        color: #6b7280;
        margin-bottom: 14px;
        font-weight: 500;
    }
    .metric-label-sub {
        font-size: 11px;
        color: #9ca3af;
        font-weight: 400;
        margin-left: 4px;
    }
    .metric-value {
        font-size: 30px;
        font-weight: 700;
        color: #111827;
        line-height: 1.2;
    }
    .metric-unit {
        font-size: 15px;
        font-weight: 500;
        color: #6b7280;
    }
    .metric-divider {
        color: #d1d5db;
        margin: 0 6px;
        font-weight: 300;
    }
    .metric-caption {
        font-size: 12px;
        color: #9ca3af;
        margin-top: 10px;
    }
    .metric-none {
        font-size: 24px;
        font-weight: 700;
        color: #111827;
    }

    /* 절차 카드 */
    .step-card-header {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 8px;
        padding-bottom: 12px;
        border-bottom: 1px solid #e5e7eb;
    }
    .step-card-title { font-size: 14px; font-weight: 700; color: #111827; }
    .step-card-count { font-size: 11px; color: #9ca3af; }

    .step-item {
        display: flex;
        align-items: flex-start;
        padding: 12px 0;
        border-bottom: 1px dashed #e5e7eb;
    }
    .step-item:last-child { border-bottom: none; padding-bottom: 0; }
    .step-circle {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #2563eb;
        color: white;
        width: 24px;
        height: 24px;
        font-size: 12px;
        font-weight: 700;
        border-radius: 50%;
        margin-right: 12px;
        flex-shrink: 0;
        margin-top: 1px;
    }
    .step-text { flex: 1; }
    .step-title { font-size: 13.5px; font-weight: 600; color: #111827; }
    .step-sub { font-size: 12px; color: #6b7280; margin-top: 3px; }

    /* 지원/근무 카드 */
    .support-title {
        font-size: 14px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 12px;
        padding-bottom: 10px;
        border-bottom: 1px solid #e5e7eb;
    }
    .bullet-list { list-style: none; padding: 0; margin: 0; }
    .bullet-list li {
        position: relative;
        padding-left: 14px;
        margin-bottom: 10px;
        font-size: 13.5px;
        color: #374151;
        line-height: 1.5;
    }
    .bullet-list li:before {
        content: "•"; position: absolute; left: 0; color: #6b7280;
    }
    .contact-box {
        margin-top: 14px;
        padding: 12px 14px;
        background: #f9fafb;
        border-radius: 4px;
        border-left: 3px solid #2563eb;
    }
    .contact-label { color: #6b7280; font-size: 11px; }
    .contact-name { color: #111827; font-weight: 600; font-size: 13.5px; margin-top: 2px; }

    /* 알림 박스 */
    .alert-warn {
        background-color: #fffbeb;
        border: 1px solid #fde68a;
        border-left: 4px solid #f59e0b;
        border-radius: 6px;
        padding: 14px 18px;
    }
    .alert-info {
        background-color: #eff6ff;
        border: 1px solid #bfdbfe;
        border-left: 4px solid #2563eb;
        border-radius: 6px;
        padding: 14px 18px;
    }
    .alert-header { margin-bottom: 6px; }
    .alert-title {
        font-size: 13px;
        font-weight: 700;
        color: #111827;
        margin-right: 8px;
    }
    .alert-tag {
        display: inline-block;
        font-size: 10px;
        padding: 2px 8px;
        border-radius: 3px;
        font-weight: 700;
        vertical-align: middle;
    }
    .alert-tag-warn { background-color: #f59e0b; color: white; }
    .alert-tag-info { background-color: #2563eb; color: white; }
    .alert-body { font-size: 13px; color: #374151; line-height: 1.6; }

    .footer-note {
        text-align: right;
        font-size: 11px;
        color: #9ca3af;
        margin-top: 32px;
        padding-top: 16px;
        border-top: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# 사이드바: 채널 선택
# ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏬 유통점 채널")
    st.caption("하나투어 · 채널별 입점 안내")
    selected_channel = st.selectbox(
        "채널 선택",
        list(CHANNELS.keys()),
        index=0,
    )
    st.divider()
    st.caption("문의: 영업전략팀")

# ─────────────────────────────────────────────────────
# 헬퍼 함수
# ─────────────────────────────────────────────────────
def section_header(num: int, title: str):
    st.markdown(
        f'<div class="section-wrap">'
        f'<span class="section-num">{num}</span>'
        f'<span class="section-title">{title}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

def render_steps(steps: list, total: int):
    items_html = ""
    for i, (title, sub) in enumerate(steps, 1):
        sub_html = f'<div class="step-sub">{sub}</div>' if sub else ""
        items_html += (
            f'<div class="step-item">'
            f'<div class="step-circle">{i}</div>'
            f'<div class="step-text">'
            f'<div class="step-title">{title}</div>'
            f'{sub_html}'
            f'</div></div>'
        )
    return items_html

# ─────────────────────────────────────────────────────
# 본문: 선택된 채널 상세
# ─────────────────────────────────────────────────────
data = CHANNELS[selected_channel]

# ① 상단 헤더
col1, col2, col3 = st.columns([6, 1.2, 1.5])
with col1:
    st.markdown(
        f'<span class="channel-tag" style="background-color:{data["tag_color"]};">{data["tag"]}</span>'
        f'<span class="page-title">{selected_channel} 신규입점 절차</span>'
        f'<div class="page-subtitle">{data["subtitle"]}</div>',
        unsafe_allow_html=True,
    )
with col2:
    st.link_button("유통점 모집공고", data["notice_url"], use_container_width=True)
with col3:
    st.link_button("입점제안서 양식 다운로드", data["proposal_url"],
                   type="primary", use_container_width=True)

# ② 안내 배너
st.markdown(
    f'<div class="info-banner">'
    f'<b><a href="{data["notice_url"]}">[유통점 모집공고]</a></b>에서 모집 조건 확인 후 문의 부탁드립니다. '
    f'동일 점포에 복수 지원 시 내부 평가지표에 근거하여 평가 진행 후 선정합니다.'
    f'</div>',
    unsafe_allow_html=True,
)

# ③ 임대 · 관리비
section_header(1, "임대 · 관리비")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        f'<div class="card">'
        f'<div class="metric-label">보증금</div>'
        f'<div class="metric-none">{data["deposit"]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
with c2:
    if data["rent_dual"] != "-":
        rent_html = (
            f'<span class="metric-value">{data["rent_dual"]}</span>'
            f'<span class="metric-unit">만원</span>'
            f'<span class="metric-divider"> / </span>'
            f'<span class="metric-value">{data["rent_solo"]}</span>'
            f'<span class="metric-unit">만원</span>'
        )
    else:
        rent_html = f'<div class="metric-none">{data["rent_caption"]}</div>'
    st.markdown(
        f'<div class="card">'
        f'<div class="metric-label">임대료<span class="metric-label-sub">(계약관계 기준)</span></div>'
        f'<div>{rent_html}</div>'
        f'<div class="metric-caption">{data["rent_caption"]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        f'<div class="card">'
        f'<div class="metric-label">관리비</div>'
        f'<div class="metric-none">{data["mgmt_fee"]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

# ④ 입점 절차
section_header(2, "입점 절차")

c1, c2 = st.columns(2)
with c1:
    if data["steps_a"]:
        items = render_steps(data["steps_a"], len(data["steps_a"]))
        st.markdown(
            f'<div class="card">'
            f'<div class="step-card-header">'
            f'<span class="step-card-title">A. 공식인증예약센터</span>'
            f'<span class="step-card-count">총 {len(data["steps_a"])}단계</span>'
            f'</div>{items}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="card">정보 추가 예정</div>', unsafe_allow_html=True)

with c2:
    if data["steps_b"]:
        items = render_steps(data["steps_b"], len(data["steps_b"]))
        st.markdown(
            f'<div class="card">'
            f'<div class="step-card-header">'
            f'<span class="step-card-title">B. 일반대리점</span>'
            f'<span class="step-card-count">총 {len(data["steps_b"])}단계</span>'
            f'</div>{items}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="card">정보 추가 예정</div>', unsafe_allow_html=True)

# ⑤ 지원 방법 / 근무 규정
st.markdown('<div style="height: 16px;"></div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    if data["support"]:
        bullets = "".join([f"<li>{s}</li>" for s in data["support"]])
        st.markdown(
            f'<div class="card">'
            f'<div class="support-title">지원 방법</div>'
            f'<ul class="bullet-list">{bullets}</ul>'
            f'<div class="contact-box">'
            f'<div class="contact-label">영업전략팀 담당자</div>'
            f'<div class="contact-name">{data["contact"]}</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="card">정보 추가 예정</div>', unsafe_allow_html=True)

with c2:
    if data["work_rules"]:
        bullets = "".join([f"<li>{r}</li>" for r in data["work_rules"]])
        st.markdown(
            f'<div class="card">'
            f'<div class="support-title">근무 규정</div>'
            f'<ul class="bullet-list">{bullets}</ul>'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="card">정보 추가 예정</div>', unsafe_allow_html=True)

# ⑥ 특이사항 · 퇴점 안내
section_header(3, "특이사항 · 퇴점 안내")

c1, c2 = st.columns(2)
with c1:
    st.markdown(
        f'<div class="alert-warn">'
        f'<div class="alert-header">'
        f'<span class="alert-title">특이사항</span>'
        f'<span class="alert-tag alert-tag-warn">주의</span>'
        f'</div>'
        f'<div class="alert-body">{data["special_notice"]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f'<div class="alert-info">'
        f'<div class="alert-header">'
        f'<span class="alert-title">퇴점 내용</span>'
        f'<span class="alert-tag alert-tag-info">중요</span>'
        f'</div>'
        f'<div class="alert-body">{data["exit_condition"]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

# ⑦ 푸터
st.markdown(
    '<div class="footer-note">본 안내는 신규입점 가이드용이며, 세부 조건은 영업전략팀 확인을 권장합니다.</div>',
    unsafe_allow_html=True,
)
