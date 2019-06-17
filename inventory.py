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
            self.money += temp
