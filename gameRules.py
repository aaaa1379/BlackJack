# -*- coding: utf-8 -*-
"""
Created on Thu Apr 07 21:30:35 2016

@author: Akii
"""

class GameState:
    DECK = "Deck"    
    
    H17 = "Hits on Soft 17"
    S17 = "Stands on Soft 17"    
    
    DOA   = "Double On Any 2 Cards"
    DOA9  = "Double On 9/10/11 only"
    DOA10 = "Double On 10/11 only"
    
    DAS  = "Double After Split"
    NDAS = "No Double After Split"
    
    RSA = "Re-Split Any 2 Cards"

    ES = "Early Surrender"
    LS = "Late Surrender"
    NS = "No Surrender"
    
    
    ClassicRules = {
        DECK: 8,
        H17: H17,
        DOA: DOA,
        DAS: DAS,
        RSA: RSA,
        ES:  ES,
    }
    
    

class Role:
    PLAYER = "Player"
    DEALER = "Dealer"

class Decision:
    HIT = "Hit"
    STAND = "Stand"
    DOUBLE = "Double"
    SPLIT = "Split"
    SURRENDER = "Surrender"
    
    MAP = {
        1: HIT,
        2: STAND,
        3: DOUBLE,
        4: SPLIT,
        5: SURRENDER,
    }

class EndStep:
    # You Can Not Access This Decision
    NEXT = "Continue!!!!"    
    #  1.5x => BLACKJACK
    #  1.0x => WIN
    #  0.0x => DRAW
    # -0.5x => SURRENDER
    # -1.0x => BUST and LOST
    BLACKJACK = "Blackjack"
    SURRENDER = "Surrender"
    BUST = "Bust"
    STAND = "Stand"

    WIN = "Win"
    DRAW = "Draw"
    LOSE = "Lose"
    