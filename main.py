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
ROULETTE_POST = 'ROULETTE PUBLIC TEST 1'

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

def getBalance(player):
    cursor.execute('''SELECT total FROM users WHERE username = ?''', (player,))
    data = cursor.fetchone()
    return data[0]

def setBalance(player, amount):
    cursor.execute('''UPDATE users SET total = ? WHERE username = ?''', (amount, player))
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

def genPayout(betAmt, odds, player, bet):
    payout = betAmt * odds
    updateBalance(player, True, betAmt, payout)
    return payout

def playRoulette(bet, player): # Ex. "!roulette Black 100" or "!roulette 18 100" or "!roulette black,100 even,100
    redNums = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    blackNums = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    greenNums = [0]
    thirds = ['1st12', '2nd12', '3rd12']
    halves = ['1stHalf', '2ndHalf']
    probs = [0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267,
            0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267,
            0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267,
            0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267, 0.0267,
            0.0388]
    finalResult = ""
    result = 0

    # Split bet string into segments to handle

    def genResult():
        # Generate results
        return numpy.random.choice(numpy.arange(0, 37), p=probs)

    def verifyResult(result):
        # Verify results
        if result in redNums:
            return 'Red ' + str(result)
        elif result in blackNums:
            return 'Black ' + str(result)
        elif result in greenNums:
            return 'Green ' + str(result)
        else:
            return None

    # returns a list containing payout (if applicable) and reply string
    def datLogicTho(bet, finalResult, player, betCount):
        returnStr = ''
        if len(bet) == 3:
            bet = [bet[1].replace(',', ''), bet[2]]
        theMainBet = str(bet[0])
        wager = int(bet[1].replace(',', ''))
        print(theMainBet + ' ' + str(wager))
    	# Logic behind payouts
        finalResultSegs = finalResult.split(' ')
        if theMainBet.lower() == 'black' or theMainBet.lower() == 'red': # If the player bets Red or Black (Note: player cannot bet on Green)
            if theMainBet.lower() == finalResultSegs[0].lower():
                payout = genPayout(wager, 2, player, bet) # 1:1 odds
                returnStr = '> Bet ' + str(betCount) + ': Won, +' + str(wager) + '\n\n'
            else:
                updateBalance(player, False, wager, 0)
                returnStr = '> Bet ' + str(betCount) + ': Lost, -'  + str(wager) + '\n\n'
        elif theMainBet in thirds: # If the player bets one of the dozens (1st 12, 2nd 12, 3rd 12)
            if theMainBet == '1st12' and (result >= 1 and result <= 12):
                payout = genPayout(wager, 3, player, bet) # 2:1 odds
                returnStr = '> Bet ' + str(betCount) + ': Won, +' + str(wager) + '\n\n'
            elif theMainBet == '2nd12' and (result >= 13 and result <= 24):
                payout = genPayout(wager, 3, player, bet) # 2:1 odds
                returnStr = '> Bet ' + str(betCount) + ': Won, +' + str(wager) + '\n\n'
            elif theMainBet == '3rd12' and (result >= 25 and result <= 36):
                payout = genPayout(wager, 3, player, bet) # 2:1 odds
                returnStr = '> Bet ' + str(betCount) + ': Won, +' + str(wager) + '\n\n'
            else:
                updateBalance(player, False, wager, 0)
                returnStr = '> Bet ' + str(betCount) + ': Lost, -'  + str(wager) + '\n\n'
        elif theMainBet in halves: # If the player bets on one of the halves
            if theMainBet == '1stHalf' and (result >= 1 and result <= 18):
                payout = genPayout(wager, 2, player, bet) # 1:1 odds
                returnStr = '> Bet ' + str(betCount) + ': Won, +' + str(wager) + '\n\n'
            elif theMainBet == '2ndHalf' and (result >= 19 and result <= 36):
                payout = genPayout(wager, 2, player, bet) # 1:1 odds
                returnStr = '> Bet ' + str(betCount) + ': Won, +' + str(wager) + '\n\n'
            else:
                updateBalance(player, False, wager, 0)
                returnStr = '> Bet ' + str(betCount) + ': Lost, -'  + str(wager) + '\n\n'
        elif theMainBet.lower() == 'even' or theMainBet.lower() == 'odd': # If player bets for result to be an odd or even number (0 is automatic win)
            if str(bet[1].lower()) == 'odd':
                if result % 2 == 1:
                    payout = genPayout(wager, 2, player, bet) # 1:1 odds
                    returnStr = '> Bet ' + str(betCount) + ': Won, +' + str(wager) + '\n\n'
                else:
                    updateBalance(player, False, wager, 0)
                    returnStr = '> Bet ' + str(betCount) + ': Lost, -'  + str(wager) + '\n\n'
            elif theMainBet.lower() == 'even':
                if result % 2 == 0:
                    payout = genPayout(wager, 2, player, bet) # 1:1 odds
                    returnStr = '> Bet ' + str(betCount) + ': Won, +' + str(wager) + '\n\n'
                else:
                    updateBalance(player, False, wager, 0)
                    returnStr = '> Bet ' + str(betCount) + ': Lost, -'  + str(wager) + '\n\n'
        elif int(theMainBet) >= 0 and int(theMainBet) <= 36: # If the player bets a number (1, 2, 3, ...)
            if int(theMainBet) == result:
                payout = genPayout(wager, 35, player, bet) # 35:1 odds
                returnStr = '> Bet ' + str(betCount) + ': Won, +' + str(wager) + '\n\n'
            else:
                updateBalance(player, False, wager, 0)
                returnStr = '> Bet ' + str(betCount) + ': Lost, -'  + str(wager) + '\n\n'
        else:
            print('error in datLogicTho in playRoulette')
        return returnStr

    result = genResult() # only do once
    finalResult = verifyResult(result)
    replyStr = '> Result: ' + finalResult + '\n\n'
    print(replyStr)
    bet = [str(x) for x in bet]
    # Handle one bet or multiple bets
    if ',' in bet[1]:
        count = 0
        for i in range(1, len(bet)): # handle each bet seperately
            print('Bet found: ' + bet[i])
            if ',' in bet[i]:
                count = count + 1
                data = bet[i].split(',') # black,100 -> [black, 100]
                if (len(data) > 2): # If wager includes commas
                    wager = ''
                    for x in range(1, len(data)):
                        wager += data[x]
                    print (wager)
                    data = [data[0], wager]
                mainBet = str(data[0])
                if mainBet.lower() == 'black' or mainBet.lower() == 'red':
                    replyStr += datLogicTho(data, finalResult, player, count)
                elif mainBet in thirds:
                    replyStr += datLogicTho(data, finalResult, player, count)
                elif mainBet in halves:
                    replyStr += datLogicTho(data, finalResult, player, count)
                elif mainBet.lower() == 'even' or mainBet.lower() == 'odd':
                    replyStr += datLogicTho(data, finalResult, player, count)
                elif int(data[0]) >= 0 and int(data[0]) <= 36:
                    replyStr += datLogicTho(data, finalResult, player, count)
                else:
                    replyStr += 'Cannot make a bet on ' + bet[1] + '\n'
            else:
                replyStr += 'Invalid betting format'
    else:
        if bet[1].lower() == 'black' or bet[1].lower() == 'red':
            replyStr += datLogicTho(bet, finalResult, player, 1)
        elif bet[1] in thirds:
            replyStr += datLogicTho(bet, finalResult, player, 1)
        elif bet[1] in halves:
            replyStr += datLogicTho(bet, finalResult, player, 1)
        elif bet[1].lower() == 'even' or bet[1].lower() == 'odd':
            replyStr += datLogicTho(bet, finalResult, player, 1)
        elif int(bet[1]) >= 0 and int(bet[1]) <= 36:
            replyStr += datLogicTho(bet, finalResult, player, 1)
        else:
            replyStr = 'Cannot make a bet on ' + bet[1] + '\n'

    return replyStr

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
        if message[0] == '!roulette' and ',' not in message[1]:
            print('Roulette game found')
            print(comment.body)
            player = comment.author.name
            amount = int(message[2].replace(',', ''))
            if verifyPlayer(player) == True:
                initialBalance = getBalance(player)
                if verifyBetAmount(player, amount) == True:
                    print(player + ' verified')
                    result = playRoulette(message, player)
                    replyComment = 'You bet a total of ' + str(amount) + ' credits\n\n'
                    replyComment += result
                    newBalance = getBalance(player)
                    netPayout = newBalance - initialBalance
                    if (netPayout >= 0):
                        replyComment += 'You won a total of ' + str(netPayout) + ' credits\n\n'
                        replyComment += 'Current Balance: ' + str(newBalance)
                    else:
                        replyComment += 'You lost a total of ' + str(abs(netPayout)) + ' credits\n\n'
                        replyComment += 'Current Balance: ' + str(newBalance)
                    repComm = comment.reply(replyComment)
                    repComm.mod.distinguish(how='yes', sticky=False)
                else:
                    repComm = comment.reply('You lack the amount of credits to place this bet. Please message /u/lasreddit_boss !balance to see your current balance')
                    repComm.mod.distinguish(how='yes', sticky=False)
            else:
                comment.reply('You are not signed up yet. Please message /u/lasreddit_boss !signup to signup and start playing!')
        elif message[0] == '!roulette' and ',' in message[1]:
            print('Roulette game found')
            print(comment.body)
            player = comment.author.name
            if verifyPlayer(player) == True:
                initialBalance = getBalance(player)
                sum = 0
                for i in range(1, len(message)):
                    if ',' in message[i]:
                        data = message[i].split(',')
                        if len(data) > 2:
                            wager = ''
                            for x in range(1, len(data)):
                                wager += data[x]
                            sum = sum + int(wager)
                        else:
                            sum = sum + int(data[1]) # add up bet amounts
                if verifyBetAmount(player, sum) == True:
                    print(player + ' verified')
                    result = playRoulette(message, player)
                    replyComment = 'You bet a total of ' + str(sum) + ' credits\n\n'
                    replyComment += result
                    newBalance = getBalance(player)
                    netPayout = newBalance - initialBalance
                    if (netPayout >= 0):
                        replyComment += 'You won a total of ' + str(netPayout) + ' credits\n\n'
                        replyComment += 'Current Balance: ' + str(newBalance)
                    else:
                        replyComment += 'You lost a total of ' + str(abs(netPayout)) + ' credits\n\n'
                        replyComment += 'Current Balance: ' + str(newBalance)
                    repComm = comment.reply(replyComment)
                    repComm.mod.distinguish(how='yes', sticky=False)
                else:
                    repComm = comment.reply('You lack the amount of credits to place this bet. Please message /u/lasreddit_boss !balance to see your current balance')
                    repComm.mod.distinguish(how='yes', sticky=False)
            else:
                comment.reply('You are not signed up yet. Please message /u/lasreddit_boss !signup to signup and start playing!')
        else:
            print('Syntax Err')
            comment.reply('Incorrect Syntax: Refer to the rules for the game')
            db.commit()

def scanGames():
    subreddit = reddit.subreddit(SUBREDDIT)
    for submission in subreddit.top(limit=None):
        postTitle = submission.title
        if postTitle == ROULETTE_POST:
            findRouletteGame(postTitle)

setUpDB()
#setBalance('kproggsu', 1000000)
showUsersTable()
scanGames()

"""
!roulette red,10 black,10 5,10
You bet a total of 30 credits
Result: Red 34
Bet 1: Win, +20
Bet 2: Lost -10
Bet 3: Lost -10
You won/lost a total of 10 credits
New Balance: ####
"""
