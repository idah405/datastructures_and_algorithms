import random
def guess(x):
    random_number = random.randint (1, x)
    guess = 0
    while guess != random_number:
        guess= int(input(f'please enter a number between 1 and {x}: '))
        if guess < random_number:
            print('too low, please guess again')
        elif guess < random_number:
            print('too high, please guess again')
    print(f'yaaay, {random_number} is the correct number')
guess(10)

def computer_guess(x):
    low = 1
    high = x
    feedback = ''

    while feedback !='c':
        guess = random.randint(low,high)
        feedback = input(f'is the number {guess} too low(L), too high(H) or correcr(C)? ').lower()
        if feedback == 'l':
            low = guess - 1
        elif feedback == 'h':
            high= guess + 1
    print(f'the computer has guessed {guess} correctly!')
computer_guess(10)

