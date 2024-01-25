# PiOrder
Raspberry Pi Food Ordering System

## OVERVIEW ##
This project aims to implement a PiOrder: Raspberry Pi Food Ordering System where instead of having a cashier to give you receipt, you key in what you want yourself, on Raspberry PI 3B+. The project uses keypad as the access mode. When the user tries to access the system, the data is fetched from SQLite database which is inbuilt database on the Raspberry PI 3B+, then the user is presented with food menu and their corresponding prices if it's code is identified. You can as well add as many users as you can to the system manually through simple database insert statement.

### Hardware Used ###
1. Raspberry PI 3B+
2. LCD 16X2 display I2C
3. 4X3 Keypad
4. USB to Serial (TTL) Module.
5. Micro USB to USB adapter.

### Software Used ###
1. VNC Viewer
2. Python 3 IDLE
3. SQLite 
4. Rasperian OS

##### DESCRIPTIONS #####

#### Raspberry PI 3B+ ####
Raspberry Pi is a low cost, credit-card based sized computer that plugs into a computer monitor and uses standard keyboard and mouse. It is capable little device that enables people of all ages to explore computing, and to learn how to program in languages like python.
Raspberry Pi 3B+ is ideal for making embedded Internet of Things (IoT) projects. At the heart of Raspberry Pi 3B+ is a 1GHz BCM2835 single-core processor with 512MB RAM.
Since we are using Raspberry Pi and it has only micro USB port we will be needing Micro USB to USB adapter to handle for external peripherals.

#### LCD 16X2 display I2C ####
The 16X2 LCD display screen uses only 4 pins the SCL, SDA, VCC, and GND when interfacing with Raspberry Pi. The advantage of using it is to save on the number of pins used on the Raspberry Pi.

#### UART ####
The Universal Asynchronous Receiver Transmitter is a device for asynchronous serial communication in which the data format and transmission speeds are configurable. A UART is usually an individual (or part of an) integrated circuit (IC) used for serial communication over a computer or peripheral device serial port. UARTs are now commonly included in micro controllers. The Raspberry Pi already has 2 GPIO pins for UART, so we are able to connect the sensor directly to the Raspberry Pi.

#### SOFTWARE SETUP ####
Before we start, we need to do some installations and set up different libraries and tools to get our codes to run properly.
## Setup for I2C LCD ##
On terminal log in to your Pi and enter *sudo raspi-config* to access the configuration menu.
Then arrow down and select Advanced settings.
Then select I2C Enable/Disable automatic loading
Choose Yes at the next prompt
Exit the configuration menu
Reboot the Pi to activate the settings.

Run the following commands on your terminal:
*sudo apt-get install i2c-tools*
We also need to install SMBUS library, which is the python library we're going to use to access the I2C bus on the Pi:
*sudo apt-get install python-smbus*
Now reboot the Pi and log in again, with your LCD connected, enter *i2cdetect -y 1* in the terminal. This will show you table of addresses for each I2C device connected to your Pi.
## Functional requirements workflow ##
1. User verification - system prompts the user to enter a code using keypad, then user should press # to finish entering the code.
2. Code validation - system should verify the entered code against a stored list of valid codes in the SQLite database.
3. User authentication - if the entered code is valid, the system should authenticate the user and display a welcome message.
4. Menu Display - The system will display a main menu on a LCD screen after user authentication.
5. Food selection - System will allow the user to select food items suing the keypad. Each food item will have a corresponding code for selection.
6. Payment process - When the user chooses to proceed with payment, the system should calculate the total price based on the selected food items. The system will display a payment confirmation message on the LCD screen.
7. Database interaction - The system will interact with an SQLite database to store user information and validate codes.
8. Error Handling - System will handle errors gracefully, such as displaying "Invalid Code" message or handling unexpected inputs.
9. User exit - The system will now allow the user to exit the program.
10. Database - The system shall update the database i.e deducting funds from the student account after successful "pay now"
