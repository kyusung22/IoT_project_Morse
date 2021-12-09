#-*-coding:utf-8-*-

# 필요한 라이브러리를 불러옵니다. 
import RPi_I2C_driver
import RPi.GPIO as GPIO 
from time import *

# 사용할 GPIO 핀의 번호를 선정합니다.
button1_pin = 15
button2_pin = 14 
count= 0
count2=0
red = 17
green= 27 
blue = 22

# 불필요한 warning 제거
GPIO.setwarnings(False) 
# GPIO핀의 번호 모드 설정
GPIO.setmode(GPIO.BCM) 

# 버튼 핀의 입력설정 , PULL DOWN 설정 
GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(button2_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(red,GPIO.OUT)
GPIO.setup(green,GPIO.OUT)
GPIO.setup(blue,GPIO.OUT)

GPIO.output(red,0)
GPIO.output(green,0)
GPIO.output(blue,0)

lcd = RPi_I2C_driver.lcd(0x27)

# Turn on the cursor:
lcd.cursor()

word_morse= ''
word_eng= ''
word_eng_c=''
word_list=''
once = True

morse_eng = {
    '.-'   : 'A',
	'-...' : 'B',
	'-.-.' : 'C',
	'-..'  : 'D',
	'.'    : 'E',
	'..-.' : 'F',
	'--.'  : 'G',
	'....' : 'H',
	'..'   : 'I',
	'.---' : 'J',
    '-.-'  : 'K',
	'.-..' : 'L',
	'--'   : 'M',
	'-.'   : 'N',
	'---'  : 'O',
	'.--.' : 'P',
	'--.-' : 'Q',
	'.-.'  : 'R',
	'...'  : 'S',
	'-'    : 'T',
	'..-'  : 'U',
	'...-' : 'V',
	'.--'  : 'W',
	'-..-' : 'X',
	'-.--' : 'Y',
	'--..' : 'Z',
    '.....' : ' ' 
}
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def merge_(s):
    global word_morse
    word_morse = word_morse + s

def merge_e(s1):
    global word_eng
    word_eng = word_eng+ s1

def merge_e_c(s1):
    global word_eng_c
    word_eng_c=word_eng_c+s1
   #  print(word_eng_c)

def merge_e_c_toNULL():
    global word_eng_c
    word_eng_c=''

def make_word(word_m):
    global word_list
    word_list = word_m.split('/')
    print(word_list)

def word_view():
    make_word(word_morse)

    try:
        for i in range(len(word_list)-2):
            merge_e(morse_eng[word_list[i]])
    except KeyError:
        print("Invalid Morsecode included.1111111111111")

    print("result = " + word_eng)

def word_view_while():
    global word_eng_c
    make_word(word_morse)

    try:
        for i in range(len(word_list)-1):
            merge_e_c(morse_eng[word_list[i]])
    except KeyError:
        pass

    lcd.clear()
    lcd.print(word_eng_c)
    

    merge_e_c_toNULL()
# def button2_callback(channel):
#     merge_("/")
#     print("" + word_morse)

def blueLight():
    GPIO.output(blue,1)
    sleep(0.2)
    GPIO.output(blue,0)

def greenLight():
    GPIO.output(green,1)
    sleep(0.2)
    GPIO.output(green,0)

def redLight():
    GPIO.output(red,1)
    sleep(0.2)
    GPIO.output(red,0)

def yelLight():
    GPIO.output(red,1)
    GPIO.output(green,1)
    sleep(0.2)
    GPIO.output(red,0)
    GPIO.output(green,0)

def lcd_short():
    lcd.print("short push") #short push.
    sleep(1)
    lcd.clear()

def lcd_long():
    lcd.print("long push") #short push.
    sleep(1)
    lcd.clear()

    


while 1:  #무한반복 
    
    # 만약 버튼핀에 High(1) 신호가 들어오면, "Button pushed!" 을 출력합니다.
    if GPIO.input(button1_pin) == GPIO.HIGH:
        count+=1

    if GPIO.input(button1_pin) == GPIO.LOW:
        if(count==1):       
            blueLight()
            merge_(".")
            print("" + word_morse)
            #lcd_short()    #들어가면 속도가 현저히 느려짐

        elif (count>=2):
            greenLight()
            merge_("-")
            print("" + word_morse)
            #lcd_long()

        count=0

    if GPIO.input(button2_pin) == GPIO.HIGH:
        count2+=1
    if GPIO.input(button2_pin) == GPIO.LOW:
        
        if(count2>=1):
            merge_("/")
            yelLight()      #노란색 불 내는 법 알아보기
            word_view_while()
            # 버튼2 푸쉬 시 마다 글자가 나오게 하려면 ? --> 글자가 한번에가 아닌 그때마다 완성되어야 함
            print("" + word_morse)

        count2=0
            
    if ('//' in word_morse):
            redLight()
            print(" 끝! ")
            break

    sleep(0.2)    # 0.3초 딜레이 

word_view()