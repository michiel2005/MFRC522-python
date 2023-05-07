import os
import subprocess

def find_file(uid) :
    if os.path.isdir('./userNotes/{}'.format(uid)) :
        everythinExists = True
        if os.path.isfile('./userNotes/{}/{}'.format(uid, uid)) == False:
            everythinExists = False 
            open('./userNotes/{}/{}'.format(uid, uid), 'a').close()
        if os.path.isfile('./userNotes/{}/test.txt'.format(uid, uid)) == False:
            everythinExists = False
            f = open('./userNotes/{}/test.txt'.format(uid, uid), 'a')
            f.write("ABCDE")
            f.close()
        
        if everythinExists == False :
            return False
        else :
            return True
    else :
        os.mkdir('./userNotes/{}'.format(uid))
        open('./userNotes/{}/{}'.format(uid, uid), 'a').close()
        f = open('./userNotes/{}/test.txt'.format(uid), 'a')
        f.write("ABCDE")
        f.close()
        return False

def decrypt_and_open_file(uid, key):
    print("Decrypting/..../././../././././..//")
    subprocess.call(['nano', 'userNotes/{}/{}'.format(uid, uid)])