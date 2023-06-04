import os
from pydoc import plain
import subprocess
from Crypto.Cipher import AES

def find_file(uid) :
    if os.path.isdir('./userNotes/{}'.format(uid)) :
        everythingExists = True
        if os.path.isfile('./userNotes/{}/{}.txt'.format(uid, uid)) == False:
            everythingExists = False 
            f = open('./userNotes/{}/{}.txt'.format(uid, uid), 'a')
            f.write("You can type here...\nYou can quit with ctrl + x")
            f.close()
        if os.path.isfile('./userNotes/{}/nonce.txt'.format(uid, uid)) == False:
            everythingExists = False
            f = open('./userNotes/{}/nonce.txt'.format(uid, uid), 'a')
            f.close()
        if os.path.isfile('./userNotes/{}/tag.txt'.format(uid, uid)) == False:
            everythingExists = False
            f = open('./userNotes/{}/tag.txt'.format(uid, uid), 'a')
            f.close()
        
        return everythingExists
    else :
        os.mkdir('./userNotes/{}'.format(uid))
        f = open('./userNotes/{}/{}.txt'.format(uid, uid), 'a')
        f.write("You can type here...\nYou can quit with ctrl + x")
        f.close()
        open('./userNotes/{}/nonce.txt'.format(uid), 'a').close()
        open('./userNotes/{}/tag.txt'.format(uid), 'a').close()
        return False

def decrypt_and_open_file(uid, key):
    nonce = 0
    tag = 0
    if os.path.isdir('./userNotes/{}'.format(uid)) :
        if os.path.isfile('./userNotes/{}/nonce.txt'.format(uid, uid)):
            f = open('./userNotes/{}/nonce.txt'.format(uid, uid), 'rb')
            nonce = f.read()
        if os.path.isfile('./userNotes/{}/tag.txt'.format(uid, uid)):
            f = open('./userNotes/{}/tag.txt'.format(uid, uid), 'rb')
            tag = f.read()
        else:
            print("ERROR Your nonce or tag somehow missing or corrupted")
            return

    if os.path.isdir('./userNotes/{}'.format(uid)) :
        if os.path.isfile('./userNotes/{}/{}.txt'.format(uid, uid)):
            f = open('./userNotes/{}/{}.txt'.format(uid, uid), 'rb')
            ciphertext = f.read()
            f.close()
            cipher = AES.new(key, AES.MODE_EAX, nonce)
            plaintext = cipher.decrypt(ciphertext)
            try:
                cipher.verify(tag)
                f = open('./userNotes/{}/{}.txt'.format(uid, uid), 'w')
                f.write(plaintext.decode())
                f.close()
                subprocess.call(['nano', './userNotes/{}/{}.txt'.format(uid, uid)])
            except ValueError:
                print("Key incorrect or message corrupted")

def encrypt_file(uid, key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    tag = 0

    if os.path.isdir('./userNotes/{}'.format(uid)) :
        if os.path.isfile('./userNotes/{}/{}.txt'.format(uid, uid)):
            cipher = AES.new(key, AES.MODE_EAX)
            nonce = cipher.nonce
            f = open('./userNotes/{}/{}.txt'.format(uid, uid), 'r')
            data = f.read()
            f.close()
            open('./userNotes/{}/{}.txt'.format(uid, uid), 'w').close() #used to empty the file
            f = open('./userNotes/{}/{}.txt'.format(uid, uid), 'wb')
            ciphertext, tag = cipher.encrypt_and_digest(str.encode(data))
            f.write(ciphertext)
            f.close()

    if os.path.isdir('./userNotes/{}'.format(uid)) :
        if os.path.isfile('./userNotes/{}/nonce.txt'.format(uid, uid)):
            f = open('./userNotes/{}/nonce.txt'.format(uid, uid), 'wb')
            f.write(nonce)
            f.close()
        if os.path.isfile('./userNotes/{}/tag.txt'.format(uid, uid)):
            f = open('./userNotes/{}/tag.txt'.format(uid, uid), 'wb')
            f.write(tag)
            f.close()