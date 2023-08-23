from microbit import *
import radio

# Configure the radio module with group 6
radio.config(group=6)
radio.on()

# Morse code mapping from signals to characters
mc_map =  {
    ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E", "..-.": "F", "--.": "G",
    "....": "H", "..": "I", ".---": "J", "-.-": "K", ".-..": "L", "--": "M", "-.": "N",
    "---": "O", ".--.": "P", "--.-": "Q", ".-.": "R", "...": "S", "-": "T", "..-": "U",
    "...-": "V", ".--": "W", "-..-": "X", "-.--": "Y", "--..": "Z",
    ".----": "1", "..---": "2", "...--": "3", "....-": "4", ".....": "5",
    "-....": "6", "--...": "7", "---..": "8", "----.": "9", "-----": "0"
}

# Timing intervals for dot and dash signals
dotInterval = 230
dashInterval = 470

# Time threshold for recognizing a complete letter
letterThreshold = 1000

# Buffer to store received Morse code signals
buf = ''

# Keep track of when waiting started
startedToWait = running_time()

# Function to decode a Morse code buffer to a character
def decode(buffer):
    return mc_map.get(buf, '?')

# Main loop
while True:
    # Calculate how long no key has been pressed
    waiting = running_time() - startedToWait
    signal = radio.receive()
    
    # If button A (dot) was pressed
    if button_a.was_pressed():
        display.show('.')
        radio.send('.')
        sleep(50)
        display.clear()
        
    # If button B (dash) was pressed
    elif button_b.was_pressed():
        display.show('-')
        radio.send('-')
        sleep(50)
        display.clear()
        
    # If a Morse code signal is received
    if signal:
        if signal == '.':
            buf += '.'
            display.show('.')
            sleep(dotInterval)
            display.clear()
        elif signal == '-':
            buf += '-'
            display.show('-')
            sleep(dashInterval)
            display.clear()

        # Reset waiting time since a signal has been received
        startedToWait = running_time()

    # If waiting is greater than a second and there's a buffer
    elif len(buf) > 0 and waiting > letterThreshold:
        character = decode(buf)
        buf = ''
        display.show(character)
