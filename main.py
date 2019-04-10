import random as rd
import datetime as dt
import pickle
import resource


class Character:
    def __init__(self, name, cls, race, stat, value, description):  # 기본적인 캐릭터의 정보생성자입니다.
        self.status = Status(name, cls, race, stat[0], stat[1], stat[2],stat[3], stat[4], stat[5], value, description)
        self.inventory = Inventory()
        self.action = Action()

    def show_info(self):  # /캐릭터확인 명령어를위한 함수입니다.
        self.status.show_status(self.inventory)
        self.status.show_equip_status()

    def meleeattack(self, op):  # 근접공격 명령어를위한 함수입니다.
        self.action.meleeAttack(op, self.status)

    def check_body(self, monster):  # 몬스터 루팅을위한 함수
        self.action.check_body(self.inventory, monster)

    def equip(self, item):
        if item.type == 'weapon':
            self.inventory.item_setter(self.status.weapon_unequip())
            self.status.equip(self.inventory.item_getter(item.name))

class Status:
    def __init__(self, name, cls, race, str, dex, con, wis, int, cha, value, description):
        self.name = name
        self.str = str
        self.str_correction = 0
        self.dex = dex
        self.dex_correction = 0
        self.con = con
        self.con_correction = 0
        self.wis = wis
        self.wis_correction = 0
        self.int = int
        self.int_correction = 0
        self.cha = cha
        self.cha_correction = 0
        self.armor = 0
        self.cur_exp = 0
        self.cls = cls  # 직업을 담는 변수입니다.
        self.race = race  # 종족을 담는 변수입니다.
        self.equip_w = Weapon('주먹') # 장비하고있는 무기
        self.equip_a = Armor('없음')
        self.equip_s = Armor('없음')
        self.battle_stat = False  # 전투중인지 아닌지를 표현합니다.
        self.health_stat = []  # 적용중인 약화효과를 표현합니다.
        self.value = value  # 가치관을 담는 변수입니다.
        self.whole_penalty = 0  # 현재 적용중인 패널티를 담는 변수입니다.
        self.temp_whole_penalty = 0
        self.damage_correction = 0
        self.description = description
        self.attack_range = []
        self.micro_attack = False
        if cls == '전사':
            self.max_hp = self.con + 10
            self.damage_dice = 10
            self.weight_limit = self.str + 12
        elif cls == '드루이드':
            self.max_hp = self.con + 6
            self.damage_dice = 6
            self.weight_limit = self.str + 6
        elif cls == '음유시인':
            self.max_hp = self.con + 6
            self.damage_dice = 6
            self.weight_limit = self.str + 9
        elif cls == '마법사':
            self.max_hp = self.con + 4
            self.damage_dice = 4
            self.weight_limit = self.str + 7
        elif cls == '사제':
            self.max_hp = self.con + 8
            self.damage_dice = 6
            self.weight_limit = self.str + 10
        elif cls == '사냥꾼':
            self.max_hp = self.con + 8
            self.damage_dice = 8
            self.weight_limit = self.str + 11
        elif cls == '성기사':
            self.max_hp = self.con + 10
            self.damage_dice = 10
            self.weight_limit = self.str + 12
        elif cls == '도적':
            self.max_hp = self.con + 6
            self.damage_dice = 8
            self.weight_limit = self.str + 9
        self.cur_hp = self.max_hp
        self.cur_weight = 0
        self.level = 1
        self.basic_stat_correction_updater()

    def level_up(self):
        if self.level == 10:
            print('더이상 레벨업 할수 없어보이는군요..')
        else:
            reduce = self.level + 7
            if reduce > self.cur_exp:
                print('경험치가 부족해보입니다...')
            else:
                self.cur_exp -= reduce
                print('근력 : {} ({})\n'
              '민첩 : {} ({})\n'
              '체력 : {} ({})\n'
              '지혜 : {} ({})\n'
              '지식 : {} ({})\n'
              '매력 : {} ({})\n'.format(self.str, self.stat_correction_getter(self.str_correction),
                                      self.dex, self.stat_correction_getter(self.dex_correction),
                                      self.con, self.stat_correction_getter(self.con_correction),
                                      self.wis, self.stat_correction_getter(self.wis_correction),
                                      self.int, self.stat_correction_getter(self.int_correction),
                                      self.cha, self.stat_correction_getter(self.cha_correction)))
                while True:
                    answer = input('이중 어느것을 올리시겠습니까? : ')
                    for i in resource.status_name:
                        if i in answer:
                            answer = i
                    if self.stat_controller(answer, 1):
                        print('{} 능력치가 1 올라갑니다.'.format(i))
                        break
        self.level += 1

    def show_status(self, inventory):
        print('이름 : {}\n'
              '종족 : {}\n'
              '가치관 : {}\n'
              '레벨 : {}\n'
              'HP : {} / {}\n'
              '근력 : {} ({})\n'
              '민첩 : {} ({})\n'
              '체력 : {} ({})\n'
              '지혜 : {} ({})\n'
              '지식 : {} ({})\n'
              '매력 : {} ({})\n'
              '피해주사위 : d{}\n'
              '피해 보정치 : {}\n'
              '소지 경험치 : {}\n'
              '소지 무게 : {} / {}\n'
              '소지 금 : {}\n'
              '장갑 : {}\n'
              '적용중인 약화효과 : {}'.format(self.name, self.race, self.value, self.level, self.cur_hp, self.max_hp,
                                      self.str, self.stat_correction_getter(self.str_correction),
                                      self.dex, self.stat_correction_getter(self.dex_correction),
                                      self.con, self.stat_correction_getter(self.con_correction),
                                      self.wis, self.stat_correction_getter(self.wis_correction),
                                      self.int, self.stat_correction_getter(self.int_correction),
                                      self.cha, self.stat_correction_getter(self.cha_correction),
                                      self.damage_dice, self.stat_correction_getter(self.damage_correction),
                                      self.cur_exp, self.cur_weight, self.weight_limit, inventory.money, self.armor, self.weakness_getter()))

    def show_equip_status(self):  # 착용장비를 출력하는 함수입니다.
        print('무기 : {}\n'
              '갑옷 : {}\n'
              '방패 : {}'.format(self.equip_w.name, self.equip_a.name, self.equip_s.name))

    def weakness_controller(self, name, a_o_r):  # 약화효과의 증감을위한 함수입니다.
        if a_o_r == 'a':
            if name in self.health_stat:
                pass
            else:
                self.health_stat.append(name)
                if name == '무기력':
                    self.stat_correction_controller('근력', -1)
                elif name == '경련':
                    self.stat_correction_controller('민첩', -1)
                elif name == '쇠약':
                    self.stat_correction_controller('체력', -1)
                elif name == '당황':
                    self.stat_correction_controller('지혜', -1)
                elif name == '얼떨떨':
                    self.stat_correction_controller('지식', -1)
                else:
                    self.stat_correction_controller('매력', -1)
        else:
            self.health_stat.remove(name)
            if name == '무기력':
                self.stat_correction_controller('근력', 1)
            elif name == '경련':
                self.stat_correction_controller('민첩', 1)
            elif name == '쇠약':
                self.stat_correction_controller('체력', -1)
            elif name == '당황':
                self.stat_correction_controller('지혜', -1)
            elif name == '얼떨떨':
                self.stat_correction_controller('지식', -1)
            else:
                self.stat_correction_controller('매력', -1)

    def weakness_getter(self):
        if len(self.health_stat) == 0:
            return '없음'
        result = ''
        for i in self.health_stat:
            result += i
            result += ', '
        return result [:-2]

    def stat_controller(self, name, num):  # 레벨업 등의 사유로 스탯 증감을 위한 함수입니다.
        if name == '근력':
            if self.str == 18 and u_o_d == 'u':
                print('더이상 힘을 올릴수 없습니다.')
                return False
            else:
                self.str += num
                self.weight_limit += num
        elif name == '민첩':
            if self.dex == 18 and u_o_d == 'u':
                print('더이상 민첩을 올릴수 없습니다.')
                return False
            else:
                self.dex += num
        elif name == '체력':
            if self.con == 18 and u_o_d == 'u':
                print('더이상 체력을 올릴수 없습니다.')
                return False
            else:
                self.con += num
                self.max_hp += num
                self.cur_hp = self.max_hp
        elif name == '지식':
            if self.int == 18 and u_o_d == 'u':
                print('더이상 자식을 올릴수 없습니다.')
                return False
            else:
                self.int += num
        elif name == '지혜':
            if self.wis == 18 and u_o_d == 'u':
                print('더이상 지혜를 올릴수 없습니다.')
                return False
            else:
                self.wis += num
        elif name == '매력':
            if self.cha == 18 and u_o_d == 'u':
                print('더이상 매력을 올릴수 없습니다.')
                return False
            else:
                self.cha += num
        else:
            return False
        self.basic_stat_correction_updater()
        return True

    def basic_stat_correction_updater(self):  # 통합적 스탯 보정 증감을 위한 함수입니다.
        def cal(num):
            correction = 0
            if num == 18:
                correction += 3
            elif num > 15:
                correction += 2
            elif num > 12:
                correction += 1
            elif num < 9:
                correction -= 1
            elif num < 6:
                correction -= 2
            elif num < 4:
                correction -= 3
            return correction
        self.str_correction = cal(self.str)
        self.dex_correction = cal(self.dex)
        self.con_correction = cal(self.con)
        self.int_correction = cal(self.int)
        self.wis_correction = cal(self.wis)
        self.cha_correction = cal(self.cha)

    def stat_correction_controller(self, name, num):  # 스탯보정을위한 추가 함수입니다.
        if name == '근력':
            self.str_correction += num
        elif name == '민첩':
            self.dex_correction += num
        elif name == '체력':
            self.con_correction += num
        elif name == '지식':
            self.int_correction += num
        elif name == '지혜':
            self.wis_correction += num
        else:
            self.cha_correction += num

    def stat_correction_getter(self, num):
        if num == 0:
            return '0'
        elif num > 0:
            return '+' + str(num)
        else:
            return str(num)

    def equip(self, item):  # 무기를 장비하는 함수입니다. 이미 장비하고있는게있다면 해당장비를 반환합니다.
        if item.type == 'weapon':
            self.equip_w = item
            self.attack_range_controller(item)
            if '정밀' in item.tag:
                self.micro_attack_changer()
        elif item.type == 'armor':
            self.equip_a = item
            self.armor_controller(item.armor)
            if item.tag == '불편':
                self.penalty_controller(1)
        elif item.type == 'shield':
            self.equip_s = item
            self.armor_controller(item.armor)
            if item.tag == '불편':
                self.penalty_controller(1)

    def weapon_unequip(self):  # 무기 해제 함수입니다.
        temp = self.equip_w
        self.equip(Weapon('주먹'))
        if '정밀' in temp.tag:
            self.micro_attack_changer()
        if temp.name == '주먹':
            return
        return temp

    def micro_attack_changer(self):
        if self.micro_attack:
            self.micro_attack = False
        else:
            self.micro_attack = True

    def armor_unequip(self):  # 갑옷 해제 함수입니다.
        temp = self.equip_a
        self.equip(Armor('없음'))
        self.armor_controller(-temp.armor)
        if temp.tag == '불편':
            self.penalty_controller(-1)
        if temp.name == '없음':
            return
        return temp

    def shiled_unequip(self):  # 방패 해제 함수입니다.
        temp = self.equip_s
        self.equip(Shild('없음'))
        self.armor_controller(-temp.armor)
        if temp.tag == '불편':
          self.penalty_controller(-1)
        if temp.name == '없음':
            return
        return temp

    def battle_status_changer(self):
        if self.battle_stat:
            self.battle_stat = False
        else:
            self.battle_stat =  True

    def armor_controller(self, num):  # 장갑의 증감을 다루는 함수입니다.
        self.armor += num

    def damage_correction_controller(self, num):  # 데미지 보정의 증감을 담당하는 함수입니다.
        self.damage_correction += num

    def damage_dice_controller(self, num):  # 데미지 다이스를 조정하는 함수이며 인수로 받은값으로 변환합니다.
        self.damage_dice = num

    def maxhp_controller(self, num):  # 최대 체력을 조정하는 함수입니다.
        self.max_hp += num

    def curhp_controller(self, action, num):  # 현재 체력을 조정하는 함수입니다. 0 이되면 황천길 액션을 호출합니다.
        self.cur_hp += num
        if self.cur_hp <= 0:
            action.death(self)

    def curexp_controller(self, num):  # 현재 경험치를 조정하는 함수입니다.
        self.cur_exp += num

    def weightlimit_controller(self, num):  # 최대 소지무게를 조정하는 함수입니다.
        self.weight_limit += num

    def curweight_controller(self, num):  # 현재 소지무게를 조정하는 함수입니다.
        self.cur_weight += num

    def attack_range_controller(self, item):  # 무기를 장착할때 공격가능 거리를 변결해주는 함수입니다.
        self.attack_range = item.range

    def action_controller(self, action):  # 레벨업등으로 액션이 추가될때 사용되는 함수입니다.
        self.action.append(action.name)

    def penalty_controller(self, num):  # 전체 판정의 패널티를 조종하는 함수입니다.
        self.whole_penalty += num


class Inventory:  # 인벤토리 클래스입니다.
    def __init__(self):  # 생성자로 space속성을 추가합니다.
        self.space = []
        self.money = 0

    def item_getter(self, name):  # 가방에서 아이템을 꺼내는 함수입니다.
        for idx, item in enumerate(self.space):
            if item.name == name:
                return self.space.pop(idx)
        return False

    def item_setter(self, item):  # 가방에 아이템을 집어넣는 함수입니다.
        self.space.append(item)

    def show_inventory(self):  # 가방의 내용물을 출력해주는 함수입니다.
        for item in self.space:
            item.show_info()

    def money_controller(self, num):  # 소지금의 증감을 담당하는 함수입니다.
        temp = self.money
        if temp + num < 0:
            print('소지금이 부족한듯싶군요...')
        else:
            self.money = temp


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


class Equipment:

    def take_on(self):
        if self.equip_stat:
            print('이미 해당 장비를 착용중입니다.')
        else:
            self.equip_stat = True
            print('{} 을/를 장비했습니다.')

    def take_off(self):
        if self.equip_stat:
            self.equip_stat = False
        else:
            print('해당 장비를 입고있지 않습니다.')

    def get_this(self):
        print('{} 이/가 가방에 추가되었습니다.'.format(name))

    def show_info(self):
        print('{} ) 장갑:{} {}닢 무게:{} {}'.format(self.name, self.armor, self.price, self.weight, self.tag))


class Armor(Equipment):
    def __init__(self, name):
        self.name = name
        self.equip_stat = False
        self.type = 'armor'
        self.tag = ''
        for i in resource.armor_list:
            if name == i[0]:
                self.armor = i[1]
                self.price = i[2]
                self.weight = i[3]
                if len(i) > 4:
                    self.tag = i[4]
                else: self.tag = ''


class Shiled(Equipment):
    def __init__(self, name):
        self.name = name
        self.equip_stat = False
        self.type = 'shiled'
        self.tag = ''
        for i in resource.armor_list:
            if name == i[0]:
                self.armor = i[1]
                self.price = i[2]
                self.weight = i[3]
                if len(i) > 4:
                    self.tag = i[4]
                else: self.tag = ''


class Weapon(Equipment):
    def __init__(self, name):
        self.name = name
        self.equip_stat = False
        self.tag = []
        self.type ='weapon'
        for i in resource.weapon_list:
            if name == i[0]:
                self.damage = i[-3]
                self.price = i[-2]
                self.weight = i[-1]
                self.range = i[1]
                if len(i) > 5:
                    idx = 2
                    for j in range(len(i) - 5):
                        self.tag.append(i[idx])
                        idx += 1
                else:
                    self.tag = ''

    def show_info(self):
        range = ''
        if len(self.range) > 1:
            for i in self.range:
                range += i
                range +=', '
            range = range[:-2]
        else:
            range = self.range[0]

        print('{} ) 공격범위: {} {} 닢 무게:{}'.format(self.name, range, self.price, self.weight))


class Item:
    def __init__(self, name):
        self.name = name
        for i in resource.item_list:
            if name == i[0]:
                self.pcs = i[1]
                self.price = i[2]
                self.weight = i[3]
                self.description = i[-1]
                if i[4] == '느림':
                    self.late = True
                else: self.late = False
        print('{} 이/가 가방에 추가되었습니다.'.format(name))

    def use_this(self):
        self.pcs -= 1
        if self.pcs == 0:
            return False
        else: return True

    def get_description(self):
        return self.description

    def show_info(self):  # 정보를 출력하는 함수입니다.
        print('{}) 수량 : {} 무게: {} {}'.format(self.name, self.pcs, self.weight, self.description))


class Monster:
    def __init__(self, name):
        self.name = name
        for i in resource.monster_list:
            if name == i[0]:
                self.attack_name = i[1]
                self.attack_reach = i[2]
                self.damage_pcs = i[3]
                self.damage_dice = i[4]
                self.max_hp = i[5]
                self.cur_hp = i[5]
                self.armor = i[6]
                self.features = []
                self.dead = False
                self.stuff = [3, Weapon('레이피어'), Armor('사슬 갑옷')]
                self.far = None
                self.add_dam = 0
                if len(i) > 7:
                    self.features = i[7:-1]

    def get_cur_hp(self):  # 남은체력을 모호하게 표현해주는 함수입니다.
        balance = self.cur_hp / self.max_hp * 100
        if balance == 100:
            return resource.monster_hp_list[0]
        elif balance >= 80:
            return resource.monster_hp_list[1]
        elif balance >= 60:
            return resource.monster_hp_list[2]
        elif balance >= 40:
            return resource.monster_hp_list[3]
        elif balance >= 20:
            return resource.monster_hp_list[4]
        elif balance > 0:
            return resource.monster_hp_list[5]
        else:
            return resource.monster_hp_list[-1]

    def get_damage(self, damage):
        correction_damage = damage - self.armor
        self.cur_hp -= correction_damage
        if self.cur_hp < 1:
            self.dead = True
        if correction_damage < 0:
            correction_damage = 0
        return correction_damage

    def coming_for_you(self):
        if self.far != '한걸음':
            pass

    def normal_attack(self):  # 일반공격으로 선공당했을때의 함수입니다.
        pass

    def sneak_attack(self):  # 암습으로 선공당했을때의 함수입니다.
        pass


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
        if self.battle_status:
            self.battle_status = False
        else:
            self.battle_status = True

    def session_setter(self, name):  # 세션을 추가합니다.
        self.cur_session = Session(name)


DM = Master()
DM.player.append(Character('테스트', '전사', '엘프', [16, 15, 13, 12, 9, 8], '선', '메롱'))
DM.monster_setter('고블린')
while True:
    answer = DM.what_now()
    if answer == 'end game':
        break