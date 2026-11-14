import json
import os

# 퀴즈 클래스 정의
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self):
        print(f"\n[문제] {self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice}")

    def is_correct(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }


# 설정 및 기본 데이터
QUIZ_FILE = "quiz_data.json"
SAVE_FILE = "save_data.json"

DEFAULT_QUIZ_DATA = [
    {
        "question": f"문제{i}",
        "choices": ["선택1", "선택2", "선택3", "선택4"],
        "answer": 1
    }
    for i in range(1, 21)
]


# 퀴즈 데이터 로드 및 손상 시 복구
def load_quiz_data():
    try:
        if not os.path.exists(QUIZ_FILE):
            raise FileNotFoundError

        with open(QUIZ_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Quiz(**d) for d in data]

    except (FileNotFoundError, json.JSONDecodeError):
        print("\n퀴즈 파일이 없거나 손상되었습니다.")
        print("기본 데이터로 복구합니다.")

        with open(QUIZ_FILE, "w", encoding="utf-8") as f:
            json.dump(
                DEFAULT_QUIZ_DATA,
                f,
                ensure_ascii=False,
                indent=4
            )

        return [Quiz(**d) for d in DEFAULT_QUIZ_DATA]


# 퀴즈 데이터 저장
def save_quiz_data(quiz_list):
    with open(QUIZ_FILE, "w", encoding="utf-8") as f:
        data = [quiz.to_dict() for quiz in quiz_list]
        json.dump(data, f, ensure_ascii=False, indent=4)


# 공통 입력 검증 함수
def get_valid_input(prompt, min_val, max_val):
    while True:
        user_input = input(prompt).strip()

        if not user_input:
            print("입력이 비어있습니다. 다시 입력해주세요.")
            continue

        try:
            choice = int(user_input)

            if min_val <= choice <= max_val:
                return choice
            else:
                print(
                    f"잘못된 입력입니다. "
                    f"{min_val}에서 {max_val} 사이의 숫자를 입력해주세요."
                )

        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력해주세요.")


# 새로운 퀴즈 추가
def add_quiz(quiz_list):
    print("\n------ 새로운 퀴즈 추가 ------")

    question = input("문제를 입력하세요: ").strip()

    choices = []

    for i in range(1, 5):
        choice = input(f"선택지 {i}를 입력하세요: ").strip()
        choices.append(choice)

    answer = get_valid_input(
        "정답 번호를 입력하세요 (1-4): ", 1, 4
    )

    new_quiz = Quiz(question, choices, answer)
    quiz_list.append(new_quiz)

    save_quiz_data(quiz_list)

    print("새로운 퀴즈가 추가되었습니다!")


# 진행 상황 저장
def save_progress(index, score):
    data = {
        "last index": index,
        "score": score
    }

    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )


# 진행 상황 불러오기
def load_progress():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            if (
                isinstance(data, dict)
                and type(data.get("last index")) is int
                and type(data.get("score")) is int
                and data["last index"] >= 0
                and 0 <= data["score"] <= data["last index"]
            ):
                return data

        except (json.JSONDecodeError, OSError):
            pass

        print("저장 기록이 손상되었습니다. 새 게임을 시작합니다.")

    return None


# 메인 게임 로직
def start_quiz(quiz_list):
    if not quiz_list:
        print("\n퀴즈 데이터가 없습니다.")
        print("먼저 문제를 추가해주세요.")
        return

    progress = load_progress()

    start_index = 0
    score = 0

    # 이전 기록 확인
    if progress:
        saved_index = progress["last index"]
        saved_score = progress["score"]

        if saved_index < len(quiz_list):
            print("\n이전 기록이 있습니다.")
            print(f"진행 위치: {saved_index + 1}번 문제")
            print(f"현재 점수: {saved_score}개 정답")

            while True:
                yn = input(
                    "이어서 하시겠습니까? (y/n): "
                ).strip().lower()

                if yn == "y":
                    start_index = saved_index
                    score = saved_score
                    break

                elif yn == "n":
                    start_index = 0
                    score = 0
                    print("\n새 게임을 시작합니다.")
                    break

                else:
                    print("y 또는 n을 입력해주세요.")

    print("\n퀴즈를 시작합니다!")

    next_index = start_index

    try:
        # 시작 위치 및 점수 저장
        save_progress(next_index, score)

        for i in range(start_index, len(quiz_list)):
            quiz = quiz_list[i]

            print(f"\n진행 상황: {i + 1}/{len(quiz_list)}")

            quiz.display()

            user_answer = get_valid_input(
                "정답 번호를 입력하세요: ",
                1,
                len(quiz.choices)
            )

            if quiz.is_correct(user_answer):
                print("정답입니다!")
                score += 1

            else:
                print(
                    f"틀렸습니다. "
                    f"정답은 {quiz.answer}번입니다."
                )

            # 다음 문제 위치와 점수 자동 저장
            next_index = i + 1
            save_progress(next_index, score)

        # 모든 문제 완료
        print("\n" + "=" * 30)
        print("      🎉 퀴즈 종료 🎉")
        print(f"   맞은 개수: {score} / {len(quiz_list)}")
        print(
            f"   최종 점수: "
            f"{int(score / len(quiz_list) * 100)}점"
        )
        print("=" * 30)

        # 퀴즈 완료 시 세이브 파일 삭제
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
            print("\n퀴즈 완료! 저장 기록이 삭제되었습니다.")

    except (KeyboardInterrupt, EOFError):
        print("\n퀴즈가 중단되었습니다.")
        print("현재까지 진행 상황을 저장합니다.")

        save_progress(next_index, score)
        return


# 메인 메뉴
def main():
    quiz_list = load_quiz_data()

    while True:
        print("\n" + "=" * 30)
        print("       🎮 퀴즈 게임 🎮")
        print("=" * 30)
        print("1. 퀴즈 시작")
        print("2. 새로운 퀴즈 추가")
        print("3. 종료")
        print("=" * 30)

        try:
            menu = get_valid_input(
                "메뉴를 선택하세요 (1-3): ", 1, 3
            )

            if menu == 1:
                start_quiz(quiz_list)

            elif menu == 2:
                add_quiz(quiz_list)

            elif menu == 3:
                print("\n게임을 종료합니다.")
                break

        except (KeyboardInterrupt, EOFError):
            print("\n게임을 종료합니다.")
            break


# 프로그램 실행
if __name__ == "__main__":
    main()
