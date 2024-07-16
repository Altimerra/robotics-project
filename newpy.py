# To integrate UART communication between the Raspberry Pi Pico and an ESP32 for switching between manual control and line following modes, you'll need to set up UART on the Pico. The ESP32 can send commands to switch modes and control the robot manually.

# ### Wiring Assumptions
# - **UART TX on ESP32** connected to **UART RX on Pico** (e.g., `GP16`).
# - **UART RX on ESP32** connected to **UART TX on Pico** (e.g., `GP17`).
# - **Analog Multiplexer**: Control pins connected to `GP10`, `GP11`, `GP12`, and `GP13` (for S0, S1, S2, S3).
# - **Multiplexer Output**: Connected to `GP26` (ADC0).
# - **Digital IR Sensors**: Connected to `GP14` and `GP15`.
# - **Motor A**: Connected to pins `GP0` and `GP1`.
# - **Motor B**: Connected to pins `GP2` and `GP3`.
# - **PWM** control using `GP4` and `GP5` for speed control.

# ### Code Explanation
# 1. **UART Communication**: Setup UART to receive commands from the ESP32.
# 2. **Mode Switching**: Implement switching between manual control and line following modes based on UART commands.
# 3. **Manual Control**: Implement functions to control the robot manually via UART commands.

# ### MicroPython Code

# ```python
from machine import Pin, PWM, ADC, UART
from time import sleep

# Motor A pins
motorA_forward = Pin(0, Pin.OUT)
motorA_backward = Pin(1, Pin.OUT)
motorA_speed = PWM(Pin(4))

# Motor B pins
motorB_forward = Pin(2, Pin.OUT)
motorB_backward = Pin(3, Pin.OUT)
motorB_speed = PWM(Pin(5))

# Set PWM frequency
motorA_speed.freq(1000)
motorB_speed.freq(1000)

# Multiplexer control pins
mux_pins = [Pin(10, Pin.OUT), Pin(11, Pin.OUT), Pin(12, Pin.OUT), Pin(13, Pin.OUT)]

# ADC pin
adc = ADC(Pin(26))

# Digital IR sensors
left_ir = Pin(14, Pin.IN)
right_ir = Pin(15, Pin.IN)

# UART setup
uart = UART(1, baudrate=115200, tx=Pin(17), rx=Pin(16))

# Modes
MODE_LINE_FOLLOWING = 0
MODE_MANUAL_CONTROL = 1
mode = MODE_LINE_FOLLOWING

def select_mux_channel(channel):
    """Select the given channel on the multiplexer."""
    for i in range(4):
        mux_pins[i].value((channel >> i) & 1)

def read_ir_sensors():
    """Read values from the IR sensor array via the multiplexer."""
    sensor_values = []
    for channel in range(8):
        select_mux_channel(channel)
        sleep(0.001)  # Small delay to allow the multiplexer to settle
        sensor_values.append(adc.read_u16())
    return sensor_values

def calculate_position(sensor_values):
    """Calculate the position of the line based on sensor readings."""
    weighted_sum = sum(i * value for i, value in enumerate(sensor_values))
    total = sum(sensor_values)
    return weighted_sum / total if total > 0 else -1  # Return -1 if no line detected

def set_speed(speed):
    """Set the speed of the motors (0-65535)."""
    motorA_speed.duty_u16(speed)
    motorB_speed.duty_u16(speed)

def stop():
    """Stop both motors."""
    motorA_forward.low()
    motorA_backward.low()
    motorB_forward.low()
    motorB_backward.low()

def move_forward(speed=32768):
    """Move the car forward at the given speed."""
    motorA_forward.high()
    motorA_backward.low()
    motorB_forward.high()
    motorB_backward.low()
    set_speed(speed)

def move_backward(speed=32768):
    """Move the car backward at the given speed."""
    motorA_forward.low()
    motorA_backward.high()
    motorB_forward.low()
    motorB_backward.high()
    set_speed(speed)

def turn_left(speed=32768):
    """Turn the car left at the given speed."""
    motorA_forward.low()
    motorA_backward.high()
    motorB_forward.high()
    motorB_backward.low()
    set_speed(speed)

def turn_right(speed=32768):
    """Turn the car right at the given speed."""
    motorA_forward.high()
    motorA_backward.low()
    motorB_forward.low()
    motorB_backward.high()
    set_speed(speed)

def follow_line():
    """Follow the line based on IR sensor readings."""
    sensor_values = read_ir_sensors()
    position = calculate_position(sensor_values)
    
    if position == -1:  # No line detected by the analog sensors
        if left_ir.value() == 0:  # Line detected on the left
            turn_left()
        elif right_ir.value() == 0:  # Line detected on the right
            turn_right()
        else:
            stop()  # Stop if no line is detected
    else:
        # Define the center position (middle of the sensor array)
        center_position = (len(sensor_values) - 1) / 2
        
        # Determine the error (difference from the center)
        error = position - center_position
        
        # Set motor speeds based on the error
        base_speed = 32768  # Adjust base speed as needed
        correction = int(error * 1000)  # Adjust correction factor as needed
        
        left_speed = max(0, base_speed - correction)
        right_speed = max(0, base_speed + correction)
        
        motorA_speed.duty_u16(left_speed)
        motorB_speed.duty_u16(right_speed)

def manual_control(command):
    """Control the robot manually based on UART commands."""
    if command == b'F':
        move_forward()
    elif command == b'B':
        move_backward()
    elif command == b'L':
        turn_left()
    elif command == b'R':
        turn_right()
    elif command == b'S':
        stop()

# Example usage
if __name__ == "__main__":
    try:
        while True:
            if uart.any():
                command = uart.read(1)
                if command == b'M':  # Switch to manual control mode
                    mode = MODE_MANUAL_CONTROL
                elif command == b'A':  # Switch to line following mode
                    mode = MODE_LINE_FOLLOWING
                else:
                    manual_control(command)
            
            if mode == MODE_LINE_FOLLOWING:
                follow_line()
            sleep(0.1)
    except KeyboardInterrupt:
        stop()
# ```

# ### Notes
# 1. **UART Communication**: The code sets up UART communication on `GP16` (RX) and `GP17` (TX).
# 2. **Mode Switching**: The mode can be switched between manual control and line following using UART commands (`b'M'` for manual and `b'A'` for automatic/line following).
# 3. **Manual Control**: Commands (`b'F'` for forward, `b'B'` for backward, `b'L'` for left, `b'R'` for right, and `b'S'` for stop) are used to control the robot manually.
# 4. **Main Loop**: The main loop reads UART commands and switches modes or controls the robot accordingly.

# Upload this code to your Raspberry Pi Pico using a tool like Thonny, and ensure your motor driver, motors, multiplexer, IR sensors, and UART connections are properly set up. Adjust the sensor pins and correction factor as necessary for your specific hardware.