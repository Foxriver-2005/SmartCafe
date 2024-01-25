#!/usr/bin/env python
import RPi.GPIO as GPIO
import sqlite3
import I2C_LCD_driver
from gpiozero import Button
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(11, GPIO.OUT)
GPIO.setwarnings(False)

# Connect to SQLite database (or create a new one)
db = sqlite3.connect('card.db')  # SQLite database file (e.g., card.db)
cursor = db.cursor()

# Create users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        code TEXT
    )
''')

# Create students_balance table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS balance (
        id INTEGER PRIMARY KEY,
        name TEXT,
        balance INTEGER DEFAULT 0,
        FOREIGN KEY (id) REFERENCES users (id)
    )
''')

db.commit()

mylcd = I2C_LCD_driver.lcd(port=1)

# Keypad GPIO pin configuration
L1 = 27
L2 = 21
L3 = 20
L4 = 10

C1 = 22
C2 = 17
C3 = 16

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if GPIO.input(C1) == 1:
        return characters[0]
    if GPIO.input(C2) == 1:
        return characters[1]
    if GPIO.input(C3) == 1:
        return characters[2]
    GPIO.output(line, GPIO.LOW)
    return None

def get_key_pressed():
    while True:
        key_pressed = None
        for line, chars in zip([L1, L2, L3, L4], ["123", "456", "789","*0#"]):
            if readLine(line, chars):
                key_pressed = readLine(line, chars)
                break
			
        if key_pressed:
            return key_pressed

def display_menu():
    mylcd.lcd_clear()
    mylcd.lcd_display_string("1. Proceed", 1)
    mylcd.lcd_display_string("2. Exit", 2)

def display_foods_menu():
    mylcd.lcd_clear()
    mylcd.lcd_display_string("3. Tea    Ksh 20", 1)
    mylcd.lcd_display_string("4. Rice   Ksh 30", 2)
    mylcd.lcd_display_string("5. Chapo  Ksh 15 each", 3)
    mylcd.lcd_display_string("6. Ugali  Ksh 20", 4)

def display_additional_foods():
    mylcd.lcd_clear()
    mylcd.lcd_display_string("Additional options:", 1)
    mylcd.lcd_display_string("7. Pizza  Ksh 40", 2)
    mylcd.lcd_display_string("8. Salad  Ksh 25", 3)
    mylcd.lcd_display_string("Press * to go back", 4)

#def deduct_balance(b, amount):
    # Deduct the amount from the student's balance
#    cursor.execute("SELECT balance FROM balance WHERE id = ?", (id,))
#    current_balance = cursor.fetchone()[0]
#    new_balance = current_balance - amount
#    cursor.execute("UPDATE balance SET balance = ? WHERE id = ?", (new_balance, id))
#    db.commit()

def deduct_balance(id, amount):
    # Deduct the amount from the student's balance
    cursor.execute("SELECT balance FROM balance WHERE id = ?", (id,))
    current_balance = cursor.fetchone()[0]
    new_balance = current_balance - amount
    cursor.execute("UPDATE balance SET balance = ? WHERE id = ?", (new_balance, id))
    db.commit()


def process_payment(id, total_price):
    deduct_balance(id, total_price)

def main():
    while True:
        # Code verification
        mylcd.lcd_display_string("Enter Code:", 1)
        mylcd.lcd_display_string("(# to continue)", 2)

        code = ""
        while True:
            key = get_key_pressed()

            if key == '#':
                break
            elif key == '*':
                display_menu()
                break
            else:
                code += key
                print('entered code', code)
                time.sleep(0.2)

        # Verify code against the database
        cursor.execute("SELECT id, name FROM users WHERE code = ?", (code,))
        result = cursor.fetchone()

        if result:
            id, name = result
            mylcd.lcd_clear()
            mylcd.lcd_display_string("Welcome " + name, 1)
            GPIO.output(11, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(11, GPIO.LOW)
            mylcd.lcd_clear()

            display_menu()

            selected_foods = []
            total_price = 0

            while True:
                key = get_key_pressed()

                if key == '1':
                    display_foods_menu()
                elif key == '2':
                    mylcd.lcd_clear()
                    mylcd.lcd_display_string("Goodbye!", 1)
                    time.sleep(2)
                    mylcd.lcd_clear()
                    GPIO.cleanup()
                    return
                elif key == '0':
                    display_additional_foods()
                elif key == '*':
                    display_menu()

                elif key == '#':
                    if not selected_foods:
                        mylcd.lcd_clear()
                        mylcd.lcd_display_string("Nothing selected", 1)
                        time.sleep(2)
                        mylcd.lcd_clear()
                        display_menu()
                    else:
                        for food in selected_foods:
                            total_price += food[1]

                        mylcd.lcd_clear()
                        mylcd.lcd_display_string(
                            "Total: Ksh {}".format(total_price), 1)
                        mylcd.lcd_display_string("1. Pay now", 2)
                        mylcd.lcd_display_string("2. Back", 3)

                        while True:
                            key = get_key_pressed()

                            if key == '1':
                                # Deduct funds and show current balance
                                process_payment(id, total_price)
                                
                                cursor.execute("SELECT balance FROM balance WHERE id = ?", (id,))
                                current_balance = cursor.fetchone()[0]
                                
                                mylcd.lcd_clear()
                                mylcd.lcd_display_string(
                                    "Payment successful!", 1)
                                mylcd.lcd_display_string(
                                    "Balance: Ksh {}".format(current_balance), 2)
                                time.sleep(3)
                                mylcd.lcd_clear()
                                display_menu()
                                break

                            elif key == '2':
                                mylcd.lcd_clear()
                                display_foods_menu()
                                break

                else:
                    # Handle food selection
                    food_number = int(key)
                    if 1 <= food_number <= 4:
                        selected_foods.append(
                            (food_number, get_food_price(food_number)))
                        mylcd.lcd_clear()
                        mylcd.lcd_display_string(
                            "Selected: {}".format(get_food_name(food_number)), 1)
                        mylcd.lcd_display_string(
                            "Price: Ksh {}".format(get_food_price(food_number)), 2)

                    elif 5 <= food_number <= 6:
                        selected_foods.append(
                            (food_number, get_additional_food_price(food_number)))
                        mylcd.lcd_clear()
                        mylcd.lcd_display_string(
                            "Selected: {}".format(get_additional_food_name(food_number)), 1)
                        mylcd.lcd_display_string(
                            "Price: Ksh {}".format(get_additional_food_price(food_number)), 2)

                    time.sleep(2)
                    mylcd.lcd_clear()

        else:
            mylcd.lcd_clear()
            mylcd.lcd_display_string("Invalid Code!", 1)
            time.sleep(2)
            mylcd.lcd_clear()

def get_food_name(food_number):
    food_names = {
        3: "Tea",
        4: "Rice",
        5: "Chapo",
        6: "Ugali",
    }
    return food_names.get(food_number, "Unknown Food")

def get_food_price(food_number):
    food_prices = {
        1: 20,
        2: 30,
        3: 15,
        4: 20,
    }
    return food_prices.get(food_number, 0)

def get_additional_food_name(food_number):
    additional_food_names = {
        5: "Pizza",
        6: "Salad",
    }
    return additional_food_names.get(food_number, "Unknown Food")

def get_additional_food_price(food_number):
    additional_food_prices = {
        5: 40,
        6: 25,
    }
    return additional_food_prices.get(food_number, 0)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

