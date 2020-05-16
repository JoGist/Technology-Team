import smbus
import threading
import time

class Imu():
    def __init__(self):
        #acc_fchoiceb vale solo 0 o 1, gy_fchoiceb 00-11
        self.config = {"acc_fchoiceb":0,"gy_fchoiceb":0,"acc_dlpf":0,"gy_dlpf":0}
        self.acc = {"x":0,"y":0,"z":0}
        self.gyro = {"x":0,"y":0,"z":0}
        #acquisizione temperatura ok, elaborazione dati da implementare
        self.temperature = 25
        self.address = 0x68
        self.scaler = 16.4
        self.gyrooff = [0,0,0]
        self.acceloff = [0,0,0]
        self.magnetoff = [0,0,0]
        self.th_flag = 0
        self._power_mgmt_1 = 0x6b
        self._power_mgmt_2 = 0x6c
        self.bus = smbus.SMBus(1)
        self.bus.write_byte_data(self.address, self._power_mgmt_1, 1)
        self.setup()

    # sampleratedivider, DLPF, fondoscala acc e gyro
    def setup(self, gyro_filter=0, accel_filter=0,samplediv=0, fsgyro=0, fsaccel=0):
        pass

    def sampleratedivider(self,value):
        #value deve essere compreso tra 0 e 255
        #samplerate = internalsamplerate/(1+value)
        addr = 25
        if(value>255):
            value = 255
        elif(value<0):
            value = 0
        self.write_byte(addr,value)

    def dlpf(self,gy_value,acc_value):
        #value deve essere compreso tra 0 e 7
        #value crescente diminuisce la banda passante, 7 e' un eccezione
        gy_addr = 26
        acc_addr = 29
        gy_value=min(7,gy_value)
        gy_value=max(0,gy_value)
        acc_value=min(7,acc_value)
        acc_value=max(0,acc_value)
        self.write_byte(gy_addr,gy_value)
        data = self.config["acc_fchoiceb"]<<3 + acc_value
        self.write_byte(acc_addr,data)
        self.config["gy_dlpf"] = gy_value
        self.config["acc_dlpf"] = acc_value
        #non c'e' bisogno di formattare il byte perche' gli altri campi sono 0

    def fs_select(self,fs_gyro,fs_acc):
        #fs_gyro-> 0,1,2,3 ->(250,500,1000,2000)dps
        #quando fchoiceb e' 0 il dlpf e' attivo, fchoice-> 0,1,2,3-> 3 dlpf spento
        addr_gyro = 27
        addr_acc = 28
        fs_gyro = min(3,fs_gyro)
        fs_gyro = max(0,fs_gyro)
        fs_acc = min(3,fs_acc)
        fs_acc = max(0,fs_acc)
        gy_value = fs_gyro<<3
        gy_value += self.config["gy_fchoiceb"]
        acc_value = fs_acc<<3
        self.write_byte(addr_gyro,gy_value)
        self.write_byte(addr_acc,acc_value)
        data = self.config["acc_fchoiceb"]<<3 + self.config["acc_dlpf"]
        self.write_byte(addr_acc+1,data)

    def merge_word(self,high,low):
        #high, bit piu' significativi
        #low, bit meno significativi
        val = (high << 8) + low
        return val

    def two_comp(self,val, bits):
        #complemento a 2
        if (val & (1 << (bits - 1))) != 0:
            val = val - (1 << bits)
        return val

    def read_datablock(self):
        #ritorna un vettore da 14 elementi con i dati, da elaborare come word
        #da 16 bit, e il tempo trascorso per la lettura
        startc=time.time()
        return self.bus.read_i2c_block_data(self.address,0x3b,14) , time.time()-startc

    def parse_block(self,dblock):
        if(len(dblock)!=14):
            return -1
        self.acc["x"]=self.two_comp(self.merge_word(dblock[0],dblock[1]),16)
        self.acc["y"]=self.two_comp(self.merge_word(dblock[2],dblock[3]),16)
        self.acc["z"]=self.two_comp(self.merge_word(dblock[4],dblock[5]),16)
        self.temperature=self.two_comp(self.merge_word(dblock[6],dblock[7]),16)
        self.gyro["x"]=self.two_comp(self.merge_word(dblock[8],dblock[9]),16)
        self.gyro["y"]=self.two_comp(self.merge_word(dblock[10],dblock[11]),16)
        self.gyro["z"]=self.two_comp(self.merge_word(dblock[12],dblock[13]),16)
        return 1

    def read_magnetometer(self):
        #da implementare
        pass

    def read_byte(self,adr):
        return self.bus.read_byte_data(self.address, adr)

    def write_byte(self, adr, data):
        self.bus.write_byte_data(self.address, adr, data)

    def autoupdate(self):
        while 1:
            #i dati sono prelevabili da self.acc["x"], self.acc["y"], etc..
            data,dur=self.read_datablock()
            if(self.parse_block(data)<0):
                print("Errore")
            if(self.th_flag==1):
                self.th_flag = 0
                exit(0)

    #blocca il thread
    def stop(self):
        #self.th_flag e' la variabile condivisa con il thread che viene controllata
        self.th_flag = 1

    #fa partire il thread
    def run(self):
        x = threading.Thread(target=self.autoupdate, args=())
        x.start()

    def test(self):
        x=0
        accx=open("accx.log","w")
        accy=open("accy.log","w")
        accz=open("accz.log","w")
        gyrox=open("gyrox.log","w")
        gyroy=open("gyroy.log","w")
        gyroz=open("gyroz.log","w")
        while x<100000:
            a,dur=self.read_datablock()
            if(self.parse_block(a)<0):
                print("Errore")
            accx.write(str(self.acc["x"])+"\n")
            accy.write(str(self.acc["y"])+"\n")
            accz.write(str(self.acc["z"])+"\n")
            gyrox.write(str(self.gyro["x"])+"\n")
            gyroy.write(str(self.gyro["y"])+"\n")
            gyroz.write(str(self.gyro["z"])+"\n")
            x+=1
        accx.close()
        accy.close()
        accz.close()
        gyrox.close()
        gyroy.close()
        gyroz.close()
