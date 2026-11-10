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
        elif choice == "2":
            print ("\n 퀴즈를 종료합니다!")
            break
        else:
            print ("\n 잘못된 입력입니다. 1번이나 2번을 선택해주세요")

if __name__ == "__main__":
    main()