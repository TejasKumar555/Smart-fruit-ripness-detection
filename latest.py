import serial
import time
import schedule
import cv2
import numpy as np
import glob


def rgb_to_single(rgb):
    # convert each color channel to a decimal value between 0 and 1
    r = rgb[0] / 255.0
    g = rgb[1] / 255.0
    b = rgb[2] / 255.0
    # concatenate the decimal values into a single value
    dec = r * 0.3 + g * 0.59 + b * 0.11
    # scale the value and convert to an integer
    single = ((dec * 9))
    return single


def main_func():
    arduino = serial.Serial('COM11', 9600)
    print('Established serial connection to Arduino')
    arduino_data = arduino.readline()

    decoded_values = str(arduino_data[0:len(arduino_data)].decode("utf-8"))
    list_values = decoded_values.split('x')

    for item in list_values:
        list_in_floats.append(float(item))

    print(f'Collected readings from Arduino: {list_in_floats}')

    # Get the temperature value from the list_in_floats
    temperature = list_in_floats[0]


    # Load the image
    img = cv2.imread(r'C:\Users\OMEN\Desktop\el bananas\vikq.png')

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define the range of yellow color in HSV color space
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    # Threshold the HSV image to get only yellow colors
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Bitwise-AND the mask and original image
    res = cv2.bitwise_and(img, img, mask=mask)

    # Get the average color of the masked area
    avg_color_per_row = np.average(res, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)

    # Convert the average color from BGR to RGB
    avg_color = avg_color[::-1]

    # Display the RGB values
    print("RGB values:")
    int_list = avg_color
    str_list = [str(i) for i in int_list]
    result = ",".join(str_list)
    print(result)

    r = rgb_to_single(int_list)
    print(r)

    if temperature < 59:
        print("Fruit is not ripe")
    elif temperature >= 59 and temperature < 68:
        if r == 0:
            print("Fruit is not ripe")
        elif r>0 and r<=1:
            print("Fruit is Over-ripened")
        else:
            print("Fruit is ripe")
    else:
        if r == 0:
            print("Fruit is not ripe")
        elif r > 0 and r<=1:
            print("Fruit is Over-ripened")
        else:
            print("Fruit is ripe")
        #if r >= 0 and r <= 2:
           # print("Fruit is not ripe")
      #  elif r >= 3 and r <= 9:
          #  print("Fruit is ripe")

    arduino_data = 0
    list_in_floats.clear()
    list_values.clear()
    arduino.close()
    print('Connection closed')
    print('<----------------------------->')


# ----------------------------------------Main Code------------------------------------
# Declare variables to be used
list_values = []
list_in_floats = []

print('Program started')

# Setting up the Arduino
schedule.every(1).seconds.do(main_func)

while True:
    schedule.run_pending()
    time.sleep(1)