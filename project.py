import curses
from curses import wrapper #helps to initilise the curses module, it allows to take over the terminal and run some commands onto it.
import time   #it will allow us to calculate time , how long are you typing for
import random  

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test: ")
    stdscr.addstr("\nPress any key to begin: ") 
    stdscr.refresh() # .refresh() is used to refresh the screen
    stdscr.getkey()  # .getkey() wait for the user to type something, it wont end the program immediately


def display_text(stdscr, target, current,  wpm=0):
    stdscr.addstr(target) 
    stdscr.addstr( f"\nWPM: {wpm}") 

    
    for i,char in enumerate(current): #enumerate() is used to give the index as well as the element.
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0,i,char,color)


def load_text():
    with open("text.txt","r") as s: #means open() store it in s and call s using s.readlines() 
        lines = s.readlines()  # its is going to give list of all the lines in the open file
        return random.choice(lines).strip()  # .strip() will remove any leading or trailing whitespace character such as "\n" character.



def wpm_test(stdscr):
    target_text  = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()  #keeps tracks of the start time and its a very large number ; it asctually means number of seconds passed known as epoch
    stdscr.nodelay(True) #do not delay waiting for user to hit a key.

    
    while True:
        time_elapsed = max(time.time() - start_time,1)
        wpm = round((len(current_text) / (time_elapsed / 60))/5) #it gives out characters per minute


        stdscr.clear()
        display_text(stdscr,target_text,current_text,wpm)
        stdscr.refresh() 
        
        if "".join(current_text) == target_text:    # "".join() converts the list into string
            stdscr.nodelay(False)
            break


        try:
            key =  stdscr.getkey()
        except:
            continue

        if ord(key) == 27: #ord() means evry key on the keyboard has some values, and "esc" has a value 27 attached to it.
            break 
        if key in ("KEY_BACKSPACE","\b", "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

  
def main(stdscr): # std screen ;std is standard output(its like a terminal where you r writinh the output)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)

    while(True):
       wpm_test(stdscr)
       stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
       key = stdscr.getkey()

       if ord(key) == 27:
           break 

wrapper(main)



