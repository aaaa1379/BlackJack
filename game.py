# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 14:03:15 2016

@author: Akii
"""

from player import Player
from player import Dealer
from dealingMachine import DealingMachine
from gameRules import GameState

class Game:
    def __init__(self):
        self.dealingMachine = DealingMachine(8, 52)
        self.rule = GameState.ClassicRules
        self.player = []
        self.dealer = 0

    def gameInit(self):
        player = Player(self.dealingMachine, self.rule, 1000000)
        dealer = Dealer(self.dealingMachine, self.rule)
        self.player.append(player)
        self.dealer = dealer

    def gameRound(self):
        # 4 step
        # initial deal
        self.dealer.initialDeal()
        for player in self.player:
            player.initialDeal()
            
        # player action
        for player in self.player:
            player.playerAction()
            
        # dealer's hand revealed
        self.dealer.playerAction()
        
        # bets settled
        for player in self.player:
            player.betSettled(self.dealer)
            print player.getMoney()