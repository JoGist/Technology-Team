import curses

actions = {
    curses.KEY_UP:    print("Su"),
    curses.KEY_DOWN:  print("Giù"),
    curses.KEY_LEFT:  print("Sinistra"),
    curses.KEY_RIGHT: print("Destra"),
}

def main(window):
    next_key = None
    while True:
        curses.halfdelay(1)
        if next_key is None:
            key = window.getch()
        else:
            key = next_key
            next_key = None
        if key != -1:
            # KEY PRESSED
            curses.halfdelay(3)
            action = actions.get(key)
            if action is not None:
                action()
            next_key = key
            while next_key == key:
                next_key = window.getch()
            # KEY RELEASED
            print("RELEASED")

curses.wrapper(main)