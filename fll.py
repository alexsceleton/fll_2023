# LEGO type:standard slot:1 
# autostart
from spike import PrimeHub, MotorPair, Motor, ColorSensor, LightMatrix
from spike.control import Timer
from time import sleep

manipulator = Motor('E')
manipulator.set_default_speed(100)
manipulator.set_stop_action('brake')
manipulator_11 = Motor('F')
manipulator_11.set_default_speed(5)
manipulator_11.set_stop_action('brake')




OPEN_POSITION = 335
CLOSE_POSITION = 220
CLOCK = 'clockwise'
CTRL_CLOCK = 'counterclockwise'

AVG = 60 # Значение серого
PWR = 80 # Мощность
G = 0.37 # Коэффицент
K = 1.7
def down():
    manipulator.run_to_position(CLOSE_POSITION, CTRL_CLOCK, 30)

def up():
    manipulator.run_to_position(OPEN_POSITION, CLOCK)

timer = Timer()
timer.reset()
hub = PrimeHub()
hub.light_matrix.show_image('HAPPY')
drive = MotorPair('C', 'D')
drive.set_motor_rotation(17.6)
drive.set_default_speed(40)
drive.set_stop_action('brake')

def right():
    drive.move(8.5, steering=100)

def left():
    drive.move(8.5, steering=-100)

def a_line(amount=None, black=None, power=PWR, g=G, k=K):
    hub.light_matrix.write('A')
    Motor('D').set_degrees_counted(0)
    while True:
        if black:
            if ColorSensor('B').get_color()=='black':
                break
        if amount:
            d = Motor('D').get_degrees_counted()
            x = d / 360 * 17.6
            if x >= amount:
                break
        current = ColorSensor('A').get_reflected_light()
        diff = AVG - current
        f = min(k*abs(diff), 50)
        r = int(power - f + g*(diff))
        l = int(power - f - g*(diff))
        drive.start_tank_at_power(l, r)
        #print('A line:', l, r)
    drive.stop()
    hub.light_matrix.write('X')

def b_line(amount=None, black=None, power=PWR, g=G, k=K):
    hub.light_matrix.write('B')
    Motor('D').set_degrees_counted(0)
    while True:
        if black:
            if ColorSensor('A').get_color()=='black':
                break
        if amount:
            d = Motor('D').get_degrees_counted()
            x = d / 360 * 17.6
            if x >= amount:
                break
        current = ColorSensor('B').get_reflected_light()
        diff = AVG - current
        f = min(k*abs(diff), 50)
        r = int(power - f - g*(diff))
        l = int(power - f + g*(diff))
        drive.start_tank_at_power(l, r)
        #print('B line:', l, r)
    drive.stop()
    hub.light_matrix.write('X')

def mission_6():
    '''
    гибридный автомабиль
    '''
    drive.move(21)
    a_line(23)
    drive.move(6, steering=100)
    drive.move(10)
    manipulator.run_to_position(302)
    down()
    print('Elapsed time:', timer.now())

def mission_2_1():
    '''
    нефтяная платформа
    '''
    drive.move(3)
    a_line(25)
    a_line(black=True)
    down()
    drive.move(6, steering=-100)
    for r in range(0, 4):
        manipulator.run_to_position(270, CLOCK, 100)
        down()
    drive.move(6, steering=100)
    print('Elapsed time m2: ', timer.now())

def mission_8():
    '''
    просмотр телевизора
    '''
    down()
    drive.move(10)
    drive.move(-10)
    up()
    print('Elapsed time m8: ', timer.now())

def mission_13():
    '''
    фабрика игрушек
    '''
    manipulator.run_to_position(230, CLOCK, 100)
    drive.move(4)
    manipulator.run_to_position(240, CLOCK, 100)
    sleep(1)
    drive.move(-4)
    up()
    drive.move(2.5)
    drive.move(6, steering=100)
    print('Elapsed time m13:', timer.now())

def mission_5():
    '''
    умная сеть(розетка, вилка)
    '''
    a_line(40)
    a_line(black=True)
    drive.move(5)
    left()
    drive.move(-4)
    down()
    drive.move(-3)
    up()
    drive.move(9)
    right()
    drive.move(1)
    print('Elapsed time m5:', timer.now())

def mission_9():
    '''
    Электростанция
    '''
    drive.move(3)
    a_line(42)
    a_line(black=True, power=75)
    drive.move(-3.5)
    left()
    down()
    drive.move(5)
    manipulator.run_to_position(255, CLOCK)
    drive.move(3)
    manipulator.run_to_position(263, CLOCK)
    drive.move(9)
    #drive.move(-11)
    up()
    drive.move(4)
    drive.move(9, steering=100)
    drive.move(-8)
    down()
    drive.move(150, speed=100 )
    print('Elapsed time m9:', timer.now())

def mission_4():
    '''
    солнечная ферма(3 энэргетических элемента около энэргохранилища)
    '''
    a_line(black=True)
    drive.move(4)
    left()
    drive.move(10)
    down()
    drive.move(-22)
    drive.move(4.25, speed=25, steering=100)
    manipulator.run_to_position(235)
    drive.move(30)
    down()
    drive.move(-10)
    drive.move(10, steering=100)
    drive.move(100, speed=100)

def mission_3_1():
    '''
    энэргохранилище(три элемента)
    '''
    manipulator.stop()
    drive.move(3)
    a_line(42)
    sleep(0.3)
    a_line(black=True)
    drive.move(2)
    right()
    a_line(5)
    drive.move(25)
    a_line(black=True)
    drive.move(3)
    right()
    a_line(black=True)
    left()
    drive.move(2.5)
    drive.move(4.25, steering=100)
    manipulator.run_to_position(240, CTRL_CLOCK, 30)
    up()
    drive.move(4.25, steering=100)
    drive.move(-10)
    a_line(black=True)
    print('Elapsed time m3:', timer.now())

def mission_7():
    '''
    ветряная турбина
    '''
    drive.move(44)
    drive.move(4.25, steering=-100)
    drive.move(-4.5)
    manipulator.run_to_position(225, CTRL_CLOCK, 30)
    for d in range(1, 5):
        drive.move(7)
        drive.move(-7)
    drive.move(1)
    manipulator.run_to_position(230, CLOCK, 30)
    drive.move(-3.5)
    down()

def mission_14():
    '''
    aкамуляторная батарея
    '''
    drive.move(5)
    drive.move(13, steering=-100)
    drive.move(39)
    drive.start(-100, 30)
    # while True:
    #     if ColorSensor('B').get_color()=='black':
    #         break
    drive.stop()
    b_line(black=True)
    drive.move(5)
    b_line(35, power=60)
    drive.move(4.25, steering=100)
    drive.move(3)
    up()
    drive.move(-3)
    drive.move(12.75, steering=100)


def mission_3_2():
    '''
    энэргохранилище(ящик)
    '''
    a_line(black=True)
    drive.move(5)
    a_line(black=True)
    left()
    drive.move(2)
    drive.move(4.25, steering=100)
    drive.move(-1.8)
    manipulator.run_to_position(220, CTRL_CLOCK, 30)
    drive.move(-7)
    drive.move(3, steering=100)
    drive.move(20)
    drive.move(6.5, steering=100)
    drive.move(60)

def mission_15_right():
    '''
    домики(справо)
    '''
    drive.move(15, speed=100)
    up()
    

def mission_10_1():
    '''
    водохранилище(ближний водный элемент)
    '''
    down()
    drive.move(-20)

def mission_10_2():
    '''
    водохранилище(два дальнихэлемента)
    '''
    drive.move(3)
    a_line(42)
    a_line(black=True)
    drive.move(12.75, steering=100)
    drive.move(15)
    drive.move(4.25, steering=-100)
    down()
    drive.move(3, steering=100, speed=10)
    drive.move(3, steering=-100)
    up()
    drive.move(3, steering=100, speed=10)
    down()
    drive.move(-16)
    drive.move(8.5, steering=100)
    drive.move(20)
    drive.move(4.25, steering=100)

def mission_10_3():
    '''
    водохранилище(вешаем)
    '''
    drive.move(3)
    a_line(30, power=30)
    drive.move(30, steering=3)
    manipulator_11.run_to_position(210)
    drive.move(-7)
    manipulator_11.run_to_position(227)
    drive.move(10)
    manipulator_11.run_to_position(120)
    drive.move(-7)
    drive.move(8.5,steering=100)
    down()
    up()
    drive.move(5)
    drive.move(8.5, steering=-100)
    manipulator_11.run_to_position(120)
    drive.move(-58)

def mission_2_2():
    drive.move(-25)
    drive.move(45)    

def mission_2_3_and_12():
    '''
    грузовик и эн.б. в центр
    '''
    drive.move(-4.25, steering=100)
    drive.move(32)
    right()
    drive.move(22)

def mission_11():
    '''
    водная электростанция
    '''    
    manipulator.run_to_position(270)
    drive.move(20)
    up()
    drive.move(-25)
    sleep(2)
    drive.move(2)
    down()
    drive.move(-20)

def group_1():
    mission_2_1()
    mission_13()
    mission_5()
    mission_4()

def group_2():
    mission_3_1()
    mission_7()
    mission_14()
    mission_3_2()

def group_3():  
    mission_8()

def group_4():
    mission_11()
    sleep(4) 
    mission_15_right()  

def group_5():
    mission_9()    

def group_7():
    mission_6()
    mission_2_3_and_12()

group_1()
print('Elapsed time: ', timer.now())

# 6
# drive.move(3)
# a_line(42)
# a_line(black=True)
# drive.move(90)
# 7
# mission_6()
# 8
# mission_2_2()
# 9
#mission_15()
# 10
#mission_2_3_and_12()
# a_line(black=True, power=80, g=0.37, k=1.7)