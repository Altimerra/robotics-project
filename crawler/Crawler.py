import Components
import gpiozero

class Crawler:
    auto_mode:bool = False
    speed:float = 1.0

    def __init__(self, drivetrain:gpiozero.Robot, ultrasonic:gpiozero.DistanceSensor, irarray:Components.IRArray):
        self.drivetrain = drivetrain
        self.ultrasonic = ultrasonic
        self.irarray = irarray

    def parse_message(self,msg:str):
        message = msg.split(sep=',')

        match message[0]:
            case 'mode':
                match message[1]:
                    case 'auto':
                        self.auto_mode = True
                    case 'remote':
                        self.auto_mode = False
            case 'control' if not self.auto_mode:
                match message[1]:
                    case 'left':
                        self.drivetrain.left(self.speed)
                    case 'right':
                        self.drivetrain.right(self.speed)
                    case 'forward':
                        self.drivetrain.forward(self.speed)
                    case 'backward':
                        self.drivetrain.backward(self.speed)

    def automode():
        pass
