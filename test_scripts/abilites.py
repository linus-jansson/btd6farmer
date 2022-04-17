import keyboard, time

prev = time.time()

while True:
    if time.time()-prev >= 1:
        keyboard.send("1")
        time.sleep(0.2)
        keyboard.send("2")
        time.sleep(0.2)
        print(time.time()-prev)
        prev = time.time()
