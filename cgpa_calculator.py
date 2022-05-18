grades = [
    (3,10),
    (3,9),
    (1,10),
    (3,10),
    (1,10),
    (4,10),
    (1,7),

    (4,9),
    (4,8),
    (4,10),
    (1,7),
    (4,6),

    (4,10),
    (3,10),
    (4,10),
    (1,9),
    (1,8),
    (1,7),

    (3,8),
    (4,9),
    (3,9),
    (4,8),

    (4,9),
    (4,7),
    (2,9),
    (4,9),

    (3,8),
    (4,8),
    (3,9),
    (3,8),
    (4,9),
    (4,8),

    (3,10),
    (4,8),
    (3,8),
    (1.5,10),
    (4.5,8), # cn
    (4.5,10), #dl 
]

wt_sum = 0
total_credit = 0

for (credit, grade) in grades:
    total_credit += credit
    wt_sum += (credit * grade)

print(f"cgpa: {wt_sum/total_credit:.2f}")

sgpa = [
    (3,10),
    (4,8),
    (3,8),
    (1.5,10),
    (4.5,8), # cn
    (4.5,10), #dl 
]


wt_credit = 0
total_credit = 0
for credit,grade in sgpa:
    wt_credit += (credit * grade)
    total_credit += credit

print(f'sgpa {wt_credit/total_credit:.2f}')

