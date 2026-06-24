import streamlit as st

# ─────────────────────────────────────────────────────
# 페이지 기본 설정
# ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="유통점 채널 대시보드",
    page_icon="🏬",
    layout="wide",
)

# ─────────────────────────────────────────────────────
# 채널 데이터 (이 부분만 수정하면 채널 추가/변경 가능)
# ─────────────────────────────────────────────────────
CHANNELS = {
    "홈플러스": {
        "icon": "🏬",
        "category": "대형마트",
        "status": "운영중",
        "deposit": "없음",
        "rent": "듀얼 70 / 단독 80만원",
        "mgmt_fee": "없음",
        "commission": "-1단계",
        "exit_notice": "30일 전",
        "contact": "이강일B / 노태성",
        "notice_url": "https://app.notion.com/p/e95a5614ef634ab5bd48e6c9df5f4bbf",
        "proposal_url": "#",
        "steps_a": [
            ("입점제안서 제출", None),
            ("선정 품의 진행", "영업전략팀 상신"),
            ("전자계약 체결", "글로싸인 발송"),
            ("관광사업자 및 사업자 등록", "주소변경"),
        ],
        "steps_b": [
            ("입점제안서 제출", None),
            ("공식인증 개설 신청 관련서류 게시판 등록 및 신용정보조회",
             "개설 품의 작성 제외 — 영업전략팀 선정 품의로 갈음"),
            ("선정 품의 진행", "영업전략팀 상신"),
            ("전자계약 체결", "글로싸인 발송"),
            ("관광사업자 및 사업자 등록", "주소변경"),
        ],
        "work_rules": [
            "근무 시 출입증(명찰) 패용",
            "홈플러스 매장 영업시간 준수",
            "부재 시 **부재 중 팻말 + 점포 담당자 소통 필수**",
        ],
        "special_notice": "홈플러스 입점 대리점은 등급커미션 **−1단계** 적용",
        "exit_condition": "하나투어 → 홈플러스 공문 발송일 기준 **최소 30일 전** 퇴점 내용 공유 시 중도퇴점 패널티 면제",
    },
    "이마트": {
        "icon": "🛒",
        "category": "대형마트",
        "status": "운영중",
        "deposit": "TBD",
        "rent": "TBD",
        "mgmt_fee": "TBD",
        "commission": "TBD",
        "exit_notice": "TBD",
        "contact": "TBD",
        "notice_url": "#",
        "proposal_url": "#",
        "steps_a": [],
        "steps_b": [],
        "work_rules": [],
        "special_notice": "내용 추가 예정",
        "exit_condition": "내용 추가 예정",
    },
    "롯데마트": {
        "icon": "🏪",
        "category": "대형마트",
        "status": "준비중",
        "deposit": "TBD",
        "rent": "TBD",
        "mgmt_fee": "TBD",
        "commission": "TBD",
        "exit_notice": "TBD",
        "contact": "TBD",
        "notice_url": "#",
        "proposal_url": "#",
        "steps_a": [],
        "steps_b": [],
        "work_rules": [],
        "special_notice": "내용 추가 예정",
        "exit_condition": "내용 추가 예정",
    },
    "백화점": {
        "icon": "🏢",
        "category": "백화점",
        "status": "준비중",
        "deposit": "TBD",
        "rent": "TBD",
        "mgmt_fee": "TBD",
        "commission": "TBD",
        "exit_notice": "TBD",
        "contact": "TBD",
        "notice_url": "#",
        "proposal_url": "#",
        "steps_a": [],
        "steps_b": [],
        "work_rules": [],
        "special_notice": "내용 추가 예정",
        "exit_condition": "내용 추가 예정",
    },
}

# ─────────────────────────────────────────────────────
# 사이드바: 채널 선택
# ─────────────────────────────────────────────────────
with st.sidebar:
    st.title("🏬 유통점 채널")
    st.caption("하나투어 · 채널별 입점 안내")

    view_mode = st.radio(
        "보기 모드",
        ["전체 개요", "채널별 상세", "채널 비교"],
        index=0,
    )

    st.divider()

    if view_mode == "채널별 상세":
        selected_channel = st.selectbox(
            "채널 선택",
            list(CHANNELS.keys()),
            index=0,
        )
    else:
        selected_channel = None

    st.divider()
    st.caption("문의: 영업전략팀")

# ─────────────────────────────────────────────────────
# 채널 상세 렌더링 함수 (재사용)
# ─────────────────────────────────────────────────────
def render_channel_detail(name: str, data: dict):
    # 상단 헤더
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.title(f"{data['icon']} {name} 신규입점 절차")
        st.caption(f"{data['category']} · 유통점 입점 안내")
    with col2:
        st.link_button("유통점 모집공고", data["notice_url"], use_container_width=True)
    with col3:
        st.link_button("입점제안서 양식", data["proposal_url"],
                       type="primary", use_container_width=True)

    st.divider()

    # 안내 박스
    st.info(
        "📌 **유통점 모집공고**에서 조건 확인 후 문의 부탁드립니다.  \n"
        "동일 점포 복수 지원 시 내부 평가지표에 근거하여 평가 진행 후 선정됩니다."
    )

    # KPI 카드
    st.subheader("임대·관리비")
    k1, k2, k3 = st.columns(3)
    k1.metric("보증금", data["deposit"])
    k2.metric("임대료", data["rent"], help="계약관계 기준")
    k3.metric("관리비", data["mgmt_fee"])

    st.divider()

    # 입점 절차
    st.subheader("입점 절차")
    if data["steps_a"] or data["steps_b"]:
        tab_a, tab_b = st.tabs(["A. 공식인증예약센터", "B. 일반대리점"])
        with tab_a:
            for i, (title, sub) in enumerate(data["steps_a"], 1):
                with st.container(border=True):
                    st.markdown(f"### {i}단계 · {title}")
                    if sub:
                        st.caption(sub)
        with tab_b:
            for i, (title, sub) in enumerate(data["steps_b"], 1):
                with st.container(border=True):
                    st.markdown(f"### {i}단계 · {title}")
                    if sub:
                        st.caption(sub)
    else:
        st.warning("입점 절차 정보가 아직 등록되지 않았습니다.")

    st.divider()

    # 지원 방법 / 근무 규정
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("지원 방법")
        with st.container(border=True):
            st.write(
                "입점 희망 대리점과 소통하며 입점제안서 작성 후 "
                "**영업전략팀** 에게 쪽지 전달."
            )
            st.caption(f"담당자: {data['contact']}")
    with c2:
        st.subheader("근무 규정")
        with st.container(border=True):
            if data["work_rules"]:
                st.markdown("\n".join([f"- {rule}" for rule in data["work_rules"]]))
            else:
                st.caption("근무 규정 정보가 아직 등록되지 않았습니다.")

    st.divider()

    # 특이사항 / 퇴점 조건
    c3, c4 = st.columns(2)
    with c3:
        st.warning(f"⚠️ **특이사항**  \n{data['special_notice']}")
    with c4:
        st.success(f"✅ **퇴점 조건**  \n{data['exit_condition']}")

# ─────────────────────────────────────────────────────
# 메인 영역: 모드별 화면 분기
# ─────────────────────────────────────────────────────

# ===== ① 전체 개요 =====
if view_mode == "전체 개요":
    st.title("📊 유통점 채널 대시보드")
    st.caption("하나투어 · 전체 채널 한눈에 보기")
    st.divider()

    # 전체 KPI
    total = len(CHANNELS)
    active = sum(1 for d in CHANNELS.values() if d["status"] == "운영중")
    preparing = sum(1 for d in CHANNELS.values() if d["status"] == "준비중")

    k1, k2, k3 = st.columns(3)
    k1.metric("전체 채널", f"{total}개")
    k2.metric("운영중", f"{active}개")
    k3.metric("준비중", f"{preparing}개")

    st.divider()

    # 채널 카드 그리드
    st.subheader("채널 목록")
    cols = st.columns(2)
    for i, (name, data) in enumerate(CHANNELS.items()):
        with cols[i % 2]:
            with st.container(border=True):
                st.markdown(f"### {data['icon']} {name}")
                st.caption(f"{data['category']} · {data['status']}")
                sub_c1, sub_c2 = st.columns(2)
                sub_c1.metric("임대료", data["rent"])
                sub_c2.metric("커미션", data["commission"])
                st.caption(f"담당: {data['contact']}")

# ===== ② 채널별 상세 =====
elif view_mode == "채널별 상세":
    render_channel_detail(selected_channel, CHANNELS[selected_channel])

# ===== ③ 채널 비교 =====
elif view_mode == "채널 비교":
    st.title("📋 채널 비교")
    st.caption("주요 조건을 한눈에 비교")
    st.divider()

    import pandas as pd
    df = pd.DataFrame([
        {
            "채널": f"{d['icon']} {name}",
            "카테고리": d["category"],
            "상태": d["status"],
            "보증금": d["deposit"],
            "임대료": d["rent"],
            "관리비": d["mgmt_fee"],
            "커미션": d["commission"],
            "퇴점통보": d["exit_notice"],
            "담당자": d["contact"],
        }
        for name, d in CHANNELS.items()
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)
