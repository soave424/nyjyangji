import streamlit as st

st.set_page_config(layout="wide",  initial_sidebar_state="collapsed")


def main():
    st.title('남양주양지초 2025 유지보수 신청')
    # 제공된 구글 시트 링크
    sheet_url = 'https://docs.google.com/spreadsheets/d/1jZWdoiz9J7WSHSrwgYSDjNqmOqPe0u52ZPlON6mEH9w/edit?usp=sharing'

    st.markdown("유지보수 신청을 구글 시트 작성으로 바꾸었습니다. 순서대로 작성해주세요.")

    st.link_button("구글 시트 바로가기", sheet_url)

    # IFRAME으로 구글 시트 임베드
    st.components.v1.iframe(sheet_url, height=800,
                            scrolling=True, width=1200)


if __name__ == '__main__':
    main()
