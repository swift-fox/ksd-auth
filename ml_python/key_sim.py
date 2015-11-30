'''
Simulate and test key press and release event
'''


from Tkinter import *
from pattern_match import PatternMatch
import time

startTime = 0
passwd = ''
keyPress = []
keyRelease = []

prev_passwd = ''
patterns = []

def getTimeInMills():
    return time.time()

def keyup(e):
    global  startTime, keyPress, keyRelease, passwd, prev_passwd, patterns
    if e.keysym == 'Return':
        startTime = 0
        print('password: ', passwd)
        print('keyPress: ', keyPress)
        print('keyRelease: ', keyRelease)

        if not prev_passwd or len(patterns) < len(passwd):
            prev_passwd = passwd
            patterns.append((keyPress, keyRelease))
        elif prev_passwd != passwd:
            print('Password is not equal to the previous one.')
        else:
            patterns.append((keyPress, keyRelease))
            pm = PatternMatch()
            print(pm.is_similar(patterns[-1], patterns[:-1], "MAH_DIST"))
        passwd = ''
        keyPress = []
        keyRelease = []
    else:
        keyRelease.append(getTimeInMills() - startTime)
        passwd += str(e.char)

def keydown(e):
    global startTime, keyRelease, passwd
    if e.keysym == 'Return':
        return
    if(startTime == 0):
        startTime = getTimeInMills()
        keyPress.append(0)
    else:
        keyPress.append(getTimeInMills() - startTime)

if __name__ == '__main__':
    tk = Tk()
    tk.bind("<KeyPress>", keydown)
    tk.bind("<KeyRelease>", keyup)
    tk.mainloop()
