# 도서관 대출 웹 — 대출 규칙은 전부 solution.py 의 LibraryLoan 이 판단합니다. (웹에는 규칙 없음)
import re

from flask import Flask, jsonify, render_template, request

from solution import LibraryLoan

app = Flask(__name__)

# 서버 전체에서 하나만 만들어 계속 사용 → 지금까지의 대출 기록을 기억
lib = LibraryLoan()


def to_number(text):
    # 웹 입력은 글자로 들어오므로 "10" 같은 정수 모양만 int 로 바꿈.
    # "2.5" 는 float, 그 밖의 값은 글자 그대로 넘겨서 solution.py 가 거절하게 둠.
    text = (text or "").strip()
    if re.fullmatch(r"[+-]?\d+", text):
        return int(text)
    try:
        return float(text)
    except ValueError:
        return text


def form_text(key):
    return (request.form.get(key) or "").strip()


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/borrow")
def borrow():
    name = form_text("name")
    ok = lib.borrow(form_text("book_id"), name, to_number(request.form.get("day")))
    return jsonify(ok=ok is True, loans=lib.get_loans(name))


@app.post("/return")
def return_book():
    name = form_text("name")
    overdue = lib.return_book(form_text("book_id"), name, to_number(request.form.get("day")))
    # solution.py 는 실패하면 -1, 성공하면 연체 일수(0 이상)를 돌려줌
    return jsonify(ok=overdue != -1, overdue=overdue, loans=lib.get_loans(name))


@app.get("/loans")
def loans():
    return jsonify(loans=lib.get_loans((request.args.get("name") or "").strip()))


if __name__ == "__main__":
    app.run(debug=True)
