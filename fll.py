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
PWR = 50 # Мощность
G = 0.5 # Коэффицент


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
drive.set_default_speed(30)
drive.set_stop_action('brake')

def right():
    drive.move(8.5, steering=100)

def left():
    drive.move(8.5, steering=-100)

def a_line(amount=None, black=None, power=PWR):
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
        r = int(power + G*(AVG - current))
        l = int(power - G*(AVG - current))
        drive.start_tank_at_power(l, r)
    drive.stop()
    hub.light_matrix.write('X')

def b_line(amount=None, black=None):
    hub.light_matrix.write('b')
    Motor('D').set_degrees_counted(0)
    while True:
        if black:
            if ColorSensor('A').get_color()=='black':
                break
        if amount:
            c = Motor('D').get_degrees_counted()
            x = c / 360 * 17.6
            if x >= amount:
                break
        current = ColorSensor('B').get_reflected_light()
        r = int(PWR + G*(AVG - current))
        l = int(PWR - G*(AVG - current))
        drive.start_tank_at_power(r, l)
    drive.stop()
    hub.light_matrix.write('X')

def mission_6():
    '''
    гибридный автомабиль
    '''
    drive.move(2)
    a_line(amount=23)
    down()
    drive.move(6, steering=100)
    drive.move(10)
    up()
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
        manipulator.run_to_position(255, CLOCK, 100)
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
    manipulator.run_to_position(227, CLOCK, 100)
    drive.move(4)
    manipulator.run_to_position(237, CLOCK, 100)
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
    a_line(amount=40)
    a_line(black=True)
    drive.move(6)
    left()
    drive.move(-2)
    down()
    drive.move(-5)
    up()
    drive.move(9)
    right()
    print('Elapsed time m5:', timer.now())

def mission_9():
    '''
    Электростанция
    '''
    drive.move(3)
    a_line(42)
    a_line(black=True)
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
    drive.move(4.5, steering=100)
    manipulator.run_to_position(235)
    drive.move(30)
    down()
    drive.move(-10)
    drive.move(10, steering=100)
    drive.move(100)

def mission_3_1():
    '''
    энэргохранилище(три элемента)
    '''
    drive.move(3)
    a_line(42)
    a_line(black=True)
    drive.move(2)
    right()
    a_line(5)
    drive.move(30)
    a_line(black=True)
    drive.move(3)
    right()
    a_line(black=True)
    left()
    drive.move(2)
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
    drive.move(7)
    drive.move(13, steering=-100)
    drive.move(39)
    drive.start(-100, 30)
    while True:
        if ColorSensor('B').get_color()=='black':
            break
    drive.stop()
    b_line(black=True)
    drive.move(5)
    b_line(35)
    drive.move(4.25, steering=100)
    drive.move(3)

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
    drive.move(2, steering=100)
    drive.move(20)
    drive.move(6.5, steering=100)

def mission_15():
    '''
    домики
    '''
    drive.move(30)
    up()
    drive.move(-15)

def mission_11_1():
    '''
    водохранилище(ближний водный элемент)
    '''
    down()
    drive.move(-20)

def mission_11_2():
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

def mission_11_3():
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
    down()
    up()
    drive.move(5)
    drive.move(12.75, steering=-100)
    manipulator_11.run_to_position(120)
    drive.move(-58)

def mission_2_2_and_12():
    '''
    грузовик и в центр
    '''
    drive.move(20)
    a_line(black=True)
    drive.move(2)
    right()
    a_line(amount=30)
    drive.move(4.25, steering=100)
    drive.move(20)

mission_2_2_and_12()
