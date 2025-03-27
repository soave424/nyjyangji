import streamlit as st


def main():
    st.title('구글 시트 보기')

    # 제공된 구글 시트 링크
    sheet_url = 'https://docs.google.com/spreadsheets/d/1jZWdoiz9J7WSHSrwgYSDjNqmOqPe0u52ZPlON6mEH9w/edit?usp=sharing'

    # IFRAME으로 구글 시트 임베드
    st.components.v1.iframe(sheet_url, height=600, scrolling=True, width=800)


if __name__ == '__main__':
    main()
