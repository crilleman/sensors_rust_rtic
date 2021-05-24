import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial

# initialize serial port
ser = serial.Serial()
ser.port = '/dev/ttyACM0'
ser.baudrate = 115200
ser.timeout = 20  # specify timeout when using readline()
ser.open()
ser.flush()

if ser.is_open == True:
    print("\nAll right, serial port now open. Configuration:\n")
    print(ser, "\n")  # print serial parameters
else:
    exit(1)

# Parameters
x_len = 100         # Number of points to display
y_range = [0, 35000]  # Range of possible Y values to display
# Create figure for plotting
fig = plt.figure(1)
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, x_len))
ys = [0] * x_len
ax.set_ylim(y_range)
# Add labels
plt.title('VOC(SRAW) over Time')
plt.xlabel('Samples')
plt.ylabel('SRAW ')

# Parameters
x_len2 = 100         # Number of points to display
y_range2 = [0, 1]  # Range of possible Y values to display
# Create figure for plotting
fig2 = plt.figure(2)
ax2 = fig2.add_subplot(1, 1, 1)
xs2 = list(range(0, x_len2))
ys2 = [0] * x_len2
ax2.set_ylim(y_range2)
# Add labels
plt.title('Sound pressure (Pa) over Time')
plt.xlabel('Samples')
plt.ylabel('Pa ')

# Parameters
x_len3 = 100         # Number of points to display
y_range3 = [0, 35]  # Range of possible Y values to display
# Create figure for plotting
fig3 = plt.figure(3)
ax3 = fig3.add_subplot(1, 1, 1)
xs3 = list(range(0, x_len3))
ys3 = [0] * x_len3
ax3.set_ylim(y_range3)
# Add labels
plt.title('Temperature over Time')
plt.xlabel('Samples')
plt.ylabel('Temperature (°C)')


# Create a blank line. We will update the line in animate
line, = ax.plot(xs, ys)
line2, = ax2.plot(xs2, ys2)
line3, = ax3.plot(xs3, ys3)

# This function is called periodically from FuncAnimation
def animate2(i, ys2):

    # Read temperature (Celsius) from TMP102
    #temp_c = round(tmp102.read_temp(), 2)
    ser_bytes = ser.readline()
    while ser_bytes != b'MIC\n':
        ser_bytes = ser.readline()

    #parse string found, read data
    ser_bytes = ser.readline()
    #print(ser_bytes)
    decoded_bytes = float(ser_bytes[0:len(ser_bytes)].decode("utf-8"))
    #print(decoded_bytes)

    # Add y to list
    ys2.append(decoded_bytes)

    # Limit y list to set number of items
    ys2 = ys2[-x_len2:]

    # Update line with new Y values
    line2.set_ydata(ys2)

    return line2,
# Set up plot to call animate() function periodically
ani2 = animation.FuncAnimation(fig2,
    animate2,
    fargs=(ys2,),
    interval=10,
    blit=True)

# This function is called periodically from FuncAnimation
def animate(i, ys):

    # Read temperature (Celsius) from TMP102
    #temp_c = round(tmp102.read_temp(), 2)

    ser_bytes = ser.readline()
    while ser_bytes != b'AIR\n':
        ser_bytes = ser.readline()
    # parse string found, read data
    ser_bytes = ser.readline()

    decoded_bytes = int(ser_bytes[0:len(ser_bytes)].decode("utf-8"))
    #print(decoded_bytes)

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
    interval=500,
    blit=True)


# This function is called periodically from FuncAnimation
def animate3(i, ys3):
    # Read temperature (Celsius) from TMP102
    #temp_c = round(tmp102.read_temp(), 2)
    ser_bytes = ser.readline()
    while ser_bytes != b'TMP\n':
        ser_bytes = ser.readline()
    #parse string found, read data
    ser_bytes = ser.readline()
    #print(ser_bytes)
    decoded_bytes = float(ser_bytes[0:len(ser_bytes)].decode("utf-8"))
    #print(decoded_bytes)
    # Add y to list
    ys3.append(decoded_bytes)
    # Limit y list to set number of items
    ys3 = ys3[-x_len3:]
    # Update line with new Y values
    line3.set_ydata(ys3)
    return line3,
# Set up plot to call animate() function periodically
ani2 = animation.FuncAnimation(fig3,
    animate3,
    fargs=(ys3,),
    interval=500,
    blit=True)
plt.show()
