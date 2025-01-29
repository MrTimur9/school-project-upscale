import time
a, b = 1, 1
while True:
    a, b = a + b, a
    print(a)
    time.sleep(1)