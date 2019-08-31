"""CPU functionality."""

import sys

LDI = 0b10000010
HLT = 0b00000001
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] *256
        self.reg = [0] * 8
        self.pc = 0
        self.reg[7] = 255

    def load(self, file):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        program = []

        f = open(file, "r")
        fcont = f.readlines()
        for x in fcont:
            if x != "\n" and x[0] != "#":
                program.append(int(x[:8], 2))
        print(program)


        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        ir = self.pc 
        running = True

        while running:
            command = self.ram_read(ir)
            operand_a = self.ram_read(ir + 1)
            operand_b = self.ram_read(ir + 2)
            if command == LDI: 
                self.reg[operand_a] = int(operand_b)
                ir += 3
            elif command == PRN: 
                print(self.reg[operand_a])
                ir += 2
            elif command == MUL: 
                self.reg[operand_a]= self.reg[operand_a] * self.reg[operand_b]
                ir += 3
            elif command == ADD:
                self.reg[operand_a] = self.reg[operand_a] + self.reg[operand_b]

                ir += 3
            elif command == PUSH:
                sp = (self.reg[7]-1 )% 255
                self.reg[7] = (sp) % 255
                self.ram_write(self.reg[operand_a], sp) 
                ir += 2
            elif command == POP:
                sp = self.reg[7]
                value = self.ram_read(sp)
                self.reg[operand_a] = value
                self.reg[7] = (sp + 1) % 255
                ir +=2
            elif command == CALL:
                regAdd = self.ram_read(operand_a)
                addJump = self.reg[regAdd]
                
                next_command = ir + 2
                sp = (self.reg[7]-1 )% 255
                
                self.reg[7] = (sp) % 255
                self.ram_write(int(next_command), sp) 

                ir = addJump
            elif command == RET:
                sp = self.reg[7]
                return_address = self.ram_read(sp)
                self.reg[7] = (sp + 1) % 255

                ir = return_address
            elif command == HLT: 
                running = False
        
