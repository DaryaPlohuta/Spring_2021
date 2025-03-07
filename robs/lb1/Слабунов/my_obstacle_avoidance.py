"""my_avoid_obstacles controller."""

"""Braitenberg-based obstacle-avoiding robot controller."""

from controller import Robot, Compass

# Get reference to the robot.
robot = Robot()

# Get robot's Compass device
compass = robot.getCompass("compass")

# Get simulation step length.
timeStep = int(robot.getBasicTimeStep())

# Constants of the Thymio II motors and distance sensors.
maxMotorVelocity = 9.53
distanceSensorCalibrationConstant = 360

# Get left and right wheel motors.
leftMotor = robot.getMotor("motor.left")
rightMotor = robot.getMotor("motor.right")

# Get frontal distance sensors.
outerLeftSensor = robot.getDistanceSensor("prox.horizontal.0")
centralLeftSensor = robot.getDistanceSensor("prox.horizontal.1")
centralSensor = robot.getDistanceSensor("prox.horizontal.2")
centralRightSensor = robot.getDistanceSensor("prox.horizontal.3")
outerRightSensor = robot.getDistanceSensor("prox.horizontal.4")

# Enable distance sensors.
outerLeftSensor.enable(timeStep)
centralLeftSensor.enable(timeStep)
centralSensor.enable(timeStep)
centralRightSensor.enable(timeStep)
outerRightSensor.enable(timeStep)

# Enable the Compass
compass.enable(timeStep)

# Disable motor PID control mode.
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

# Set the initial velocity of the left and right wheel motors.
leftMotor.setVelocity(maxMotorVelocity)
rightMotor.setVelocity(maxMotorVelocity)

while robot.step(timeStep) != -1:
    # Read values from four distance sensors and calibrate.
    outerLeftSensorValue = outerLeftSensor.getValue() / distanceSensorCalibrationConstant
    centralLeftSensorValue = centralLeftSensor.getValue() / distanceSensorCalibrationConstant
    centralSensorValue = centralSensor.getValue() / distanceSensorCalibrationConstant
    centralRightSensorValue = centralRightSensor.getValue() / distanceSensorCalibrationConstant
    outerRightSensorValue = outerRightSensor.getValue() / distanceSensorCalibrationConstant
    
    # To read values compass
    compassValues = compass.getValues()

    # Detected obstacles
    if outerLeftSensorValue != 0 or centralLeftSensorValue != 0:
        leftMotor.setVelocity(maxMotorVelocity)
        rightMotor.setVelocity(-0.5 * maxMotorVelocity) 
    elif centralSensorValue != 0 or outerRightSensorValue != 0 or centralRightSensorValue != 0:
        leftMotor.setVelocity(-0.5 * maxMotorVelocity)
        rightMotor.setVelocity(maxMotorVelocity)
        
    # Not detected obstacles
    if outerLeftSensorValue == 0 and centralLeftSensorValue == 0 and centralSensorValue == 0 and centralRightSensorValue == 0 and outerRightSensorValue == 0:
        if compassValues[0] > 0.001:
            leftMotor.setVelocity(maxMotorVelocity)
            rightMotor.setVelocity(0.9 * maxMotorVelocity)
        elif compassValues[0] < -0.001:
            leftMotor.setVelocity(0.9 * maxMotorVelocity)
            rightMotor.setVelocity(maxMotorVelocity)
        else:
            leftMotor.setVelocity(maxMotorVelocity)
            rightMotor.setVelocity(maxMotorVelocity)