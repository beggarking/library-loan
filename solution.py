# 도서관 대출 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

BOOKS = ("B001", "B002", "B003", "B004", "B005")
LOAN_DAYS = 14
MAX_LOANS = 3


def _valid_day(day):
    # 1 이상의 정수만 허용 (True/False 는 정수로 보지 않음)
    return isinstance(day, int) and not isinstance(day, bool) and day >= 1


def _valid_book(book_id):
    # 리스트 같은 해시 불가능한 값이 들어와도 에러 없이 False 가 되도록 튜플로 비교
    return book_id in BOOKS


class LibraryLoan:
    def __init__(self):
        # book_id -> (name, 빌린 날)
        self._loans = {}
        # (name, 정지 시작일, 정지 마지막 날) 목록 (이름이 어떤 값이어도 에러 없도록 리스트로 보관)
        self._suspensions = []

    def _is_suspended(self, name, day):
        # 정지 기간은 "반납한 날부터" 이므로 그 구간 안의 날짜만 막음 (날짜 순서는 검사하지 않음).
        # 기간이 겹치면 구간이 이어져 더 늦게 끝나는 쪽까지 막히고, 일수를 더하지는 않음
        return any(n == name and start <= day <= end for n, start, end in self._suspensions)

    def _held_by(self, name):
        # 그 사람이 지금 빌리고 있는 (book_id, 반납 기한) 목록
        return [(b, d + LOAN_DAYS) for b, (n, d) in self._loans.items() if n == name]

    def borrow(self, book_id, name, day):
        # 1. 없는 책 번호
        if not _valid_book(book_id):
            return False
        # 2. day 가 1 이상의 정수가 아님
        if not _valid_day(day):
            return False
        # 3. 이미 누군가 빌려 간 책
        if book_id in self._loans:
            return False
        held = self._held_by(name)
        # 4. 이미 3권을 빌리고 있음
        if len(held) >= MAX_LOANS:
            return False
        # 5. 반납 기한이 지난 책을 갖고 있음 (day > 반납 기한)
        if any(day > due for _, due in held):
            return False
        # 6. 대출 정지 기간
        if self._is_suspended(name, day):
            return False

        self._loans[book_id] = (name, day)
        return True

    def return_book(self, book_id, name, day):
        if not _valid_book(book_id) or not _valid_day(day):
            return -1
        loan = self._loans.get(book_id)
        # 그 사람이 빌리고 있지 않음 (남이 빌린 책, 빌리지 않은 책, 이미 반납한 책)
        if loan is None or loan[0] != name:
            return -1
        borrowed_day = loan[1]
        # 빌린 날보다 이른 날짜
        if day < borrowed_day:
            return -1

        overdue = max(0, day - (borrowed_day + LOAN_DAYS))
        del self._loans[book_id]

        if overdue > 0:
            # 반납한 날부터 연체 일수만큼 정지 → day ~ day + overdue - 1
            self._suspensions.append((name, day, day + overdue - 1))
        return overdue

    def get_loans(self, name):
        # 반납 기한 순, 같으면 책 번호 순
        return sorted(self._held_by(name), key=lambda x: (x[1], x[0]))
