import keyboard, time

prev = time.time()

while True:
    if time.time()-prev >= 3:
        keyboard.send("3")
        prev = time.time()
