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
        self.current_index = 0
        self.current_score = 0
        self.load_state()

    def load_state(self):
        if not os.path.exists(self.STATE_FILE):
            return

        try:
            with open(self.STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                
                quiz_data = data.get("quizzes", [])
                self.quiz_list = [Quiz(q['question'], q['choices'], q['answer']) for q in quiz_data]

                self.best_score = data.get("best_score", 0)
                
                progress = data.get("in_progress", {})
                self.current_index = progress.get("current_index", 0)
                self.current_score = progress.get("current_score", 0)
                
                print(f"✅ 데이터를 성공적으로 불러왔습니다. (퀴즈: {len(self.quiz_list)}개)")

        except PermissionError:
            print(f"⚠️ 권한 에러: '{self.STATE_FILE}' 파일을 읽을 권한이 없습니다. 파일 속성에서 읽기 권한을 확인해주세요.")
        except json.JSONDecodeError:
            print(f"⚠️ 데이터 파싱 에러: '{self.STATE_FILE}' 형식이 올바르지 않습니다.")
        except Exception as e:
            print(f"⚠️ 데이터를 불러오는 중 예기치 못한 오류 발생: {e}")

    def save_state(self):
        try:
            state_data = {
                "quizzes": [q.to_dict() for q in self.quiz_list],
                "best_score": self.best_score,
                "in_progress": {
                    "current_index": self.current_index,
                    "current_score": self.current_score
                }
            }
            with open(self.STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(state_data, f, ensure_ascii=False, indent=4)
        except PermissionError:
            print(f"❌ 권한 에러: '{self.STATE_FILE}'에 저장할 권한이 없습니다. 다른 프로그램에서 파일을 사용 중인지 확인하세요.")
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
    
    def update_best_score(self, score):
        if score > self.best_score:
            print(f"🎊 축하합니다! 최고 기록을 경신했습니다! ({self.best_score} -> {score})")
            self.best_score = score
        else:
            print(f"현재 최고 기록: {self.best_score}")

    def start_quiz(self):
        if not self.quiz_list:
            print("\n❌ 등록된 퀴즈가 없습니다. 퀴즈를 먼저 추가해주세요!")
            return

        if self.current_index > 0:
            print(f"\n📝 이전에 {self.current_index}번 문제까지 풀었습니다.")
            choice = input("▶️ 이어서 푸시겠습니까? (y/n): ").strip().lower()
            
            if choice != 'y':
                print("♻️ 처음부터 다시 시작합니다.")
                self.current_index = 0
                self.current_score = 0
            else:
                print(f"🚀 {self.current_index + 1}번 문제부터 재개합니다!")

        total_quizzes = len(self.quiz_list)
        
        for i in range(self.current_index, total_quizzes):
            quiz = self.quiz_list[i]
            
            print(f"\n[문제 {i + 1} / {total_quizzes}]")
            print(f"질문: {quiz.question}")
            
            for idx, choice in enumerate(quiz.choices, 1):
                print(f"{idx}. {choice}")
            
            user_answer = input("답변 입력 (그만두기: q) > ").strip()
            
            if user_answer.lower() == 'q':
                print("\n💾 진행 상황을 저장하고 메뉴로 나갑니다.")
                return

            try:
                if int(user_answer) == quiz.answer:
                    print("✅ 정답입니다!")
                    self.current_score += 1
                else:
                    print(f"❌ 틀렸습니다. 정답은 [{quiz.answer}] 입니다.")
            except ValueError:
                print("⚠️ 숫자 번호를 입력해주세요. 이번 문제는 틀린 것으로 처리됩니다.")

            self.current_index = i + 1

        print("\n" + "=" * 30)
        print(f"🎊 모든 문제를 다 풀었습니다!")
        print(f"📊 이번 회차 점수: {self.current_score} / {total_quizzes}")
        print("=" * 30)

        # 최고 점수 갱신 (메서드 호출)
        self.update_best_score(self.current_score)
        
        # 중요: 다음 게임을 위해 진행 상황 초기화
        self.current_index = 0
        self.current_score = 0
        
        # 변경된 최고 점수와 초기화된 진행 상황을 파일에 저장
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