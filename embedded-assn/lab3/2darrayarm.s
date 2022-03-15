main   
       ldr     r0, =array1
       ldr     r1, =array2
       mov r2, #0
       mov r3, #0


loop1   
        cmp r2,#3
        bge endloop
        mov r3, #0
loop2
        cmp r3,#3
        bge contloop1
        ; r2 -> i , r3 ->j 
        ; todo -> r1[i][j] = r0[j][i]
        ; r4 -> address of r1[i,j]
        mov r4, #3
        mov r5, #4
        mul r4,r4,r2
        add r4,r4,r3
        mul r4,r4,r5
        add r4, r4,r1
        
        ; r5 -> address of r0[j,i]
        mov r6,#3
        mul r6,r3,r6
        add r6,r6,r2
        mul r6,r6,r5
        add r6,r6,r0
        ldr r7,[r6]
        ;storing the transpose
        str r7,[r4]

        add r3,r3,#1
        B loop2

contloop1
        add r2,r2,#1
        B loop1

endloop end

array1 DCD     1,2,3
       DCD     4,5,6
       DCD     7,8,9

array2 DCD     0,0,0
       DCD     0,0,0
       DCD     0,0,0





