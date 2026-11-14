import json
import os

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
        return {"question": self.question, "choices": self.choices, "answer": self.answer}

class QuizGame:
    def __init__(self):
        self.STATE_FILE = "state.json"
        self.SAVE_FILE = "save_data.json"
        self.DEFAULT_QUIZ_DATA = [
            {"question": f"기본 문제 {i}", "choices": ["선택1", "선택2", "선택3", "선택4"], "answer": 1}
            for i in range(1, 6)
        ]
        self.quiz_list, self.best_score = self.load_state()
        
        # 파일이 없으면 초기 생성
        if not os.path.exists(self.STATE_FILE):
            self.save_state()

    def load_state(self):
        if not os.path.exists(self.STATE_FILE):
            return [Quiz(**d) for d in self.DEFAULT_QUIZ_DATA], 0
        try:
            with open(self.STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                quizzes = [Quiz(**q) for q in data.get("quizzes", [])]
                best_score = data.get("best_score", 0)
                return quizzes, best_score
        except:
            return [Quiz(**d) for d in self.DEFAULT_QUIZ_DATA], 0

    def save_state(self):
        state_data = {
            "quizzes": [q.to_dict() for q in self.quiz_list],
            "best_score": self.best_score
        }
        with open(self.STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state_data, f, ensure_ascii=False, indent=4)

    def get_valid_input(self, prompt, min_val, max_val):
        while True:
            try:
                val = int(input(prompt))
                if min_val <= val <= max_val: return val
                print(f"{min_val}~{max_val} 사이를 입력하세요.")
            except ValueError: print("숫자를 입력하세요.")

    def view_quiz_list(self, wait=True):
        print("\n" + "="*30 + "\n      📚 퀴즈 목록\n" + "="*30)
        if not self.quiz_list:
            print("등록된 퀴즈가 없습니다.")
        else:
            for i, quiz in enumerate(self.quiz_list, 1):
                print(f"{i}. {quiz.question}")
        if wait: input("\n엔터를 누르면 메뉴로 돌아갑니다...")

    # --- 퀴즈 삭제 기능 ---
    def delete_quiz(self):
        if not self.quiz_list:
            print("\n❌ 삭제할 퀴즈가 없습니다."); return

        self.view_quiz_list(wait=False) # 목록을 먼저 보여줌
        choice = self.get_valid_input("\n삭제할 번호를 입력하세요 (취소: 0): ", 0, len(self.quiz_list))
        
        if choice == 0:
            print("삭제가 취소되었습니다.")
            return

        removed = self.quiz_list.pop(choice - 1) # 리스트에서 삭제
        self.save_state() # 변경사항 파일 저장
        print(f"\n✅ 삭제 완료: '{removed.question}'")

    def add_quiz(self):
        print("\n--- 새 퀴즈 추가 ---")
        question = input("문제: ")
        choices = [input(f"선택지 {i}: ") for i in range(1, 5)]
        answer = self.get_valid_input("정답 (1-4): ", 1, 4)
        self.quiz_list.append(Quiz(question, choices, answer))
        self.save_state()
        print("✅ 추가되었습니다!")

    def start_quiz(self):
        if not self.quiz_list: return
        score = 0
        for i, quiz in enumerate(self.quiz_list):
            quiz.display()
            if quiz.is_correct(self.get_valid_input("정답: ", 1, 4)):
                print("정답!"); score += 1
            else: print("오답!")
        
        print(f"\n최종 점수: {score}/{len(self.quiz_list)}")
        if score > self.best_score:
            self.best_score = score
            self.save_state()

    def run(self):
        while True:
            print("\n1.시작 2.추가 3.목록 4.최고점수 5.종료 6.삭제") 
            choice = self.get_valid_input("선택: ", 1, 6)
            
            if choice == 1: self.start_quiz()
            elif choice == 2: self.add_quiz()
            elif choice == 3: self.view_quiz_list()
            elif choice == 4: print(f"\n🏆 최고 점수: {self.best_score}")
            elif choice == 5: break
            elif choice == 6: self.delete_quiz() 

if __name__ == "__main__":
    QuizGame().run()