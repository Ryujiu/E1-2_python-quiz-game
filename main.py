# 1. 퀴즈데이터
quiz_list = [
    {"question": "문제1", "answer": "정답1"},
    {"question": "문제2", "answer": "정답2"},
    {"question": "문제3", "answer": "정답3"},
    {"question": "문제4", "answer": "정답4"},
    {"question": "문제5", "answer": "정답5"},
    {"question": "문제6", "answer": "정답6"},
    {"question": "문제7", "answer": "정답7"},
    {"question": "문제8", "answer": "정답8"},
    {"question": "문제9", "answer": "정답9"},
    {"question": "문제10", "answer": "정답10"},
    {"question": "문제11", "answer": "정답11"},
    {"question": "문제12", "answer": "정답12"},
    {"question": "문제13", "answer": "정답13"},
    {"question": "문제14", "answer": "정답14"},
    {"question": "문제15", "answer": "정답15"},
    {"question": "문제16", "answer": "정답16"},
    {"question": "문제17", "answer": "정답17"},
    {"question": "문제18", "answer": "정답18"},
    {"question": "문제19", "answer": "정답19"},
    {"question": "문제20", "answer": "정답20"}
    ]


# 2. 메인 로직
def main():
    while True:
        print("========================================")
        print("               퀴즈 맞추기               ")
        print("========================================")
        print("1. 시작하기")
        print("2. 종료하기")
        print("========================================")

        choice = input("원하는 메뉴 번호를 입력하세요: ")

        if choice == "1": 
            print ("\n 퀴즈를 시작합니다!")
            score = 0

            for quiz in quiz_list:
                print(f"\n{quiz['question']}")
                user_answer = input("정답을 입력하세요:")
                if user_answer == quiz['answer']:
                    print("정답입니다")
                    score += 1
                else:
                    print(f"틀렸습니다. 정답은 {quiz['answer']}입니다.")
                print(f"\n 최종 점수: {score}/{len(quiz_list)}")
        elif choice == "2":
            print ("\n 퀴즈를 종료합니다!")
            break
        else:
            print ("\n 잘못된 입력입니다. 1번이나 2번을 선택해주세요")

if __name__ == "__main__":
    main()