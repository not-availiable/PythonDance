xSpeedCoefficient = 0
ySpeedCoefficient = 0
rotSpeedCoefficient = 0
maxXSpeed = .5
maxYSpeed = .5
maxRotSpeed = 100
songState = 0
beatIncrement = 0
beatTimer = 0
beatHappens = False
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
def start():
    global maxXSpeed
    global maxYSpeed
    global maxRotSpeed
    global songState
    global beatIncrement
    global beatTimer
    global beatHappens
    #init
    firstTime = True
    #state 0
    rotationMultiplier = 1
    #stat 3
    gimbalRotationCoefficient = 0


    robot_ctrl.set_mode(rm_define.robot_mode_free)
    tools.timer_ctrl(rm_define.timer_start)
    while True:
        #chassis_ctrl.set_wheel_speed(100,100,100,100)
        variable_time = tools.timer_current()
        if variable_time - beatTimer > beatIncrement:
            beatHappens = True
            beatTimer = variable_time


        print(variable_time)


        if songState == 0:
            if firstTime:
                beatIncrement = .75
                firstTime = False
            if beatHappens:
                rotationMultiplier *= -1
                beatHappens = False


            xSpeedCoefficient = math.cos(variable_time)
            ySpeedCoefficient = math.sin(variable_time)
            rotSpeedCoefficient = rotationMultiplier


            if variable_time > 3:
                songState = 1
                firstTime = True
        if songState == 1:
            if firstTime:
                #gimbal_ctrl.recenter()
                beatIncrement = .75
                firstTime = False
            if beatHappens:
                rotationMultiplier *= -1
                beatHappens = False   
            xSpeedCoefficient = 0
            ySpeedCoefficient = 0
            rotSpeedCoefficient = rotationMultiplier
            #gimbal_ctrl.set_rotate_speed(rotationMultiplier)
            gimbal_ctrl.rotate_with_speed(-rotationMultiplier * maxRotSpeed,0)
            if variable_time > 10:
                songState = 2;
                firstTime = True
        if songState == 2:
            if firstTime:
                beatIncrement = 1;
                firstTime = False
            if beatHappens:
                gun_ctrl.fire_once()
                beatHappens = False
            xSpeedCoefficient = 0
            ySpeedCoefficient = 0
            rotSpeedCoefficient = 0
            gimbal_ctrl.rotate_with_speed(math.cos(variable_time) * maxRotSpeed, math.sin(variable_time * maxRotSpeed))
            if variable_time > 15:
                songState = 3;
                firstTime = True;
        if songState == 3: 
            if firstTime:
                beatIncrement = .75;
                firstTime = False
                gimbalRotationCoefficient = -.2
            if beatHappens:
                beatHappens = False
                if gimbalRotationCoefficient == -.2:
                    gimbalRotationCoefficient = 1.1
                else:
                    gimbalRotationCoefficient = -.2
            xSpeedCoefficient = 0
            ySpeedCoefficient = 0
            rotSpeedCoefficient = .5
            gimbal_ctrl.rotate_with_speed(gimbalRotationCoefficient * maxRotSpeed, 0)
            if variable_time > 20:
                songState = 4;
                firstTime = True;
        if songState == 4:
            if firstTime:
                firstTime = False
                xSpeedCoefficient = 0
                ySpeedCoefficient = 0
                rotSpeedCoefficient = 0
                gimbal_ctrl.rotate_with_speed(gimbalRotationCoefficient * maxRotSpeed, 0)
                gimbal_ctrl.angle_ctrl(0, 0)


        chassis_ctrl.move_with_speed(xSpeedCoefficient * maxXSpeed, ySpeedCoefficient * maxYSpeed, rotSpeedCoefficient * maxRotSpeed)



