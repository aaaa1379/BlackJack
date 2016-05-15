# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 14:03:15 2016

@author: Akii
"""

import sys, getopt
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

    def gameRound(self, strategy=None):
        # 4 step
        # initial deal
        self.dealer.initialDeal()
        for player in self.player:
            player.initialDeal()
                    
        # player action
        for player in self.player:
            player.playerAction(self.dealer, strategy)
            
        # dealer's hand revealed
        self.dealer.playerAction()
        
        # bets settled
        for player in self.player:
            player.betSettled(self.dealer)
            print player.getMoney()
        print "--------------------"
            
def main():

    strategy = ''
    gameround = 1
    try:
        argv = sys.argv[1:]
        opts, args = getopt.getopt(argv,"hs:r:",["strategy=", "gameround="])
    except getopt.GetoptError:
        print 'test.py -s <strategy>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'game.py -s <strategy>'
            sys.exit()
        if opt in ("-r", "--gameround"):
            gameround = int(arg)
        elif opt in ("-s", "--strategy"):
            strategy = arg
        else:
            strategy = ''
            
    print " <><><>", strategy, gameround            
            
    game = Game()
    game.gameInit()
    for i in range(gameround):
        game.gameRound(strategy)

if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    