import random
from mailbox import FormatError

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:
    def __init__(self, cards=None):
        self.cards = cards if cards is not None else []

    def create_cards(self):
        suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
        ranks = [
            ("Two", 2), ("Three", 3), ("Four", 4), ("Five", 5), ("Six", 6),
            ("Seven", 7), ("Eight", 8), ("Nine", 9), ("Ten", 10),
            ("Jack", 10), ("Queen", 10), ("King", 10), ("Ace", 11)
        ]

        for suit in suits:
            for rank, value in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)
        return self.cards

    def deal(self):
        return self.cards.pop() if self.cards else None


class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def win_bet_bj(self):
        self.total += self.bet*1.5

    def lose_bet(self):
        self.total -= self.bet
class User:
    def __init__(self,username=str(),chips=Chips()):
        self.username = username
        self.chips = chips
def Hit(deck=Deck(),hand=Hand()):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def HitOrStand(deck=Deck(),hand=Hand(),name=str()):
    inpt=""
    while True:
        inpt=input("Hit or Stand? (h or s): ")
        if inpt.lower() == 'h':
            Hit(deck,hand)
        elif inpt.lower() == 's':
            print(f"{name} stands. Dealer is playing.")
        else:
            print("Invalid input. Please try again.")
            continue
        break
    return inpt

def ShowSomeCards(playerHand=Hand(),dealerHand=Hand(),name=str()):
    print("Dealer's hand:")
    print("<card hidden>")
    print(dealerHand.cards[1])
    print("\n")
    print(f"{name}'s hand:")
    for card in playerHand.cards:
        print(str(card))
    print("\n")
    print(f"{name}'s points = {playerHand.value}")
    print("\n")

def ShowAllCards(playerHand=Hand(),dealerHand=Hand(),name=str()):
    print("\n Dealer's hand:")
    for card in dealerHand.cards:
        print(str(card))
    print("\n")
    print(f"Dealer's points = {dealerHand.value}")
    print("\n")
    print(f"{name}'s hand:")
    for card in playerHand.cards:
        print(str(card))
    print("\n")
    print(f"{name}'s points = {playerHand.value}")
    print("\n")

def PlayerBusts(playerHand=Hand(),dealerHand=Hand(),chips=Chips(),name=str()):
    print(f"{name} busts!")
    chips.lose_bet()

def PlayerWins(playerHand=Hand(),dealerHand=Hand(),chips=Chips(),name=str()):
    print(f"{name} wins!")
    chips.win_bet()

def PLayerWinsBlackJack(playerHand=Hand(),dealerHand=Hand(),chips=Chips(),name=str()):
    print(f"{name} has Black Jack!")
    chips.win_bet_bj()

def DealerBusts(playerHand=Hand(),dealerHand=Hand(),chips=Chips()):
    print("Dealer busts!")
    chips.win_bet()

def DealerWins(playerHand=Hand(),dealerHand=Hand(),chips=Chips()):
    print("Dealer wins!")
    chips.lose_bet()

def Push(playerHand=Hand(),dealerHand=Hand(),name=str()):
    print(f"Dealer and {name} tie! It's a push.")

def TakeBet(chips=Chips()):
    while True:
        try:
            print("\n")
            chips.bet=int(input("How many chips would you like to bet: "))
            if chips.bet>chips.total or chips.total<=0:
                print("You can't bet that many chips")
                continue
            else:
                break
        except FormatError:
            print("You must write a number")
            continue
    return chips.bet

def Insurance(playerHand=Hand(),dealerHand=Hand(),chips=Chips(),name=str()):
    insuranceChips = Chips()
    inpt=""
    if dealerHand.cards[1].rank == 'Ace':
        while True:
            inpt=input("You can insure, do you want to? (y/n): ")
            if inpt.lower() == 'y':
                while insuranceChips.total > chips.bet/2:
                    try:
                        print("\n")
                        insuranceChips.total=int(input("How many chips would you like to insure: "))
                        if insuranceChips.total>chips.bet/2:
                            print(f"You can't insure that many chips (can be up to {chips.bet / 2} chips)")
                            continue
                        else:
                            break
                    except FormatError:
                        print("You must write a number")
                        continue
                ShowAllCards(playerHand,dealerHand,name)
                if dealerHand.cards[0].rank == 'Ten' or dealerHand.cards[0].rank == 'Jack'or dealerHand.cards[0].rank == 'Queen'or dealerHand.cards[0].rank == 'King':
                    if playerHand.value<dealerHand.value:
                        chips.lose_bet()
                        insuranceChips.win_bet()
                        chips.total+=2*insuranceChips.total
                        break

                    else:
                        insuranceChips.win_bet()
                        chips.total+=2*insuranceChips.total
                        break
                else:
                    if playerHand.value>dealerHand.value:
                        chips.win_bet()
                        chips.total-=insuranceChips.total
                        break

                    elif playerHand.value<dealerHand.value:
                        chips.lose_bet()
                        chips.total-=insuranceChips.total
                        break

                    else:
                        insuranceChips.lose_bet()
                        chips.total-=insuranceChips.total
                        break
            elif inpt.lower() == 'n':
                break
            else:
                print("Wrong input")
    return inpt.lower()


def Split(playerHand1=Hand(),dealerHand=Hand(),deck=Deck(),chips=Chips(),bet=Chips(),name=str()):
    playerHand2=Hand()
    points=int(playerHand1.value/2)
    playerHand2.cards.append(playerHand1.cards[1])
    playerHand1.value=points
    playerHand2.value=points
    playerHand1.cards.pop()
    inpt1=""
    inpt2=""

    print("Hand1: ")
    ShowSomeCards(playerHand1,dealerHand,name)
    while inpt1.lower()!='s':
        inpt1=HitOrStand(deck,playerHand1,name)
        if playerHand1.value == 21 and len(playerHand1.cards) == 2:
            PLayerWinsBlackJack(playerHand1, dealerHand, bet, name)
            break
        ShowSomeCards(playerHand1, dealerHand, name)
        if playerHand1.value>21:
            PlayerBusts(playerHand1,dealerHand,bet,name)
            chips.total-=bet.total
            break

    print("Hand2: ")
    ShowSomeCards(playerHand2, dealerHand, name)
    while inpt2.lower() != 's':
        inpt2 = HitOrStand(deck, playerHand2, name)
        if playerHand2.value == 21 and len(playerHand2.cards) == 2:
            PLayerWinsBlackJack(playerHand2, dealerHand, bet, name)
            break
        ShowSomeCards(playerHand2, dealerHand, name)
        if playerHand2.value > 21:
            PlayerBusts(playerHand2, dealerHand, bet, name)
            chips.total -= bet.total
            break
    if playerHand2.value<=21 or playerHand1.value<=21:
        while dealerHand.value<17:
            Hit(deck,dealerHand)
        ShowAllCards(playerHand2, dealerHand, name)

        print("Hand1: ")
        if playerHand1.value>21:
            PlayerBusts(playerHand1, dealerHand, bet, name)
        elif dealerHand.value>21:
            DealerBusts(playerHand1, dealerHand, chips)
        elif dealerHand.value>playerHand1.value:
            DealerWins(playerHand1, dealerHand, chips)
        elif playerHand1.value>dealerHand.value:
            PlayerWins(playerHand1, dealerHand, chips,name)
        else:
            Push(playerHand1,dealerHand,name)

        print("\nHand2: ")

        if playerHand2.value>21:
            PlayerBusts(playerHand2, dealerHand, bet, name)
        elif dealerHand.value>21:
            DealerBusts(playerHand2, dealerHand, chips)
        elif dealerHand.value>playerHand2.value:
            DealerWins(playerHand2, dealerHand, chips)
        elif playerHand2.value>dealerHand.value:
            PlayerWins(playerHand2, dealerHand, chips,name)
        else:
            Push(playerHand2,dealerHand,name)
    if chips.total<=0:
        print("You lost all of your chips")

def main():
    username=input("Please enter your username: ")
    user=User(username,)
    print(f"\nWelcome to Blackjack {user.username}")
    print(f"You have {user.chips.total} chips")
    deck=Deck()
    for i in range(0,9):
        deck.create_cards()
    shuffledStack=deck.shuffle()
    shuffledDeck=Deck(shuffledStack)
    while user.chips.total>0:
        playerHand=Hand()
        dealerHand=Hand()

        insurance=""
        splitInput=""
        inpt=""

        for i in range(0,5):
            if i<2:
                playerCard=shuffledDeck.deal()
                playerHand.add_card(playerCard)
            else:
                dealerCard = shuffledDeck.deal()
                dealerHand.add_card(dealerCard)

        dealerHand.adjust_for_ace()
        bet=Chips()
        bet.total=TakeBet(user.chips)

        ShowSomeCards(playerHand,dealerHand,user.username)

        while inpt.lower()!='s':
            if playerHand.value ==21 and len(playerHand.cards)==2:
                PLayerWinsBlackJack(playerHand,dealerHand,user.chips,user.username)
                break
            if user.chips.total-bet.total>=2 and bet.total>=2:
                insurance=Insurance(playerHand,dealerHand,user.chips,user.username)
                if insurance=="y":
                    break
            if user.chips.total-bet.total>=bet.total and inpt.lower()!='h':
                card1=playerHand.cards[0]
                card2=playerHand.cards[1]
                if card1.rank==card2.rank:
                    while splitInput.lower()!= 'n':
                        splitInput=input("Would you like to split? (y/n): ")
                        if splitInput.lower()=='y':
                            Split(playerHand,dealerHand,shuffledDeck,user.chips,bet,user.username)
                            break
                        elif splitInput.lower()=='n':
                            playerHand.adjust_for_ace()
                            while inpt.lower()!='s':
                                inpt=HitOrStand(shuffledDeck,playerHand,user.username)
                                ShowSomeCards(playerHand,dealerHand,user.username)
                                if playerHand.value > 21:
                                    PlayerBusts(playerHand, dealerHand,user.chips,user.username)
                                    break
                        else:
                            continue
                    if splitInput.lower()=='y'or splitInput.lower()=='n':
                        break
            inpt =HitOrStand(shuffledDeck,playerHand,user.username)
            ShowSomeCards(playerHand,dealerHand,user.username)
            if playerHand.value > 21:
                PlayerBusts(playerHand, dealerHand, user.chips, user.username)
                break
        if playerHand.value <= 21 and insurance.lower()!="y" and splitInput.lower()!="y":
            while dealerHand.value < 17:
                Hit(shuffledDeck,dealerHand)
            ShowAllCards(playerHand, dealerHand, user.username)

            if dealerHand.value > 21:
                DealerBusts(playerHand, dealerHand, user.chips)

            elif dealerHand.value>playerHand.value:
                DealerWins(playerHand, dealerHand, user.chips)

            elif playerHand.value>dealerHand.value:
                PlayerWins(playerHand, dealerHand, user.chips,user.username)
            else:
                Push(playerHand, dealerHand, user.username)
        print(f"\n {user.username}'s chips: {user.chips.total}")
        print("\n")
        if user.chips.total<=0:
            print("You have no chips")
            break
        while True:
            newGame=input("Do you want to play again? (y/n): ")
            if newGame.lower()=='y':
                break
            elif newGame.lower()=='n':
                print("Thank you for playing")
                return
            else:
                print("Wrong input")
                continue
if __name__ == "__main__":
    main()
