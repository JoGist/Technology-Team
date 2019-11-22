from Led import Led
import time

# button = Led(13); #Yellow
# button = Led(4); #GREEN
# button = Led(18); #Red
button = Led(17); #BLUE
while True:
    # print("ciao");
    button.on();
    time.sleep(0.1)
    button.off();
    time.sleep(0.1)
