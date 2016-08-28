def printCommunication(requests, responses):
    
    def __print(preMsg, packetDict):
        for clientId in requests:
            print preMsg
            
            spacer = '  '
            
            print spacer, 'From/To:', clientId
            print spacer, 'Status:', packetDict[clientId].status
            print spacer, 'Content:',  packetDict[clientId].content
            

    if(requests):
        __print("Request: ", requests)
    
    if(responses):
        __print("Response: ", responses)
    