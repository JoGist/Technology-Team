from Button import Button
import time

button = Button(21);
button.daemon = True;
button.start();
while True:
    # print("ciao");
    print(button.status);
    # time.sleep(0.01)
