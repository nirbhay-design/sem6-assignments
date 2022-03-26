AREA sum, CODE
ENTRY
EXPORT __main
__main  MOV r0, #10
        MOV r1, #3
        ADD r0, r0, r1
stop    B stop
        END