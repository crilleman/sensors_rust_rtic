import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial

# initialize serial port
ser = serial.Serial()
ser.port = '/dev/ttyACM0'
ser.baudrate = 115200
ser.timeout = 100  # specify timeout when using readline()
ser.open()

ser.flush()

if ser.is_open == True:
    print("\nAll right, serial port now open. Configuration:\n")
    print(ser, "\n")  # print serial parameters
else:
    exit(1)

# Parameters
x_len = 1000         # Number of points to display
y_range = [0, 1.4]  # Range of possible Y values to display

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
plt.title('Sound pressure over Time')
plt.xlabel('Samples')
plt.ylabel('Sound pressure (Pa)')

# This function is called periodically from FuncAnimation
def animate(i, ys):

    # Read temperature (Celsius) from TMP102
    #temp_c = round(tmp102.read_temp(), 2)
    ser_bytes = ser.readline()
    #print(ser_bytes)
    decoded_bytes = float(ser_bytes[0:len(ser_bytes)].decode("utf-8"))
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
    fargs=(ys,),
    interval=50,
    blit=True)
plt.show()
