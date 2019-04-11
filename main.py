import random as rd
import datetime as dt
import pickle
import resource
import inventory as inven
import status
import monster as mob
import item


class Character:
    def __init__(self, name, cls, race, stat, value, description):  # 기본적인 캐릭터의 정보생성자입니다.
        self.status = status.Status(name, cls, race, stat[0], stat[1], stat[2],stat[3], stat[4], stat[5], value, description)
        self.inventory = inven.Inventory()
        self.action = Action()

    def show_info(self):  # /캐릭터확인 명령어를위한 함수입니다.
        self.status.show_status(self.inventory)
        self.status.show_equip_status()

    def meleeattack(self, op):  # 근접공격 명령어를위한 함수입니다.
        self.action.meleeAttack(op, self.status)

    def check_body(self, monster):  # 몬스터 루팅을위한 함수
        self.action.check_body(self.inventory, monster)

    def equip(self, item):  # 무기장비를 위한함수입니다.
        if item.type == 'weapon':
            self.inventory.item_setter(self.status.weapon_unequip())
            self.status.equip(self.inventory.item_getter(item.name))

        elif itme.type == 'armor':



class Action:  # 모든 액션을 담는 클래스입니다.
    def __init__(self):
        self.have =  ['근접공격', '원거리공격', '이동', '상황파악', '지식더듬기', '위험돌파', '방어', '협상', '야영',
                      '파수', '레벨업', '축하연', '구매', '판매', '휴식', '구인', '소지품확인']

    def got_damage(self, damage):
        if damage > 5:
            random_sentence_printer(resource.get_damage_sentence_hurt)
        elif damage > 3:
            random_sentence_printer(resource.get_damage_sentence_normal)
        else:
            random_sentence_printer(resource.get_damage_sentence_not_hurt)

    def give_damamge(self, damage):
        if damage > 5:
            random_sentence_printer(resource.damage_sentence_good)
        elif damage > 3:
            random_sentence_printer(resource.damage_sentence_normal)
        else:
            random_sentence_printer(resource.damage_sentence_bad)

    def get_attack(self, op, status):  # 반격당하는 함수입니다.
        if op.dead:
            print('{} 는 쓰러졌다'.format(op.name))
        else:
            damage = rollDice(op.damage_pcs, op.damage_dice, op.add_dam)
            damage -= status.armor
            self.got_damage(damage)
            status.curhp_controller(self, -damage)

    def meleeAttack(self, op, status):  # 기본적으로 근력판정, 10 이상은 공격후 회피(혹은 빈틈을 주고 1d6딜 추가) 7~9는 공격성공후 빈틈
        if DM.player[0].status.micro_attack:
            correction = status.dex_correction
        else:
            correction = status.str_correction
        roll = rollDice(2, 6, correction)
        if roll > 9:
            choose = int(input('공격은 멋들어지게 들어갈것같습니다! 어떻게 할까요??\n1.공격을 명중시킨뒤 회피\n2.빈틈을 보이고 1d6 피해를 더주기\n: '))
            if choose == 1:
                print('{}은(는) {}을(를) 공격한뒤 {}의 공격을 회피했다!'.format(status.name, op.name, op.name))
                damage = rollDice(1, status.damage_dice, status.damage_correction)
                print('{}의 피해를 {}에게 주었다.'.format(op.get_damage(damage), op.name))
                self.give_damamge(damage)
            else:
                print('{}은(는) {}을(를) 강하게 공격했다!'.format(status.name, op.name))
                damage = rollDice(1, status.damage_dice, status.damage_correction)
                damage += rollDice(1, 6, 0)
                print('{}의 피해를 {}에게 주었다.'.format(op.get_damage(damage), op.name))
                self.give_damamge(damage)
                self.get_attack(op, status)
        elif roll > 6:
            print('{}은(는) {}를 공격했다! 하지만 헛점을 보이고 말았다'.format(status.name, op.name))
            damage = rollDice(1, status.damage_dice, status.damage_correction)
            print('{}의 피해를 {}에게 주었다.'.format(op.get_damage(damage), op.name))
            self.give_damamge(damage)
            self.get_attack(op, status)
        else:
            print('{}는 공격을 피하곤 반격해왔다!'.format(op.name))
            self.get_attack(op, status)
        return roll

    def missileAttack(self):  # 민첩판정 10이상은 명중, 7~9는 곤경,-1d6피해, 발수1줄이기중 플레이어 선택
        pass

    def breakThrough(self):  # 본인이 원하는 방법(판정)으로 위험을 돌파함 10이상이면 무리없이 원하는것을 얻음
        pass                 # 7~9는 덜좋은결과, 어려운선택, 불리한거래중 한가지

    def defense(self):  # 사람,물건,장소를 지키는 액션, 체력판정, 10+ 예비3점 7~9 예비1점
        pass            # 방어태세동안 대상이 공격받을시 예비1점 소모로 한가지선택 / 대신맞음,피해나효과 반으로, 공격자빈틈만들어, 지정한 우리편 캐릭터의 다음판정 +1, 자기레벨만큼 피해를 상대에게 가함

    def stagKnowledge(self):  # 지식더듬기, 지식판정을해서 10+ 유용한 사실 7~9 흥미롭기만한 사실
        pass

    def graspSituatino(self):  # 상황파악, 지혜판정 10+ 3개선택, 7~9 1개선택 /여기서 최근무슨일?,무슨일이 일어나려고하는가?,어떤것에 주의를 기울여야하는가?, 여기서 나에게 유용하거나 값진것은 무엇?, 이 상황은 누가 장악?, 여기서 겉보기와 다른것은 무엇?
        pass

    def nagotiation(self):  # 협상, 매력판정 10+ 시키는것을함, 7~9 약속을 보장할 무언가를 요구
        pass

    def coOperation(self):  # 협조혹은 방해
        pass

    def death(self, status):  # 황천길, 2d6을 굴려, 10+ 단순기절 7~9 거래를 해서 성공하면 기절
        input('{} 은(는) 체력이 다해 눈앞이 캄캄해졌습니다...\n'.format(status.name))
        script_reader(resource.death_describe)
        print('"{} 왔느냐..."'.format(status.name))
        result = rollDice(2, 6, 0)
        if result > 9:
            script_reader(resource.death_talking_alive)
            status.cur_hp = 1
        elif result > 7:
            print('7이상 테스트')
        else:
            print('게임 오버')

    def tooHeavy(self):  # 최고하중 +1, +2까지는 모든 판정 -1패널티 그 이상은 액션을 할때 무게1 버리고 -1판정으로 액션
        pass

    def camping(self):  # 식량 하나소비함, 위험한곳에선 파수가능, 레벌업가능, 몇시간 자면 최대hp절반만큼 치유
        pass

    def gaurding(self):  # 야영중의 파수, 무언가 다가올때 지혜판정 10+ 전원이 다음판정 +1 7~9 파수성공, 6- 습격당함
        pass

    def traveling(self):  # 험난한여정, 일행을 길잡이,척후,보급으로 정하고 비는 파트는 6판정 지혜판정이며 척후의경우 기습을10+로 기습을할수있음
        pass

    def levelUp(self):  # 쉴 시간이 있고 경험치가 현재레벨+7 이상인경우 렙업, 고급액션(법사는주문)하나 선택, 능력치1증가 최대 18
        pass

    def throwParty(self):  # 100골드를 써서 2d6을 굴림, 추가100골드당 +1판정 10+일때 세가지, 7~9한가지 6-한가지 고르지만 뭔가 크게잘못됨
        pass  # /도움이 되는 NPC와 친해짐, 좋은기회의 소문을 들음, 유용한정보를 얻음, 축하연도중 나쁜일이 안생김

    def closeSession(self):  # 세션종료 인연이해결되면 새인연 설정후 경험치+1, 가치관액션이 발동했다면 경험치+1,
        pass  # 일행이 세계에대해 뭔가 새롭고 중요한 사실을 배웠거나, 중요한괴물혹은 적을 극복했는가, 기억에 남을 보물을 얻었는가에서 해당되는것에 각각 경험치+1

    def getSupply(self):  # 보급, 흔하지않은것은 매력판정을해서 10+면 원하는물건을 공정가격에구매가능, 7~9 비싸거나 비슷한것만있음
        pass

    def resting(self):  # 하루종일 쉬면 hp모두회복 3일쉬면 약화효과 하나골라서 제거, 의사도움받고있으면 이틀만에 약화 치유
        pass

    def hiring(self):  # 구인광고를 내면 2d6판정, 보수가 높다고하면 +1, 목적을 알리면 +1, 보물 일부를 나눠준다고하면 +1, 평판이좋으면 +1
        pass  # 10+ 괜찮은 사람몇명이 응해서 고를수있음, 7~9자격미달들이옴, 6- 자존심 센 도련님, 정신 나간 용병, 위장한 적 등등이 옴,
              # 다 돌려보내면 다음 구인에 -1패널티

    def infamous(self):  # 악명, 말썽을 만든곳에 다시오면 매력판정 10+ 모두가자신을 알아봄 7~9마스터가 셋중고름
        pass  # / 경비대의 체포명령, 누가 현상금을 걸음, 내 범행때문에 소중한사람이 곤경에 처함

    def practice(self):  # 1~2주시간을보내면 예비1점, 1개월 3점 , 수련성과가 드러난상황에서 얘비를 사용해 판정에 +1
        pass  # 한 판정에 예비는 한개밖에 못씀

    def action_adder(self, name):  # 사용할수있는 액션을 추가해주는 함수입니다.
        self.have.append(name)

    def check_body(self, inventory, op):  # 죽은 몬스터를 루팅하는 함수입니다.
        money = op.stuff.pop(0)
        inventory.money_controller(money)
        print('{} 닢을 얻었습니다.'.format(money))
        if len(op.stuff) > 0:
            for i in op.stuff:
                inventory.item_setter(i)
                print('{} 를 얻었습니다. '.format(i.name))


class Place:
    pass


class Log:
    def __init__(self, string):
        self.timestamp = dt.datetime.now()
       # self.type = type  # 문장의 타입을 담는 합수 / 예: 전투, 대화, 상황묘사
        self.sentence = string

    def get_log(self):
        return str(self.timestamp) + ') ' + self.sentence


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


def rollDice(pcs, num, correction):  # 주사위를 굴리는 함수입니다. 인수로 몇개인지 몇면체인지, 보정값을 받습니다.
    result = []
    for i in range(pcs):
        result.append(rd.randint(1, num))
    num = 0
    string = ''
    for i in result:
        num += i
        string += str(i) + ' + '
    num += correction
    string += str(correction) + ' = ' + str(num)
    print(string)
    return num  # 결과를 출력하며, 최종 값을 반환합니다.


class Session:  # 세션을 담습니다.
    def __init__(self, name):  # 리소스에 미리 설정된 데이터를 이름으로 검색해, 속성에 담습니다.
        for i in resource.session:
            if i[0] == name:
                self.session = i
                break
        self.name = name
        self.monster = []
        for i in range(self.session[2]):
            self.monster.append(Monster(self.session[1]))
        script_reader(self.session[3])


class Master:
    def __init__(self):  # 마스터의 생성자로, 플레이어 캐릭터와, 세션, 장소들을 담고있습니다.
        self.player = []
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
                for monster in cur_monster:
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

        else:
            if '근접공격' in string:
                for monster in self.cur_monster:
                    if monster.name in string:
                        self.player[0].meleeattack(monster)
            elif '소지품확인' in string:
                if self.battle_status:
                    print('전투중엔 불가능합니다...')
                    return
                for i in self.cur_monster:
                    if i.name in string and i.dead:
                        self.player[0].check_body(i)
                        self.monster_remover(i)
                    else:
                        print('주변에 죽어있지 않은듯합니다.')
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
            self.alive_monster_checker()
            self.log.append(Log(string))

    def monster_setter(self, name):  # 전투상황에 돌입하게 몬스터를 추가하는 함수입니다.
        self.cur_monster.append(mob.Monster(name))
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
        if self.battle_status:
            self.battle_status = False
        else:
            self.battle_status = True

    def session_setter(self, name):  # 세션을 추가합니다.
        self.cur_session = Session(name)


DM = Master()
DM.player.append(Character('테스트', '전사', '엘프', [16, 15, 13, 12, 9, 8], '선', '메롱'))
DM.monster_setter('고블린')

if __name__ == '__main__':
    while True:
        answer = DM.what_now()
        if answer == 'end game':
            break