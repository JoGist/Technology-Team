
import time, sys
from library_py.Rover import Rover
from library_py.blackbox_py.BlackBox import BlackBox


def main():
    name = "Hector"
    coordinatesTarget = {'latitude':41.893345,'longitude':12.492247};
    # 41.892901, 12.492967
    # 41.893428, 12.491881

    # 41.893354, 12.492258
    k = 0;
    for arg in sys.argv[1:]:
        print(arg);
        if(k == 0):
            name = arg;
        if(k == 1):
            coordinatesTarget['latitude'] = arg;
        if(k == 2):
            coordinatesTarget['longitude'] = arg;
        k = k + 1;

    rover = Rover(name,coordinatesTarget);
    rover.daemon = True;
    rover.start();

    black_box = BlackBox(rover.getHeaderData(),False);
    black_box.daemon = True;
    black_box.start();

    while(True):
        black_box.updateData(rover.getData());
        # print(rover.getData());
        time.sleep(0.1);

if __name__ == '__main__':
    main()
