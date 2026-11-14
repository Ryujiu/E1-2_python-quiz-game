import json
import os

# 1. 데이터 모델 클래스 (기존과 동일)
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


# 2. 게임 관리 클래스
class QuizGame:
    def __init__(self):
        # 파일 경로 및 기본 데이터 설정
        self.QUIZ_FILE = "quiz_data.json"
        self.SAVE_FILE = "save_data.json"
        self.SCORE_FILE = "high_score.txt"
        self.DEFAULT_QUIZ_DATA = [
            {"question": f"문제{i}", "choices": ["선택1", "선택2", "선택3", "선택4"], "answer": 1}
            for i in range(1, 21)
        ]
        
        # 데이터 초기 로드
        self.quiz_list = self.load_quiz_data()
        self.high_score = self.load_high_score()

    # --- 데이터 관리 메서드 ---
    def load_quiz_data(self):
        try:
            if not os.path.exists(self.QUIZ_FILE):
                raise FileNotFoundError
            with open(self.QUIZ_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Quiz(**d) for d in data]
        except (FileNotFoundError, json.JSONDecodeError):
            print("\n퀴즈 파일이 없거나 손상되었습니다. 기본 데이터로 복구합니다.")
            with open(self.QUIZ_FILE, "w", encoding="utf-8") as f:
                json.dump(self.DEFAULT_QUIZ_DATA, f, ensure_ascii=False, indent=4)
            return [Quiz(**d) for d in self.DEFAULT_QUIZ_DATA]

    def save_quiz_data(self):
        with open(self.QUIZ_FILE, "w", encoding="utf-8") as f:
            data = [quiz.to_dict() for quiz in self.quiz_list]
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_high_score(self):
        if not os.path.exists(self.SCORE_FILE): return 0
        try:
            with open(self.SCORE_FILE, 'r', encoding='utf-8') as f:
                return int(f.read().strip())
        except: return 0

    def save_high_score(self, score):
        self.high_score = score
        with open(self.SCORE_FILE, 'w', encoding='utf-8') as f:
            f.write(str(score))

    def save_progress(self, index, score):
        data = {"last index": index, "score": score}
        with open(self.SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_progress(self):
        if os.path.exists(self.SAVE_FILE):
            try:
                with open(self.SAVE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict) and "last index" in data:
                    return data
            except: pass
        return None

    # --- 유틸리티 메서드 ---
    def get_valid_input(self, prompt, min_val, max_val):
        while True:
            user_input = input(prompt).strip()
            if not user_input: continue
            try:
                choice = int(user_input)
                if min_val <= choice <= max_val: return choice
                print(f"{min_val}~{max_val} 사이의 숫자를 입력하세요.")
            except ValueError:
                print("숫자를 입력해주세요.")

    # --- 게임 기능 메서드 ---
    def add_quiz(self):
        print("\n------ 새로운 퀴즈 추가 ------")
        question = input("문제를 입력하세요: ").strip()
        choices = [input(f"선택지 {i}를 입력하세요: ").strip() for i in range(1, 5)]
        answer = self.get_valid_input("정답 번호(1-4): ", 1, 4)
        
        self.quiz_list.append(Quiz(question, choices, answer))
        self.save_quiz_data()
        print("퀴즈가 추가되었습니다!")

    def view_quiz_list(self):
        print("\n" + "="*30 + "\n      📚 퀴즈 목록\n" + "="*30)
        if not self.quiz_list:
            print("등록된 퀴즈가 없습니다.")
        else:
            for i, quiz in enumerate(self.quiz_list, 1):
                print(f"{i}. {quiz.question} (정답: {quiz.answer})")
        input("\n엔터를 누르면 메뉴로 돌아갑니다...")

    def start_quiz(self):
        if not self.quiz_list:
            print("\n퀴즈 데이터가 없습니다."); return

        progress = self.load_progress()
        start_index, score = 0, 0

        if progress:
            if self.get_valid_input(f"이전 기록({progress['last index']+1}번부터)을 이어서 하시겠습니까? (1.Yes / 2.No): ", 1, 2) == 1:
                start_index, score = progress["last index"], progress["score"]

        try:
            for i in range(start_index, len(self.quiz_list)):
                quiz = self.quiz_list[i]
                print(f"\n진행 상황: {i + 1}/{len(self.quiz_list)}")
                quiz.display()
                
                user_answer = self.get_valid_input("정답 번호: ", 1, 4)
                if quiz.is_correct(user_answer):
                    print("정답입니다!"); score += 1
                else:
                    print(f"틀렸습니다. 정답은 {quiz.answer}번입니다.")
                
                self.save_progress(i + 1, score)

            print(f"\n🏁 종료! 점수: {score}/{len(self.quiz_list)}")
            if score > self.high_score:
                print(f"🎊 최고 기록 경신! ({self.high_score} -> {score})")
                self.save_high_score(score)
            
            if os.path.exists(self.SAVE_FILE): os.remove(self.SAVE_FILE)

        except (KeyboardInterrupt, EOFError):
            print("\n중단되었습니다. 현재 위치가 저장됩니다.")

    # --- 메인 루프 ---
    def run(self):
        while True:
            print("\n" + "="*30 + "\n       🎮 퀴즈 게임\n" + "="*30)
            print("1. 시작 | 2. 추가 | 3. 목록 | 4. 최고 점수 | 5. 종료")
            menu = self.get_valid_input("선택: ", 1, 5)

            if menu == 1: self.start_quiz()
            elif menu == 2: self.add_quiz()
            elif menu == 3: self.view_quiz_list()
            elif menu == 4: print(f"\n🏆 최고 점수: {self.high_score}점")
            elif menu == 5: print("\n게임을 종료합니다."); break

# 실행부
if __name__ == "__main__":
    game = QuizGame()
    game.run()