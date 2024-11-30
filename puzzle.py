import streamlit as st
import random
import logic  # 기존의 logic.py를 사용
import constants as c  # 기존의 constants.py를 사용

# 게임 상태 초기화
if "matrix" not in st.session_state:
    st.session_state.matrix = logic.new_game(c.GRID_LEN)
    st.session_state.history = []

# 게임 상태 업데이트
def update_matrix(direction):
    matrix = st.session_state.matrix
    commands = {
        "up": logic.up,
        "down": logic.down,
        "left": logic.left,
        "right": logic.right,
    }
    if direction in commands:
        new_matrix, done = commands[direction](matrix)
        if done:
            st.session_state.matrix = logic.add_two(new_matrix)
            st.session_state.history.append(matrix)
        if logic.game_state(st.session_state.matrix) == 'win':
            st.session_state.message = "You Win!"
        elif logic.game_state(st.session_state.matrix) == 'lose':
            st.session_state.message = "You Lose!"

# 게임 화면 그리기
def draw_grid():
    for row in st.session_state.matrix:
        cols = st.columns(c.GRID_LEN)
        for idx, cell in enumerate(row):
            color = (
                c.BACKGROUND_COLOR_DICT[cell]
                if cell != 0
                else c.BACKGROUND_COLOR_CELL_EMPTY
            )
            cols[idx].markdown(
                f"<div style='background-color: {color}; "
                f"text-align: center; font-size: 24px; "
                f"border-radius: 5px; padding: 10px;'>"
                f"{cell if cell != 0 else ''}</div>",
                unsafe_allow_html=True,
            )

# UI 구성
st.title("2048 Game")
st.write("Use the buttons below to play the game.")

# 그리드 그리기
draw_grid()

# 방향 버튼
col1, col2, col3, col4 = st.columns(4)
if col1.button("⬆️"):
    update_matrix("up")
if col2.button("⬅️"):
    update_matrix("left")
if col3.button("➡️"):
    update_matrix("right")
if col4.button("⬇️"):
    update_matrix("down")

# 뒤로 가기 버튼
if st.button("Undo"):
    if st.session_state.history:
        st.session_state.matrix = st.session_state.history.pop()

# 게임 메시지 출력
if "message" in st.session_state:
    st.subheader(st.session_state.message)
