import RPi.GPIO as GPIO

import time





class Keypad:

    def __init__(self, row_pins, col_pins):

        self.row_pins = row_pins

        self.col_pins = col_pins



        # Set GPIO mode and initialize pins

        if GPIO.getmode() is None:

            GPIO.setmode(GPIO.BCM)

        GPIO.setwarnings(False)



        # Initialize rows as inputs with pull-up resistors

        for row_pin in self.row_pins:

            GPIO.setup(row_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)



        # Initialize columns as outputs

        for col_pin in self.col_pins:

            GPIO.setup(col_pin, GPIO.OUT)

            GPIO.output(col_pin, GPIO.HIGH)



    def get_key(self):

        key = None



        # Scan each column

        for i in range(len(self.col_pins)):

            GPIO.output(self.col_pins[i], GPIO.LOW)



            # Check each row

            for j in range(len(self.row_pins)):

                if GPIO.input(self.row_pins[j]) == GPIO.LOW:

                    key = self.get_key_from_matrix(i, j)



            GPIO.output(self.col_pins[i], GPIO.HIGH)



            if key:

                break



        return key



    def get_key_from_matrix(self, col, row):

        # Define the key matrix

        keys = [

            ['1', '2', '3'],

            ['4', '5', '6'],

            ['7', '8', '9'],

            ['*', '0', '#']

        ]



        return keys[row][col]



    def cleanup(self):

        # Cleanup GPIO settings

        GPIO.cleanup()





# Example usage:

if __name__ == "__main__":

    keypad = Keypad(row_pins=[27,21,20,10], col_pins=[22, 17, 16])



    try:

        while True:

            key = keypad.get_key()

            if key:

                print(f"Pressed: {key}")

                time.sleep(0.2)  # Optional debounce time



    except KeyboardInterrupt:

        pass



    finally:

        keypad.cleanup()

