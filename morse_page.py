from flask import Flask, request
from flask import render_template
import RPi.GPIO as GPIO 
from time import *

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("morse.html")

button1_pin = 15
button2_pin = 14 
count1= 0
count2= 0
red = 17
green= 27 
blue = 22
led=4
speed = 0.5 # 음과 음 사이 연주시간 설정 (0.5초)

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
GPIO.setup(18, GPIO.OUT)
# PWM 인스턴스 p를 만들고  GPIO 18번을 PWM 핀으로 설정, 주파수  = 100Hz
p = GPIO.PWM(18, 262) 

GPIO.output(red,0)
GPIO.output(green,0)
GPIO.output(blue,0)
GPIO.output(led,0)

word_morse= ''
word_eng= ''
word_eng_c=''
word_list=''
input_eng=''
output_eng=''
final_word=''
once = True

#모스 --> 알파벳 딕셔너리
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
#알파벳 --> 모스 딕셔너리
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

#모스부호를 입력받는 경우 사용하는 함수
@app.route("/merge_") 
def merge_(s):
    global word_morse
    word_morse = word_morse + s
#알파벳을 입력받는 경우 사용하는 함수
@app.route("/merge_e") 
def merge_e(s1):
    global word_eng
    word_eng = word_eng+ s1

#알파벳--> 모스부호 에서 출력되는 영어 문자열
@app.route("/merge_o") 
def merge_o(s1):
    global output_eng
    output_eng = output_eng+ s1

#입력받는 모스부호를 구분자'/'를 기준으로 나누는 함수
@app.route("/make_word") 
def make_word(word_m):
    global word_list
    word_list = word_m.split('/')

strErrorState= "There is not incorrect Morsecode"
strError= False

#입력받는 모스부호를 morse_eng 딕셔너리에서 매칭시키고 merge하는 함수
@app.route("/word_view") 
def word_view():
    global final_word
    global word_morse
    global word_list
    global morse_eng
    global word_eng
    global strError

    make_word(word_morse)

    try:
        for i in range(len(word_list)-1):
            merge_e(morse_eng[word_list[i]])
    except KeyError:
        strError= True

#   print("wordng= "+ word_eng)
    final_word=word_eng

#모스 --> 알파벳 번역 후 LED 점멸과 Buzzer 소리를 실행시키는 함수 
@app.route("/play") 
def play():
    global output_eng
    global p
    global speed
    
    for i in range(len(output_eng)-1):
        print(output_eng[i])
        sleep(0.3)
        p.ChangeFrequency(262)
        if output_eng[i]=='.':
            GPIO.output(led,1)
            p.start(10)
            
            sleep(0.5)
            
            GPIO.output(led,0)
            p.stop()  
        elif output_eng[i]=='-':
            GPIO.output(led,1)
            p.start(10)

            sleep(1.5)
            
            GPIO.output(led,0)
            p.stop()  
        elif output_eng[i] == '/':
            sleep(1.5) 
        else:
            sleep(0)

    return str("ok")

# 단신호 입력 시 RGB LED에서 BLUE 점등
@app.route("/blueLight")
def blueLight():
    GPIO.output(blue,1)
    sleep(0.2)
    GPIO.output(blue,0)

# 장신호 입력 시 RGB LED에서 GREEN 점등
@app.route("/greenLight")
def greenLight():
    GPIO.output(green,1)
    sleep(0.2)
    GPIO.output(green,0)

# 구분자 신호 입력 시 RGB LED에서 RED 점등
@app.route("/redLight")
def redLight():
    GPIO.output(red,1)
    sleep(0.2)
    GPIO.output(red,0)

# push button을 통해 모스부호를 입력받는 함수
try:
    @app.route("/inputMode")
    def inputMode():
        global count1
        global count2
        global word_morse
        count1= 0
        count2= 0
        word_morse= ''
        isExit = 0

        while 1:  #무한반복 
            if GPIO.input(button1_pin) == GPIO.HIGH:
                sleep(0.2)
                count1+=1
                sleep(0.2)
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
                sleep(0.2)
                count2+=1
                sleep(0.1)
            if GPIO.input(button2_pin) == GPIO.LOW:
                if(count2>=1):
                    merge_("/")
                    redLight() 
                count2=0
                
            if ('//' in word_morse):
                isExit+=1
                if(isExit == 1):
                    redLight()
                    print(" 끝! ")

            sleep(0.1)    # 0.3초 딜레이 
        word_view()
except :
    pass

#모스부호를 입력받은 후 딕셔너리에서 매칭시켜 완성한 알파벳을 다시 웹으로 전송하는 코드
@app.route('/sub_Mor', methods=['POST','GET'])                       # index.html에서 이 주소를 접속하여 해당 함수를 실행
def sub_Mor():
    if request.method == 'POST':
        print("post conversion")
        pass

    elif request.method=='GET':
        global word_morse
        global final_word
        global strErrorState
        word_view()

        word_morse2= word_morse
        final_word2=final_word
        word_morse=''
        final_word=''

        if(strError == False):
            return render_template('morse.html', nata=str(word_morse2), mata= str(final_word2))
        elif(strError):
            return render_template('morse.html', nata = str(word_morse2), mata= str(strErrorState))

#알파벳을 입력받은 후 딕셔너리에서 매칭시켜 완성한 모스부호를 다시 웹으로 전송하는 코드
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

        try:
            for i in range(len(list1)):
                output_eng = output_eng+ (eng_morse[list1[i].upper()])+'/'
        except KeyError:
            output_eng=" Sorry ! Only support for Alphabet. "
        
        print("입력받은 알파벳 : "+ input_eng)
        print("매칭된 모스부호 : " + output_eng)

    return render_template('morse.html', data=str(output_eng))


if __name__ == "__main__":
    app.run(host="0.0.0.0")