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
        self.quiz_list = []
        self.best_score = 0
        self.load_state()

    def load_state(self):
        if not os.path.exists(self.STATE_FILE):
            print("ℹ️ 저장된 데이터가 없어 기본 문제를 로드합니다.")
            self.quiz_list = [Quiz(f"기본 문제 {i}", ["1", "2", "3", "4"], 1) for i in range(1, 4)]
            return

        try:
            with open(self.STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.quiz_list = [Quiz(**q) for q in data.get("quizzes", [])]
                self.best_score = data.get("best_score", 0)
        except json.JSONDecodeError:
            print("❌ 데이터 파일이 손상되었습니다. 기본 설정으로 시작합니다.")
            self.quiz_list = [Quiz("기본 문제", ["1", "2", "3", "4"], 1)]
        except Exception as e:
            print(f"❌ 알 수 없는 오류 발생: {e}")

    def save_state(self):
        try:
            state_data = {
                "quizzes": [q.to_dict() for q in self.quiz_list],
                "best_score": self.best_score
            }
            with open(self.STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(state_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"❌ 저장 중 오류가 발생했습니다: {e}")

    def get_valid_input(self, prompt, min_val, max_val):
        while True:
            try:
                val = int(input(prompt))
                if min_val <= val <= max_val:
                    return val
                print(f"⚠️ 경고: {min_val}에서 {max_val} 사이의 숫자를 입력해주세요.")
            except ValueError:
                print("⚠️ 에러: 문자가 아닌 '숫자'를 입력해야 합니다.")

    def start_quiz(self):
        if not self.quiz_list:
            print("\n❌ 등록된 문제가 없습니다. 2번 메뉴에서 문제를 먼저 추가해주세요!")
            return

        print(f"\n🚀 퀴즈를 시작합니다! (총 {len(self.quiz_list)}문제)")
        score = 0
        for i, quiz in enumerate(self.quiz_list, 1):
            print(f"\n[{i}/{len(self.quiz_list)}번 문제]")
            quiz.display()
            user_ans = self.get_valid_input("정답 입력: ", 1, 4)
            
            if quiz.is_correct(user_ans):
                print("✅ 정답입니다!")
                score += 1
            else:
                print(f"❌ 틀렸습니다. 정답은 {quiz.answer}번입니다.")
        
        print(f"\n🏁 퀴즈 종료! 내 점수: {score}/{len(self.quiz_list)}")
        if score > self.best_score:
            print(f"🎊 축하합니다! 최고 기록을 경신했습니다! ({self.best_score} -> {score})")
            self.best_score = score
            self.save_state()

    def delete_quiz(self):
        if not self.quiz_list:
            print("\n❌ 삭제할 퀴즈가 없습니다.")
            return

        print("\n--- 퀴즈 삭제 모드 ---")
        for i, quiz in enumerate(self.quiz_list, 1):
            print(f"{i}. {quiz.question}")
        
        choice = self.get_valid_input("\n삭제할 번호를 입력하세요 (취소: 0): ", 0, len(self.quiz_list))
        
        if choice == 0:
            print("🔙 삭제를 취소하고 메뉴로 돌아갑니다.")
            return

        removed = self.quiz_list.pop(choice - 1)
        self.save_state()
        print(f"🗑️  삭제 완료: '{removed.question}' 문제가 제거되었습니다.")

    def run(self):
        print("\n" + "=" * 30)
        print("       🎮 퀴즈 게임 🎮")
        print("=" * 30)

        try:
            while True:
                print("\n" + "─" * 8 + " [ 메뉴 선택 ] " + "─" * 8)
                print(" 1. 🚀 퀴즈 시작")
                print(" 2. ➕ 퀴즈 추가")
                print(" 3. 📚 퀴즈 목록")
                print(" 4. 🏆 최고 점수 확인")
                print(" 5. 🗑️  퀴즈 삭제")
                print(" 6. ❌ 종료")
                print("─" * 30)
                
                # 메뉴가 6번까지 있으니 범위를 1~6으로 설정
                choice = self.get_valid_input("선택 > ", 1, 6)
                
                if choice == 1: self.start_quiz()
                elif choice == 2: self.add_quiz()
                elif choice == 3: self.view_quiz_list()
                elif choice == 4: print(f"\n🏆 현재 최고 점수: {self.best_score}점")
                elif choice == 5: self.delete_quiz()
                elif choice == 6: 
                    print("\n프로그램을 종료합니다. 다음에 또 봐요! 👋")
                    break

        except KeyboardInterrupt:
            print("\n\n👋 사용자에 의해 프로그램이 강제 종료되었습니다. 안전하게 종료합니다.")
        
        finally:
            self.save_state()
            print("💾 모든 데이터가 안전하게 저장되었습니다.")

    # (기존 add_quiz, view_quiz_list는 동일하게 유지)
    def add_quiz(self):
        print("\n--- 새 퀴즈 추가 ---")
        question = input("문제 내용을 입력하세요: ")
        choices = [input(f"선택지 {i}: ") for i in range(1, 5)]
        answer = self.get_valid_input("정답 번호 (1-4): ", 1, 4)
        self.quiz_list.append(Quiz(question, choices, answer))
        self.save_state()
        print("✅ 퀴즈가 성공적으로 추가되었습니다!")

    def view_quiz_list(self):
        print("\n📚 현재 등록된 퀴즈 목록")
        if not self.quiz_list:
            print("- 등록된 문제가 없습니다.")
        else:
            for i, quiz in enumerate(self.quiz_list, 1):
                print(f"{i}. {quiz.question}")
        input("\n(엔터를 누르면 메뉴로 돌아갑니다)")

if __name__ == "__main__":
    QuizGame().run()