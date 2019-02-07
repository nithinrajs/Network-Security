import random

class EscapeRoom:

    def start(self):       #initializer
        self.time = 100
        self.StateOpen = []
        self.visible = []       #This is a list of all the things the player has unlocked or seen.
        self.things = []
        self.code = self.CodeLock()

    def command(self, commandString):  #Command Parser
        if commandString.strip == "":
            return ""
        commandParts = commandString.split(" ")
        function = "_cmd_"+commandParts[0]
        if not hasattr(self, function):
            return "You don't know how to do that."
        result = getattr(self, function)(commandParts[1:])
        self.AdvanceClock()
        #if self.status() == "dead":
         #   result += "\nOh no! The clock starts ringing!!! After a few seconds, the room fills with a deadly gas..."        
        return result

    def CodeLock(self):
        pin = random.randint(0,9999)
        code_pin = '{:04}'.format(pin).zfill(4)
        return code_pin

    def _cmd_look(self, LookParts):
        if len(LookParts) == 0:
            return "{}\nYou are in a locked room. There is only one door and it has a numeric keypad.Above the door is a clock that reads {}.Across from the door is a large mirror. Below the mirror is an old chest.The room is old and musty and the floor is creaky and warped.".format(self.code,self.time)
        elif len(LookParts) == 1 and LookParts[0] != "in":
            if LookParts[0] == "door" and "glasses" in self.things:
                key = "".join(sorted(str(self.code)))
                keys = []
                for i in key:
                    if i not in keys:
                        keys.append(i)
                keys = ",".join(map(str,keys))
                return "The door is strong and highly secured. The door is locked and requires a 4-digit code to open. But now you're wearing these glasses you notice something! There are smudges on the digits {}.".format(keys)
            elif LookParts[0] == "door" and "glasses" not in self.things:
                return "The door is strong and highly secured. The door is locked and requires a 4-digit code to open."
            elif LookParts[0] == "mirror" and "hairpin" in self.things:
                return "You look in the mirror and see yourself"
            elif LookParts[0] == "mirror" and "hairpin" not in self.things:
                self.visible.append("hairpin")
                return "You look in the mirror and see yourself... wait, there's a hairpin in your hair. Where did that come from?"
            elif LookParts[0] == "chest":
                return "An old chest. It looks worn, but it's still sturdy."
            elif LookParts[0] == "floor":
                self.visible.append("floor")
                return "The floor makes you nervous. It feels like it could fall in. One of the boards is loose."
            elif LookParts[0] == "board" and "floor" not in self.visible:
                return "You don't see that here." 
            elif LookParts[0] == "board" and "floor" in self.visible:
                self.visible.append("board")
                return "The board is loose, but won't come up when you pull on it. Maybe if you pried it open with something."
            elif LookParts[0] == "board" and "pry" not in self.StateOpen:    #1111
                return "The board has been pulled open. You can look inside."
            elif LookParts[0] == "hairpin" and "hairpin" not in self.visible:
                return "You don't see that here."
            elif LookParts[0] == "hairpin" and "hairpin" in self.visible:
                return "You see nothing special."
            elif LookParts[0] == "hammer" and "hammer" not in self.things: #11111
                return "You don't see that here."
            elif LookParts[0] == "hammer" and "hammer" in self.things:
                return "You see nothing special."
            elif LookParts[0] == "glasses" and "glasses" not in self.things: #11111
                return "You don't see that here."
            elif LookParts[0] == "glasses" and "glasses" in self.things:
                return "These look like spy glasses. Maybe they reveal a clue!"
            elif LookParts[0] == "clock":
                return "You see nothing special."
            else:
                return "You don't see that here."
        elif len(LookParts) == 2 and LookParts[0] == "in":
            if LookParts[1] == "chest" and "hammer" not in self.things and "chest" in self.StateOpen:
                return "Inside the chest you see: a hammer."
            elif LookParts[1] == "chest" and "hammer" in self.things and "chest" in self.StateOpen:
                return "Inside the chest you see: ."
            elif LookParts[1] == "board" and "glasses" not in self.visible and "board" in self.StateOpen:
                self.visible.append("glasses")
                return "Inside the board you see: a glasses."
            elif LookParts[1] == "board" and "glasses" in self.visible and  "board" in self.StateOpen:
                return "Inside the board you see: ."
            else:
                return "You can't look in that!"
        else:
            pass

    def _cmd_get(self,GetParts):
        if len(GetParts) == 0:
            return "Get What?"
        elif len(GetParts) == 1 and GetParts[0] != "from":
            if GetParts[0] == "hairpin" and "hairpin" not in self.visible:
                return "You don't see that."
            elif GetParts[0] == "hairpin" and "hairpin" in self.visible and "hairpin" not in self.things:
                self.things.append("hairpin")
                return "You got it."
            elif GetParts[0] == "hairpin" and "hairpin" in self.things and "hairpin" in self.visible:
                return "You already have that."
            elif GetParts[0] == "board" and "board" not in self.visible:
                return "You don't see that."
            elif GetParts[0] == "board" and "board" in self.visible:
                return "You can't get that."
            elif GetParts[0] == ("door" or "clock" or "mirror" or "chest" or "floor"):
                return "You can't get that."
            elif GetParts[0] == "hammer" and "hammer" in self.things:
                return "You already have that."
            elif GetParts[0] == "glasses" and "glasses" in self.things:
                return "You already have that."
            else:
                return "You don't see that."
        elif len(GetParts) == 3 and GetParts[1] == "from":
            if GetParts[0] == "hammer" and GetParts[2] == "chest" and "chest" not in self.StateOpen:
                return "It's not open."
            elif GetParts[0] == "hammer" and GetParts[2] == "chest" and "chest" in self.StateOpen:
                self.things.append("hammer")
                return "You got it."
            elif GetParts[0] == "hammer" and GetParts[2] == "chest" and "chest" in self.StateOpen and "hammer" in self.things:
                return "You don't see that."
            elif GetParts[0] == "glasses" and GetParts[2] == "board" and "board" not in self.StateOpen:
                return "It's not open."
            elif GetParts[0] == "glasses" and GetParts[2] == "board" and "board" in self.StateOpen:
                self.visible.append("glasses")
                return "You got it."
            elif GetParts[0] == "glasses" and GetParts[2] == "board" and "board" in self.StateOpen and "glasses" in self.things:
                return "You don't see that."
            elif (GetParts[2] != "chest") and (GetParts[2] != "board"):  #11111
                return "You can't get something out of that!"
            else:
                return "You don't see that."

    def _cmd_unlock(self,UnlockParts):
        if len(UnlockParts) == 0:
            return "Unlock what?"
        elif len(UnlockParts) == 3 and UnlockParts[1] == "with":
            if UnlockParts[0] == "chest":
                if UnlockParts[2] == "hairpin" and "hairpin" in self.things and "chest" not in self.StateOpen:
                    self.visible.append("chest")
                    return "You hear a click! It worked!"
                elif (UnlockParts[2] == "hairpin" and "hairpin" not in self.things) or UnlockParts[2] != "hairpin": #11111
                    return "You don't have a hairpin."
                elif UnlockParts[2] == "hairpin" and "hairpin" in self.things and "chest" in self.StateOpen:
                    return "It's already unlocked."
                else:
                    pass

            elif UnlockParts[0] == "door":
                if UnlockParts[2] == str(self.code) and "glasses" in self.things and "door" not in self.visible:
                    self.visible.append("door")
                    return "You hear a click! It worked!"
                elif UnlockParts[2] != str(self.code) and "glasses" in self.things and "door" not in self.visible:
                    return "That's not the right code!"
                elif len(UnlockParts[2]) < 4 and "glasses" in self.things and "door" not in self.visible:
                    return "The code must be 4 digits."
                elif not UnlockParts[2].isnumeric() and "glasses" in self.things and "door" not in self.visible:
                    return "That's not a valid code."
                elif "door" in self.visible:
                    return "It's already unlocked."
                else:
                    pass
            elif UnlockParts[0] == ("clock" or "mirror" or "hairpin" or "floor" or "board" or "hammer" or "glasses"):
                return "You can't unlock that!"
            else:
                return "You don't see that here."
        else:
            pass


    def _cmd_open(self,OpenParts):
        if len(OpenParts) == 0:
            return "Open what?"
        elif len(OpenParts) == 1:
            if OpenParts[0] == "chest" and "chest" not in self.visible:
                return "It's locked."
            elif OpenParts[0] == "door" and "door" not in self.visible:
                return "It's locked."
            elif OpenParts[0] == "chest" and "chest" in self.visible:
                self.StateOpen.append("chest")
                return "You open the chest."
            elif OpenParts[0] == "chest" and "chest" in self.StateOpen:
                return "It's already open!"
            elif OpenParts[0] == "door" and "door" in self.visible:
                self.StateOpen.append("door")
                return "You open the door."
            elif OpenParts[0] == ("clock" or "mirror" or "hairpin" or "floor" or "board" or "hammer" or "glasses"):
                return "You can't open that!"
            else:
                return "You don't see that."
        else:
            pass

    def _cmd_pry(self,PryParts):
        if len(PryParts) == 3 and PryParts[1] == "with":
            if PryParts[0] == "board" and "board" not in self.visible:
                return "You don't see that."
            elif PryParts[0] == "board" and "hammer" not in self.things and "board" in self.visible and "board" not in self.StateOpen:
                return "You don't have a hammer."
            elif PryParts[0] == "board" and "hammer" in self.things and "board" in self.visible and "board" not in self.StateOpen:
                self.StateOpen.append("board")
                return "You use the hammer to pry open the board. It takes some work, but with some blood and sweat, you manage to get it open."
            elif PryParts[0] == "board" and "hammer" in self.things and "board" in self.visible and "board" in self.StateOpen:
                return "It's already pried open."
            elif PryParts[0] == "board" and PryParts[2] != "hammer":
                return "You don't have a hammer"
            elif OpenParts[0] == ("clock" or "mirror" or "hairpin" or "floor" or "door" or "hammer" or "glasses" or "chest"):
                return "Don't be stupid! That won't work!"
            else:
                return "You don't see that."
        else:
            pass

    def _cmd_wear(self,WearParts):
        if len(WearParts) == 1:
            if WearParts[0] == "glasses" and "glasses" not in self.visible:
                return "You don't have a glasses."
            elif WearParts[0] == "glasses" and "glasses" in self.visible:
                self.things.append("glasses")
                return "You are now wearing the glasses."
            elif WearParts[0] == "glasses" and "glasses" in self.things:
                return "You're already wearing them!"
            else:
                return "You can't wear that!"
        else:
            return "You don't have a glasses."

        

    def _cmd_inventory(self,InventParts):
        if len(InventParts) == 0:
            return "You are carrying a {}.".format(", ".join(self.things))
        else:
            pass

    
    def status(self):                                                       #Reports whether the users is "dead", "locked", or "escaped
        state = [state for state in self.StateOpen if state == "door"]
        state_str = ' '.join(state)     #Check the open list for door object
        if state_str == "door" and self.time > 0:
            return "escaped" #Escaped
        elif self.time <= 0:
             return "dead" #Dead
        elif state_str != "door":
            return "locked"    #Locked
        

    def AdvanceClock(self): #Reduce the timer counter
        self.time -= 1

    def Inventory(self):
        pass


def main():
    room = EscapeRoom()
    room.start()
    while room.status() == "locked":
        command = input(">> ")
        output = room.command(command)
        print(output)
        if room.status() == "escaped":
            print("Congratulations! You escaped!")
            continue
        elif room.status() == "dead":
            print("Oh no! The clock starts ringing!!! After a few seconds, the room fills with a deadly gas...")
            continue

if __name__ == "__main__":
    main()
