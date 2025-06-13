import random

# echo-16 cpu made by las-r on github
# v0.3

class BreakLoop(Exception):
    pass

# cpu & memory class
class e16:
    # initialize
    def __init__(self, screen, width, height, scale, mhz=0.005, debug=False):
        self.screen = screen
        self.mhz = mhz * 1000000
        self.debug = debug
        self.disp = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]
        self.SCALE = scale
        
        # system states
        self.paused = False
        
        # memory
        self.mem = bytearray(65536)
        self.stk = []
        
        # pointers
        self.pc = 512
        self.i = 0
        self.j = 0
        
        # registers (16-bit)
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.f = 0
        self.g = 0
        self.h = 0
        
        # flags (1-bit)
        self.l = False # generic flag, can be set anytime
        self.m = False # generic flag, can be set anytime
        self.n = False # borrow / negative flag
        self.o = False # carry / overflow flag
        
        # timers
        self.dt = 0
        self.st = 0
        
    # memory functions
    def mem16(self, loc):
        return (self.mem[loc] << 8) + self.mem[(loc + 1) & 65535]
    def loadRom(self, filename):
        with open(filename, "rb") as rom:
            raw = bytearray(rom.read())
            data = raw.split(bytes([0xaf]), 1)
            data0 = data[0] + bytes([0xaf])
            self.mem[512:512 + len(data0)] = data0
            if len(data) > 1:
                self.mem[512 + len(data0):512 + len(data0) + len(data[1])] = data[1]
    
    # math functions
    def add(self, x, y):
        res = x + y
        self.o = res > 65535
        return res & 65535
    def sub(self, x, y):
        res = x - y
        self.o = res < 0
        return res & 65535
        
    # display functions
    def fillDisp(self, col):
        self.disp = [[col for _ in range(len(self.disp[0]))] for _ in range(len(self.disp))]
    def colConv(self, c):
        r = (c >> 5) & 3
        g = (c >> 2) & 7
        b = c & 3
        return (r * 255) // 3, (g * 255) // 7, (b * 255) // 3
    def putSpr(self, x, y):
        size = self.mem[self.i]
        h = size & 0x0F
        w = (size & 0xF0) >> 4
        for row in range(h):
            for umn in range(w):
                pix = self.mem[self.i + 1 + row * w + umn]
                if pix & 0b10000000:
                    col = pix >> 1
                    self.disp[y + row][x + umn] = self.colConv(col)              
    
    # execution functions
    def step(self):
        dt = self.dt
        if not self.paused:
            # unpack values
            paused = self.paused
            mem = self.mem
            pc, i, j = self.pc, self.i, self.j
            a, b, c, d, e, f, g, h = self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h
            l, m, n, o = self.l, self.m, self.n, self.o
            dt, st = self.dt, self.st
            stk = self.stk
            disp = self.disp
            mem16 = self.mem16
            add = self.add
            sub = self.sub
            fillDisp = self.fillDisp
            putSpr = self.putSpr
            colConv = self.colConv
            
            print(f"running opc {hex(mem[pc])} at {pc}")

            # get opcode
            #print(pc)
            #print(len(mem))
            opc = mem[pc]
            pc += 1
            o1 = opc >> 4
            o2 = opc & 0x0F

            # match and execute
            match o1:
                case 0:
                    match o2:
                        case 1: a = mem16(a)
                        case 2: a = mem16(b)
                        case 3: a = mem16(c)
                        case 4: a = mem16(d)
                        case 5: a = mem16(e)
                        case 6: a = mem16(f)
                        case 7: a = mem16(g)
                        case 8: a = mem16(h)
                        case 9:
                            stk.append(pc)
                            pc = a
                        case 10:
                            stk.append(pc)
                            pc = a
                        case 11:
                            if l:
                                pc = a
                        case 12:
                            if not l:
                                pc = a
                        case 13:
                            if m:
                                pc = a
                        case 14:
                            if not m:
                                pc = a
                        case 15: pc = stk.pop()
                case 1:
                    match o2:
                        case 0: pc = a
                        case 1: a = b
                        case 2: a = c
                        case 3: a = d
                        case 4: a = e
                        case 5: a = f
                        case 6: a = g
                        case 7: a = h
                        case 8: b = a
                        case 9: pc = b
                        case 10: b = c
                        case 11: b = d
                        case 12: b = e
                        case 13: b = f
                        case 14: b = g
                        case 15: b = h
                case 2:
                    match o2:
                        case 0: c = a
                        case 1: c = b
                        case 2: pc = c
                        case 3: c = d
                        case 4: c = e
                        case 5: c = f
                        case 6: c = g
                        case 7: c = h
                        case 8: d = a
                        case 9: d = b
                        case 10: d = c
                        case 11: pc = d
                        case 12: d = e
                        case 13: d = f
                        case 14: d = g
                        case 15: d = h
                case 3:
                    match o2:
                        case 0: e = a
                        case 1: e = b
                        case 2: e = c
                        case 3: e = d
                        case 4: pc = e
                        case 5: e = f
                        case 6: e = g
                        case 7: e = h
                        case 8: f = a
                        case 9: f = b
                        case 10: f = c
                        case 11: f = d
                        case 12: f = e
                        case 13: pc = f
                        case 14: f = g
                        case 15: f = h
                case 4:
                    match o2:
                        case 0: g = a
                        case 1: g = b
                        case 2: g = c
                        case 3: g = d
                        case 4: g = e
                        case 5: g = f
                        case 6: pc = g
                        case 7: g = h
                        case 8: h = a
                        case 9: h = b
                        case 10: h = c
                        case 11: h = d
                        case 12: h = e
                        case 13: h = f
                        case 14: h = g
                        case 15: pc = h
                case 5:
                    match o2:
                        case 0: a = add(a, 1)
                        case 1: b = add(b, 1)
                        case 2: c = add(c, 1)
                        case 3: d = add(d, 1)
                        case 4: e = add(e, 1)
                        case 5: f = add(f, 1)
                        case 6: g = add(g, 1)
                        case 7: h = add(h, 1)
                        case 8: a = sub(a, 1)
                        case 9: b = sub(b, 1)
                        case 10: c = sub(c, 1)
                        case 11: d = sub(d, 1)
                        case 12: e = sub(e, 1)
                        case 13: f = sub(f, 1)
                        case 14: g = sub(g, 1)
                        case 15: h = sub(h, 1)
                case 6:
                    match o2:
                        case 0: a = add(a, a)
                        case 1: b = add(b, a)
                        case 2: c = add(c, a)
                        case 3: d = add(d, a)
                        case 4: e = add(e, a)
                        case 5: f = add(f, a)
                        case 6: g = add(g, a)
                        case 7: h = add(h, a)
                        case 8: a = add(a, b)
                        case 9: b = add(b, b)
                        case 10: c = add(c, b)
                        case 11: d = add(d, b)
                        case 12: e = add(e, b)
                        case 13: f = add(f, b)
                        case 14: g = add(g, b)
                        case 15: h = add(h, b)
                case 7:
                    match o2:
                        case 0: a = (a << 1) & 65535
                        case 1: b = sub(b, a)
                        case 2: c = sub(c, a)
                        case 3: d = sub(d, a)
                        case 4: e = sub(e, a)
                        case 5: f = sub(f, a)
                        case 6: g = sub(g, a)
                        case 7: h = sub(h, a)
                        case 8: a = sub(a, b)
                        case 9: a = (a << 1) & 65535
                        case 10: c = sub(c, b)
                        case 11: d = sub(d, b)
                        case 12: e = sub(e, b)
                        case 13: f = sub(f, b)
                        case 14: g = sub(g, b)
                        case 15: h = sub(h, b)
                case 8:
                    match o2:
                        case 0:
                            a = mem16(pc)
                            pc += 2
                        case 1: b |= a
                        case 2: c |= a
                        case 3: d |= a
                        case 4: e |= a
                        case 5: f |= a
                        case 6: g |= a
                        case 7: h |= a
                        case 8: a |= b
                        case 9:
                            b = mem16(pc)
                            pc += 2
                        case 10: c |= b
                        case 11: d |= b
                        case 12: e |= b
                        case 13: f |= b
                        case 14: g |= b
                        case 15: h |= b
                case 9:
                    match o2:
                        case 0: a, b = b, a
                        case 1: b ^= a
                        case 2: c ^= a
                        case 3: d ^= a
                        case 4: e ^= a
                        case 5: f ^= a
                        case 6: g ^= a
                        case 7: h ^= a
                        case 8: a ^= b
                        case 9: g, h = h, g
                        case 10: c ^= b
                        case 11: d ^= b
                        case 12: e ^= b
                        case 13: f ^= b
                        case 14: g ^= b
                        case 15: h ^= b
                case 10:
                    match o2:
                        case 0: dt = a
                        case 1: dt = b
                        case 2: dt = c
                        case 3: dt = d
                        case 4: dt = e
                        case 5: dt = f
                        case 6: dt = g
                        case 7: dt = h
                        case 8: st = a
                        case 9: st = b
                        case 10: a = random.randint(0, 65535)
                        case 11:
                            if not l:
                                pc += 1
                        case 12:
                            if not m:
                                pc += 1
                        case 13:
                            if not n:
                                pc += 1
                        case 14:
                            if not o:
                                pc += 1
                        case 15:
                            raise BreakLoop
                case 11:
                    match o2:
                        case 0:
                            if not dt:
                                pc += 1
                        case 1: b &= a
                        case 2: c &= a
                        case 3: d &= a
                        case 4: e &= a
                        case 5: f &= a
                        case 6: g &= a
                        case 7: h &= a
                        case 8: a &= b
                        case 9:
                            if not dt:
                                pc += 1
                        case 10: c &= b
                        case 11: d &= b
                        case 12: e &= b
                        case 13: f &= b
                        case 14: g &= b
                        case 15: h &= b
                case 12:
                    match o2:
                        case 0: a = ~a
                        case 1: b = ~b
                        case 2: c = ~c
                        case 3: d = ~d
                        case 4: e = ~e
                        case 5: f = ~f
                        case 6: g = ~g
                        case 7: h = ~h
                        case 8: pc += a
                        case 9: pc += b
                        case 10: pc += c
                        case 11: pc += d
                        case 12: pc += e
                        case 13: pc += f
                        case 14: pc += g
                        case 15: pc += h
                case 13:
                    match o2:
                        case 0: i = a
                        case 1: i = b
                        case 2: i = c
                        case 3: i = d
                        case 4: i = e
                        case 5: i = f
                        case 6: i = g
                        case 7: i = h
                        case 8: putSpr(a, b)
                        case 9: putSpr(c, d)
                        case 10: putSpr(e, f)
                        case 11: putSpr(g, h)
                        case 12: j = a
                        case 13: b = a
                        case 14:
                            col = mem[pc]
                            pc += 1
                            fillDisp(colConv(col & 0b01111111))
                        case 15: fillDisp((0, 0, 0))
                case 14:
                    match o2:
                        case 0:
                            if not a:
                                pc += 1
                        case 1:
                            if not b:
                                pc += 1
                        case 2:
                            if not c:
                                pc += 1
                        case 3:
                            if not d:
                                pc += 1
                        case 4:
                            if not e:
                                pc += 1
                        case 5:
                            if not f:
                                pc += 1
                        case 6:
                            if not g:
                                pc += 1
                        case 7:
                            if not h:
                                pc += 1
                        case 8:
                            if a:
                                pc += 1
                        case 9:
                            if b:
                                pc += 1
                        case 10:
                            if c:
                                pc += 1
                        case 11:
                            if d:
                                pc += 1
                        case 12:
                            if e:
                                pc += 1
                        case 13:
                            if f:
                                pc += 1
                        case 14:
                            if g:
                                pc += 1
                        case 15:
                            if h:
                                pc += 1
                case 15:
                    match o2:
                        case 0: l = True
                        case 1: m = True
                        case 2: l = False
                        case 3: m = False
                        case 4: l = not l
                        case 5: m = not m
                        case 6:
                            if not a == b:
                                pc += 1
                        case 7:
                            if not c == d:
                                pc += 1
                        case 8:
                            if not e == f:
                                pc += 1
                        case 9:
                            if not g == h:
                                pc += 1
                        case 10:
                            if a == b:
                                pc += 1
                        case 11:
                            if c == d:
                                pc += 1
                        case 12:
                            if e == f:
                                pc += 1
                        case 13:
                            if g == h:
                                pc += 1
                        case 14:
                            paused = True
                        case 15:
                            l = False
                            m = False
                            n = False
                            o = False
            
            # repack values
            self.paused = paused
            self.mem = mem
            self.pc, self.i, self.j = pc, i, j
            self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h = a, b, c, d, e, f, g, h
            self.l, self.m, self.n, self.o = l, m, n, o
            self.dt, self.st = dt, st
            self.stk = stk
            self.mem16 = mem16
        else:
            if not dt:
                paused = False
