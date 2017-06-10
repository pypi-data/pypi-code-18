#!/usr/bin/python
import distribuPy as dpy

def main():
    dtc = dpy.DistributedTaskClient()
    ip = "192.168.1.6"
    port = 25565 #picked this at random
    dtc.setup(ip, port)
    print("Setup complete")
    dtc.run()

if __name__ == '__main__':
    main()
