NUM_TO_GUESS = 10


def main():
    guess = input('Please enter your guess:')
    guess = int(guess)
    if guess > NUM_TO_GUESS:
        print('Too high')
    elif guess < NUM_TO_GUESS:
        print('Too low')
    else:
        print('You got it!')


if __name__ == '__main__':
    main()
