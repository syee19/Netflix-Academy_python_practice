'''
다크리네이머 만들기

git에서 add하는 것처럼 스테이지에 이름을 변경할 파일을 담은 후
일괄적으로 이름 변경 기능을 수행하는 프로그램

rename_list의 요소
file_element = {
    'file_name': None,
    'file_path': None,
}

'''
import os
import sys
import re
from datetime import datetime
import json


class DarkRenamer:
    def __init__(self, path) -> None:
        self.path = path    # path는 최상위 경로
        self.pointer = path # pointer는 파일 목록을 보여줄 현재 위치
        self.rename_list = []  # 변경하고자 하는 파일을 담기 위한 리스트
        pass
    
    def print_pointer(self):
        '''
        현재 위치의 파일 및 디렉토리를 출력하는 함수
        '''
        print(f">현재 위치: {self.pointer}<\n")
        list = os.listdir(self.pointer)
        if len(list) == 0:
            print(f"{self.pointer}은 빈 디렉토리입니다.")
            return True
        if not os.path.samefile(self.pointer, self.path):
            print(' 📂  ..\n')
        for i in range(len(list)):
            if os.path.isdir(os.path.join(self.pointer, list[i])):
                icon = '📁'
            else:
                icon = '📄'
            row = '   %s\t%s'%(icon, list[i])
            print(row)
        return True
    
    def print_list(self):
        '''
        self.rename_list를 터미널에 출력하는 함수
        '''
        print(f">변경할 파일 {len(self.rename_list)}개:\n")
        if len(self.rename_list) == 0:
            print("  아직 담긴 파일이 없습니다.")
            return True
        print('  %-s\t%-15s\t%s\n'%('번호', '현재 이름', '파일 경로'))
        for i in range(len(self.rename_list)):
            row = '    %-.2d\t%-20s\t%s'%(i+1, self.rename_list[i]['file_name'],self.rename_list[i]['file_path'])
            print(row)
        return True

    def add_file(self, file_name):
        '''
        변경하고자 하는 파일을 self.rename_list에 추가하는 함수
        실행 후 self.point 아래의 file_name이 리스트에 포함되어있으면 True, 아니면 False 반환
        '''
        file_path = os.path.join(self.pointer, file_name)
        if os.path.isdir(file_path):
            input(f"{file_name}은 파일이 아닙니다.")
            return False
        if not os.path.isfile(file_path):
            input(f"{self.pointer} 경로에 {file_name}가 없습니다.")
            return False
        file_element = {
            'file_name': file_name,
            'file_path': file_path,
        }
        if file_element in self.rename_list:
            input(f"{file_path}가 이미 포함되어있습니다.")
            return True
        self.rename_list.append(file_element)
        return True
    
    def remove_file(self, index):
        '''
        self.rename_list에서 인덱스에 해당하는 요소를 제외시키는 함수
        '''
        if not index in range(len(self.rename_list)):
            input("존재하지 않는 번호입니다.")
            return False
        del self.rename_list[index]
        return True
    
    def move_pointer(self, des):
        '''
        현재 위치를 이동하는 함수
        '''
        if des == '..':
            if os.path.samefile(self.pointer, self.path):
                input("최상위 디렉토리입니다.")
                return False
            self.pointer = os.path.dirname(self.pointer)
            return True
        if des in os.listdir(self.pointer):
            if os.path.isfile(des):
                input("파일로는 이동할 수 없습니다.")
                return False
            self.pointer = os.path.join(self.pointer, des)
            return True
        input("이동할 수 없는 목적지입니다.")
        return False
    
    def change_exp(self, new_exp):
        '''
        self.rename_list의 파일들의 확장자를 new_exp로 변경하는 함수
        '''
        if not new_exp.isalpha():
            input("잘못된 확장자명입니다.")
            return False
        change_list = []
        for i in range(len(self.rename_list)):            
            old_name = os.path.basename(self.rename_list[i]['file_path'])
            new_name = re.sub(".\w+$", '.' + new_exp, self.rename_list[i]['file_name'])
            dir_name = os.path.dirname(self.rename_list[i]['file_path'])
            
            os.rename(os.path.join(dir_name, old_name), os.path.join(dir_name, new_name))
            
            self.rename_list[i]['file_name'] = new_name
            self.rename_list[i]['file_path'] = os.path.join(dir_name, new_name)
            
            change_list.append({'old name': old_name, 'new name': new_name, 'dir name': dir_name, 'time': datetime.now().strftime('%c')})
        
        print('-'*70)
        print('  %-15s\t%-15s\t%s\n'%('변경 전', '변경 후', '파일 위치'))
        for i in change_list:
            print('  %-15s\t%-15s\t%s'%(i['old name'], i['new name'], i['dir name']))   
        self.record_log(change_list)
        input("확장자명 변경을 완료했습니다.")
        return True
    
    def do_cmd(self):
        print("a: 추가 / r: 제외 / m: 이동 / n: 이름변경 / e: 종료")
        cmd = input("실행할 명령을 입력하세요.>> ")
        if cmd == 'a':
            file_name = input("추가할 파일 이름을 입력하세요.>> ")
            return self.add_file(file_name)             
        if cmd == 'r':
            str = input("제외할 파일의 번호를 입력하세요.>> ")
            if not str.isdigit():
                input("입력이 숫자가 아닙니다. 처음부터 다시 시도하세요.")
                return False
            index = int(str)-1
            return self.remove_file(index)
        if cmd == 'm':
            des = input("이동할 목적지를 입력하세요.>> ")
            return self.move_pointer(des)
        if cmd == 'n':
            # 확장자 바꾸기
            # 나중에 다른 기능 추가 예정...!
            exp = input("변경할 확장자 명을 입력하세요.>> .")
            return self.change_exp(exp)
        if cmd == 'e':
            exit()
        return
    
    def record_log(self, change_list):
        '''
        이름 변경 후 로그를 저장하는 함수
        '''
        path = os.path.expanduser('~/rename_log.json')
        with open(path, 'a') as json_file:
            json.dump(change_list, json_file)
        return


def print_line():
    print('-'*70)
    return

def main():
    path = os.getcwd()
    if len(sys.argv) == 2:
        path = sys.argv[1]
    renamer = DarkRenamer(path)
    while True:
        os.system('clear')
        print('\n\t\t<<<Dark Renamer>>>')
        print_line()
        renamer.print_pointer()
        print_line()
        renamer.print_list()        
        print_line()
        renamer.do_cmd()
    return

if __name__ == '__main__':
    main()