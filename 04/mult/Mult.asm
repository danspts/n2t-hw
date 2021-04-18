// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// num1 * num2 = num1 + num1 + ... + num1, num2 times
    // i = 0
    @i
    M=0
    // sum = 0
    @sum
    M=0
(LOOP)
    // if R1 - i == 0 , jump to END (if R1 == i jump to END)
    @R1
    D=M
    @i
    D=D-M
    @END
    D;JEQ
    // sum += R0 (will add R0 to sum R1 times, the "actual" multipication)
    @sum
    D=M
    @R0
    D=D+M
    @sum
    M=D
    // i += 1
    @i
    M=M+1
    // jump to start
    @LOOP
    0;JMP
(END)
    // R2 = sum
    @sum
    D=M
    @R2
    M=D
(REALEND)
    @REALEND
    0;JMP //infinite loop
