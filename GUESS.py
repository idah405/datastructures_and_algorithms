import random

def guess(x):
    random_number = random.randint(1, x)
    guess = 0
    while guess !=random_number:
        guess =int( input(f'please guess a number between 1 and {x}: '))

        if guess > random_number:
            print(' too high please try again')
        elif guess < random_number:
            print('too low please try again')   

    print(f'congratulations you guessed {random_number} right!')
guess(10)

def computer_guess(x):
    low = 1
    high = x
    feedback = ''
    while feedback !='c':
        if low !=high:
            guess = random.randint(low, high)
        else:
            low    
        guess = random.randint(low, high)   
        feedback = input(f'is {guess} too low(L), too high(H) or correct(C)?? ').lower()
        if feedback == 'h':
            high = guess+1
        elif feedback == 'l':
            low = guess-1

    print(f'you guessed {guess} correctly!')
computer_guess(10)        
        



    








    




