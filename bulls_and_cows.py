import random
import re

class BNC:
    def __init__(self) -> None:
        self.set_range(0, 9) # 기본값 0부터 9까지의 정수를 사용
        self.set_answer() # 정답 설정
        print(f"정답: {self.answer_list}") # 확인용, 실제 실행시에는 출력하지 않아야 함
        return
    
    def set_range(self, start, end):
        '''
        게임에 사용할 숫자의 범위를 설정하는 함수
        '''
        self.range = range(start, end+1)
        return
    
    def set_answer(self):
        '''
        맞춰야 할 숫자 3개를 결정하는 함수
        '''
        self.answer_list = random.sample(self.range, 3)
        return
    
    def get_guess(self):
        '''
        사용자가 예측한 숫자 3개를 입력받는 함수
        제대로 된 형식으로 입력할 때까지 반복
        '''
        guess_list = []
        input_str = input(f"{self.range[0]}부터 {self.range[-1]}의 숫자 중에서 3개를 골라 입력하세요.(띄어쓰기로 구분)\n  >> ")
        m = re.match("^ *(\d+) (\d+) (\d+) *$", input_str)
        if m:
            for i in range(1, 4):
                if int(m.group(i)) in self.range:
                    guess_list.append(int(m.group(i)))
            if not len(guess_list) == 3:
                print("범위를 벗어난 숫자가 있습니다. 다시 입력해주세요.")
                guess_list = self.get_guess()
        else:
            print("잘못된 형식입니다. 다시 입력해주세요.")
            guess_list = self.get_guess()
        return guess_list
    
    def is_answer(self, guess_list):
        '''
        입력과 정답을 비교해 S,B,O를 출력하는 함수
        숫자 3개를 모두 맞춘 경우에만 True 반환
        '''
        count_S = 0
        count_B = 0
        
        for i in range(0, 3):
            if guess_list[i] in self.answer_list:
                if self.answer_list.index(guess_list[i]) == i:
                    # print(f'{guess_list[i]}는 스트라이크')
                    count_S += 1
                else:
                    # print(f'{guess_list[i]}는 볼')
                    count_B += 1
        
        print(f"\n예측: {guess_list}")
        if count_S == 3:
            print(f"정답입니다! 축하합니다~")
            return True
        elif count_S + count_B == 0:
            print(f"결과: 이런이런... 아웃입니다. 다시 시도해보세요!")
        else:
            print(f"결과: {count_S}S{count_B}B  다시 시도해보세요!")  
        return False

def main():
    print("<< 숫자 야구 게임 >>")
    my_bnc = BNC()    
    while not my_bnc.is_answer(my_bnc.get_guess()):
        # while not 뒤의 my_bnc.is_answer(my_bnc.get_guess())가 True가 될 때까지 반복하게 됨
        # 즉, 사용자가 숫자 3개를 모두 맞출 때까지 반복
        pass

if __name__ == '__main__':
    main()