#!/usr/bin/env python
# -*- coding: utf8 -*-

from Crypto.Cipher import AES
import time
import OPi.GPIO as GPIO
import MFRC522
import FileManager
import signal
import random
import string

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

def search_good_card():
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    
    # If a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected")
     
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    
    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
    
        # Print UID
        print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
    
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
    
        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 0, key, uid)
        print("\n")
    
        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            if MIFAREReader.checkUIDRigid() == False:
                return False
        else:
            print("Authentication error")
            return False

        MIFAREReader.MFRC522_StopCrypto1()
    else:
        return False
    
    return True


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return result_str

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Clear bitmask
    MIFAREReader.MFRC522_StopCrypto1()

    if search_good_card() != True:
        continue


    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected")

    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    if status == MIFAREReader.MI_OK:
    
        uidString = str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])

        isKeyUsed = FileManager.find_file(uidString)

        MIFAREReader.MFRC522_SelectTag(uid)


        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 4, key, uid)
        print("\n")

        if status == MIFAREReader.MI_OK:

            encyptionKey = ""
            if isKeyUsed == False :
                encyptionKey = get_random_string(16)
                dataKey = []
                for letter in encyptionKey :
                        dataKey.append(ord(letter))
                print(encyptionKey)
                MIFAREReader.MFRC522_Write(4, dataKey)
                FileManager.encrypt_file(uidString, str.encode(encyptionKey))
            else :
                data = MIFAREReader.MFRC522_Read(4)
                for x in data :
                    encyptionKey += chr(x)
                print("Key...---..")
                print(encyptionKey)
                print("Key...---..")

            FileManager.decrypt_and_open_file(uidString, str.encode(encyptionKey))
            FileManager.encrypt_file(uidString, str.encode(encyptionKey))

            # Variable for the data to write
            data = []

            # Fill the data with 0xFF
            for x in range(0,16):
                data.append(0xFF)

            print("Sector 8 looked like this:")
            # Read block 8
            MIFAREReader.MFRC522_Read(4)
            print("\n")

            print("Sector 8 will now be filled with 0xFF:")
            # Write the data
            MIFAREReader.MFRC522_Write(4, data)
            print("\n")

            print("It now looks like this:")
            # Check to see if it was written
            MIFAREReader.MFRC522_Read(4)
            print("\n")

            data = []
            # Fill the data with 0x00
            for x in range(0,16):
                data.append(0x00)

            print("Now we fill it with 0x00:")
            MIFAREReader.MFRC522_Write(4, data)
            print("\n")

            print("It is now empty:")
            # Check to see if it was written
            MIFAREReader.MFRC522_Read(4)
            print("\n")

            # Stop
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print("Authentication error")
            continue
