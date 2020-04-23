from enum import Enum

class FieldState(Enum):
    EMPTY = 1
    BOX = 2
    WALL = 3

class Field:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state

class Box:
    def __init__(self, len_x, len_y):
        self.len_x = len_x
        self.len_y = len_y

class Magazine:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.fill_factor = 0.0
        self.is_filled = False
        self.wall_blocks_count = 0
        self.next_box_index = 0   # index of field where trying to insert a next box will begin

        self.fields = []
        x = 0
        y = 0
        for i in range(self.X*self.Y):
            self.fields.append(Field(x,y,FieldState.EMPTY))
            x += 1
            if (x == X):
                x = 0
                y += 1
    
    def setFieldStateToWall(self, x, y):
        self.__setFieldState(x, y, FieldState.WALL)
        self.wall_blocks_count += 1
    
    def setFieldStateToEmpty(self, x, y):
        if (self.__setFieldState(x, y, FieldState.EMPTY) == FieldState.WALL):
            self.wall_blocks_count -= 1

    def __setFieldState(self, x, y, state):
        assert (x >= 0)
        assert (x <= self.X)
        assert(y >= 0)
        assert (y <= self.Y)
        oldstate = self.fields[x + y*self.X].state
        self.fields[x + y*self.X].state = state
        return oldstate

    def getFieldState(self, x, y):
        assert (x >= 0)
        assert (x <= self.X)
        assert (y >= 0)
        assert (y <= self.Y)
        
        state = ""
        if self.fields[x + y*self.X].state == FieldState.EMPTY: state = "empty"
        elif self.fields[x + y*self.X].state == FieldState.WALL: state = "wall"
        elif self.fields[x + y*self.X].state == FieldState.BOX: state = "box"
        assert (state != "")

        return state

    def addBox(self, box):
        # First, mark fields which will be occupied by the box and see if you can
        # insert it. If not, change the starting point and try again. Keep it until
        # you insert the box or the starting point is out of range.
        box_fields = []
        start_index = self.next_box_index
        while (start_index < len(self.fields)):
            start_y = start_index // self.X
            start_x = start_index - (start_y*self.X)
            if (start_y + box.len_y > self.Y):
                # The box won't fit 
                return False 
            if (start_x + box.len_x > self.X):
                # Try in the next row
                start_index += (self.X - start_x)
                continue

            can_be_inserted = True

            for i in range(box.len_y):
                index = start_x + self.X*(start_y + i)
                for j in range (box.len_x):
                    if (self.__checkIfFieldIsConflicting(index)):
                        start_index += 1
                        can_be_inserted = False
                        break # inner for loop            
  
                    # This field is not conflicting - mark it
                    box_fields.append(index)
                    index += 1

                if (not can_be_inserted):
                    box_fields.clear()
                    break # outer for loop

            if (can_be_inserted):
                # Insert the box in the marked fields
                for i in box_fields:
                    self.fields[i].state = FieldState.BOX
                # Update fill factor
                self.fill_factor += len(box_fields)/(len(self.fields) - self.wall_blocks_count)
                # Move the next box starting point
                self.next_box_index = start_index + box.len_x + 1
                
                return True

        # Starting index out of range - this box won't fit in the magazine
        return False 

    def __checkIfFieldIsConflicting(self, index):
        # Check same field conflicts and (x-1, y), (x+1, y), (x, y-1) neighbors conflicts
        #
        if (
            self.fields[index].state == FieldState.WALL
            or self.fields[index].state == FieldState.BOX
            or (self.fields[index-1].state == FieldState.BOX and index % self.X != 0)
            or (index >= self.X and self.fields[index - self.X].state == FieldState.BOX)
            or (index+1 < len(self.fields) and self.fields[index+1].state == FieldState.BOX
                and (index+1) % self.X != 0
                )
        ):
            return True

        # Check corner conflicts
        #
        if (index >= self.X): # at least second row
            
            if (index % self.X != 0): # not at the left edge

                # Check conflict at the left-bottom corner of the box
                if (self.fields[index - self.X - 1].state == FieldState.BOX
                    and self.fields[index-1] != FieldState.WALL
                    and self.fields[index-self.X] != FieldState.WALL
                ):
                    return True

            if ((index+1) % self.X != 0): # not at the right edge

                # Check conflict at the right-bottom corner of the box
                if (self.fields[index - self.X + 1].state == FieldState.BOX
                    and self.fields[index+1] != FieldState.WALL
                    and self.fields[index-self.X] != FieldState.WALL
                ):
                    return True
        
        # No conflicts
        return False

    def removeAllBoxes(self):
        self.fill_factor = 0.0
        self.next_box_index = 0
        self.is_filled = 0
        for i in range (self.X*self.Y):
            if (self.fields[i].state == FieldState.BOX):
                self.fields[i].state = FieldState.EMPTY

    #def checkIfMagazineIsFilled(self):
    #    # Check if there is place for a box in the magazine - which actually
    #    # means checking if there is place for a 1x1 box
    #    index = self.next_box_index
    #    while (index < len(self.fields)):
    #        if (self.fields[index].state == FieldState.WALL
    #            or self.fields[index].state == FieldState.BOX
    #            or (self.fields[index-1].state == FieldState.BOX and index % self.X != 0)
    #            or (index >= self.X and self.fields[index - self.X].state == FieldState.BOX)
    #            or (index+1 < len(self.fields) and self.fields[index+1].state == FieldState.BOX
    #              and (index+1) % self.X != 0)):
    #                index += 1
    #        else:
    #            return False
    #    return True



        
     
        
        



