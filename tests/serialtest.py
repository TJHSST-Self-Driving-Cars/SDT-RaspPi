# serial test
import serial, time

ser = serial.Serial('/dev/serial0', 115200, timeout=1)
while True:
    '''
    # ser.write(bytes(66))
    ser.write((66).to_bytes(1, "big"))
    time.sleep(1)
    print(f"sent message?")
    '''
    if (x:=ser.readline()) != b'\r\n': 
        print(x, " <-- from arduino")
        ser.write(x)
    time.sleep(0.01)
