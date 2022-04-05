from Crypto.Hash import SHA256
import random,time,os

def find_hash(text):
   new_hash = SHA256.new()
   new_hash.update(bytes(text,'utf-8'))
   return new_hash.hexdigest()

def condition(text1,text2,first_bits=4):
   return (text1[:first_bits] == text2[:first_bits])

def generate_random(num):
   text = list('abcdefghijklmnopqrstuvwxyz0123456789.')
   random_bits = ''.join(random.sample(text,num))
   return random_bits

def write_to_file(filename,iterations,array):
   with open(filename,'a') as f:
      string = f'iterations: {iterations} ----------\nlen: {len(array)}\n{" ".join(map(lambda x:str(x),array))}\n\n'
      f.write(string)

def generate_pairs(size1,size2):
   p1 = generate_random(size1) + '@iitj.ac.in'
   p2 = generate_random(size2) + "@iitj.ac.in"
   return p1,p2


h1 = find_hash('sharma.59@iitj.ac.in')
print(h1)

def n_calls(h1,match_value):
   t1 = time.perf_counter();

   l = []
   iterations = 0
   max_iterations = int(1e6)
   while (True):
      generated_value = generate_random(9) + '@iitj.ac.in'
      h2 = find_hash(generated_value)
      iterations += 1
      if (condition(h1,h2,match_value)):
         l.append(generated_value)
         break;
      if (iterations > max_iterations):
         break;

   if (len(l) > 0):
      write_to_file('output1.txt',iterations,l)
   else:
      print('len = 0')

   t2 = time.perf_counter()

   print(f'completed in {(t2-t1)/60:.2f} Mins')
   return iterations;

def find_pairs(values_match):
   t1 = time.perf_counter();

   l = []
   iterations = 0
   max_iterations = int(1e6)
   values_map = {}
   while (True):
      generated_value1 = generate_random(9) + "@iitj.ac.in"
      h1 = find_hash(generated_value1)
      iterations += 1
      if (h1[:values_match] in values_map):
         l.append((values_map[h1[:values_match]],generated_value1))
         break;
      else:
         values_map[h1[:values_match]] = generated_value1;
      if (iterations > max_iterations):
         break;

   # print(len(l))

   # print(l)
   if (len(l) > 0):
      write_to_file('output2.txt',iterations,l)
   else:
      print('len = 0')

   t2 = time.perf_counter()

   print(f'completed in {(t2-t1)/60:.2f} Mins')
   return iterations;

# check_iterations(h1)
filenames = ['output1.txt','output2.txt']
for filename in filenames:
   if (os.path.exists(filename)):
      os.remove(filename)

output1_iterations = 0
output2_iterations = 0
n = 10;
for i in range(n):
   output1_iterations += n_calls(h1,2) / n
   output2_iterations += find_pairs(2) / n

with open('output1.txt','a') as f:
   f.write(str(int(output1_iterations)))

with open('output2.txt','a') as f:
   f.write(str(int(output2_iterations)))




exit(0)


def check_iterations(h1):
   t1 = time.perf_counter();

   l = []
   iterations = int(1e6)
   for i in range(iterations):
      generated_value = generate_random(9) + '@iitj.ac.in'
      h2 = find_hash(generated_value)
      if (condition(h1,h2)):
         l.append(generated_value)

   # print(len(l))

   # print(l)
   if (len(l) > 0):
      write_to_file('output.txt',iterations,l)
   else:
      print('len = 0')

   t2 = time.perf_counter()

   print(f'completed in {(t2-t1)/60:.2f} Mins')

def check_pairs():
   t1 = time.perf_counter();

   l = []
   iterations = 0
   max_iterations = int(1e6)
   while (True):
      generated_value1,generated_value2 = generate_pairs(9,10)
      h1 = find_hash(generated_value1)
      h2 = find_hash(generated_value2)
      iterations += 1
      if (condition(h1,h2)):
         l.append((generated_value1,generated_value2))
         break;
      if (iterations > max_iterations):
         break;

   # print(len(l))

   # print(l)
   if (len(l) > 0):
      write_to_file('output3.txt',iterations,l)
   else:
      print('len = 0')

   t2 = time.perf_counter()

   print(f'completed in {(t2-t1)/60:.2f} Mins')
   return iterations;
