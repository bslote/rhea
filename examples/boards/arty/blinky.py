
import myhdl
from myhdl import (Signal, intbv, always_seq, always_comb, concat)

from rhea.build.boards import get_board

@myhdl.block
def arty_blink(led, btn, sw, clock):
    maxcnt = int(clock.frequency)
    cnt = Signal(intbv(0, min=0, max=maxcnt))
    toggle = Signal(bool(0))
    nled = len(led)

    @always_seq(clock.posedge, reset=None)
    def rtl():
        if cnt == maxcnt-1:
            toggle.next = not toggle
            cnt.next = 0
        else:
            cnt.next = cnt + 1

    @always_comb
    def rtl_assign():
        if btn | sw:
            for i in range(nled):
                led.next[i] = btn[i] | sw[i];
        else:
            for i in range(nled):
                led.next[i] = toggle

    return rtl, rtl_assign


def build():
    brd = get_board('arty')
    assert brd
    flow = brd.get_flow(arty_blink)
    flow.run()


def main():
    build()


if __name__ == '__main__':
    main()
