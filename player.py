# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 17:46:43 2016

@author: Akii
"""

from dealingMachine import Deck
from gameRules import Role
from gameRules import Decision
from gameRules import EndStep

class Player:
    def __init__(self, dm, rule, money):
        self.dealingMachine = dm
        self.handCards = []
        self.rule = rule
        self.money = money

    def initialDeal(self):
        handCard = HandCard(self.dealingMachine, self.rule, self.money * 0.001)
        handCard.initialAction(Role.PLAYER)
        self.handCards.append(handCard)
    def playerAction(self):
        for handCard in self.handCards:
            while handCard.getAction():
                self.printAction(handCard)
                decision = raw_input("INPUT >>   ")
                splitHandCard = handCard.action(Decision.MAP[int(decision)])
                if splitHandCard:
                    self.handCards.append(splitHandCard)
                #self.action(handCard)
    def action(self, handCard):
        if Decision.SPLIT in handCard.getAction():
            return Decision.SPLIT
        if Decision.STAND in handCard.getAction() and handCard.getSumOfCards() > 16:
            return Decision.STAND
        if Decision.DOUBLE in handCard.getAction() and handCard.getSumOfCards() <= 11:
            return Decision.DOUBLE
        if Decision.HIT in handCard.getAction() and handCard.getSumOfCards() <= 16:
            return Decision.HIT
        
    def betSettled(self, dealer):
        for handCard in self.handCards:
            bet = handCard.getBetMoney()
            earn = 0
            endStep = handCard.getEndStep()
            winlose = handCard.getWinLose(dealer.getHandCard())
            if endStep is EndStep.BUST:
                earn += -1.0 * bet
            if endStep is EndStep.SURRENDER:
                earn += -0.5 * bet
                
            if endStep is EndStep.BLACKJACK:
                if winlose is EndStep.WIN:
                    earn +=  1.5 * bet
                if winlose is EndStep.DRAW:
                    earn +=  0.0 * bet
                    
            if endStep is EndStep.STAND:
                if winlose is EndStep.WIN:
                    earn +=  1.0 * bet
                if winlose is EndStep.DRAW:
                    earn +=  0.0 * bet
                if winlose is EndStep.LOSE:
                    earn += -1.0 * bet
            self.money += earn
            self.printResult(handCard, dealer, earn)
            

    def getMoney(self):
        return self.money

    def printAction(self, handCard):
        print "--------------------"
        print "1: Hit, 2: Stand, 3: Double, 4: Split, 5: Surrender"
        print "Hand Card", handCard.getHandCard()
        print "Sum Cards", handCard.getSumOfCards()
        print "Action", handCard.getAction()
        print "Money", self.money
        print "Bet", handCard.getBetMoney()
        
    def printResult(self, handCard, dealer, earn):
        endStep = handCard.getEndStep()
        winlose = handCard.getWinLose(dealer.getHandCard())
        self.printHandCard(handCard)
        print "Dealer Cards", dealer.getHandCard().getHandCard()
        print "Dealer Sum  ", dealer.getHandCard().getSumOfCards()
        print "EndStep", endStep
        print "Result", winlose
        print "Earn", earn
        
    def printHandCard(self, handCard):
        print "Player Cards", handCard.getHandCard()
        print "Player Sum  ", handCard.getSumOfCards()
        #print "NumberOfCards", handCard.getNumberOfCards()
        #print "NumberOfAces", handCard.getNumberOfAces()
        #print "Action", handCard.getAction()
        #print "BetMoney", handCard.getBetMoney()
        #print "EndStep", handCard.getEndStep()
        
class Dealer:
    def __init__(self, dm, rule):
        self.dealingMachine = dm
        self.handCard = 0
        self.rule = rule
    def initialDeal(self):
        self.handCard = HandCard(self.dealingMachine, self.rule)
        self.handCard.initialAction(Role.DEALER)
    def playerAction(self):
        handCard = self.handCard
        while handCard.getAction():
            decision = self.action(handCard)
            handCard.action(decision)
    def action(self, handCard):
        if Decision.STAND in handCard.getAction() and handCard.getSumOfCards() > 17:
            return Decision.STAND
        if Decision.HIT in handCard.getAction() and handCard.getSumOfCards() <= 17:
            return Decision.HIT
    def getHandCard(self):
        return self.handCard
        
class HandCard:
    def __init__(self, dm, rule, betMoney = 100):
        self.dealingMachine = dm
        self.rule = rule
        self.role = 0        
        self.cards = []
        self.sumOfCards = 0
        self.betMoney = betMoney
        self.endStep = EndStep.NEXT
        
    def initialAction(self, role):
        self.role = role
        if role is Role.PLAYER:
            self.draw()
            self.draw()
        if role is Role.DEALER:
            self.draw()

    def action(self, decision):
        if decision not in self.getAction():
            raise Exception("decision not in getAcion().")
        if decision is Decision.HIT:
            self.draw()
        if decision is Decision.STAND:
            self.endStep = EndStep.STAND
        if decision is Decision.SURRENDER:
            self.endStep = EndStep.SURRENDER
        if decision is Decision.DOUBLE:
            self.draw()
            self.betMoney *= 2.0
            self.endStep = EndStep.STAND
        if decision is Decision.SPLIT:
            card = self.pop()
            self.draw()            

            splitHandCard = HandCard(self.dealingMachine, self.rule, self.betMoney)
            splitHandCard.give(card)
            splitHandCard.draw()
            return splitHandCard
            
            
    def pop(self):
        card = self.cards.pop()
        return card

    def draw(self):
        card = self.dealingMachine.getCard()
        self.cards.append(card)
        
    def give(self, card):
        self.cards.append(card)
    
    def getHandCard(self):
        return self.cards
        
    def getSumOfCards(self):
        sumOfCards = 0        
        for card in self.cards:
            sumOfCards += Deck.VALUE[card]
        for i in range(self.getNumberOfAces()):
            if sumOfCards > 21:
                sumOfCards -= 10
        return sumOfCards
        
    def getNumberOfCards(self):
        return len(self.cards)
        
    def getNumberOfAces(self):
        return self.cards.count(Deck.Card_A)
        
    def getBetMoney(self):
        return self.betMoney
        
    def getAction(self):
        nextStep = []
        if self.endStep in [EndStep.STAND, EndStep.SURRENDER]:
            return nextStep
        if self.getSumOfCards() < 21:
            nextStep.append(Decision.HIT)
        if self.getSumOfCards() <= 21 and self.getNumberOfCards() is not 0:
            nextStep.append(Decision.STAND)
        if self.role is Role.PLAYER and self.getSumOfCards() < 21 and self.getNumberOfCards() is 2:
            nextStep.append(Decision.DOUBLE)
        if self.role is Role.PLAYER and self.getSumOfCards() < 21 and self.cards and self.cards.count(self.cards[0]) is self.getNumberOfCards():
            nextStep.append(Decision.SPLIT)
        if self.role is Role.PLAYER and self.getSumOfCards() < 21 and self.getNumberOfCards() is not 0:
            nextStep.append(Decision.SURRENDER)
        return nextStep
        
    def getEndStep(self):
        if self.getSumOfCards() > 21:
            self.endStep = EndStep.BUST
        if self.getSumOfCards() is 21 and self.getNumberOfCards is 2:
            self.endStep = EndStep.BLACKJACK
        return self.endStep
        
    def getWinLose(self, dealer):
        playerEndStep = self.getEndStep()
        dealerEndStep = dealer.getEndStep()
        playerSumCard = self.getSumOfCards()
        dealerSumCard = dealer.getSumOfCards()
        if playerEndStep in [EndStep.NEXT]:
            raise ValueError("getWinLose: HandCard.endStep does not in stand/bust/blackjack/surrender.")
        if playerEndStep in [EndStep.SURRENDER, EndStep.BUST]:
            return EndStep.LOSE
        if playerEndStep in [EndStep.BLACKJACK]:
            if dealerEndStep in [EndStep.BLACKJACK]:
                return EndStep.DRAW
            else:
                return EndStep.WIN
        if playerEndStep in [EndStep.STAND]:
            if dealerEndStep in [EndStep.BLACKJACK]:
                return EndStep.LOSE
            if dealerEndStep in [EndStep.SURRENDER, EndStep.BUST]:
                return EndStep.WIN
            if dealerEndStep in [EndStep.STAND]:
                if playerSumCard > dealerSumCard:
                    return EndStep.WIN
                if playerSumCard is dealerSumCard:
                    return EndStep.DRAW
                if playerSumCard < dealerSumCard:
                    return EndStep.LOSE
