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
                    self.features = i[7:-2]

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

    def normal_attack(self, character):  # 일반공격으로 선공당했을때의 함수입니다.
        print('{}가 공격해왔다!'.format(self.name))
        character.action.get_attack(self, character.status)

    def sneak_attack(self):  # 암습으로 선공당했을때의 함수입니다.
        pass

    def get_good_knowledge(self):  # 지식더듬기 대성공일때 문구를 반환하는 함수
        return self.knowledge1 + self.knowledge2

    def get_knowledge(self):  # 지식더듬기 부분성공일때 문구를 반환하는 함수
        return self.knowledge1

class Goblin(Monster):
    def __init__(self):
        self.name = '고블린'
        self.attack_name = '창 공격'
        self.attack_reach = ['한걸음', '몇걸음']
        self.damage_pcs = 1
        self.damage_dice = 6
        self.max_hp = 3
        self.cur_hp = self.max_hp
        self.armor = 1
        self.features = ['대집단', '작음', '지능적', '조직적']
        self.dead = False
        self.stuff = [2]
        self.distance = None
        self.add_dam = 0
        self.knowledge1 = '이들이 어디서 왔는지는 아무도 모릅니다. 엘프들은 드워프 잘못이라고 합니다.' \
                         '땅속 깊은 곳에서 자기들끼리 살던 것을 공연히 파내어 지상에 불러들였다는것입니다.' \
                         '드워프들은 고블린이 엘프의 자손이라고 합니다. 엘프들이 버린 아이들이 어둠속에서 자라나 지금에 이르렀다는 것입니다.' \
                         '그러나 사실을 말하자면 고블린들은 태고적부터 여기에 있었고, 문명 종족들이 모두 쇠퇴하여 사라진 뒤에도' \
                         '아마 남을 것입니다. 고블린은 결코 멸망하지 않습니다. 수가 너무나 많기 때문입니다.'
        self.knowledge2 = '가만히 두면 더욱 불어날것입니다.'