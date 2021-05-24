import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import datetime

# initialize serial port
ser = serial.Serial()
ser.port = '/dev/ttyACM0'
ser.baudrate = 115200
ser.timeout = 1100  # specify timeout when using readline()
ser.open()
ser.flush()

if ser.is_open == True:
    print("\nAll right, serial port now open. Configuration:\n")
    print(ser, "\n")  # print serial parameters
else:
    exit(1)

t_delta1 = []
t_delta2 = []
t_delta1.append(datetime.datetime.now())    # Time difference for the last 100 readings
t_delta2.append(datetime.datetime.now())    # Time difference for the last 100 readings
t_flag = 0



# Parameters
x_len = 10000         # Number of points to display
y_range = [20000, 35000]  # Range of possible Y values to display

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, x_len))
ys = [0] * x_len
ax.set_ylim(y_range)

# Initialize communication with TMP102
#tmp102.init()

# Create a blank line. We will update the line in animate
line, = ax.plot(xs, ys)

# Add labels
#plt.title('Temperature over Time')
plt.xlabel('Samples')
plt.ylabel('SRAW ')



# This function is called periodically from FuncAnimation
def animate(i, ys,):
    # Read temperature (Celsius) from TMP102
    #temp_c = round(tmp102.read_temp(), 2)
    ser_bytes = ser.readline()
    #print(ser_bytes)
    decoded_bytes = int(ser_bytes[0:len(ser_bytes)].decode("utf-8"))
    #print(decoded_bytes)
    #decoded_bytes = 11;

    # Add y to list
    ys.append(decoded_bytes)

    # Limit y list to set number of items
    ys = ys[-x_len:]

    # Update line with new Y values
    line.set_ydata(ys)

    return line,
# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig,
    animate,
    fargs=(ys, ),
    interval=100,
    blit=True)
plt.show()
