import time
import matplotlib.pyplot as plt
start = time.time()
x = []
y = []
ser = serial.Serial('COM6', 2000000, timeout=0)
time.sleep(2)
fig = plt.figure()
plt.ion()  # turn on interactive mode
fig.canvas.draw()
plt.show(block=False)

while True:
    line = ser.readline() # read a byte
    if line:
        string = line.decode() # convert the byte string to a unicode string
        #num = re.findall(r"[-+]?\d*\.\d+|\d+", string)
        num = float(string)
        end = time.time()
        y.append(num)
        time_elapsed= end - start
        x.append(time_elapsed)
        plt.cla()
        plt.plot(x, y, 'red')
        plt.pause(0.05) 
        plt.draw()