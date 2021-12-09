from flask import Flask, request
from flask import render_template
import RPi_I2C_driver
import RPi.GPIO as GPIO 
from time import *

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("morse.html")

button1_pin = 15
button2_pin = 14 
count1= 0
count2=0
red = 17
green= 27 
blue = 22
led=4

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
GPIO.setup(led,GPIO.OUT)

GPIO.output(red,0)
GPIO.output(green,0)
GPIO.output(blue,0)
GPIO.output(led,0)

lcd = RPi_I2C_driver.lcd(0x27)

# Turn on the cursor:
lcd.cursor()

word_morse= ''
word_eng= ''
word_eng_c=''
word_list=''
input_eng=''
output_eng=''
final_word=''
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

eng_morse = {
    'A'   : '.-'   ,
	'B' : '-...',
	'C' : '-.-.',
	'D'  : '-..',
	'E'    : '.',
	'F' : '..-.',
	'G'  : '--.',
	'H' : '....',
	'I'   : '..',
	'J' : '.---',
   	'K'  : '-.-',
	'L' : '.-..',
	'M'   : '--',
	'N'   : '-.',
	'O'  : '---',
	'P' : '.--.',
	'Q' : '--.-',
	'R'  : '.-.',
	'S'  : '...',
	'T'    : '-',
	'U'  : '..-',
	'V' : '...-',
	'W'  : '.--',
	'X' : '-..-',
	'Y' : '-.--',
	'Z' : '--..',
    	' ' : '.....' 
}
@app.route("/merge_") 
def merge_(s):
    global word_morse
    word_morse = word_morse + s

@app.route("/merge_e") 
def merge_e(s1):
    global word_eng
    word_eng = word_eng+ s1

@app.route("/merge_o") 
def merge_o(s1):
    global output_eng
    output_eng = output_eng+ s1

@app.route("/merge_e_c") 
def merge_e_c(s1):
    global word_eng_c
    word_eng_c=word_eng_c+s1
   #  print(word_eng_c)

@app.route("/merge_e_c_toNULL") 
def merge_e_c_toNULL():
    global word_eng_c
    word_eng_c=''

@app.route("/make_word") 
def make_word(word_m):
    global word_list
    word_list = word_m.split('/')
    #print("word list :  " + str(word_list))

@app.route("/word_view") 
def word_view():
    global final_word
    global word_morse
    global word_list
    global morse_eng
    global word_eng

    make_word(word_morse)

    try:
        for i in range(len(word_list)-1):
            merge_e(morse_eng[word_list[i]])
           # print("for loop inner : "+morse_eng[word_list[i]])
    except KeyError:
        print("Invalid Morsecode included.1111111111111")

    print("wordng= "+ word_eng)
    final_word=word_eng

@app.route("/word_view_while") 
def word_view_while():
    global word_eng_c
    global word_list
    global word_morse

    make_word(word_morse)

    try:
        for i in range(len(word_list)):
            merge_e_c(morse_eng[word_list[i]])
    except KeyError:
        pass

    lcd.clear()
    lcd.print(word_eng_c)
    
    merge_e_c_toNULL()

@app.route("/play") 
def play():
        global output_eng
        try:
            for i in range(len(output_eng)+1):
                print(output_eng[i])
                sleep(0.3)
                if output_eng[i]=='.':
                    GPIO.output(led,1)
                    sleep(0.5)
                    GPIO.output(led,0)
                elif output_eng[i]=='-':
                    GPIO.output(led,1)
                    sleep(1.5)
                    GPIO.output(led,0)
                elif output_eng[i] == '/':
                    sleep(1.5)
                else:
                    pass
        except IndexError:
            pass

@app.route("/blueLight")
def blueLight():
    GPIO.output(blue,1)
    sleep(0.2)
    GPIO.output(blue,0)

@app.route("/greenLight")
def greenLight():
    GPIO.output(green,1)
    sleep(0.2)
    GPIO.output(green,0)

@app.route("/redLight")
def redLight():
    GPIO.output(red,1)
    sleep(0.2)
    GPIO.output(red,0)

@app.route("/yelLight")
def yelLight():
    GPIO.output(red,1)
    sleep(0.2)
    GPIO.output(red,0)

@app.route("/inputMode")
def inputMode():
    global count1
    global count2
    global word_morse

    while 1:  #무한반복 
    # 만약 버튼핀에 High(1) 신호가 들어오면, "Button pushed!" 을 출력합니다.
        if GPIO.input(button1_pin) == GPIO.HIGH:
            count1+=1

        if GPIO.input(button1_pin) == GPIO.LOW:
            if(count1==1):       
                blueLight()
                merge_(".")
                print("" + word_morse)
                

            elif (count1>=2):
                greenLight()
                merge_("-")
                print("" + word_morse)

            count1=0

        if GPIO.input(button2_pin) == GPIO.HIGH:
            count2+=1
        if GPIO.input(button2_pin) == GPIO.LOW:
            if(count2>=1):
                merge_("/")
                yelLight() 
                word_view_while()
                # 버튼2 푸쉬 시 마다 글자가 나오게 하려면 ? --> 글자가 한번에가 아닌 그때마다 완성되어야 함

            count2=0
                
        if ('//' in word_morse):
                redLight()
                print(" 끝! ")
                break

        sleep(0.2)    # 0.3초 딜레이 

    word_view()

@app.route('/sub_Mor', methods=['POST','GET'])                       # index.html에서 이 주소를 접속하여 해당 함수를 실행
def sub_Mor():
    print("sub_mor")
    if request.method == 'POST':
        print("post conversion")
        pass

    elif request.method=='GET':
        global word_morse
        global final_word
        word_view()
        print("return = "+word_morse)
        print("word-english ? : "+final_word)
        word_morse2= word_morse
        final_word2=final_word
        word_morse=''
        final_word=''
        return render_template('morse.html', nata=str(word_morse2), mata= str(final_word2))

@app.route('/sub_Eng', methods=['POST','GET'])                       # index.html에서 이 주소를 접속하여 해당 함수를 실행
def sub_Eng():
    if request.method=='GET':
        temp=request.args.get('texta1')

        global input_eng
        global output_eng
        output_eng=''
        
        temp=str(temp)
        input_eng=temp
        list1= list(input_eng)

        for i in range(len(list1)):
            output_eng = output_eng+ (eng_morse[list1[i].upper()])+'/'

        print("@@ : "+ input_eng)
        print("##################" + output_eng)
    return render_template('morse.html', data=str(output_eng))

if __name__ == "__main__":
    app.run(host="0.0.0.0")