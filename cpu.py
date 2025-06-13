# echo-16 cpu made by las-r on github
# v0.1

# cpu & memory class
class e16:
    # initialize
    def __init__(self, mhz=2, debug=False):
        self.mhz = mhz * 1000000
        self.debug = debug
        
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
        
    # math functions
    def add(self, x, y):
        res = x + y
        self.o = res > 65535
        return res & 65535
    def sub(self, x, y):
        res = x - y
        self.o = res < 0
        return res & 65535
        
    # step function
    def step(self):
        # unpack values
        mem = self.mem
        pc = self.pc
        a, b, c, d, e, f, g, h = self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h
        l, m, n, o = self.l, self.m, self.n, self.o
        stk = self.stk
        mem16 = self.mem16
        add = self.add
        sub = self.sub

        # get opcode
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
                    case 0: a = a
                    case 1: a = b
                    case 2: a = c
                    case 3: a = d
        
        # reassign values back to self
        self.mem = mem 
        self.pc = pc
        self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h = a, b, c, d, e, f, g, h
        self.stk = stk
