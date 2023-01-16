import re

class PasswordChecker:
    char_type = {
        'upper' : r'[A-Z]',
        'lower' : r'[a-z]',
        'num' : r'[0-9]',
        'exmark' : r'[~!@#$%^&*]',
        'invalid' : r'[^A-Za-z0-9~!@#$%^&*]',
    }    
    password = ''
    
    def print_rules(self):
        '''
        터미널에 비밀번호 생성 규칙을 출력하는함수
        '''
        rules = '영대문자, 영소문자, 숫자 및 특수문자 중 3종류 이상으로 구성하여 최소 9자 이상으로 입력합니다.\
            \n※ 사용 가능 특수문자: ~ ! @ # $ % ^ & *'
        print(rules)
        return
    
    def get_password(self):
        '''
        객체에 저장된 password를 반환하는 함수
        '''
        return self.password
    
    def set_password(self, password):
        '''
        password를 객체에 저장하는 함수
        '''
        self.password = password
        return
    
    def check_password(self, password):
        '''
        password가 조건을 만족하는지 확인하는 함수
        유효한 경우 해당 password를 self.password로 저장
        '''
        if len(password) < 9:
            print("비밀번호는 최소 9자리 이상이어야 합니다.")
            return False
        invalid = self.find_invalid(password)
        if invalid:
            print(f"유효하지 않은 문자 {invalid}를 포함하고 있습니다.")
            return False
        if not self.check_type_count(password):
            print("영대문자, 영소문자, 숫자 및 특수문자 중 3종류 이상을 포함해야 합니다.")
            return False
        self.set_password(password)
        return True

    def check_type_count(self, string):
        '''
        string에 영대문자, 영소문자, 숫자 및 특수문자 중 3종류 이상이 포함되는지 확인하는 함수
        '''
        type_count = 0
        for type in self.char_type:
            if self.is_exist(type, string):
                # print(type)
                type_count += 1
        if type_count >= 3:
            return True
        return False
    
    def is_exist(self, type, string):
        '''
        string에 해당 type이 포함되는지 확인하는 함수
        '''
        pattern = self.char_type[type]
        if re.findall(pattern, string):
            return True
        return False
    
    def find_invalid(self, string):
        '''
        string에서 유효하지 않은 문자를 찾아 반환하는 함수
        '''
        f = re.findall(self.char_type['invalid'], string)
        if f:
            res = ', '.join(f)
            return res
        return None
        
def main():
    checker = PasswordChecker()
    checker.print_rules()
    while not checker.check_password(input("체크할 비밀번호를 입력하세요.>> ")):
        pass    
    print("비밀번호 설정이 완료되었습니다. :", checker.get_password())

if __name__ == '__main__':
    main()