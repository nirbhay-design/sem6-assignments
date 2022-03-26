MAIN   MOV     r1, #2
       LDR     r2, =LABEL
       ldr     r3 , [r2,#4]
       END

LABEL  DCD     4,2
