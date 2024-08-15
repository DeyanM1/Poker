"""
0 = ♦ Karo
1 = ♠ Pik
2 = ♥ Herz
3 = ♣ Kreuz

7, 8, 9, 10, J, D, K, A
2, 3, 4, 5, 6, 7, 8, 9, 10, J, D, K, A

Finished Combinations: 1. Royal Flush; 2. Straight Flush; 3. Four of a Kind; 4. Full House; 5. Flush; 6. Straight; 7. Three of a Kind; 8. Two Pair; 9. One Pair; 10. High Card

TODO: Implement tie card comparison; implement better print; line: 239
"""

import random
from collections import Counter

GERMAN_CARDS = False
PLAYER_COUNT = 2
ALL_CARDS = False
GERMAN_CARDS = False
INFINITE_MODE = False
SCORE_MODE = False



ICONS = ["0", "1", "2", "3"]
NUMSSMALL = ["7", "8", "9", "10", "J", "Q" if not GERMAN_CARDS else "D", "K", "A"]
NUMSALL = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q" if not GERMAN_CARDS else "D", "K", "A"]
deck = []
COMBINATIONS = ["High Card" "One Pair", "Two Pair", "Three of a Kind", "Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush", "Royal Flush"]



def generate_deck():
    deck.clear()
    for icon in range(len(ICONS)):
        for num in range(len(NUMSALL if ALL_CARDS else NUMSSMALL)):
            deck.append([ICONS[icon], NUMSALL[num] if ALL_CARDS else NUMSSMALL[num]])
    
def sortByNums(cards):
    order = NUMSALL if ALL_CARDS else NUMSSMALL

    order_dict = {value: index for index, value in enumerate(order)}

    sorted_cards = sorted(cards, key=lambda card: order_dict[card[1]]) 
    
    return sorted_cards   

def sortByIcons(cards):
    order = ICONS
    
    order_dict = {value: index for index, value in enumerate(order)}

    sorted_cards = sorted(cards, key=lambda card: order_dict[card[0]])
    
    return sorted_cards
    
    

class Player:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.score = 0
        self.cards = [[], [], [], [], []]
        self.wins = 0
        
        self.combinations = []
        self.combinationScore = 0
    
    def generate(self, indexList: list):
        for index in indexList:
            index = int(index)
            card = deck.pop()
            self.cards[index] = card
        
    def calculateScore(self):
        if self.checkStreet() != False:
            self.cards = sortByIcons(self.cards)
            match self.checkStreet():
                case "RoyalFlush": self.combinations.append("RoyalFlush"); self.combinationScore = 10
                case "StraightFlush": self.combinations.append("StraightFlush"); self.combinationScore = 9
                case "Flush": self.combinations.append("Flush"); self.combinationScore = 6
                case "Straight": self.combinations.append("Straight"); self.combinationScore = 5

            
        elif self.checkSame() != False:
            self.cards = sortByNums(self.cards)
            match self.checkSame():
                case "FullHouse": self.combinations.append("FullHouse"); self.combinationScore = 7
                case "ThreeOfAKind": self.combinations.append("ThreeOfAKind"); self.combinationScore = 4
                case "FourOfAKind": self.combinations.append("FourOfAKind"); self.combinationScore = 8
                case "2Pair": self.combinations.append("2Pair"); self.combinationScore = 3
                case "1Pair": self.combinations.append("1Pair"); self.combinationScore = 2
        
        else:
            self.cards = sortByNums(self.cards)
            self.combinations.append("HighCard"); self.combinationScore = 1
            
        
        
    def checkSame(self):
        self.cards = sortByNums(self.cards)
        ranks = [card[1] for card in self.cards]
    
        pairs = 0
        ThreeOfAKind = 0
        FourOfAKind = 0
        
        rank_counts = Counter(ranks)
        for rank, count in rank_counts.items():
            if count == 2:
                pairs += 1
            if count == 3:
                ThreeOfAKind += 1
            if count == 4:
                FourOfAKind += 1

        if ThreeOfAKind == 1 and pairs == 1:
            return "FullHouse"
        elif FourOfAKind == 1:
            return "FourOfAKind"
        elif ThreeOfAKind == 1:
            return "ThreeOfAKind"
        elif pairs == 2:
            return "2Pair"
        elif pairs == 1:
            return "1Pair"
        else:
            return False
 
    def checkStreet(self):
        self.cards = sortByIcons(self.cards)
        
        ranks = [card[0] for card in self.cards]
    
        allSame = True

        
        rank_counts = Counter(ranks)
        for rank, count in rank_counts.items():
            if count == 5:
                allSame = True
            else:
                allSame = False
                
                
                      
                
        order_dict = {value: index for index, value in enumerate(NUMSALL)}
    
        ranks = [card[1] for card in self.cards]
        
        sorted_ranks = sorted(ranks, key=lambda rank: order_dict[rank])
        
        for i in range(len(sorted_ranks) - 1):
            if order_dict[sorted_ranks[i]] + 1 != order_dict[sorted_ranks[i + 1]]:
                if allSame:
                    return "Flush"
                return False
    
        
        if allSame and self.cards == [["2", "10"], ["2","J"], ["2", "Q" if not GERMAN_CARDS else "D"], ["2", "K"], ["2", "A"]]: # Royal Flush
            return "RoyalFlush"
        elif allSame:
            return "StraightFlush"
        elif not allSame:
            return "Straight"
        else:
            return False 
          
    def printCards(self):
        readyCards = []
        for card in self.cards:
            printCard = card.copy()
            match card[0]:
                case "0":
                    printCard[0] = "♦"
                case "1":
                    printCard[0] = "♠"
                case "2":
                    printCard[0] = "♥"
                case "3":
                    printCard[0] = "♣"
            readyCards.append(printCard)

        return readyCards
    
    
     
def prepare():
    players = []
    
    generate_deck()
    random.shuffle(deck)
    
    for _ in range(PLAYER_COUNT):
        player = Player(f"Player {_+1}", _+1)
        players.append(player)
    
    for _ in range(5):
        for player in players:
            player.generate([_])
            #print(player.cards)
    
    return players, deck

def calculateWinner(players: list):
    winner = ["", 0] # id, score
    wins = 0
    
    for player in players:
        if player.combinationScore == winner[1]:
            pass
        elif player.combinationScore > winner[1]:
            winner = [player.id, player.combinationScore]
        else:
            continue

    for player in players:
        if player.id == winner[0]:
            player.wins += 1
            wins = player.wins
            
            
    return f"Player {winner[0]} wins with a {COMBINATIONS[winner[1]-2]} point combination! Total wins: {wins}"





if __name__ == "__main__":
    players, deck = prepare()
    round = 1


    won = False
    while won != True:
        print(f"---------- Round {round} ----------")
        
        # TODO: Print score if infinite mode
        
        print(f"Total cards in deck: {len(deck)}")
        for player in players:
            player.cards = sortByNums(player.cards)
            print(f"{player.name} has the following cards: {player.printCards()}")
            indexToRerollRaw = list(input("Enter index to reroll (separated with ',') -> ").replace(",", "").replace(" ", ""))
            indexToReroll = []
            
            for _ in range(len(indexToRerollRaw)): indexToReroll.append(int(indexToRerollRaw[_]) - 1)
            
            player.generate(indexToReroll)
            print(f"{player.name} got the following cards: {player.printCards()}")
            player.calculateScore()
            print(player.combinations)
        
        
        
        print(calculateWinner(players))
        
        
        if INFINITE_MODE:
            won = False
            round += 1
        else:           
            won= True