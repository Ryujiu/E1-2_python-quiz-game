import json
import os

# 1. 퀴즈 클래스 정의
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

quiz_list = [
    Quiz("문제1", ["선택1", "선택2", "선택3", "선택4"], 1),
    Quiz("문제2", ["선택1", "선택2", "선택3", "선택4"], 1),
    Quiz("문제3", ["선택1", "선택2", "선택3", "선택4"], 1),
    Quiz("문제4", ["선택1", "선택2", "선택3", "선택4"], 1),
    Quiz("문제5", ["선택1", "선택2", "선택3", "선택4"], 1),
    Quiz("문제6", ["선택1", "선택2", "선택3", "선택4"], 1),
    Quiz("문제7", ["선택1", "선택2", "선택3", "선택4"], 1),
    Quiz("문제8", ["선택1", "선택2", "선택3", "선택4"], 1),
    Quiz("문제9", ["선택1", "선택2", "선택3", "선택4"], 1),
    Quiz("문제10", ["선택1", "선택2", "선택3", "선택4"], 1),
    Quiz("문제11", ["선택1", "선택2", "선택3", "선택4"], 1),
    Quiz("문제12", ["선택1", "선택2", "선택3", "선택4"], 1),
    Quiz("문제13", ["선택1", "선택2", "선택3", "선택4"], 1),
    Quiz("문제14", ["선택1", "선택2", "선택3", "선택4"], 1),
    Quiz("문제15", ["선택1", "선택2", "선택3", "선택4"], 1),
    Quiz("문제16", ["선택1", "선택2", "선택3", "선택4"], 1),
    Quiz("문제17", ["선택1", "선택2", "선택3", "선택4"], 1),
    Quiz("문제18", ["선택1", "선택2", "선택3", "선택4"], 1),
    Quiz("문제19", ["선택1", "선택2", "선택3", "선택4"], 1),
    Quiz("문제20", ["선택1", "선택2", "선택3", "선택4"], 1)
    ]

# 2. 공통 입력 검증 함수
def get_valid_input(prompt, min_val, max_val):
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                print("입력이 비어있습니다. 다시 입력해주세요.")
                continue
            choice = int(user_input)
            if min_val <= choice <= max_val:
                return choice
            else:
                print(f"잘못된 입력입니다. {min_val}에서 {max_val} 사이의 숫자를 입력해주세요.")
        
        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력해주세요.")

# 2. 퀴즈 시작
def start_quiz(quiz_list):
        print ("\n 퀴즈를 시작합니다!")
        score = 0
    
        for quiz in quiz_list:
            quiz.display()
            user_answer = get_valid_input("정답 번호를 입력하세요: ", 1, 4)
            if quiz.is_correct(user_answer):
                print("정답입니다!")
                score += 1
            else:
                print(f"틀렸습니다. 정답은 {quiz.answer}번입니다.")

        print("\n========================================")
        print("\n         모든 문제를 풀었습니다!")
        print(f"\n             최종점수 : {score}/{len(quiz_list)}")
        print("\n========================================")


# 3. 메인 로직
def main():
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
        
if __name__ == "__main__":
    main()