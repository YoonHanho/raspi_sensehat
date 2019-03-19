from sense_hat import SenseHat
import time

import requests
from bs4 import BeautifulSoup

sense = SenseHat()

#sense.clear()         # 초기화 #sense.clear((0,0,0))
sense.set_rotation(180)   # 0,90,180,270 rotation
sense.low_light=True       #  밝기 낮춘다. 원상태로 하려면 False


red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
yellow = (255, 255, 0)

magenta = (255, 0, 255)
cyan = (0, 255, 255)
white = (255,255,255)
nothing = (0,0,0)      # icon 코드에서 씀
pink = (255,105, 180)


########### 1. 주가
# 스크래핑 코드
index_dict = {'KOSPI': 'https://finance.naver.com/sise/sise_index.nhn?code=KOSPI',
              'KOSDAQ':'https://finance.naver.com/sise/sise_index.nhn?code=KOSDAQ',
              'S&P500':'https://finance.naver.com/world/sise.nhn?symbol=SPI@SPX',
              'NI225': 'https://finance.naver.com/world/sise.nhn?symbol=SHS@000001',
              'HSI':   'https://finance.naver.com/world/sise.nhn?symbol=HSI@HSI',
              'SSE':   'https://finance.naver.com/world/sise.nhn?symbol=SHS@000001',
              'DAX':   'https://finance.naver.com/world/sise.nhn?symbol=XTR@DAX30',
              'FTSE':  'https://finance.naver.com/world/sise.nhn?symbol=LNS@FTSE100'}

def make_index(index_name, url):
    """
    return :
      1. 요청한 지수별로 등락, 등락율
      2. 상승과 하락시 글자색을 빨간색, 파란색을 주기 위해, 등락부호를 함께 리턴한다.
    """
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    if index_name in ['KOSPI', 'KOSDAQ']: # 국내지수 
        price = soup.select_one('div#quotient > em').text
        t = soup.select_one('div#quotient > span').text
        up_point, up_percent = t.split()
        up_percent = up_percent[:-2]
    else:   # 해외지수는 국내지수와 HTML이 틀림
        price = soup.select('#content > div.rate_info > div.today > p.no_today > em')[0].text.strip()
        up_point = soup.select('#content > div.rate_info > div.today > p.no_exday > em')[0].text.strip()
        up_percent = soup.select('#content > div.rate_info > div.today > p.no_exday > em')[1].text.strip().replace('\n','')[1:-1]

    up_point = up_percent[0] + up_point  # 주가 상승값에 +- 부호 붙여주기

    #print(index_name, price, up_point, up_percent)
    script = ' '.join([index_name, price, up_point, up_percent])
    return up_percent[0], script

def show_stockprice():
    """ 주가가 상승이면 red, 하락이면 blue 주기 """
    for i, u in index_dict.items():
        up_down, script = make_index(i, u)
        text_colour = red if up_down == '+' else blue
        sense.show_message(script, text_colour=text_colour, back_colour=black, scroll_speed=0.05)             
        time.sleep(1)    
    """
    sense_script = [['KOSPI +3.1 +0.01%', red, black],
                ['DOW -10.1 -0.11%', blue, black]]

    for script, text_colour, back_colour in sense_script:
        # print(a,b,c) 
        sense.show_message(script, text_colour=text_colour, back_colour=back_colour, scroll_speed=0.05)    
    """    
        
########### 2. 팀 소개        
def show_introteam():
    sense.show_message("Hello Bigdata Team!", text_colour=blue, back_colour=black, scroll_speed=0.05)
        

########### 3. 시계
def show_timer():

    number = [
    [[0,1,1,1], # Zero
    [0,1,0,1],
    [0,1,0,1],
    [0,1,1,1]],
    [[0,0,1,0], # One
    [0,1,1,0],
    [0,0,1,0],
    [0,1,1,1]],
    [[0,1,1,1], # Two
    [0,0,1,1],
    [0,1,1,0],
    [0,1,1,1]],
    [[0,1,1,1], # Three
    [0,0,1,1],
    [0,0,1,1],
    [0,1,1,1]],
    [[0,1,0,1], # Four
    [0,1,1,1],
    [0,0,0,1],
    [0,0,0,1]],
    [[0,1,1,1], # Five
    [0,1,1,0],
    [0,0,1,1],
    [0,1,1,1]],
    [[0,1,0,0], # Six
    [0,1,1,1],
    [0,1,0,1],
    [0,1,1,1]],
    [[0,1,1,1], # Seven
    [0,0,0,1],
    [0,0,1,0],
    [0,1,0,0]],
    [[0,1,1,1], # Eight
    [0,1,1,1],
    [0,1,1,1],
    [0,1,1,1]],
    [[0,1,1,1], # Nine
    [0,1,0,1],
    [0,1,1,1],
    [0,0,0,1]]
    ]
    noNumber = [0,0,0,0]

    hourColor = [255,0,0] # Red
    minuteColor = [0,255,255] # Cyan
    empty = [0,0,0] # Black/Off

    clockImage = []

    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min

    for index in range(0, 4):
        if (hour >= 10):
            clockImage.extend(number[int(hour/10)][index])
        else:
            clockImage.extend(noNumber)
        clockImage.extend(number[int(hour%10)][index])

    for index in range(0, 4):
        clockImage.extend(number[int(minute/10)][index])
        clockImage.extend(number[int(minute%10)][index])

    for index in range(0, 64):
        if (clockImage[index]):
            if index < 32:
                clockImage[index] = hourColor
            else:
                clockImage[index] = minuteColor
        else:
            clockImage[index] = empty

    #sense.set_rotation(90) # Optional
    #sense.low_light = True # Optional
    sense.set_pixels(clockImage)

################ 3-1. 시계 텍스트 형 ---------> 이거 더 보기 깔끔하다    
def show_timetext():
    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min
    if hour > 12:
        script = "It's {0}:{1} p.m.".format(hour-12, str(minute).rjust(2,'0'))
    else:
        script = "It's {0}:{1} a.m.".format(hour, str(minute).rjust(2,'0'))    
    sense.show_message(script, text_colour=yellow, back_colour=black, scroll_speed=0.05)    
    
############### 4.1 아이콘
def show_icons():
    #sense.low_light = True # Optional

    def trinket_logo():
        G = green
        Y = yellow
        B = blue
        O = nothing
        logo = [
        O, O, O, O, O, O, O, O,
        O, Y, Y, Y, B, G, O, O,
        Y, Y, Y, Y, Y, B, G, O,
        Y, Y, Y, Y, Y, B, G, O,
        Y, Y, Y, Y, Y, B, G, O,
        Y, Y, Y, Y, Y, B, G, O,
        O, Y, Y, Y, B, G, O, O,
        O, O, O, O, O, O, O, O,
        ]
        return logo

    def raspi_logo():
        G = green
        R = red
        O = nothing
        logo = [
        O, G, G, O, O, G, G, O, 
        O, O, G, G, G, G, O, O,
        O, O, R, R, R, R, O, O, 
        O, R, R, R, R, R, R, O,
        R, R, R, R, R, R, R, R,
        R, R, R, R, R, R, R, R,
        O, R, R, R, R, R, R, O,
        O, O, R, R, R, R, O, O,
        ]
        return logo

    def plus():
        W = white
        O = nothing
        logo = [
        O, O, O, O, O, O, O, O, 
        O, O, O, W, W, O, O, O,
        O, O, O, W, W, O, O, O, 
        O, W, W, W, W, W, W, O,
        O, W, W, W, W, W, W, O,
        O, O, O, W, W, O, O, O,
        O, O, O, W, W, O, O, O,
        O, O, O, O, O, O, O, O,
        ]
        return logo

    def equals():
        W = white
        O = nothing
        logo = [
        O, O, O, O, O, O, O, O, 
        O, W, W, W, W, W, W, O,
        O, W, W, W, W, W, W, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, W, W, W, W, W, W, O,
        O, W, W, W, W, W, W, O,
        O, O, O, O, O, O, O, O,
        ]
        return logo

    def heart():
        P = pink
        O = nothing
        logo = [
        O, O, O, O, O, O, O, O,
        O, P, P, O, P, P, O, O,
        P, P, P, P, P, P, P, O,
        P, P, P, P, P, P, P, O,
        O, P, P, P, P, P, O, O,
        O, O, P, P, P, O, O, O,
        O, O, O, P, O, O, O, O,
        O, O, O, O, O, O, O, O,
        ]
        return logo

    images = [trinket_logo, trinket_logo, plus, raspi_logo, raspi_logo, equals, heart, heart]
    count = 0

    while True:
        sense.set_pixels(images[count % len(images)]())
        time.sleep(.75)
        count += 1
        if count > 20:
            break
    
    
########## 5. 습도 
# 온도는 정확하지 않음
# 추후 습도 상태 설명 : 양호(good, dry, ...)
def show_humid():
	humidity = sense.get_humidity()
	if humidity <40:
		script = "humidity is {0:,.0f}%. {1}".format(humidity, "Dry, Dry")     
		text_colour = yellow
	elif humidity >70:
		script = "humidity is {0:,.0f}%. {1}".format(humidity, "Damp, Damp")     
		text_colour = red
	else:
		script = "humidity is {0:,.0f}%. {1}".format(humidity, "Moderate Humidity")          
		text_colour = green
	sense.show_message(script, text_colour=yellow, back_colour=black, scroll_speed=0.075)  # 속도 약간 늦춰줌

    
if __name__ == "__main__":

	count = 0
	while True:
		show_stockprice()
		show_introteam()
		time.sleep(1)
		show_timetext()
		show_timer()  # sleep 줘야 함
		time.sleep(2)
		show_icons()
		show_humid()		
		"""
		count += 1
		if count > 1:
			break			
		"""

	sense.clear()
