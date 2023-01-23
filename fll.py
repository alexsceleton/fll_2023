from spike import PrimeHub, MotorPair, Motor, ColorSensor, LightMatrix
from spike.control import Timer
from time import sleep

manipulator = Motor('E')
manipulator.set_default_speed(100)



OPEN_POSITION = 335
CLOSE_POSITION = 220
CLOCK = 'clockwise'
CTRL_CLOCK = 'counterclockwise'

AVG = 60 # Значение серого
PWR = 50 # Мощность
G = 0.6 # Коэффицент


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
drive.set_default_speed(100)
drive.set_stop_action('brake')

def a_line(amount=None, black=None):
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
        r = int(PWR + G*(AVG - current))
        l = int(PWR - G*(AVG - current))
        drive.start_tank_at_power(l, r)
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

def mission_2():
    '''
    нефтяная платформа
    '''
    drive.move(3)
    a_line(25)
    a_line(black=True)
    down()
    drive.move(5, steering=-100)
    for r in range(0, 4):
        manipulator.run_to_position(255, CLOCK, 100)
        down()
    drive.move(5, steering=100)
    print('Elapsed time m2: ', timer.now())

def mission_8():
    '''
    просмотр телевизора
    '''
    down()
    drive.move(10, speed=30)
    drive.move(-10)
    up()
    print('Elapsed time m8: ', timer.now())

def mission_13():
    '''
    фабрика игрушек
    '''
    manipulator.run_to_position(227, CLOCK, 100)
    drive.move(4, speed=30)
    manipulator.run_to_position(237, CLOCK, 100)
    sleep(1)
    drive.move(-4, speed=30)
    up()
    drive.move(2.5, speed=30)
    drive.move(6, steering=100)
    print('Elapsed time m13:', timer.now())
    
def mission_5():
    '''
    умная сеть(розетка, вилка) 
    '''
    a_line(amount=40)
    a_line(black=True)
    drive.move(6)
    drive.move(8.5, steering=-100)
    drive.move(-2)
    down()
    drive.move(-3)
    up()
    print('Elapsed time m5:', timer.now())

# mission_2()
# mission_13()
#mission_5()
