import RPi.GPIO as GPIO
import sys

#     GPIO    
relay_pin = 11  #  ̵   ģ   Ŀ      ţ   BOARDģʽ    11      

#     GPIOģʽ
GPIO.setmode(GPIO.BOARD)  # ʹ  BOARDģʽ
GPIO.setwarnings(False)  #     GPIO    
GPIO.setup(relay_pin, GPIO.OUT)  #  ̵       

#   ʼ״̬
relay_state = False

def toggle_relay(state):
    global relay_state
    #    ڸߵ ƽ     ļ̵       Ҫ        ״̬
    relay_state = not state
    GPIO.output(relay_pin, relay_state)
    print(f"Relay state: {'ON' if relay_state else 'OFF'}")

def main():
    print("Press '1' to turn ON the electromagnet.")
    print("Press '0' to turn OFF the electromagnet.")
    print("Press 'q' to quit.")

    try:
        while True:
            command = input("Enter command: ")
            if command == '1':
                toggle_relay(True)
            elif command == '0':
                toggle_relay(False)
            elif command.lower() == 'q':
                break
            else:
                print("Invalid command. Please enter '1', '0', or 'q'.")

            #    ӵ       
            current_state = GPIO.input(relay_pin)
            print(f"Current GPIO state: {current_state}")
    finally:
        GPIO.cleanup()  #     GPIO״̬

if __name__ == "__main__":
    main()
