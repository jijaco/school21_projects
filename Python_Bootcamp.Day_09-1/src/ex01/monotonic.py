import ctypes
import time


class timespeck(ctypes.Structure):
    _fields_ = [
        ('tv_sec', ctypes.c_ulonglong),
        ('tv_nsec', ctypes.c_long)
    ]


def monotonic():
    t_speck = timespeck()
    std = ctypes.CDLL('libc.so.6')
    std.clock_gettime(4, ctypes.pointer(t_speck))
    return t_speck.tv_sec + round(float(('0.' + str(t_speck.tv_nsec))))


if __name__ == '__main__':
    print(monotonic())
    print(time.monotonic())
