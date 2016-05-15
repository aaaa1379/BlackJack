# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 17:46:43 2016

@author: Akii
"""

from dealingMachine import Deck
from gameRules import Role
from gameRules import Decision
from gameRules import EndStep
import strategy

class Player:
    def __init__(self, dm, rule, money):
        self.dealingMachine = dm
        self.handCards = []
        self.rule = rule
        self.money = money

    def initialDeal(self):
        # Bet = total x (0.004628 x true count + 0.009669) when count ≥ 1
        bet = self.money * (0.005 * self.dealingMachine.getCounting() + 0.01)
        handCard = HandCard(self.dealingMachine, self.rule, bet)
        handCard.initialAction(Role.PLAYER)
        self.handCards = []
        self.handCards.append(handCard)
    def playerAction(self, dealer, agent=''):
        for handCard in self.handCards:
            while handCard.getAction():
                self.printAction(handCard, dealer.getHandCard())
                if agent is '':
                    decision = raw_input("INPUT >>> ")        # number 1~5
                    decision = Decision.MAP[int(decision)]     # convert to Decision.HIT...
                else:
                    agentMethod = getattr(strategy, agent)
                    decision = agentMethod(handCard, dealer.getHandCard())
                    #decision = easyAction(handCard, dealer)
                    print "INPUT >>>", decision
                splitHandCard = handCard.action(decision)
                if splitHandCard:
                    self.handCards.append(splitHandCard)
                #self.action(handCard)
        
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
            self.printResult(handCard, dealer.getHandCard(), earn)
            

    def getMoney(self):
        return self.money

    def printAction(self, handCard, dealerHandCard):
        print "1: Hit, 2: Stand, 3: Double, 4: Split, 5: Surrender"
        print "Player      %2d %s" %(handCard.getSumOfCards(), handCard.getCards())
        print "Dealer      %2d %s" %(dealerHandCard.getSumOfCards(), dealerHandCard.getCards())
        print "Your Action", handCard.getAction()
        print "Your Money ", self.money
        print "Your Bet   ", handCard.getBetMoney()
        
    def printResult(self, handCard, dealerHandCard, earn):
        endStep = handCard.getEndStep()
        winlose = handCard.getWinLose(dealerHandCard)
        print "Player      %2d %s" %(handCard.getSumOfCards(), handCard.getCards())
        print "Dealer      %2d %s" %(dealerHandCard.getSumOfCards(), dealerHandCard.getCards())
        print "EndStep    ", endStep, winlose
        print "Earn       ", earn
        
        
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
        """ Step: initial deal """
        self.role = role
        if role is Role.PLAYER:
            self.__draw__()
            self.__draw__()
        if role is Role.DEALER:
            self.__draw__()

    def action(self, decision):
        """ Step: player action """
        if decision not in self.getAction():
            raise Exception("decision not in getAcion().")
        if decision is Decision.HIT:
            self.__draw__()
        if decision is Decision.STAND:
            self.endStep = EndStep.STAND
        if decision is Decision.SURRENDER:
            self.endStep = EndStep.SURRENDER
        if decision is Decision.DOUBLE:
            self.__draw__()
            self.betMoney *= 2.0
            self.endStep = EndStep.STAND
        if decision is Decision.SPLIT:
            card = self.__pop__()
            self.__draw__()            

            splitHandCard = HandCard(self.dealingMachine, self.rule, self.betMoney)
            splitHandCard.__give__(card)
            splitHandCard.__draw__()
            return splitHandCard
            
            
    def __pop__(self):
        card = self.cards.pop()
        return card

    def __draw__(self):
        card = self.dealingMachine.getCard()
        self.cards.append(card)
        
    def __give__(self, card):
        self.cards.append(card)
    
    def getCards(self):
        """ return an array with hand cards 
            Ex. ['Card_5', 'Card_2'] """
        return self.cards
        
    def getSumOfCards(self):
        """ return sum of hand cards """
        sumOfCards = 0        
        for card in self.cards:
            sumOfCards += Deck.VALUE[card]
        for i in range(self.getNumberOfAces()):
            if sumOfCards > 21:
                sumOfCards -= 10
        return sumOfCards
        
    def getNumberOfCards(self):
        """ return the number of cards in your hand card """
        return len(self.cards)
        
    def getNumberOfAces(self):
        """ return the number of aces in your hand card """
        return self.cards.count(Deck.Card_A)
        
    def getBetMoney(self):
        """ get you bet money in this round """
        return self.betMoney
        
    def getAction(self):
        """ return actions Decision.HIT, Decision.STAND ......
            Ex. ['Hit', 'Stand'] """
        nextStep = []
        if self.endStep in [EndStep.STAND, EndStep.SURRENDER]:
            return nextStep
        if self.getSumOfCards() < 21:
            nextStep.append(Decision.HIT)
        if self.getSumOfCards() <= 21 and self.getNumberOfCards() is not 0:
            nextStep.append(Decision.STAND)
        if self.getSumOfCards() < 21 and self.getNumberOfCards() is 2:
            nextStep.append(Decision.DOUBLE)
        if self.getSumOfCards() < 21 and self.cards and self.cards.count(self.cards[0]) is self.getNumberOfCards():
            nextStep.append(Decision.SPLIT)
        if self.getSumOfCards() < 21 and self.getNumberOfCards() is not 0:
            nextStep.append(Decision.SURRENDER)
        return nextStep
      
    def getEndStep(self):
        """ check the end step is bust or blackjack """
        if self.getSumOfCards() > 21:
            self.endStep = EndStep.BUST
        if self.getSumOfCards() is 21 and self.getNumberOfCards() is 2:
            self.endStep = EndStep.BLACKJACK
        return self.endStep      
      
    def getWinLose(self, dealerHandCard):
        """ Step: Dealer's hand revealed
            you get win or lose after compete with dealer. 
            return: EndStep.LOST, EndStep.DRAW, EndStep.WIN """
        playerEndStep = self.getEndStep()
        dealerEndStep = dealerHandCard.getEndStep()
        playerSumCard = self.getSumOfCards()
        dealerSumCard = dealerHandCard.getSumOfCards()
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

