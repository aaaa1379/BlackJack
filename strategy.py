# -*- coding: utf-8 -*-
"""
Created on Sat May 14 05:11:12 2016

@author: Akii
"""

from gameRules import Decision
from dealingMachine import Deck

def easyAction(player, dealer):
    """ 
    here player is mean player hand card 
    here dealer is mean dealer hand card 
    command-line arguments:
        game.py -s easyAction
    usage:
        player.getSumOfCards()
        player.getNumberOfCards()
        player.getNumberOfAces()
        player.getBetMoney()
        player.getAction()
    """
    
    if Decision.SPLIT in player.getAction():
        return Decision.SPLIT
    if Decision.STAND in player.getAction() and player.getSumOfCards() > 16:
        return Decision.STAND
    if Decision.DOUBLE in player.getAction() and player.getSumOfCards() <= 11:
        return Decision.DOUBLE
    if Decision.HIT in player.getAction() and player.getSumOfCards() <= 16:
        return Decision.HIT
        
def basicStrategy(player, dealer):
    """
    see the easyAction first
    command-line arguments:
        game.py -s basicStrategy
    """
    
    action = "S"
        
    if Decision.SPLIT in player.getAction():
        mapTable = [
            # dealer hand card
            #2	 3	 4	 5	 6	 7	 8	 9	 T	 A 
            "P",	"P",	"P",	"P",	"P",	"P",	"H",	"H",	"H",	"RH",  # (2,2)
            "P",	"P",	"P",	"P",	"P",	"P",	"H",	"H",	"H",	"RH",  # (3,3)
            "H",	"H",	"H",	"P",	"P",	"H",	"H",	"H",	"H",	"H",   # (4,4)
            "DH",	"DH",	"DH",	"DH",	"DH",	"DH",	"DH",	"DH",	"H",	"H",   # (5,5)
            "P",	"P",	"P",	"P",	"P",	"H",	"H",	"H",	"H",	"RH",  # (6,6)
            "P",	"P",	"P",	"P",	"P",	"P",	"H",	"H",	"RH",	"RH",  # (7,7)
            "P",	"P",	"P",	"P",	"P",	"P",	"P",	"P",	"RP",	"RP",  # (8,8)
            "P",	"P",	"P",	"P",	"P",	"S",	"P",	"P",	"S",	"S",   # (9,9)
            "S",	"S",	"S",	"S",	"S",	"S",	"S",	"S",	"S",	"S",   # (T,T)
            "P",	"P",	"P",	"P",	"P",	"P",	"P",	"P",	"P",	"P",   # (A,A)
            ]
        playerItr = Deck.VALUE[player.getCards()[0]]
        dealerItr = Deck.VALUE[dealer.getCards()[0]]
        itr = 10 * (playerItr - 2) + (dealerItr - 2)
        print "(p,d,itr)", playerItr, dealerItr, itr
        action = mapTable[itr]
        
        print "(p,d,itr,act)", playerItr, dealerItr, itr, action
        
    if Decision.SPLIT not in player.getAction() and player.getNumberOfAces() > 0:
        mapTable = [
            # dealer hand card
            #2	 3	 4	 5	 6	 7	 8	 9	 T	 A 
            "H",	"H",	"H",	"DH",	"DH",	"H",	"H",	"H",	"H",	"H",  # Ace + 2
            "H",	"H",	"H",	"DH",	"DH",	"H",	"H",	"H",	"H",	"H",  # Ace + 3
            "H",	"H",	"DH",	"DH",	"DH",	"H",	"H",	"H",	"H",	"H",  # Ace + 4
            "H",	"H",	"DH",	"DH",	"DH",	"H",	"H",	"H",	"H",	"H",  # Ace + 5
            "H",	"DH",	"DH",	"DH",	"DH",	"H",	"H",	"H",	"H",	"H",  # Ace + 6
            "DS",	"DS",	"DS",	"DS",	"DS",	"S",	"S",	"H",	"H",	"H",  # Ace + 7
            "S",	"S",	"S",	"S",	"DS",	"S",	"S",	"S",	"S",	"S",  # Ace + 8
            "S",	"S",	"S",	"S",	"S",	"S",	"S",	"S",	"S",	"S",  # Ace + 9
            "S",	"S",	"S",	"S",	"S",	"S",	"S",	"S",	"S",	"S",  # Ace + 10
            ]
        playerItr = player.getSumOfCards() - Deck.VALUE[Deck.Card_A]
        dealerItr = Deck.VALUE[dealer.getCards()[0]]
        itr = 10 * (playerItr - 2) + (dealerItr - 2)
        print "(p,d,itr)", playerItr, dealerItr, itr
        action = mapTable[itr]
        
        print "(p,d,itr,act)", playerItr, dealerItr, itr, action
        
    if Decision.SPLIT not in player.getAction():
        mapTable = [
            # dealer hand card
            #2	 3	 4	 5	 6	 7	 8	 9	 T	 A 
            "H",	"H",	"H",	"H",	"H",	"H",	"H",	"H",	"H",	"RH", # Hard 5
            "H",	"H",	"H",	"H",	"H",	"H",	"H",	"H",	"H",	"RH", # Hard 6
            "H",	"H",	"H",	"H",	"H",	"H",	"H",	"H",	"H",	"RH", # Hard 7
            "H",	"H",	"H",	"H",	"H",	"H",	"H",	"H",	"H",	"H",  # Hard 8
            "H",	"DH",	"DH",	"DH",	"DH",	"H",	"H",	"H",	"H",	"H",  # Hard 9
            "DH",	"DH",	"DH",	"DH",	"DH",	"DH",	"DH",	"DH",	"H",	"H",  # Hard 10
            "DH",	"DH",	"DH",	"DH",	"DH",	"DH",	"DH",	"DH",	"DH",	"DH",  # Hard 11
            "H",	"H",	"S",	"S",	"S",	"H",	"H",	"H",	"H",	"RH", # Hard 12
            "S",	"S",	"S",	"S",	"S",	"H",	"H",	"H",	"H",	"RH", # Hard 13
            "S",	"S",	"S",	"S",	"S",	"H",	"H",	"H",	"RH",	"RH", # Hard 14
            "S",	"S",	"S",	"S",	"S",	"H",	"H",	"H",	"RH",	"RH", # Hard 15
            "S",	"S",	"S",	"S",	"S",	"H",	"H",	"RH",	"RS",	"RH", # Hard 16
            "S",	"S",	"S",	"S",	"S",	"S",	"S",	"S",	"S",	"RS", # Hard 17
            "S",	"S",	"S",	"S",	"S",	"S",	"S",	"S",	"S",	"S",  # Hard 18
            "S",	"S",	"S",	"S",	"S",	"S",	"S",	"S",	"S",	"S",  # Hard 19
            "S",	"S",	"S",	"S",	"S",	"S",	"S",	"S",	"S",	"S",  # Hard 20
            "S",	"S",	"S",	"S",	"S",	"S",	"S",	"S",	"S",	"S",  # Hard 21
            ]
        playerItr = player.getSumOfCards()
        dealerItr = Deck.VALUE[dealer.getCards()[0]]
        itr = 10 * (playerItr - 5) + (dealerItr - 2)
        print "(p,d,itr)", playerItr, dealerItr, itr
        action = mapTable[itr]
        
        print "(p,d,itr,act)", playerItr, dealerItr, itr, action

    if action[0] is "R" and Decision.SURRENDER in player.getAction():
        return Decision.SURRENDER
    if action[0] is "H" and Decision.HIT in player.getAction():
        return Decision.HIT
    if action[0] is "S" and Decision.STAND in player.getAction():
        return Decision.STAND
    if action[0] is "D":
        if Decision.DOUBLE in player.getAction():
            return Decision.DOUBLE
        elif action[1] is "H" and Decision.HIT in player.getAction():
            return Decision.HIT
        elif action[1] is "S" and Decision.STAND in player.getAction():
            return Decision.STAND
    if action[0] is "P" and Decision.SPLIT in player.getAction():
        return Decision.SPLIT

