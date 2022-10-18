class Column:
    def __init__(self, _id, _amountOfFloors, _amountOfElevators):
        self.ID= _id
        self.status = []
        self.elevatorList = []
        self.callButtonList =[]
        self.requestList =[]
        self.createElevators(_amountOfElevators, _amountOfFloors)
        self.createCallButtons(_amountOfFloors)
    def createCallButtons(self,  _amountOfFloors):
        buttonFloor = 1
        callButtonID = 1
        for x in range(_amountOfFloors):
            if (buttonFloor < _amountOfFloors):
                callButton = CallButton(callButtonID, buttonFloor, 'up')
                self.callButtonList.append(callButton)
                callButtonID += 1
            if (buttonFloor > 1):
                callButton = CallButton(callButtonID, buttonFloor, 'down')
                self.callButtonList.append(callButton)
                callButtonID += 1
            buttonFloor+=1
        return self.callButtonList
    
    def createElevators(self, _amountOfElevators, _amountOfFloors):
        elevatorID = 1 
        for x in range(_amountOfElevators):
            elevator = Elevator(elevatorID, _amountOfFloors)
            self.elevatorList.append(elevator)
            elevatorID += 1
        return self.elevatorList
    
    # Simulate when a user press a button outside the elevator
    def requestElevator(self, floor,direction):
        self.requestList.append(floor)
        best = self.findElevator(floor,direction)
        best.floorRequestList.append(floor)
        best.move()
        #  elevator.operateDoors()
        return best
    
    # We use a score system depending on the current elevators state. Since the bestScore and the referenceGap are 
    # higher values than what could be possibly calculated, the first elevator will always become the default bestElevator, 
    # before being compared with to other elevators. If two elevators get the same score, the nearest one is prioritized.
    def findElevator(self, requestedFloor, requestedDirection):
        bestElevator = type('', (), {})()
        bestScore = 5
        referenceGap = 10000000
        bestElevatorInformations = []
        for elevator in self.elevatorList:
            # The elevator is at my floor and going in the direction I want
            if (requestedFloor == elevator.currentFloor) & (elevator.status == 'stopped') &(requestedDirection == elevator.direction):
                bestElevatorInformations = self.checkIfElevatorIsBetter(1, elevator, bestScore, referenceGap, bestElevator,requestedFloor)
            
            # The elevator is lower than me, is coming 'Up' and I want to go 'Up'
            elif (requestedFloor > elevator.currentFloor) & (elevator.direction == 'up') &(requestedDirection == elevator.direction):
                bestElevatorInformations = self.checkIfElevatorIsBetter(2, elevator,bestScore, referenceGap, bestElevator, requestedFloor)
            
            # The elevator is higher than me, is coming 'Down' and I want to go 'Down'
            elif (requestedFloor < elevator.currentFloor) & (elevator.direction == 'down') &(requestedDirection == elevator.direction):
                bestElevatorInformations = self.checkIfElevatorIsBetter(2, elevator,bestScore, referenceGap, bestElevator, requestedFloor)
            
            # The elevator is idle
            elif elevator.status == 'idle':
                bestElevatorInformations = self.checkIfElevatorIsBetter(3, elevator,bestScore, referenceGap, bestElevator, requestedFloor)
            
            else:
                bestElevatorInformations = self.checkIfElevatorIsBetter(4, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            
            bestElevator = bestElevatorInformations[0]
            bestScore = bestElevatorInformations[1]
            referenceGap = bestElevatorInformations[2]
        return bestElevator
    

    def checkIfElevatorIsBetter(self, scoreToCheck, newElevator, bestScore, referenceGap, bestElevator, floor):
        if scoreToCheck < bestScore:
             bestScore= scoreToCheck
             bestElevator = newElevator
             referenceGap = abs(newElevator.currentFloor - floor)
        
        elif bestScore == scoreToCheck:
            gap = abs(newElevator.currentFloor - floor)
            if referenceGap > gap:
                 bestElevator = newElevator
                 referenceGap = gap
            
        
        return [bestElevator, bestScore, referenceGap]
    

class FloorRequestButton: 
    def __init__(self, _id, _floor):
        self.ID = _id
        self.status = 'OFF'
        self.floor = _floor
    
class Elevator:
    def __init__(self, _id, _amountOfFloors):
        self.ID = _id
        self.status = 'idle'
        self.currentFloor = 1
        self.direction = None
        self.door = Door(_id)
        self.floorRequestButtonList =[]
        self.floorButtonsList =[]
        self.floorRequestList = []
        self.createFloorRequestButtons(_amountOfFloors)
    
    def createFloorRequestButtons(self, _amountOfFloors):
        buttonFloor = 1
        
        FloorRequestButtonID = 1
        for i in range(_amountOfFloors):
            floorRequestButton = FloorRequestButton(FloorRequestButtonID, buttonFloor)
            self.floorRequestButtonList.append(floorRequestButton)
            buttonFloor += 1
            FloorRequestButtonID += 1
            
    
    # Simulate when a user press a button inside the elevator
    def requestFloor(self, floor):
        self.floorRequestList.append(floor)
        self.move()
        #  self.operateDoors()
    
    def move(self):
        while (len(self.floorRequestList) != 0 ):
            destination = self.floorRequestList[0]
            self.status = 'moving'
            if self.currentFloor < destination:
                self.direction = 'up'
                self.sortFloorList()
                while self.currentFloor < destination:
                    self.currentFloor += 1
                    self.screenDisplay = self.currentFloor
                
            
            elif self.currentFloor > destination:
                self.direction = 'down'
                self.sortFloorList()
                while self.currentFloor > destination:
                    self.currentFloor -= 1
                    self.screenDisplay = self.currentFloor
                
            
            self.status = 'stopped'
            self.floorRequestList.pop(0)
        
        self.status = 'idle'
    
    def sortFloorList(self):
        if self.direction == 'up':
            self.floorRequestList.sort()
        else:
            self.floorRequestList.reverse()
        

class CallButton:
    def __init__(self, _id, _floor, _direction):
        self.ID = _id
        self.status = "OFF"
        self.floor = _floor
        self.direction = _direction
class Door:
    def __init__(self, _id):
        self.ID = _id
        self.status = 'closed'

    

    
    #  operateDoors()
    #      self.door.status = opened
    #      await 5 seconds
    #      if (this is not overweight)
    #          self.door.status = closing
    #          if no obstruction
    #              self.door.status = closed
    #          
    #          else
    #              self.operateDoors()
    #          
    #      
    #      else
    #          while (this is overweight)
    #              activate overweight alarm
    #          
    #          self.operateDoors()
    #      
    #  