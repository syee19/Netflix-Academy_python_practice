'''
터미널에서 실행되는 투두 리스트 프로그램 만들기
기능
    get - 투두 리스트 가져오기
    add - 할 일 추가하기
    modify - 할 일 수정하기
    delete - 할 일 삭제하기
    done - 할 일 완료하기


    todolist의 element를 todo라고 하자
    todo(dictionary) = {
        'name' : '',
        'isdone' : False,
    }
'''
import os
import json
import argparse

class MyTodo():
    def __init__(self):        
        self.path = os.path.expanduser('~/my_todo.json')
        self.todolist = []
        self.import_json()
    
    def print_todo(self, index):
        '''
        해당 번호의 할 일을 터미널에 출력하는 함수
        '''
        isdone = ''
        if self.todolist[index]['isdone']:
            isdone = ' ✓ '
            
        print(f"   {index+1}.\t{self.todolist[index]['name']}{isdone}" )
        return
    
    def check_index(self, num):
        '''
        num이 todolist 범위 안에 있는지 확인하는 함수
        '''
        if (num - 1) in range(len(self.todolist)):
            return True 
        
        print('없는 번호입니다. 다시 입력해주세요.')
        return False
    
    def get_list(self):
        '''
        작성한 할 일들의 리스트를 터미널에 표시하는 함수
        '''        
        print('  ' + '~'*7 + ' < todo list > ' + '~'*8)        
        if len(self.todolist) == 0:
            print('\t할 일이 없습니다.\n  ' + '~'*30)
            return

        for i in range(len(self.todolist)):
            self.print_todo(i)
        
        print('  ' + '~'*30)
        return
    
    def add_todo(self, name):
        '''
        리스트에 새로운 할 일을 추가하는 함수
        '''
        new_todo = {
            'name' : '',
            'isdone' : False,
        }
        new_todo['name'] = name
        self.todolist.append(new_todo)
        return
    
    def modify_todo(self, index, new_name):
        '''
        리스트에 존재하는 할 일을 수정하는 함수
        '''
        self.todolist[index]['name'] = new_name
        return
    
    def delete_todo(self, index):
        '''
        리스트에 존재하는 할 일을 삭제하는 함수
        '''
        # self.todolist.remove(self.todolist[index])
        
        del self.todolist[index]
        return

    def reset_list(self):
        '''
        리스트에 존재하는 모든 할 일을 삭제하는 함수
        '''
        # for i in range(len(self.todolist)):
        #     self.delete_todo(0)
        # 
        
        self.todolist = []
        return
    
    def done_todo(self, index):
        '''
        리스트에 존재하는 할 일의 완료 상태를 전환하는 함수
        '''
        self.todolist[index]['isdone'] = not self.todolist[index]['isdone']
        return
    
    def import_json(self):
        '''
        JSON 파일에서 할 일 리스트를 가져오는 함수
        '''
        if os.path.isfile(self.path):
            with open(self.path, 'r') as json_file:
                self.todolist = json.load(json_file)
        return
    
    def export_json(self):
        '''
        리스트에 존재하는 할 일을 JSON 파일로 저장하는 함수
        '''
        with open(self.path, 'w') as json_file:
            json.dump(self.todolist, json_file)
        return

def main():
    my_todo = MyTodo()
    
    parser = argparse.ArgumentParser(description="투두리스트 작성 프로그램입니다. 명령을 입력해주세요.")    
    parser.add_argument("-a", "--add", type=str, help="추가할 할 일 이름")
    parser.add_argument("-m", "--modify", type=int, help="수정할 할 일 번호")
    parser.add_argument("-d", "--delete", type=int, help="삭제할 할 일 번호")
    parser.add_argument("-D", "--done", type=int, help="완료상태를 전환할 할 일 번호")    
    parser.add_argument("-r", "--reset", const=True, help="모든 할 일을 삭제합니다.", nargs='?')    
    args = parser.parse_args()
    
    
    if args.add :
        my_todo.add_todo(args.add)
    elif not args.modify == None:
        if my_todo.check_index(args.modify):
            my_todo.modify_todo(args.modify-1, new_name=input('\t수정 내용>> '))
    elif not args.delete == None:
        if my_todo.check_index(args.delete):
            my_todo.delete_todo(args.delete-1)
    elif not args.done == None:        
        if my_todo.check_index(args.done):
            my_todo.done_todo(args.done-1)
    elif args.reset:
        if input('모든 할 일을 삭제할까요? [y/N] ') == 'y':
            my_todo.reset_list()
    else:
        parser.print_help()
        print('\n')
    
    my_todo.get_list()
    my_todo.export_json()
    return

if __name__ == '__main__':
    main()
    
