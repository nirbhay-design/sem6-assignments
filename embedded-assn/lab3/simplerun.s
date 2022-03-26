main   

       ldr     r0, =array1
       ldr     r1, =array2

       ldr     r2,[r0,#8]
       str     r2,[r1,#8]


array1 DCD     1,2,3
       DCD     4,5,6
       DCD     7,8,9

array2 DCD     0,0,0
       DCD     0,0,0
       DCD     0,0,0