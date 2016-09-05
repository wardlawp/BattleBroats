'''
Created on Aug 24, 2016

@author: Philip Wardlaw
'''

from game_states import ClientState
from server_play import  ServerPlayState
from BattleBroats.attack_order import AttackOrder
from BattleBroats.board_update import BoardUpdate
from client_end import ClientEndState
from server_end import ServerEndState



class ClientPlayState(ClientState):
    """
    State class defining behaviour of client at start of game
    Ask to join, then ask has the game started
    """
    
    def __init__(self,game):
        ClientState.__init__(self,game)
        self.__attackOrder = None
        self.myGo = False
        self.__finished = False
    

    def registerHandlers(self):
        #define methods
        def strHandler(content):
            if content ==  ServerPlayState.GO:
                self.myGo = True
            elif content == ServerPlayState.NGO:
                self.myGo = False
            elif content == ServerEndState.FINISHED:
                self.__finished = True
            


        
        def boardUpdateHandler(content):
            self.game.updateBoards({content.pId :content.board})


        #register methods
        self.handlers[unicode.__name__] = strHandler
        self.handlers[str.__name__] = strHandler
        self.handlers[BoardUpdate.__name__] = boardUpdateHandler
              


    def questions(self):
        return [ServerPlayState.VIEW]

    def handle(self, packets, _input):

        self.handlePackets(packets)
        responseContent = self.questions()
        responseContent += self.handleInput(_input)
         
         
        return self.packageContent(responseContent)
            

    def handleInput(self, _input):
        self.__attackOrder = None
        if isinstance(_input, list):
            self.myGo = False
            return [AttackOrder(_input[0], _input[1])]
        
        return []
    
    def nextState(self):
        "Get the GameState that should be used next game loop"
        if self.__finished:
            return ClientEndState(self.game)
        else:
            return self




    
    
