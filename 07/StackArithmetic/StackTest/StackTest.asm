@256
D=M
@SP
M=D
@LCL
D=M
@14
M=D
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
D=M
@LCL
M=D
@5
D=D-A
ARG
M=D
(Sys.init)
0;JMP
(Sys.init.call.0)
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@COMPARE_T_0
D;JEQ
@SP
A=M
M=0
@COMPARE_F_0
0;JMP
(COMPARE_T_0)
@SP
A=M
M=-1
(COMPARE_F_0)
@SP
M=M+1
@SP
M=M+1
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@COMPARE_T_1
D;JEQ
@SP
A=M
M=0
@COMPARE_F_1
0;JMP
(COMPARE_T_1)
@SP
A=M
M=-1
(COMPARE_F_1)
@SP
M=M+1
@SP
M=M+1
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@COMPARE_T_2
D;JEQ
@SP
A=M
M=0
@COMPARE_F_2
0;JMP
(COMPARE_T_2)
@SP
A=M
M=-1
(COMPARE_F_2)
@SP
M=M+1
@SP
M=M+1
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@COMPARE_T_3
D;JLT
@SP
A=M
M=0
@COMPARE_F_3
0;JMP
(COMPARE_T_3)
@SP
A=M
M=-1
(COMPARE_F_3)
@SP
M=M+1
@SP
M=M+1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@COMPARE_T_4
D;JLT
@SP
A=M
M=0
@COMPARE_F_4
0;JMP
(COMPARE_T_4)
@SP
A=M
M=-1
(COMPARE_F_4)
@SP
M=M+1
@SP
M=M+1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@COMPARE_T_5
D;JLT
@SP
A=M
M=0
@COMPARE_F_5
0;JMP
(COMPARE_T_5)
@SP
A=M
M=-1
(COMPARE_F_5)
@SP
M=M+1
@SP
M=M+1
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@COMPARE_T_6
D;JGT
@SP
A=M
M=0
@COMPARE_F_6
0;JMP
(COMPARE_T_6)
@SP
A=M
M=-1
(COMPARE_F_6)
@SP
M=M+1
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@COMPARE_T_7
D;JGT
@SP
A=M
M=0
@COMPARE_F_7
0;JMP
(COMPARE_T_7)
@SP
A=M
M=-1
(COMPARE_F_7)
@SP
M=M+1
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@COMPARE_T_8
D;JGT
@SP
A=M
M=0
@COMPARE_F_8
0;JMP
(COMPARE_T_8)
@SP
A=M
M=-1
(COMPARE_F_8)
@SP
M=M+1
@SP
M=M+1
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M+D
@SP
M=M+1
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
M=M+1
@SP
M=M-1
@SP
A=M
M=-M
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M&D
@SP
M=M+1
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M|D
@SP
M=M+1
@SP
M=M-1
@SP
A=M
M=!M
@SP
M=M+1
