#for i in range(5):
   
   # print("knightngale")
#print ("done")

#for i in range(2,7):
 #   print("knight")
#print("yaay")  

#for i in range(4, 12, 2):
#    print(i)
#print("huraaay")    


for i in range (4):
    for j in range(i):
        print('#', end="")
    for k in range(i+1):
        print('*', end="")
    print()
x = int(input("please enter a number: "))
sum = 0
for i in range (1, x +1):
    sum +=i
print(f"the sum of the first {x} numbers is {sum}")

y = int(input("please enter the value of y: "))
sum = 0
for i in range(1, y+1):
    sum +=i
print(f"the sum of {y} is {sum}")



for i in range (6, 0, -1):
    print(i)
for i in reversed(range(1,9,1)):
    print(i)


