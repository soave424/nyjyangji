import streamlit as st
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import pytz

# MongoDB 연결 설정
MONGO_URI = "mongodb+srv://soave424:dlwhdms424!@yourcluster.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["maintenance_db"]  # 데이터베이스 이름
collection = db["requests"]  # 컬렉션 이름


def load_data():
    """MongoDB에서 데이터 불러오기"""
    data = list(collection.find({}, {"_id": 0}))  # _id 제외하고 가져오기
    return pd.DataFrame(data)


def save_data(new_entry):
    """MongoDB에 데이터 추가"""
    collection.insert_one(new_entry)


# 데이터 불러오기
data = load_data()

# 화면 레이아웃을 넓게 설정
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
st.title("🏫 유지보수 서비스 신청 게시판")

# 레이아웃 설정
col1, col2 = st.columns([2, 3])

# 왼쪽: 신청 폼
with col1:
    st.header("📝 신청하기")
    with st.form("request_form"):
        applicant = st.text_input("신청자 이름", "")
        floor = st.selectbox("교실 위치(층)", [1, 2, 3, 4, 5])
        classroom = st.text_input("교실명", "")
        content = st.text_area("유지보수 신청 내용", "")
        submit_request = st.form_submit_button("신청")

        if submit_request:
            if applicant and classroom and content:
                korea_tz = pytz.timezone('Asia/Seoul')
                date = datetime.now(korea_tz).strftime("%Y-%m-%d %a %H:%M:%S")
                new_entry = {
                    "date": date,
                    "applicant": applicant,
                    "floor": floor,
                    "classroom": classroom,
                    "content": content,
                    "status": "신청 완료",
                    "memo": ""
                }
                save_data(new_entry)
                st.success("✅ 신청이 완료되었습니다!")
                st.rerun()
            else:
                st.warning("⚠ 비어있는 내용이 있습니다.")

# 오른쪽: 신청 게시판
with col2:
    st.header("📋 신청 목록")
    pending_data = data[data["status"] == "신청 완료"]
    completed_data = data[data["status"] == "해결 완료"]

    st.subheader(f"🟠 해결 중 ({len(pending_data)}건)")
    if pending_data.empty:
        st.info("🚧 현재 신청 목록이 없습니다.")
    else:
        for idx, row in pending_data.iterrows():
            with st.expander(f"[{row['floor']}층_{row['classroom']}] {row['content'][:20]}...   ({row['date']})"):
                st.write(f"**신청자:** {row['applicant']}")
                st.write(f"**교실 위치:** {row['floor']}층 {row['classroom']}")
                st.write(f"**신청 내용:** {row['content']}")
                st.write(f"**해결 상태:** {row['status']}")
                st.write(f"**메모:** {row['memo']}")

                # 상태 변경 폼
                with st.form(key=f"status_form_{idx}"):
                    status = st.selectbox("상태 변경", ["해결 완료", "신청 완료"], index=0)
                    memo = st.text_area(
                        "메모 입력", placeholder="특이사항이 있는 경우 작성해주세요.")
                    submit_status = st.form_submit_button("확인")

                    if submit_status:
                        collection.update_one({"date": row["date"]}, {
                                              "$set": {"status": status, "memo": memo}})
                        st.success("✅ 상태가 업데이트되었습니다!")
                        st.rerun()

    st.subheader(f"✅ 완료 목록 ({len(completed_data)}건)")
    if completed_data.empty:
        st.info("🔹 해결된 요청이 없습니다.")
    else:
        for idx, row in completed_data.iterrows():
            with st.expander(f"[{row['floor']}층_{row['classroom']}] {row['content'][:20]}...   ({row['date']})"):
                st.write(f"**신청자:** {row['applicant']}")
                st.write(f"**교실 위치:** {row['floor']}층 {row['classroom']}")
                st.write(f"**신청 내용:** {row['content']}")
                st.write(f"**해결 상태:** {row['status']}")
                st.write(f"**메모:** {row['memo']}")
