import streamlit as st
import random
import logic  # 기존 logic.py 사용
import constants as c  # 기존 constants.py 사용

# 게임 상태 초기화
if "matrix" not in st.session_state:
    st.session_state.matrix = logic.new_game(c.GRID_LEN)
    st.session_state.history = []

# 게임 상태 업데이트 함수
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
st.write("Use the arrow keys to play the game.")

# 그리드 그리기
draw_grid()

# JavaScript를 사용하여 키보드 입력 감지
st.markdown(
    """
    <script>
    document.addEventListener("keydown", function(e) {
        let direction = null;
        if (e.key === "ArrowUp") {
            direction = "up";
        } else if (e.key === "ArrowDown") {
            direction = "down";
        } else if (e.key === "ArrowLeft") {
            direction = "left";
        } else if (e.key === "ArrowRight") {
            direction = "right";
        }
        if (direction) {
            fetch("/_st_keypress", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({direction: direction}),
            });
        }
    });
    </script>
    """,
    unsafe_allow_html=True,
)

# Streamlit 서버에 키보드 입력 전달
from streamlit.runtime.scriptrunner import add_request_handler

def keypress_handler(data):
    if "direction" in data:
        update_matrix(data["direction"])
    return {"success": True}

add_request_handler("/_st_keypress", keypress_handler)

# 게임 메시지 출력
if "message" in st.session_state:
    st.subheader(st.session_state.message)
