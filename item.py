import resource

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


class Shield(Equipment):
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
