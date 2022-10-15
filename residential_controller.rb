class Column
    @@no_of_column = 0
    def initialize(_id, _amountOfElevators,_amountOfFloors)
        @column_ID= _id
        @column_status = 'Online'
        @column_elevatorList = []
        @column_callButtonList =[]
        createElevators _amountOfElevators, _amountOfFloors 
        createCallButtons _amountOfFloors
    end    
        
    def createCallButtons(_amountOfFloors)
        buttonFloor = 1
        callButtonID = 1
        floor = 1
            until floor == _amountOfFloors do
                if buttonFloor < _amountOfFloors
                    callButton = CallButton(callButtonID, buttonFloor, 'up')
                    callButtonList.append(callButton)
                end
                if buttonFloor > 1
                    callButton = CallButton(callButtonID, buttonFloor, 'down')
                    callButtonList.append(callButton)
                end
                callButtonID += 1
                buttonFloor += 1
            return callButtonList
        end
    end
    def createElevators( _amountOfElevators, _amountOfFloors)
        elevatorID = 1 
        until elevatorID == _amountOfElevators do 
            elevator = Elevator(elevatorID, _amountOfFloors)
            elevatorList.append(elevator)
            elevatorID += 1
        return elevatorList
        end
    end
    # Simulate when a user press a button outside the elevator
    def requestElevator(floor,direction)
        best = findElevator(floor,direction)
        best.floorRequestList.append(floor)
        best.move()
        #  elevator.operateDoors()
        return best
    end 
    # We use a score system depending on the current elevators state. Since the bestScore and the referenceGap are 
    # higher values than what could be possibly calculated, the first elevator will always become the default bestElevator, 
    # before being compared with to other elevators. If two elevators get the same score, the nearest one is prioritized.
    def findElevator(requestedFloor, requestedDirection)
        # bestElevator = type('', (), {})()
        bestScore = 5
        referenceGap = 10000000
        bestElevatorInformations = []
        for elevator in elevatorList do
            # The elevator is at my floor and going in the direction I want
            if (requestedFloor == elevator.currentFloor) & (elevator.status == 'stopped') &(requestedDirection == elevator.direction)
                bestElevatorInformations = checkIfElevatorIsBetter(1, elevator, bestScore, referenceGap, bestElevator,requestedFloor)
            
            # The elevator is lower than me, is coming 'Up' and I want to go 'Up'
            elsif (requestedFloor > elevator.currentFloor) & (elevator.direction == 'up') &(requestedDirection == elevator.direction)
                bestElevatorInformations = checkIfElevatorIsBetter(2, elevator,bestScore, referenceGap, bestElevator, requestedFloor)
            
            # The elevator is higher than me, is coming 'Down' and I want to go 'Down'
            elsif (requestedFloor < elevator.currentFloor) & (elevator.direction == 'down') &(requestedDirection == elevator.direction)
                bestElevatorInformations = checkIfElevatorIsBetter(2, elevator,bestScore, referenceGap, bestElevator, requestedFloor)
            
            # The elevator is idle
            elsif elevator.status == 'idle'
                bestElevatorInformations = checkIfElevatorIsBetter(3, elevator,bestScore, referenceGap, bestElevator, requestedFloor)
            
            else
                bestElevatorInformations = checkIfElevatorIsBetter(4, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            end
            bestElevator = bestElevatorInformations[0]
            bestScore = bestElevatorInformations[1]
            referenceGap = bestElevatorInformations[2]
        return bestElevator
        end
    end
    

    def checkIfElevatorIsBetter(scoreToCheck, newElevator, bestScore, referenceGap, bestElevator, floor)
        if scoreToCheck < bestScore
             bestScore= scoreToCheck
             bestElevator = newElevator
             referenceGap = abs(newElevator.currentFloor - floor)
        
        elsif bestScore == scoreToCheck
            gap = abs(newElevator.currentFloor - floor)
            if referenceGap > gap
                 bestElevator = newElevator
                 referenceGap = gap
            end
        end    
        
        return [bestElevator, bestScore, referenceGap]
    
    end
end
class FloorRequestButton
    @@no_of_floorrequestbutton = 0
    def initialize(_id, _floor)
        @floorrequestbutton_ID= _id
        @floorrequestbutton_status = 'OFF'
        @floorrequestbutton_floor = _floor
    end    
end     
class Elevator 
    @@no_of_elevator = 0
    def initialize(_id, _amountOfFloors)
        @elevator_ID= _id
        @elevator_status = 'idle'
        @elevator_currentFloor = 1
        @elevator_direction = None
        @elevator_door = Door(_id)
        @elevator_floorRequestButtonList =[]
        @elevator_floorButtonsList =[]
        @elevator_floorRequestList = []
        createFloorRequestButtons(_amountOfFloors)
    end        
    def createFloorRequestButtons(_amountOfFloors)
        buttonFloor = 1
        buttonID = 1
        
            until buttonID  == _amountOfFloors do 
                floorRequestButton = FloorRequestButton(FloorRequestButtonID, buttonFloor)
                floorRequestButtonList.append(floorRequestButton)
                buttonFloor += 1
            buttonID += 1
        end
    end

            
    
    # Simulate when a user press a button inside the elevator
    def requestFloor(floor)
        floorRequestList.append(floor)
        move
        #  operateDoors()
    end    
    def move
        while len(floorRequestList) != 0 
            destination = floorRequestList[0]
            status = 'moving'
            if currentFloor < destination
                direction = 'up'
                sortFloorList()
                while currentFloor < destination
                    currentFloor += 1
                    screenDisplay = currentFloor
                end
            elsif currentFloor > destination
                direction = 'down'
                sortFloorList()
                while currentFloor > destination
                    currentFloor -= 1
                    screenDisplay = currentFloor
                end
            end 
            status = 'stopped'
            floorRequestList.pop(0)
        end
        status = 'idle'
    end
    def sortFloorList()
        if direction == 'up'
            floorRequestList.sort()
        else
            floorRequestList.reverse()
        end
    end
end
class CallButton
    @@no_of_callbutton = 0
    def initialize(_id, _floor, _direction)
        @callbutton_ID= _id
        @callbutton_status = "OFF"
        @callbutton_floor = _floor
        @callbutton_direction = _direction
    end    
end
class Door
    @@no_of_door = 0
    def initialize(_id)
        @door_ID= _id
        @door_status = 'closed'
    end    
end
    