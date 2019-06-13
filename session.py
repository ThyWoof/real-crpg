#import random as rd
import resource
from item import Item

class Session:
    pass

class Village:
    def __init__(self, name):
        if name == "세이룬":
            self.inn = [Store("부드러운 검", "싸구려 여관")]
            script = NpcSctipt('안녕하시오', "감사하오", "나는 이 '부드러운 검' 여관을 20년간 지켜온 랄프라 하오", "안녕히 가시오", "퀘스트를 줍니다.")
            test = Npc("랄프", 41, "남", script)
            self.inn[0].set_npc(test)
            self.is_player_here = False

    def show_info(self):
        print("두리번 거려보니 저기에 35년 전통을 자랑하는 '부드러운 검' 여관이 있는것이 보이는군요.")


class Spot:
    def __init__(self):
        pass

    def show_info(self):
        pass


class TrainingCenter:
    def __init__(self):
        pass


class Npc:
    def __init__(self, name, age, gender, script, store=None):  # NPC캐릭터의 이름, 나이, 대화내용들을 준비합니다.
        self.name = name
        self.age = age
        self.gender = gender
        self.script = script
        self.store = store

    def say_hello(self):  # npc가 가지고있는 인사를 출력합니다.
        print(self.script.greeting)

    def say_intro(self):  # 자기소개를 합니다.
        print(self.script.intro)

    def say_info(self):  # 뭔가 중요한 정보를 제공합니다.
        print(self.script.info)

    def say_thankyou(self): # 감사하다고 출력합니다.
        print(self.script.thankyou)

    def open_store(self, character):  # 해당 npc가 가지고있는 상품을 보여줍니다.
        if self.store == None:
            print("소유하고 있는 상점이 없습니다.")
        else:
            self.store.show_menu(character)

    def say_goodbye(self):  # 헤어질때 인사를 출력합니다.
        print(self.script.bye)

    def set_store(self, store):
        self.store = store


class Store:
    def __init__(self, name, store_type, npc=None):  # 이름과 상점 타입등을 초기값으로 지정합니다
        self.name = name
        self.type = store_type
        self.npc = npc
        self.service = Service(store_type)
        self.selling = Selling(store_type)

    def show_menu(self, character):
        self.service.show_menu(character)
        self.selling.show_menu(character)

    def set_npc(self, npc):
        self.npc = npc
        self.npc.set_store(self)

    def sell_stuff(self, name, character):
        for item in resource.item_list:
            if name == item[0]:
                if character.inventory.money > item[2]:
                    pass


    def get_service(self, name):
        pass


class Service:
    def __init__(self, type):
        if type == '싸구려 여관':
            self.sleep = resource.cheap_inn_sleep
            self.meals = resource.cheap_inn_meals

    def show_menu(self, character):
        print('--------서비스--------')
        print(self.sleep[0], self.sleep[1] - character.status.cha, "닢")
        print(self.meals[0], self.meals[1], '닢')

class Selling:
    def __init__(self, type):
        self.slot = []
        if type == "싸구려 여관":
            for item in resource.item_list:
                self.slot.append(Item(item[0]))

    def show_menu(self, character):
        print('---------판매--------')
        for item in self.slot:
            print('{} {}회분 {}닢 무게 {}'.format(item.name, item.pcs, item.price, item.weight))


class Field:
    pass


class NpcSctipt:
    def __init__(self, greet, thankyou, intro, bye, info=None):
        self.greeting = greet
        self.thankyou = thankyou
        self.intro = intro
        self.info = info
        self.bye = bye


