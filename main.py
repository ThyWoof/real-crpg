import random as rd
import datetime as dt
import pickle
import resource
from inventory import Inventory
from status import Status
from monster import Monster
from action import *
from dice import rollDice
from session import *


class Character:
    def __init__(self, name, cls, race, stat, value, description):  # 기본적인 캐릭터의 정보생성자입니다.
        self.status = Status(name, cls, race, stat[0], stat[1], stat[2],stat[3], stat[4], stat[5], value, description)
        self.inventory = Inventory()
        if cls == '전사':
            self.action = Worrior()
        else:
            pass

    def show_info(self):  # /캐릭터확인 명령어를위한 함수입니다.
        self.status.show_status(self.inventory)
        self.status.show_equip_status()

    def meleeAttack(self, op):  # 근접공격 명령어를위한 함수입니다.
        self.action.meleeAttack(op, self)

    def check_body(self, monster):  # 몬스터 루팅을위한 함수
        self.action.check_body(self, monster)

    def equip(self, item):  # 무기장비를 위한함수입니다.
        if item.type == 'weapon':
            temp = self.status.weapon_unequip()
            if temp == None:
                pass
            else:
                self.inventory.item_setter(temp)
        elif item.type == 'armor':
            temp = self.status.armor_unequip()
            if temp == None:
                pass
            else:
                self.inventory.item_setter(self.status.armor_unequip())
        else:
            temp = self.status.shield_unequip()
            if temp == None:
                pass
            else:
                self.inventory.item_setter(self.status.shield_unequip())
        self.status.equip(self.inventory.item_getter(item.name))

    def level_up(self):  # 레벨업 함수입니다.
        if self.status.level == 10:
            print('더이상 레벨업 할수 없어보이는군요..')
            return
        else:
            reduce = self.status.level + 7
            if reduce > self.status.cur_exp:
                print('경험치가 부족해보입니다...')
                return
        self.status.curexp_controller(-reduce)
        self.status.level_up()
        self.action.level_up(self)


class Log:
    def __init__(self, string, battle, master, script):
        self.timestamp = dt.datetime.now()
        self.battle = battle  # 문장의 타입을 담는 합수 / 예: 전투, 대화, 상황묘사
        self.master = master
        self.script = script
        self.sentence = string

    def get_log(self):
        return self.get_time() + ') ' + self.sentence

    def get_time(self):
        return str(self.timestamp.hour) + ':' + str(self.timestamp.minute) + ':' + str(self.timestamp.second)


def show_and_select(list):  # 보기를 나열하고 선택해서 반환하는 함수
    while True:
        for i, j in enumerate(list):
            print('{}. {}'.format(i + 1, j))
        choose = int(input('위의 보기중에 골라주세요. : '))
        result = list[choose - 1]
        choose1 = int(input('\n{} 이(가) 맞습니까?\n1.예 2.아니오 : '.format(result)))
        if choose1 == 1:
            return result
        else: pass


def random_sentence_printer(list):  # 묘사를 랜덤으로 출력해주는 함수입니다.
    print(rd.choice(list))


def script_reader(list):  # 스크립트를 출력해주는 함수입니다.
    for i in list:
        print(i)
        input()


class Master:
    def __init__(self):  # 마스터의 생성자로, 플레이어 캐릭터와, 세션, 장소들을 담고있습니다.
        self.player = []
        self.player_location = None
        self.cur_session = ''#Session('튜토리얼')
        self.cur_monster = []
        self.place = []
        self.log = []
        self.battle_status = False

    def make_new_character(self):  # 새로운 플레이어 추가 함수
        input('캐릭터를 생성합니다.')
        print()
        print('직업을 골라주세요.')
        cls = show_and_select(resource.classes)
        print('종족을 골라주세요.')
        race = show_and_select(resource.races)
        print('이름을 골라주세요.')
        name = show_and_select(resource.worrior_names)
        print('외모를 골라주세요.')
        outlook1 = show_and_select(resource.worrior_outlooking1)
        outlook2 = show_and_select(resource.worrior_outlooking2)
        outlook3 = show_and_select(resource.worrior_outlooking3)
        script_reader(resource.status_select)
        answer = int(input('어느 방법으로 하시겠습니까?\n1.3d6  2.직접배분 : '))
        if answer == 1:
            num = []
            for i in range(6):
                num.append(rollDice(3, 6, 0))
            while True:
                stat = ['근력', '민첩', '체력', '지능', '지혜', '매력']
                nums = []
                for i in num:
                    nums.append(i)
                result = []
                print('그럼, 능력치를 선택할 차례입니다.')
                for i in stat:
                    for j, k in enumerate(nums):
                        print('{}.{}'.format(j + 1, k))
                    choose = int(input('{}에 몇점을 배치할까요? : '.format(i)))
                    result.append(nums.pop(choose - 1))
                for i in range(0, 6):
                    if result[i] > 15:
                        add = '(+2)'
                    elif result[i] > 12:
                        add = '(+1)'
                    elif result[i] > 8:
                        add = ''
                    elif result[i] == 8:
                        add = '(-1)'
                    print('{} : {}{}'.format(stat[i], result[i], add))
                choose = int(input('맞습니까?\n1.예 2.아니오 : '))
                if choose == 1:
                    choose = int(input('직업은 바꾸시겠습니까?\n1.네 2.아니오 : '))
                    if choose == 2:
                        break
                    else:
                        print('직업을 골라주세요.')
                        cls = show_and_select(resource.classes)
                else:
                    pass
        else:
            while True:
                stat = ['근력', '민첩', '체력', '지능', '지혜', '매력']
                nums = [16, 15, 13, 12, 9, 8]
                result = []
                print('그럼, 능력치를 선택할 차례입니다.')
                for i in stat:
                    for j, k in enumerate(nums):
                        print('{}.{}'.format(j + 1, k))
                    choose = int(input('{}에 몇점을 배치할까요? : '.format(i)))
                    result.append(nums.pop(choose - 1))
                for i in range(0, 6):
                    if result[i] > 15:
                        add = '(+2)'
                    elif result[i] > 12:
                        add = '(+1)'
                    elif result[i] > 8:
                        add = ''
                    elif result[i] == 8:
                        add = '(-1)'
                    print('{} : {}{}'.format(stat[i], result[i], add))
                choose = int(input('맞습니까?\n1.예 2.아니오 : '))
                if choose == 1:
                    break
                else:
                    pass
        print('가치관을 골라주세요.')
        value = show_and_select(resource.values)
        description = '{}과 {}, 그리고 {}을 가진 {}은...'.format(outlook1, outlook2, outlook3, name)
        description += input('마지막으로 모험을 떠나기 전,\n어떤 생활을 해왔는지'
                             '간략하게 작성해 주세요.')
        self.player.append(Character(name, cls, race, result, value, description))
        self.player[0].equip(item.Item('주먹'))

    def what_now(self):  # 마스터의 물음입니다.
        if len(self.cur_monster) > 0:
            if len(self.cur_monster) == 1:
                monsters = '{} 상태인 {}가 앞에 있습니다.'.format(self.cur_monster[0].get_cur_hp(), self.cur_monster[0].name)
            else:
                monsters = ''
                for monster in self.cur_monster:
                    monsters += '{} 상태인 {}, '.format(monster.get_cur_hp(), monster.name)
                monsters = monsters[:-2] + ' 가 앞에 있습니다.'
            print(monsters)
        string = input("이제 어떻게 하시겠습니까?? : ")  # 질문을 한뒤, '/'를 포함하는 명령어가 아니라면 전부 로그로 들어갑니다.
        if '/' in string:
            if string == '/게임종료':
                choose = int(input("정말 종료하시겠습니까?\n부가 자네를 그리워할걸세.\n1.예 2.아니오 : "))
                if choose == 1:
                    return 'end game'
            elif string == '/시스템명령어':
                for i in resource.command_list:
                    print(i)
            elif string == '/로그보기':
                for i in self.log:
                    print(i.get_log())
            elif string == '/직전취소':
                print('미구현')
            elif string == '/캐릭터확인':
                self.player[0].show_info()
            elif string == '/일반명령어':
                script_reader(resource.command_help1)
                for i in self.player[0].action.have:
                    print(i)
                print('이상입니다.')
            elif string == '/가방확인':
                self.player[0].inventory.show_inventory()
            elif string == '/몬스터추가':
                name = input('name : ')
                self.monster_setter(name)
            elif string == '/레벨업테스트':
                self.player[0].status.curexp_controller(-7)
                self.player[0].status.level_up()
                self.player[0].action.level_up(self.player[0])

        else:
            if '근접공격' in string:
                for monster in self.cur_monster:
                    if monster.name in string:
                        self.player[0].meleeAttack(monster)
            elif '소지품확인' in string:
                if self.battle_status:
                    print('전투중엔 불가능합니다...')
                    return
                for i in self.cur_monster:
                    if i.name in string and i.dead:
                        self.player[0].check_body(i)
                        self.monster_remover(i)
                    else:
                        print('주변에 죽어있지 않은듯하군요...')
            elif '착용' in string:
                if self.battle_status:
                    print('전투중엔 불가능합니다...')
                    return
                else:
                    for item in self.player[0].inventory.space:
                        if item.name in string:
                            print('{} 을(를) 착용합니다.'.format(item.name))
                            self.player[0].equip(item)
                            break
            elif '레벨업' in string:
                if self.battle_status:
                    print('전투중엔 불가능합니다...')
                    return
                self.player[0].level_up()
            elif '지식더듬기' in string:
                for stuff in resource.knowledge:
                    if stuff[0] in string:
                        self.player[0].action.stagKnowledge(self.player[0], stuff)
            elif '이동' in string:
                if self.battle_status:
                    print('전투중엔 불가능합니다...')
                    return
                else:
                    if '세이룬' in string:
                        print('세이룬으로 이동합니다.')
                        print('세이룬 성문에 도착하자 당신 일행을 알아본 문지기가\n'
                              '재미 없다는듯 눈길한번을 안주며 지나가라고 손짓합니다.')
                        self.set_location(vill)
                        vill.is_player_here = True
                    elif '부드러운 검' in string:
                        print("'부드러운 검'여관 내부로 들어갔습니다.")
                        for store in vill.inn:
                            if store.name == '부드러운 검':
                                break
                        store.npc.say_hello()
                        store.npc.say_intro()

            elif '두리번' in string:
                self.player_location.show_info()

            self.alive_monster_checker()
            self.log.append(Log(string, self.battle_status, False, True))

    def monster_setter(self, name):  # 전투상황에 돌입하게 몬스터를 추가하는 함수입니다.
        self.cur_monster.append(Monster(name))
        if self.battle_status:
            pass
        else:
            self.battle_status_changer()

    def monster_remover(self, monster):  # 루팅이후 몬스터를 제거하는 함수입니다.
        self.cur_monster.remove(monster)

    def alive_monster_checker(self):  # 전투후, 살아남은 몬스터를 확인하는 함수입니다.
        result = [monster.dead for monster in self.cur_monster]
        if all(result):
            self.battle_status = False

    def battle_status_changer(self):  # 전투상황으로 돌입하는 함수입니다.
        self.battle_status = False if self.battle_status is True else True

    def session_setter(self, name):  # 세션을 추가합니다.
        self.cur_session = Session(name)

    def set_location(self, place):
        self.player_location = place
        self.cur_monster = []

    def set_dungeon(self, dungeon):
        print(dungeon.info)
        print(dungeon.more_info)
        for monster in dungeon.first_wave:
            self.cur_monster.append(monster)
        if self.battle_status:
            pass
        else:
            self.battle_status_changer()


DM = Master()
DM.player.append(Character('테스트', '전사', '엘프', [16, 15, 13, 12, 9, 8], '선', '메롱'))
#DM.monster_setter('고블린')
vill = Village('세이룬')
dungeon = TrainingCenter()
DM.set_dungeon(dungeon)


if __name__ == '__main__':
    while True:
        answer = DM.what_now()
        if answer == 'end game':
            break