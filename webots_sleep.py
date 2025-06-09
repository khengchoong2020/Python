#!/usr/bin/env python3

for i in range(0, 10):
    if (i //5) % 2 == 0:
        print(f'{i}')
        print(f'{(i // 5) % 2}')
        print(f"Webots active")
        # import time
        # time.sleep(i)
    else:
        print(f'{i}')
        print(f'{(i // 5) % 2}')
        print(f"Webots sleep")
        # import time
        # time.sleep(i)