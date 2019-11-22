#include "Led.h"            //Here. Again player.h must be in the current directory. or use relative or absolute path to it.
#include "Led.cpp"
int main(){
    Led red(18,"Rosso");
    Led yellow(13,"Giallo");
    Led green(4,"Verde");
    Led blue(17,"Blu");


    red.on();
    green.off();
    yellow.off();
    blue.off();
    delay(1000);			     // wait 1 sec

    red.off();
    green.on();
    yellow.off();
    blue.off();
    delay(1000);			     // wait 1 sec

    red.off();
    green.off();
    yellow.on();
    blue.off();
    delay(1000);			     // wait 1 sec

    red.off();
    green.off();
    yellow.off();
    blue.on();
    delay(1000);			     // wait 1 sec

    red.off();
    green.off();
    yellow.off();
    blue.off();

    return 0;
}
