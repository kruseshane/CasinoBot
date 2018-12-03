import praw
import sqlite3
import os.path
import time
import numpy

reddit = praw.Reddit('Reddit_Casino')

# LasReddit variables
SIGNUP = '!signup'
DB_PATH = 'database/master.sqlite'
INITIAL_AMOUNT = 1000
WELCOME_MESSAGE = 'Welcome to r/lasreddittesting! You have been given 1000 credits to use on the various games. Good Luck!'
BALANCE_MESSAGE = 'You must have 100 credits or less to request more. Your current credit count is: '
IN_DB_MSG = 'You are already signed up!'
SUBREDDIT = 'lasreddittesting'
BOSS = 'lasreddit_boss'
ROULETTE_POST = 'ROULETTE CHECKPOINT 1'

def setUpDB():
    global cursor
    global db
    if not os.path.isfile(DB_PATH):
        print('Database file not found, creating file')
        db = sqlite3.connect(DB_PATH)
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE users(username varchar(25), total int)''')
        db.commit()
    else:
        print('Database file found')
        db = sqlite3.connect(DB_PATH)
        cursor = db.cursor()


def checkInbox():
    print('Checking inbox')
    unreadMessages = reddit.inbox.unread()
    for message in unreadMessages:
        if message.body == SIGNUP:
            author = message.author.name
            if verifyPlayer(author) == False:
                print(author + ' signed up')
                cursor.execute('''INSERT INTO users(username, total) values(?, ?)''', (author, INITIAL_AMOUNT,))
                db.commit()
                message.mark_read()
                message.reply(WELCOME_MESSAGE)
            else:
                print(author + ' tried to sign up again')
                message.mark_read()
                message.reply(IN_DB_MSG)
        elif message.body == '!morecredits':
            author = message.author.name
            print(author + ' is requesting more credits')
            cursor.execute('''SELECT * FROM users WHERE username=?''', (author,))
            data = cursor.fetchone()
            balance = data[1]
            if balance <= 100:
                newBal = balance + 1000
                print(newBal)
                cursor.execute('''UPDATE users SET total=? WHERE username=?''', (newBal, author))
                db.commit()
            else:
                message.mark_read()
                message.reply(BALANCE_MESSAGE + str(balance))
        elif message.body == '!balance':
            author = message.author.name
            print(author + 'is requesting to see their balance')
            cursor.execute('''SELECT * FROM users WHERE username = ?''', (author,))
            data = cursor.fetchone()
            message.mark_read()
            message.reply('You currently have a balance of ' + str(data[1]) + ' credits')


def showUsersTable():
    cursor.execute('''SELECT * FROM users''')
    all = cursor.fetchall();
    for entry in all:
        print('{0} : {1}'.format(entry[0], entry[1]))
    db.commit()

def updateBalance(user, bool, betAmount, payout):
    if bool == True:
        cursor.execute('''SELECT * FROM users WHERE username = ?''', (user,))
        data = cursor.fetchone()
        newBalance = (data[1] - int(betAmount)) + payout
        cursor.execute('''UPDATE users SET total = ? WHERE username = ?''', (newBalance, user))
        db.commit()
    else:
        cursor.execute('''SELECT * FROM users WHERE username = ?''', (user,))
        data = cursor.fetchone()
        newBalance = data[1] - int(betAmount)
        cursor.execute('''UPDATE users SET total = ? WHERE username = ?''', (newBalance, user))
        db.commit()

def playRoulette(bet, player): # Ex. !roulette Black 100 or !roulette 18 100
    redNums = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    blackNums = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    greenNums = [0]
    thirds = ['1st12', '2nd12', '3rd12']
    probs = [0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267,
            0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267,
            0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267,
            0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267,
            0.0388]
    colorBet = ""
    numberBet = -1
    thirdsBet = ""
    red = 'red'
    black = 'black'

    # Split bet string into segments to handle
    if bet[1].lower() == black or bet[1].lower() == red:
        colorBet = bet[1]
    elif bet[1] in thirds:
        thirdsBet = bet[1]
    elif int(bet[1]) >= 0 and int(bet[1]) <= 36:
        numberBet = int(bet[1])
    else:
        return 'Cannot make a bet on ' + bet[1]

    # Generate results
    result = numpy.random.choice(numpy.arange(0, 37), p=probs)

    # Verify results
    if result in redNums:
        finalResult = 'Red ' + str(result)
    elif result in blackNums:
        finalResult = 'Black ' + str(result)
    elif result in greenNums:
        finalResult = 'Green ' + str(result)

    finalResultSegs = finalResult.split(' ')
    if bet[1] == colorBet: # If the player bets Red or Black (Note: player cannot bet on Green)
        if bet[1].lower() == finalResultSegs[0].lower():
            payout = int(bet[2]) * 2 # 2:1 odds
            updateBalance(player, True, bet[2], payout)
            return finalResult + '\nYou Win!  ----  Payout: ' + str(payout)
        else:
            updateBalance(player, False, bet[2], 0)
            return finalResult + '\nYou Lose...'
    elif bet[1] == thirdsBet: # If the player bets one of the dozens (1st 12, 2nd 12, 3rd 12)
        if bet[1] == '1st12' and (result >= 1 and result <= 12):
            payout = int(bet[2]) * 2 # 2:1 odds
            updateBalance(player, True, bet[2], payout)
            return finalResult + '\nYou Win!  ----  Payout: ' + str(payout)
        elif bet[1] == '2nd12' and (result >= 13 and result <= 24):
            payout = int(bet[2]) * 2 # 2:1 odds
            updateBalance(player, True, bet[2], payout)
            return finalResult + '\nYou Win!  ----  Payout: ' + str(payout)
        elif bet[1] == '3rd12' and (result >= 25 and result <= 36):
            payout = int(bet[2]) * 2 # 2:1 odds
            updateBalance(player, True, bet[2], payout)
            return finalResult + '\nYou Win!  ----  Payout: ' + str(payout)
        else:
            updateBalance(player, False, bet[2], 0)
            return finalResult + '\nYou Lose...'
    elif int(bet[1]) == numberBet: # If the player bets a number (1, 2, 3, ...)
        if int(bet[1]) == result:
            payout = int(bet[2]) * 35 # 35:1 odds
            updateBalance(player, True, bet[2], payout)
            return finalResult + '\nYou Win!  ----  Payout: ' + str(payout)
        else:
            updateBalance(player, False, bet[2], 0)
            return finalResult + '\nYou Lose...'

def verifyPlayer(player):
    cursor.execute('''SELECT * FROM users WHERE username = ?''', (player,))
    data = cursor.fetchone()
    if data is not None and data[0] == player:
        return True
    else:
        return False

def verifyBetAmount(player, betAmount):
    cursor.execute('''SELECT * FROM users WHERE username = ?''', (player,))
    data = cursor.fetchone()
    if data[1] - int(betAmount) < 0:
        return False
    else:
        return True

def findRouletteGame(post):
    replyComment = ''
    print('Searching ' + post + ' for roulette games')
    subreddit = reddit.subreddit(SUBREDDIT)
    for comment in subreddit.stream.comments(pause_after=1, skip_existing=True):
        if comment is None or comment.author.name == BOSS:
            checkInbox()
            continue
        message = comment.body.split(' ')
        if message[0] == '!roulette':
            print('Roulette game found')
            print(comment.body)
            player = comment.author.name
            amount = int(message[2])
            if verifyPlayer(player) == True:
                if verifyBetAmount(player, amount) == True:
                    print(player + ' verified')
                    if message[0] == '!roulette':
                        result = playRoulette(message, player)
                        replyComment = comment.reply(result)
                        replyComment.mod.distinguish(how='yes', sticky=False)
                else:
                    replyComment = comment.reply('You lack the amount of credits to place this bet. Please message /u/lasreddit_boss !balance to see your current balance')
                    replyComment.mod.distinguish(how='yes', sticky=False)
            else:
                comment.reply('You are not signed up yet. Please message /u/lasreddit_boss !signup to signup and start playing!')
        else:
            print('Syntax Err')
            comment.reply('Incorrect Syntax Ex: !roulette Black 150')
            db.commit()

def scanGames():
    subreddit = reddit.subreddit(SUBREDDIT)
    for submission in subreddit.top(limit=None):
        postTitle = submission.title
        if postTitle == ROULETTE_POST:
            findRouletteGame(postTitle)

setUpDB()
showUsersTable()

while (True):
    scanGames()
    print('Sleeping for 10 seconds')
    time.sleep(10)
