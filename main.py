import json
import os

# 1. 퀴즈 데이터 모델 클래스
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


# 2. 게임 관리 클래스
class QuizGame:
    def __init__(self):
        # 파일 경로 설정
        self.STATE_FILE = "state.json"
        self.SAVE_FILE = "save_data.json" # 진행 상황(이어하기)은 별도 관리
        
        # 기본 퀴즈 데이터 (파일이 없을 때 사용)
        self.DEFAULT_QUIZ_DATA = [
            {"question": f"기본 문제 {i}", "choices": ["선택1", "선택2", "선택3", "선택4"], "answer": 1}
            for i in range(1, 6)1
        ]
        
        # 데이터 로드 (퀴즈 목록과 최고 점수를 한 번에 가져옴)
        self.quiz_list, self.best_score = self.load_state()

    # --- [핵심] 파일 통합 저장 및 불러오기 ---
    def load_state(self):
        """state.json에서 퀴즈 목록과 최고 점수를 불러옵니다."""
        if not os.path.exists(self.STATE_FILE):
            print("\n[알림] 데이터 파일이 없어 기본 데이터를 생성합니다.")
            return [Quiz(**d) for d in self.DEFAULT_QUIZ_DATA], 0
        
        try:
            with open(self.STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 스키마 구조: {"quizzes": [...], "best_score": 0}
                quizzes = [Quiz(**q) for q in data.get("quizzes", [])]
                best_score = data.get("best_score", 0)
                
                if not quizzes: # 파일은 있는데 퀴즈가 비어있는 경우
                    quizzes = [Quiz(**d) for d in self.DEFAULT_QUIZ_DATA]
                
                return quizzes, best_score
        except (json.JSONDecodeError, KeyError, TypeError):
            print("\n[경고] 데이터 파일이 손상되었습니다. 기본 데이터로 복구합니다.")
            return [Quiz(**d) for d in self.DEFAULT_QUIZ_DATA], 0

    def save_state(self):
        """퀴즈 목록과 최고 점수를 state.json에 통합 저장합니다."""
        try:
            state_data = {
                "quizzes": [q.to_dict() for q in self.quiz_list],
                "best_score": self.best_score
            }
            with open(self.STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(state_data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"\n[오류] 파일 저장 중 문제가 발생했습니다: {e}")

    # --- 진행 상황 관리 (이어하기) ---
    def save_progress(self, index, score):
        data = {"last_index": index, "score": score}
        with open(self.SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_progress(self):
        if os.path.exists(self.SAVE_FILE):
            try:
                with open(self.SAVE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: pass
        return None

    # --- 유틸리티 메서드 ---
    def get_valid_input(self, prompt, min_val, max_val):
        while True:
            user_input = input(prompt).strip()
            if not user_input:
                print("입력이 비어있습니다.")
                continue
            try:
                choice = int(user_input)
                if min_val <= choice <= max_val:
                    return choice
                print(f"{min_val}에서 {max_val} 사이의 숫자를 입력하세요.")
            except ValueError:
                print("숫자를 입력해주세요.")

    # --- 주요 게임 기능 ---
    def add_quiz(self):
        print("\n" + "-"*10 + " 새 퀴즈 추가 " + "-"*10)
        question = input("문제 내용: ").strip()
        choices = [input(f"선택지 {i}: ").strip() for i in range(1, 5)]
        answer = self.get_valid_input("정답 번호 (1-4): ", 1, 4)
        
        self.quiz_list.append(Quiz(question, choices, answer))
        self.save_state() # 변경사항 저장
        print("✅ 퀴즈가 추가되고 state.json에 저장되었습니다!")

    def view_quiz_list(self):
        print("\n" + "="*30 + "\n      📚 등록된 퀴즈 목록\n" + "="*30)
        if not self.quiz_list:
            print("등록된 퀴즈가 없습니다.")
        else:
            for i, quiz in enumerate(self.quiz_list, 1):
                print(f"{i}. {quiz.question} (정답: {quiz.answer}번)")
        input("\n엔터를 누르면 메뉴로 돌아갑니다...")

    def start_quiz(self):
        if not self.quiz_list:
            print("\n문제가 없습니다. 먼저 추가해주세요."); return

        # 이어하기 확인
        progress = self.load_progress()
        start_index, score = 0, 0
        
        if progress and progress["last_index"] < len(self.quiz_list):
            print(f"\n이전 기록 발견: {progress['last_index']+1}번 문제부터 시작 가능")
            if input("이어서 하시겠습니까? (y/n): ").lower() == 'y':
                start_index = progress["last_index"]
                score = progress["score"]

        try:
            for i in range(start_index, len(self.quiz_list)):
                print(f"\n[{i+1}/{len(self.quiz_list)}번 문제]")
                self.quiz_list[i].display()
                
                user_ans = self.get_valid_input("정답 입력: ", 1, 4)
                if self.quiz_list[i].is_correct(user_ans):
                    print("✨ 정답입니다!")
                    score += 1
                else:
                    print(f"❌ 틀렸습니다. 정답은 {self.quiz_list[i].answer}번입니다.")
                
                # 매 문제마다 진행 상황 저장
                self.save_progress(i + 1, score)

            # 퀴즈 종료
            print(f"\n🏁 퀴즈 종료! 최종 점수: {score}/{len(self.quiz_list)}")
            
            if score > self.best_score:
                print(f"🎊 축하합니다! 최고 기록 경신: {self.best_score} -> {score}")
                self.best_score = score
                self.save_state() # 최고 점수 통합 저장
            
            if os.path.exists(self.SAVE_FILE):
                os.remove(self.SAVE_FILE) # 완료 시 세이브 삭제

        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 게임이 중단되었습니다. 현재 위치가 저장되었습니다.")

    def run(self):
        """메인 메뉴 루프"""
        while True:
            print("\n" + "="*30)
            print("      🎮 QUIZ GAME 🎮")
            print("="*30)
            print("1. 퀴즈 시작")
            print("2. 퀴즈 추가")
            print("3. 목록 보기")
            print("4. 최고 점수 확인")
            print("5. 종료")
            print("="*30)
            
            choice = self.get_valid_input("선택: ", 1, 5)
            
            if choice == 1: self.start_quiz()
            elif choice == 2: self.add_quiz()
            elif choice == 3: self.view_quiz_list()
            elif choice == 4: print(f"\n🏆 현재 최고 점수: {self.best_score}점")
            elif choice == 5: 
                print("\n게임을 종료합니다. 즐거우셨나요? 😊")
                break

# 프로그램 실행
if __name__ == "__main__":
    game = QuizGame()
    game.run()