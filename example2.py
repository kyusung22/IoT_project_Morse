import RPi_I2C_driver
from time import *

# make custom characters - eleparts logo:
# https://maxpromer.github.io/LCD-Character-Creator/

##### START EXAMPLE #####
# RPi_I2C_driver.lcd( I2C address )
lcd = RPi_I2C_driver.lcd(0x27)

# Turn on the cursor:
lcd.cursor()

# Print a message to the LCD.
lcd.print("Hello")

sleep(1)

# At 0.5c second interval " World!!!" Print
lcd.print(" World!!!", 0.5)

sleep(2)

lcd.clear()

# Turn off the cursor:
lcd.noCursor()

lcd.print("eleparts")

# set the cursor position:
lcd.setCursor(5,1)
lcd.print(".co.kr")

lcd.setCursor(12,0)

# print 'createChar'
lcd.write(0)
lcd.write(1)
lcd.write(2)
lcd.write(3)

lcd.setCursor(12,1)

lcd.write(4)
lcd.write(5)
lcd.write(6)
lcd.write(7)

sleep(2)

lcd.setCursor(11,1)

# Turn on the blinking cursor:
lcd.blink()

sleep(3)

# screen moving
for a in range(2):

    for i in range(2):
        # Move the screen to the right
        lcd.scrollDisplayLeft()
        sleep(0.4)

    for i in range(4):
        # Move the screen to the right
        lcd.scrollDisplayRight()
        sleep(0.4)

    for i in range(2):
        # Move the screen to the right
        lcd.scrollDisplayLeft()
        sleep(0.4)