#!/usr/bin/env python
# -*- coding: utf8 -*-

#import RPi.GPIO as GPIO
import OPi.GPIO as GPIO
import MFRC522
import signal
import time

continue_reading = True

relay_port = 8
GPIO.setmode(GPIO.BOARD)
GPIO.setup(relay_port, GPIO.OUT)
GPIO.output(relay_port, GPIO.LOW)

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print("Welcome to the MFRC522 data read example")
print("Press Ctrl-C to stop.")

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    print("Reading...")

    # Force lock the door
    GPIO.output(relay_port, GPIO.LOW)

    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected")
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UIDs
        print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

	# CRIAR FUNÇÃO PARA BUSCAR CORRESPONDENCIA NO BANCO DE DADOS

        print("Teste: "+ str(uid[0] == 62 and uid[1] == 54 and uid[2] == 133 and uid[3] == 89))

        if (uid[0] == 62 and uid[1] == 54 and uid[2] == 133 and uid[3] == 89):
            GPIO.output(relay_port, GPIO.HIGH)
            time.sleep(5)
        else:
            GPIO.output(relay_port, GPIO.LOW)

	#time.sleep(1)
    
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print("Authentication error")
