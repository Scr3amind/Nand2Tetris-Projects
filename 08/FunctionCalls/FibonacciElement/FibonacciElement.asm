// Bootstrap Code
@256
D=A
@SP
M=D
// Calling Sys.init with 0 args
@null$return-address0
D=A
@SP
A=M
M=D
@SP
M=M+1
// pushing LCL segment
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// pushing ARG segment
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// pushing THIS segment
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// pushing THAT segment
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@5
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
// label return-address0 
(null$return-address0)
// End Call
// function Main.fibonacci
(Main.fibonacci)
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
// lt 
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@TRUE0
D;JLT
@FALSE0
0;JMP
(TRUE0)
@SP
A=M
M=-1
@UPDATESP0
0;JMP
(FALSE0)
@SP
A=M
M=0
@UPDATESP0
0;JMP
(UPDATESP0)
@SP
M=M+1
// if-goto IF_TRUE 
@SP
M=M-1
A=M
D=M
@Main.fibonacci$IF_TRUE
D;JNE
// goto IF_FALSE 
@Main.fibonacci$IF_FALSE
0;JMP
// label IF_TRUE 
(Main.fibonacci$IF_TRUE)
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
// Return
@LCL
D=M
@FRAME
M=D
@5
D=A
@FRAME
D=M-D
A=D
D=M
@RET
M=D
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
@ARG
D=M+1
@SP
M=D
@1
D=A
@FRAME
D=M-D
A=D
D=M
@THAT
M=D
@2
D=A
@FRAME
D=M-D
A=D
D=M
@THIS
M=D
@3
D=A
@FRAME
D=M-D
A=D
D=M
@ARG
M=D
@4
D=A
@FRAME
D=M-D
A=D
D=M
@LCL
M=D
@RET
A=M
0;JMP
// label IF_FALSE 
(Main.fibonacci$IF_FALSE)
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
(UPDATESP1)
@SP
M=M+1
// Calling Main.fibonacci with 1 args
@Main.fibonacci$return-address1
D=A
@SP
A=M
M=D
@SP
M=M+1
// pushing LCL segment
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// pushing ARG segment
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// pushing THIS segment
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// pushing THAT segment
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@6
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
// label return-address1 
(Main.fibonacci$return-address1)
// End Call
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
(UPDATESP2)
@SP
M=M+1
// Calling Main.fibonacci with 1 args
@Main.fibonacci$return-address2
D=A
@SP
A=M
M=D
@SP
M=M+1
// pushing LCL segment
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// pushing ARG segment
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// pushing THIS segment
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// pushing THAT segment
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@6
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
// label return-address2 
(Main.fibonacci$return-address2)
// End Call
// add 
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M+D
(UPDATESP3)
@SP
M=M+1
// Return
@LCL
D=M
@FRAME
M=D
@5
D=A
@FRAME
D=M-D
A=D
D=M
@RET
M=D
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
@ARG
D=M+1
@SP
M=D
@1
D=A
@FRAME
D=M-D
A=D
D=M
@THAT
M=D
@2
D=A
@FRAME
D=M-D
A=D
D=M
@THIS
M=D
@3
D=A
@FRAME
D=M-D
A=D
D=M
@ARG
M=D
@4
D=A
@FRAME
D=M-D
A=D
D=M
@LCL
M=D
@RET
A=M
0;JMP
// function Sys.init
(Sys.init)
// push constant 4 
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
// Calling Main.fibonacci with 1 args
@Sys.init$return-address3
D=A
@SP
A=M
M=D
@SP
M=M+1
// pushing LCL segment
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// pushing ARG segment
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// pushing THIS segment
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// pushing THAT segment
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@6
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
// label return-address3 
(Sys.init$return-address3)
// End Call
// label WHILE 
(Sys.init$WHILE)
// goto WHILE 
@Sys.init$WHILE
0;JMP
