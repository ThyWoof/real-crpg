#import random as rd

class Session:
    pass

class Village:
    pass

class Map:
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

    def open_store(self):  # 해당 npc가 가지고있는 상품을 보여줍니다.
        if self.store == None:
            print("소유하고 있는 상점이 없습니다.")
        else:
            self.store.show_menu()

    def say_goodbye(self):  # 헤어질때 인사를 출력합니다.
        print(self.script.bye)

    def set_store(self, store):
        self.store = store


class Store:
    def __init__(self, name, store_type, npc=None):  # 이름과 상점 타입등을 초기값으로 지정합니다
        self.name = name
        self.type = store_type
        self.npc = npc

    def show_menu(self):
        print("가게 메뉴를 보여줍니다.")

    def set_npc(self, npc):
        self.npc = npc
        self.npc.set_store(self)


class Field:
    pass


class NpcSctipt:
    def __init__(self, greet, thankyou, intro, bye, info=None):
        self.greeting = greet
        self.thankyou = thankyou
        self.intro = intro
        self.info = info
        self.bye = bye


def test_code():
    name = "랄프"
    age = 41
    gender = "남"
    script = NpcSctipt('안녕하시오', "감사하오", "나는 이 '부드러운 검' 여관을 20년간 지켜온 랄프라 하오", "안녕히 가시오", "퀘스트")
    test = Npc(name, age, gender, script)
    test.say_hello()
    test.say_intro()
    test.say_info()
    test.open_store()
    test.say_goodbye()
    test_store = Store("부드러운 검", "여관")
    test_store.set_npc(test)
    test.open_store()
test_code()