// push argument 1 
@1
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1 
@SP
M=M-1
@THAT
D=A
@address
M=D
@SP
A=M
D=M
@address
A=M
M=D
// push constant 0 
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 0 
@SP
M=M-1
@0
D=A
@THAT
D=D+M
@address
M=D
@SP
A=M
D=M
@address
A=M
M=D
// push constant 1 
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 1 
@SP
M=M-1
@1
D=A
@THAT
D=D+M
@address
M=D
@SP
A=M
D=M
@address
A=M
M=D
// push argument 0 
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 2 
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub 
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
(UPDATESP0)
@SP
M=M+1
// pop argument 0 
@SP
M=M-1
@0
D=A
@ARG
D=D+M
@address
M=D
@SP
A=M
D=M
@address
A=M
M=D
// label MAIN_LOOP_START 
(null$MAIN_LOOP_START)
// push argument 0 
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
// if-goto COMPUTE_ELEMENT 
@SP
M=M-1
A=M
D=M
@null$COMPUTE_ELEMENT
D;JNE
// goto END_PROGRAM 
@null$END_PROGRAM
0;JMP
// label COMPUTE_ELEMENT 
(null$COMPUTE_ELEMENT)
// push that 0 
@0
D=A
@THAT
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push that 1 
@1
D=A
@THAT
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
// add 
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M+D
(UPDATESP1)
@SP
M=M+1
// pop that 2 
@SP
M=M-1
@2
D=A
@THAT
D=D+M
@address
M=D
@SP
A=M
D=M
@address
A=M
M=D
// push pointer 1 
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 1 
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// add 
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M+D
(UPDATESP2)
@SP
M=M+1
// pop pointer 1 
@SP
M=M-1
@THAT
D=A
@address
M=D
@SP
A=M
D=M
@address
A=M
M=D
// push argument 0 
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 1 
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub 
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
(UPDATESP3)
@SP
M=M+1
// pop argument 0 
@SP
M=M-1
@0
D=A
@ARG
D=D+M
@address
M=D
@SP
A=M
D=M
@address
A=M
M=D
// goto MAIN_LOOP_START 
@null$MAIN_LOOP_START
0;JMP
// label END_PROGRAM 
(null$END_PROGRAM)
