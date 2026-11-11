import json
import os

# 퀴즈 클래스 정의
class Quiz:
    def __init__(self, question, choices,answer):
        self.question = question
        self.choices = choices
        self.answer = answer
    def display(self):
        print(f"\n[문제]{self.question}")
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
    {"question": "문제1", "choices": ["선택1", "선택2", "선택3", "선택4"], "answer": 1},
    {"question": "문제2", "choices": ["선택1", "선택2", "선택3", "선택4"], "answer": 1},
    {"question": "문제3", "choices": ["선택1", "선택2", "선택3", "선택4"], "answer": 1},
    {"question": "문제4", "choices": ["선택1", "선택2", "선택3", "선택4"], "answer": 1},
    {"question": "문제5", "choices": ["선택1", "선택2", "선택3", "선택4"], "answer": 1},
    {"question": "문제6", "choices": ["선택1", "선택2", "선택3", "선택4"], "answer": 1},
    {"question": "문제7", "choices": ["선택1", "선택2", "선택3", "선택4"], "answer": 1},
    {"question": "문제8", "choices": ["선택1", "선택2", "선택3", "선택4"], "answer": 1},
    {"question": "문제9", "choices": ["선택1", "선택2", "선택3", "선택4"], "answer": 1},
    {"question": "문제10", "choices": ["선택1", "선택2", "선택3", "선택4"], "answer": 1},
    {"question": "문제11", "choices": ["선택1", "선택2", "선택3", "선택4"],"answer": 1},
    {"question": "문제12","choices":["선택1","선택2","선택3","선택4"],"answer": 1},
    {"question":"문제13","choices":["선택1","선택2","선택3","선택4"],"answer": 1},
    {"question":"문제14","choices":["선택1","선 택2","선택3","선택4"],"answer": 1},
    {"question":"문제15","choices":["선택1","선택2","선택3","선택4"],"answer": 1},
    {"question":"문제16","choices":["선택1","선택2","선택3","선택4"],"answer": 1},
    {"question":"문제17","choices":["선택1","선택2","선택3","선택4"],"answer": 1},
    {"question":"문제18","choices":["선택1","선택2","선택3","선택4"],"answer": 1},
    {"question":"문제19","choices":["선택1","선택2","선택3","선택4"],"answer": 1},
    {"question":"문제20","choices":["선택1","선택2","선택3","선택4"],"answer": 1}
]

# 퀴즈 데이터 로드 및 손상시 복구
def load_quiz_data():
    try:
        if not os.path.exists(QUIZ_FILE):
            raise FileNotFoundError
    
        with open(QUIZ_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Quiz(**d) for d in data]

    except (FileNotFoundError, json.JSONDecodeError):
        print("\n 퀴즈 파일이 없거나 손상되었습니다. 기본 데이터로 복구합니다.")
        with open(QUIZ_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_QUIZ_DATA, f, ensure_ascii=False, indent=4)
        return [Quiz(**d) for d in DEFAULT_QUIZ_DATA]

# 저장 및 불러오기 기능
def save_progress(index, score):
    data = {"last index": index, "score": score}
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_progress():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError):
            return None
    return None


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
                print(f"잘못된 입력입니다. {min_val}에서 {max_val} 사이의 숫자를 입력해주세요.")
        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력해주세요.")

# 메인 게임 로직

def start_quiz(quiz_list):
    progress = load_progress()
    start_index = 0
    score = 0

    if progress:
        print(f"\n 이전 기록이 있습니다. (문제 {progress['last index'] +1}번부터, 점수: {progress['score']})")
        yn = input("이어서 하시겠습니까?(y/n): ").lower()
        if yn == 'y':
            start_index = progress['last index']
            score = progress['score']

    print("\n 퀴즈를 시작합니다!")

    try:
        for i in range(start_index, len(quiz_list)):
            quiz = quiz_list[i]
            quiz.display()

            user_answer = get_valid_input("정답 번호를 입력하세요: ", 1, 4)

            if quiz.is_correct(user_answer):
                print("정답입니다!")
                score += 1
            else:
                print(f"틀렸습니다. 정답은 {quiz.answer}번입니다.") 

        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        
        print("\n========================================")
        print("\n         모든 문제를 풀었습니다!")
        print(f"\n             최종점수 : {score}/{len(quiz_list)}")
        print("\n========================================")

    except (KeyboardInterrupt, EOFError):
        print("\n 퀴즈가 중단되었습니다. 현재까지 상황을 저장합니다")
        save_progress(i, score)
        raise

def main():
    quiz_list = load_quiz_data()

    try:
        while True:
            print("========================================")
            print("               퀴즈 맞추기               ")
            print("========================================")
            print("1. 시작하기")
            print("2. 종료하기")
            print("========================================")

            choice = get_valid_input("메뉴 번호를 입력하세요: ", 1, 2)

            if choice == 1: 
                start_quiz(quiz_list)
            elif choice == 2:
                print ("\n 퀴즈를 종료합니다!")
                break
    except (KeyboardInterrupt, EOFError):
        print("\n 강제 종료 신호를 감지했습니다. 안전하게 종료합니다")

if __name__ == "__main__":
    main()