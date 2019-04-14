import resource
from dice import rollDice
import random as rd

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

    def meleeAttack(self, op, character):  # 기본적으로 근력판정, 10 이상은 공격후 회피(혹은 빈틈을 주고 1d6딜 추가) 7~9는 공격성공후 빈틈
        if character.status.micro_attack:
            correction = character.status.correction_collector('민첩')
        else:
            correction = character.status.correction_collector('근력')
        roll = rollDice(2, 6, correction)
        if roll > 9:
            choose = int(input('공격은 멋들어지게 들어갈것같습니다! 어떻게 할까요??\n1.공격을 명중시킨뒤 회피\n2.빈틈을 보이고 1d6 피해를 더주기\n: '))
            if choose == 1:
                print('{}은(는) {}을(를) 공격한뒤 {}의 공격을 회피했다!'.format(character.status.name, op.name, op.name))
                damage = rollDice(1, character.status.damage_dice, character.status.damage_correction)
                print('{}의 피해를 {}에게 주었다.'.format(op.get_damage(damage), op.name))
                self.give_damamge(damage)
            else:
                print('{}은(는) {}을(를) 강하게 공격했다!'.format(character.status.name, op.name))
                damage = rollDice(1, character.status.damage_dice, character.status.damage_correction)
                damage += rollDice(1, 6, 0)
                print('{}의 피해를 {}에게 주었다.'.format(op.get_damage(damage), op.name))
                self.give_damamge(damage)
                self.get_attack(op, character.status)
        elif roll > 6:
            print('{}은(는) {}를 공격했다! 하지만 헛점을 보이고 말았다'.format(character.status.name, op.name))
            damage = rollDice(1, character.status.damage_dice, character.status.damage_correction)
            print('{}의 피해를 {}에게 주었다.'.format(op.get_damage(damage), op.name))
            self.give_damamge(damage)
            self.get_attack(op, character.status)
        else:
            print('{}는 공격을 피하곤 반격해왔다!'.format(op.name))
            character.status.curexp_controller(1)
            self.get_attack(op, character.status)
        return roll

    def missileAttack(self):  # 민첩판정 10이상은 명중, 7~9는 곤경,-1d6피해, 발수1줄이기중 플레이어 선택
        pass

    def breakThrough(self):  # 본인이 원하는 방법(판정)으로 위험을 돌파함 10이상이면 무리없이 원하는것을 얻음
        pass                 # 7~9는 덜좋은결과, 어려운선택, 불리한거래중 한가지

    def defense(self):  # 사람,물건,장소를 지키는 액션, 체력판정, 10+ 예비3점 7~9 예비1점
        pass            # 방어태세동안 대상이 공격받을시 예비1점 소모로 한가지선택 / 대신맞음,피해나효과 반으로, 공격자빈틈만들어, 지정한 우리편 캐릭터의 다음판정 +1, 자기레벨만큼 피해를 상대에게 가함

    def stagKnowledge(self, character, stuff):  # 지식더듬기, 지식판정을해서 10+ 유용한 사실 7~9 흥미롭기만한 사실
        result = rollDice(2, 6, character.status.correction_collector('지식'))
        if result > 9:
            print(stuff[1], stuff[2])
        elif result > 6:
            print(stuff[1])
        else:
            print('아무리 머리를 쥐어짜도 이름말곤 아는게 없군요...')
            character.status.curexp_controller(1)


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

    def level_up(self, character):  # 쉴 시간이 있고 경험치가 현재레벨+7 이상인경우 렙업, 고급액션(법사는주문)하나 선택, 능력치1증가 최대 18
        print('다음은 고급액션을 골라주세요.')
        for idx, action in enumerate(resource.worrior_high_action):
            if action[0] in self.have:
                pass
            else:
                print('{}. {} / {}'.format(idx + 1, action[0], action[1]))
        while True:
            choose = int(input('무엇을 고르시겠습니까? : '))
            choose2 = int(input('{}. {}가 맞습니까?\n1.네 2.아니오 : '.format(choose, resource.worrior_high_action[choose - 1][0])))
            if choose2 == 1:
                self.have.append(resource.worrior_high_action[choose - 1][0])
                break

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

    def check_body(self, character, op):  # 죽은 몬스터를 루팅하는 함수입니다.
        money = op.stuff.pop(0)
        character.inventory.money_controller(money)
        print('{} 닢을 얻었습니다.'.format(money))
        if len(op.stuff) > 0:
            for i in op.stuff:
                character.inventory.item_setter(i)
                character.status.curweight_controller(i.weight)
                print('{} 를 얻었습니다. '.format(i.name))


class Worrior(Action):
    def meleeAttack(self, op, character):  # 기본적으로 근력판정, 10 이상은 공격후 회피(혹은 빈틈을 주고 1d6딜 추가) 7~9는 공격성공후 빈틈
        if character.status.micro_attack:
            correction = character.status.dex_correction
        else:
            correction = character.status.str_correction
        roll = rollDice(2, 6, correction)
        if roll > 9:
            choose = int(input('공격은 멋들어지게 들어갈것같습니다! 어떻게 할까요??\n1.공격을 명중시킨뒤 회피\n2.빈틈을 보이고 1d6 피해를 더주기\n: '))
            if choose == 1:
                print('{}은(는) {}을(를) 공격한뒤 {}의 공격을 회피했다!'.format(character.status.name, op.name, op.name))
                damage = rollDice(1, character.status.damage_dice, character.status.damage_correction) + self.no_mercy()
                print('{}의 피해를 {}에게 주었다.'.format(op.get_damage(damage), op.name))
                self.give_damamge(damage)
            else:
                print('{}은(는) {}을(를) 강하게 공격했다!'.format(character.status.name, op.name))
                damage = rollDice(1, character.status.damage_dice, character.status.damage_correction)
                damage += rollDice(1, 6, 0) + self.no_mercy()
                print('{}의 피해를 {}에게 주었다.'.format(op.get_damage(damage), op.name))
                self.give_damamge(damage)
                self.get_attack(op, character.status)
        elif roll > 6:
            print('{}은(는) {}를 공격했다! 하지만 헛점을 보이고 말았다'.format(character.status.name, op.name))
            damage = rollDice(1, character.status.damage_dice, character.status.damage_correction) + self.no_mercy()
            print('{}의 피해를 {}에게 주었다.'.format(op.get_damage(damage), op.name))
            self.give_damamge(damage)
            self.get_attack(op, character.status)
        else:
            print('{}는 공격을 피하곤 반격해왔다!'.format(op.name))
            character.status.curexp_controller(1)
            self.get_attack(op, character.status)
        return roll

    def level_up(self, character):  # 쉴 시간이 있고 경험치가 현재레벨+7 이상인경우 렙업, 고급액션(법사는주문)하나 선택, 능력치1증가 최대 18
        print('다음은 고급액션을 골라주세요.')
        for idx, action in enumerate(resource.worrior_high_action):
            if action[0] in self.have:
                pass
            else:
                print('{}. {} / {}'.format(idx + 1, action[0], action[1]))
        while True:
            choose = int(input('무엇을 고르시겠습니까? : '))
            name = resource.worrior_high_action[choose - 1][0]
            choose2 = int(input('{}. {}가 맞습니까?\n1.네 2.아니오 : '.format(choose, name)))
            if choose2 == 1:
                self.have.append(resource.worrior_high_action[choose - 1][0])
                break
        if name == '무쇠의 몸':
            self.iron_body(character)

    def no_mercy(self):  # 무자비 고급액션이 활성화되어있을때 추가피해를 더하는 함수입니다.
        if '무자비' in self.have and '살기등등' not in self.have:
            return rollDice(1, 4, 0)
        else:
            return 0

    def weapon_spirit(self):  # 병기의 영 고급액션, 고유병기에게 말을 걸었을떄 +매 판정으로 추가상황파악가능
        pass

    def defense_knowhow(self):  # 방어의 요령 고급액션, 방어구를 앞세워 피해를 막으면 피해는 무시되고 장갑 -1 장갑 0 이될시 아이템파괴
        pass

    def enchant_weapon(self):  # 무기강화 고급액션, 고유병기의 특징 추가
        pass

    def worriors_eyes(self):  # 전사의 눈 고급액션, 전투중 상황파악시 판정에 +1
        pass

    def threaten(self):  # 협박 고급액션, 폭력으로 협상을할때 +매 대신 +근 판정으로 협상
        pass

    def blood_smell(self):  # 피의향기 고급액션, 접근전시 같은상대로의 다음공격은 +1d4피해 추가
        pass

    def iron_body(self, character):  # 무쇠의 몸 고급액션, 장갑 +1
        character.status.armor_controller(1)

    def multi_class1(self):  # 다중직업 초급 고급액션, 다은직업액션 하나 선택
        pass

    def black_smith(self):  # 대장장이 고급액션, 마법무기를 파괴하고 고유병기에 그 마법성질을 추가
        pass



class Bard(Action):
    pass

class Rogue(Action):
    pass

class Mage(Action):
    pass

class Priest(Action):
    pass

class Paladin(Action):
    pass

class Druid(Action):
    pass

class Hunter(Action):
    pass



def random_sentence_printer(list):  # 묘사를 랜덤으로 출력해주는 함수입니다.
    print(rd.choice(list))

def script_reader(list):  # 스크립트를 출력해주는 함수입니다.
    for i in list:
        print(i)
        input()