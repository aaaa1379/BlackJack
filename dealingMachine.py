# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 19:14:15 2016

@author: Akii
"""

import random

class CardStrategy:
    """
    See More About Card Counting Strategy
    https://en.wikipedia.org/wiki/Card_counting
    """ 
    HILO = "hi-lo"


class Deck:
    Card_2 = 2
    Card_3 = 3
    Card_4 = 4
    Card_5 = 5
    Card_6 = 6
    Card_7 = 7
    Card_8 = 8
    Card_9 = 9
    Card_10= 10
    Card_J = 11
    Card_Q = 12
    Card_K = 13
    Card_A = 1
    
    LIST = {Card_2: Card_2,
            Card_3: Card_3,
            Card_4: Card_4,
            Card_5: Card_5,
            Card_6: Card_6,
            Card_7: Card_7,
            Card_8: Card_8,
            Card_9: Card_9,
            Card_10: Card_10,
            Card_J: Card_J,
            Card_Q: Card_Q,
            Card_K: Card_K,
            Card_A: Card_A}
    
    HILO = {Card_2: +1,
            Card_3: +1,
            Card_4: +1,
            Card_5: +1,
            Card_6: +1,
            Card_7:  0,
            Card_8:  0,
            Card_9:  0,
            Card_10: -1,
            Card_J: -1,
            Card_Q: -1,
            Card_K: -1,
            Card_A: -1}
        
        
class DealingMachine:
    def __init__(self, deck, autoShuffle = 0, strategy = CardStrategy.HILO):
        self.shoe = []
        self.marker = 0
        self.counting = 0
        self.autoShuffle = autoShuffle     # shuffle if cards remain this value
        self.strategy = strategy
        
        for i in range(4 * deck):
            for x, y in Deck.LIST.items():
                self.shoe.append(x)
        self.shuffle()
        
    def shuffle(self):
        random.shuffle(self.shoe)
        self.marker = 0
        self.counting = 0
        
    def getCard(self):
        if self.marker == len(self.shoe):
            raise IndexError("no more cards in dealing machine.")

        card = self.shoe[self.marker]
        self.marker += 1
        
        # card counting        
        if self.strategy == CardStrategy.HILO:
            self.counting += Deck.HILO[card]
        
        # auto shuffle
        remain = self.getRemain()
        if remain < self.autoShuffle:
            self.shuffle()
            
        return card
    
    def getCounting(self):
        return self.counting
        
    def getRemain(self):
        return len(self.shoe) - self.marker
        
    def getStrategy(self):
        return self.strategy
        
        
        
        
        
        
        
        
        
        
        