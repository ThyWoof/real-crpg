import item
import resource

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
                self.stuff = [3, item.Weapon('레이피어'), item.Armor('사슬 갑옷')]
                self.distance = None
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
        if self.distance == '몇걸음':
            self.distance = '한걸음'
        elif self.distance == '한걸음':
            pass

    def distance_controller(self, distance):
        if distance == '한걸음' and self.distance != distance:
            self.distance = distance
        elif distance == '반걸음' and self.distance != distance:
            self.distance = distance
        elif distance == '몇걸음' and self.distance != distance:
            self.distance = distance

    def normal_attack(self):  # 일반공격으로 선공당했을때의 함수입니다.
        pass

    def sneak_attack(self):  # 암습으로 선공당했을때의 함수입니다.
        pass
