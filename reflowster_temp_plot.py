#import numpy as np
import matplotlib.pyplot as mp
#import time
import serial as sr
import math

# This program is a demonstration of live plotting -- I just use known data and
# cycle over it to demonstrate how to actually get the information plotted.


def main():
    
    #serial initialization
    ser = sr.Serial()
    ser.baudrate = 9600 #set baudrate
    ser.port = 'COM3'#set port name
    ser.close() #close serial port if left open
    ser.open()  #open serial port
    if ser.isOpen() :#check to make sure
        print(ser.name) #print name if port open
    
    
    # enable interactive plotting
    mp.ion()

    # arrays that will hold time and temperature data for the plot
    x = [0]
    T = [0]

    # create an empty plot
    p, = mp.plot(x, T)
    mp.title("Oven Temperature")
    mp.xlabel("Time (s)")
    mp.ylabel("Temperature (C)")
    # set the plot y limit, which we don't want to change
    mp.ylim((0.0,280.0))
    # Set an initial small x limit (this limit will change as we add data)
    mp.xlim((0.0,1.0))


    # Get the current axis object, we need it to update x scale
    ax = mp.gca()

    # This allows the program to quit if the window is closed (which would not
    # happen otherwise -- more GUI shennanigans)
    ax.figure.canvas.mpl_connect('close_event', window_close)

    # dummy vars to hold time change and temp data
    data = 0.0
    my_t = 0.0
    #list for holding temps
    #test_temps = [] 

    # Loop and plot data. Here you would have to perform a serial read and
    # interpret (use functions), and then plot new data if it exists.
    while(True):
        # Update plot data
        p.set_data(x, T)
        # Update x scale
        ax.relim()
        ax.autoscale(axis = 'x')
        # Redraw the plot now that it has new data
        mp.draw()
        # read serial for info + store value in temp
        try:
            data = float(((ser.readline()).decode())[0:(((ser.readline()).decode()).find(' ') - 1)])	
        # exception handler for nan
        except ValueError:
            print("string etc. that couldn't be converted to float")
        
        if (math.isnan(data)) is False : 
            if (T == []) : 
                T[-1] = data    # replace first element of y if not done
                x[-1] = my_t
                my_t += 1.0
                print(T, x)
            else:
                x.append(my_t) # add another x element to list
                T.append(data) # add data to list
                mp.xlim((0.0,my_t)) #expand xlim; redundant for first call
                my_t += 1.0    # Update tracking for the next round
                print(T[-1], x[-1])

            # print last set values
           
       
        # Following 3 lines not necessary b/c not reading through file
        #i = i + 1
        #if (i >= len(test_temps)):
        #    i = 0

        # Add new data to x and T     Moved up to NaN check
        #x.append(my_t)               
        #T.append(test_temps[i])
        
        # important! -- this pause allows matplotlib to actually draw the
        # figure. It is tied into the backend GUI event loop stuff. The time is
        # arbitrary, I'm using 1/100th of a second to show how fast it can
        # actually plot.
        mp.pause(1)
        mp.show()

# Event handler to quite program if someone closes the window
def window_close(event):
    exit()

if __name__ == '__main__':
    main()


