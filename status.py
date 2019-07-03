from item import *

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
        self.equip_s = Shield('없음')
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
                print('{} 능력치가 1 올라갑니다.'.format(answer))
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
              '소지 경험치 : {} 점\n'
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
            if self.str == 18:
                print('더이상 근력을 올릴수 없습니다.')
                return False
            else:
                self.str += num
                self.weight_limit += num
        elif name == '민첩':
            if self.dex == 18:
                print('더이상 민첩을 올릴수 없습니다.')
                return False
            else:
                self.dex += num
        elif name == '체력':
            if self.con == 18:
                print('더이상 체력을 올릴수 없습니다.')
                return False
            else:
                self.con += num
                self.max_hp += num
                self.cur_hp = self.max_hp
        elif name == '지식':
            if self.int == 18:
                print('더이상 자식을 올릴수 없습니다.')
                return False
            else:
                self.int += num
        elif name == '지혜':
            if self.wis == 18:
                print('더이상 지혜를 올릴수 없습니다.')
                return False
            else:
                self.wis += num
        elif name == '매력':
            if self.cha == 18:
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

    def correction_collector(self, name):  # 인수로 받은 스탯의 패널티의 총합을 반환하는 함수입니다.
        if name == '근력':
            result = self.str_correction + self.whole_penalty + self.temp_whole_penalty
        elif name == '민첩':
            result = self.dex_correction + self.whole_penalty + self.temp_whole_penalty
        elif name == '체력':
            result = self.con_correction + self.whole_penalty + self.temp_whole_penalty
        elif name == '지식':
            result = self.int_correction + self.whole_penalty + self.temp_whole_penalty
        elif name == '지혜':
            result = self.wis_correction + self.whole_penalty + self.temp_whole_penalty
        else:
            result = self.cha_correction + self.whole_penalty + self.temp_whole_penalty
        self.temp_whole_penalty = 0
        return result

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
        if temp.name == '없음':
            return
        self.equip(Armor('없음'))
        self.armor_controller(-temp.armor)
        if temp.tag == '불편':
            self.penalty_controller(-1)
        return temp

    def shiled_unequip(self):  # 방패 해제 함수입니다.
        temp = self.equip_s
        self.equip(Shield('없음'))
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
        if num > 0:
            string = '+' + str(num)
        else:
            string = str(num)
        print('경험치가 {} 되었습니다.'.format(string))

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

class Strength:
    pass