#include "Gps.h"


Gps::Gps() {
    if(wiringPiSetupGpio() == -1) { //when initialize wiringPi failed, print message to screen
        status = false;
    }
    if ((serial_port = serialOpen ("/dev/ttyS0", 9600)) < 0){	/* open serial port */
        status = false;
    }
}
double Gps::getLatitude() {
    return latitude;
}
double Gps::getLongitude() {
    return longitude;
}
bool Gps::getStatus() {
    return longitude;
}

void Gps::updateData() {
    // printf("Update\n");
    bool found = false;
    string data("");
    // vector <string> fields;
    while(!found){
        if(serialDataAvail (serial_port)) {
            dat = serialGetchar (serial_port);		/* receive character serially*/
            data += dat;
            if (dat == '\n' ){
                // cout<<data;
                if (data.find("$GPRMC") == 0){
                    // cout<<data;
                    // fields = split(",");
                    int n = data.length();

                    // declaring character array
                    char str[n+1];
                    strcpy(str, data.c_str());
                    // cout << str;
                    // Returns first token
                    char *token = strtok(str, ",");
                    // cout<<&token;


                    // Keep printing tokens while one of the
                    // delimiters present in str[].
                    int k = 0;
                    status = false;
                    while (token != NULL)
                    {
                        // printf("%s\n", token);
                        if(k == 2){
                            string temp = token;
                            string fullString;
                            string subString;
                            double degTemp;
                            double minTemp;
                            int lengthTemp;
                            if(temp.find("A") == 0){
                                // printf("%s\n", token);
                                token = strtok(NULL, ",");
                                // printf("%s\n", token);
                                // Decode longitude
                                fullString = token;
                                // cout << fullString <<endl;
                                lengthTemp = fullString.length();
                                // cout << lengthTemp <<endl;
                                subString= fullString.substr(0, 2);
                                degTemp  = stod(subString);
                                // cout << subString<< '\n';
                                // cout << degTemp<< '\n';

                                subString= fullString.substr(2, lengthTemp-1);
                                minTemp  = stod(subString);
                                // cout << subString<< '\n';
                                // cout << minTemp<< '\n';

                                latitude = degTemp + minTemp/60;

                                token = strtok(NULL, ",");
                                // printf("%s\n", token);
                                token = strtok(NULL, ",");

                                //decode longitude
                                fullString = token;
                                // cout << fullString <<endl;
                                lengthTemp = fullString.length();
                                // cout << lengthTemp <<endl;
                                subString= fullString.substr(0, 3);
                                degTemp  = stod(subString);
                                // cout << subString<< '\n';
                                // cout << degTemp<< '\n';

                                subString= fullString.substr(3, lengthTemp-1);
                                minTemp  = stod(subString);
                                // cout << subString<< '\n';
                                // cout << minTemp<< '\n';

                                longitude = degTemp + minTemp/60;

                                // latitude = strtod(token,NULL);
                                // printf("%s\n", token);
                                status = true;
                            } else {
                                // cout <<"false";
                                status = false;
                            }
                        }

                        token = strtok(NULL, ",");
                        k++;
                    }
                    found = true;
                }
                data = "";
            }
            // printf ("%s", data) ;
        }
    }
}
