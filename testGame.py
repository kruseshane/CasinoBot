import numpy

redNums = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
blackNums = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
greenNums = [0]
probs = [0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267,
        0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267,
        0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267,
        0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267,
        0.0388]

colorBet = ""
numberBet = -1
red = 'red'
black = 'black'

bet = '!roulette red 50'

def verifyResult(val):
    if val in redNums:
        return 'Red ' + str(val)
    elif val in blackNums:
        return 'Black ' + str(val)
    elif val in greenNums:
        return 'Green ' + str(val)

# Split bet string into segments to handle
betSegs = bet.split(' ')
if betSegs[1].lower() == black or betSegs[1].lower() == red:
    colorBet = betSegs[1]
elif int(betSegs[1]) >= 0 and int(betSegs[1]) <= 36:
    numberBet = int(betSegs[1])
else:
    print('Cannot bet on ' + betSegs[1])

# Generate results
result = numpy.random.choice(numpy.arange(0, 37), p=probs)
finalResult = verifyResult(result)
print(finalResult)

finalResultSegs = finalResult.split(' ')
if betSegs[1] == colorBet:
    if betSegs[1].lower() == finalResultSegs[0].lower():
        payout = int(betSegs[2]) * 2
        print('You Win!  ----  Payout: ' + str(payout))
    else:
        print('You Lose...')
elif int(betSegs[1]) == numberBet:
    if int(betSegs[1]) == int(finalResultSegs[1]):
        print('You Win!')
        payout = int(betSegs[2]) * 35
        print('Payout: ' + str(payout))
    else:
        print("You Lose...")
