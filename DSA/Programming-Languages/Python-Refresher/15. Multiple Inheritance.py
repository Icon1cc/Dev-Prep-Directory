"""
Multiple Inheritance
Description: Demonstrate multiple inheritance by creating three classes.
A Device class with a method turn_on() that prints "Device is now on."
A Transmitter class with a method transmit(message) that prints "Transmitting: <message>".
A Radio class that inherits from both Device and Transmitter, gaining the capabilities of both parent classes.
"""

class Device():
    def turn_on(self):
        print("Device is now on")
    
class Transmitter():
    def transmit(self, message):
        self.message = message
        print(f"Transmitting {message}")

class Radio(Device, Transmitter):
    pass

my_radio = Radio()
my_radio.turn_on()
my_radio.transmit("Hello, World!")
