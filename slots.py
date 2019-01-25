import numpy
import praw

reddit = praw.Reddit('RedditCasino_Slots')

# 8-ball, dice, joker, bell, slot-machine
testEmojis = [u'\U0001F3B1', u'\U0001F3B2', u'\U0001F0CF', u'\U0001F514', u'\U0001F3B0']

# sax, guitar, piano, trumpet, violin
musicEmojis = [u'\U0001F3B7', u'\U0001F3B8', u'\U0001F3B9', u'\U0001F3BA', u'\U0001F3BB']

probs = [0.3, 0.15, 0.05, 0.3, 0.2]

def findSlotGame(post):
    replyComment = ''
    print('Searching ' + post + ' for slot games')
    subreddit = reddit.subreddit('lasreddittesting')
    for comment in subreddit.stream.comments(pause_after=1, skip_existing=True):
        if comment is None or comment.author.name == 'lasreddit_boss':
            #checkInbox()
            print('Nothing found')
            continue
        if comment.submission.title == 'EMOJI_TEST':
            message = comment.body.split(' ')
            if message[0] == '!testslot':
                print('Slot game found: Theme is test')
                theme = 'test'
                print(comment.body)
                player = comment.author.name
                print(player)
                reply = spinSlot(theme)
                comment.reply(reply)
        else:
            print('Slot game found in another post')
            comment.mod.remove()
            print('Comment deleted')

def spinSlot(type):
    slotString = ''
    logicGrid = []
    for submission in reddit.subreddit('lasreddittesting').top(limit=None):
        if submission.title == 'EMOJI_TEST':
            #findSlotGame('EMOJI_TEST')
            # Slot output
            slotString += '||||||\n'
            slotString += ':-:|:-:|:-:|:-:|:-:\n'
            for x in range(0, 3):
                logicGrid.append([])
                # Generates 1 row three times
                res1 = numpy.random.choice(testEmojis, p=probs).encode("utf-8")
                logicGrid[x].append(res1)
                res2 = numpy.random.choice(testEmojis, p=probs).encode("utf-8")
                logicGrid[x].append(res2)
                res3 = numpy.random.choice(testEmojis, p=probs).encode("utf-8")
                logicGrid[x].append(res3)
                res4 = numpy.random.choice(testEmojis, p=probs).encode("utf-8")
                logicGrid[x].append(res4)
                res5 = numpy.random.choice(testEmojis, p=probs).encode("utf-8")
                logicGrid[x].append(res5)
                slotString += res1 + '|' + res2 + '|' + res3 + '|' + res4 + '|' + res5 + '\n'
    slotString += '\n'
    slotString += slotLogic(logicGrid)
    print(logicGrid)
    return slotString

def slotLogic(lg):
    reply = ''
    # Pay Line 1
    if (lg[0][0] == lg[0][1]) and (lg[0][1] == lg[0][2]):
        if lg[0][2] is not lg[0][3]:
            reply += showPayLine1(lg[0][0], 3);
            print('First 3 in pay line 1 are the same')
        elif lg[0][2] == lg[0][3]:
            if lg[0][3] is not lg[0][4]:
                reply += showPayLine1(lg[0][0], 4);
                print('First 4 in pay line 1 are the same')
            elif lg[0][3] == lg[0][4]:
                reply += showPayLine1(lg[0][0], 5);
                print('All in pay line 1 are the same')

    # Pay Line 2
    if (lg[1][0] == lg[1][1]) and (lg[1][1] == lg[1][2]):
        if lg[1][2] is not lg[1][3]:
            reply += showPayLine2(lg[1][0], 3);
            print('First 3 in pay line 2 are the same')
        elif lg[1][2] == lg[1][3]:
            if lg[1][3] is not lg[1][4]:
                reply += showPayLine2(lg[1][0], 4);
                print('First 4 in pay line 2 are the same')
            elif lg[1][3] == lg[1][4]:
                reply += showPayLine2(lg[1][0], 5);
                print('All in second row are the same')

    # Pay Line 3
    if (lg[2][0] == lg[2][1]) and (lg[2][1] == lg[2][2]):
        if lg[2][2] is not lg[2][3]:
            reply += showPayLine3(lg[2][0], 3);
            print('First 3 in pay line 3 are the same')
        elif lg[2][2] == lg[2][3]:
            if lg[2][3] is not lg[2][4]:
                reply += showPayLine3(lg[2][0], 4);
                print('First 4 in pay line 3 are the same')
            elif lg[2][3] == lg[2][4]:
                reply += showPayLine3(lg[2][0], 5);
                print('All in pay line 3 are the same')

    # Pay Line 4
    if (lg[0][0] == lg[1][1]) and (lg[1][1] == lg[0][2]):
        if lg[0][2] is not lg[1][3]:
            reply += showPayLine4(lg[0][0], 3);
            print('First 3 in pay line 4 are the same')
        elif lg[0][2] == lg[1][3]:
            if lg[1][3] is not lg[0][4]:
                reply += showPayLine4(lg[0][0], 4);
                print('First 4 in pay line 4 are the same')
            elif lg[1][3] == lg[0][4]:
                reply += showPayLine4(lg[0][0], 5);
                print('All in pay line 4 are the same')

    # Pay Line 5
    if (lg[2][0] == lg[1][1]) and (lg[1][1] == lg[0][2]):
        if lg[0][2] is not lg[1][3]:
            reply += showPayLine5(lg[2][0], 3);
            print('First 3 in pay line 5 are the same')
        elif lg[0][2] == lg[1][3]:
            if lg[1][3] is not lg[2][4]:
                reply += showPayLine5(lg[2][0], 4);
                print('First 4 in pay line 5 are the same')
            elif lg[1][3] == lg[2][4]:
                reply += showPayLine5(lg[2][0], 5);
                print('All in pay line 5 are the same')

    # Pay Line 6
    if (lg[1][0] == lg[2][1]) and (lg[2][1] == lg[0][2]):
        if lg[0][2] is not lg[2][3]:
            reply += showPayLine6(lg[1][0], 3);
            print('First 3 in pay line 6 are the same')
        elif lg[0][2] == lg[2][3]:
            if lg[2][3] is not lg[1][4]:
                reply += showPayLine6(lg[1][0], 4);
                print('First 4 in pay line 6 are the same')
            elif lg[2][3] == lg[1][4]:
                reply += showPayLine6(lg[1][0], 5);
                print('All in pay line 6 are the same')

    # Pay Line 7
    if (lg[0][0] == lg[1][1]) and (lg[1][1] == lg[2][2]):
        if lg[2][3] is not lg[1][3]:
            reply += showPayLine7(lg[0][0], 3);
            print('First 3 in pay line 7 are the same')
        elif lg[2][2] == lg[1][3]:
            if lg[1][3] is not lg[0][4]:
                reply += showPayLine7(lg[0][0], 4);
                print('First 4 in pay line 7 are the same')
            elif lg[1][3] == lg[0][4]:
                reply += showPayLine7(lg[0][0], 5);
                print('All in pay line 7 are the same')

    # Pay Line 8
    if (lg[2][0] == lg[2][1]) and (lg[2][1] == lg[1][2]):
        if lg[1][2] is not lg[0][3]:
            reply += showPayLine8(lg[2][0], 3);
            print('First 3 in pay line 8 are the same')
        elif lg[1][2] == lg[0][3]:
            if lg[0][3] is not lg[0][4]:
                reply += showPayLine8(lg[2][0], 4);
                print('First 4 in pay line 8 are the same')
            elif lg[0][3] == lg[0][4]:
                reply += showPayLine8(lg[2][0], 5);
                print('All in pay line 8 are the same')

    # Pay Line 9
    if (lg[1][0] == lg[0][1]) and (lg[0][1] == lg[2][2]):
        if lg[2][2] is not lg[0][3]:
            reply += showPayLine9(lg[1][0], 3);
            print('First 3 in pay line 9 are the same')
        elif lg[2][2] == lg[0][3]:
            if lg[0][3] is not lg[2][4]:
                reply += showPayLine9(lg[1][0], 4);
                print('First 4 in pay line 9 are the same')
            elif lg[0][3] == lg[2][4]:
                reply += showPayLine9(lg[1][0], 5);
                print('All in pay line 9 are the same')

    return reply

def determineSymbolTest(lg):
    """
    \xf0\x9f\x94\x94 = bell
    \xf0\x9f\x8e\xb1 = 8-ball
    \xf0\x9f\x8e\xb2 = dice
    \xf0\x9f\x83\x8f = joker
    \xf0\x9f\x8e\xb0 = slot-machine
    """

    if lg[0][0] == '\xf0\x9f\x94\x94':
        return 'Bell' # 3: 10 from 1 credit. 4: 20 from 1 credit. 5: 50 from 1 credit
    elif lg[0][0] == '\xf0\x9f\x8e\xb1':
        return '8-Ball' # 3: 10 from 1 credit. 4: 20 from 1 credit. 5: 50 from 1 credit
    elif lg[0][0] == '\xf0\x9f\x8e\xb2':
        return 'Dice' # 3: 20 from 1 credit. 4: 40 from 1 credit. 5: 90 from 1 credit
    elif lg[0][0] == '\xf0\x9f\x83\x8f':
        return 'Joker' # 3: 50 from 1 credit. 4: 100 from 1 credit. 5: 250 from 1 credit
    elif lg[0][0] == '\xf0\x9f\x8e\xb0':
        return 'Slot-Machine' # 3: 15 from 1 credit. 4: 35 from 1 credit. 5: 70 from 1 credit
    else:
        return 'welp something is wrong'

X = 'X'
def showPayLine1(symbol, correct):
    reply = ''
    if correct == 3:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += symbol + '|' + symbol + '|' + symbol + '|' + X + '|' + X + '\n'
        reply += X + '|' + X + '|' + X + '|' + X + '|' + X + '\n'
        reply += X + '|' + X + '|' + X + '|' + X + '|' + X + '\n\n'
        return reply
    elif correct == 4:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += symbol + '|' + symbol + '|' + symbol + '|' + symbol + '|' + X + '\n'
        reply += X + '|' + X + '|' + X + '|' + X + '|' + X + '\n'
        reply += X + '|' + X + '|' + X + '|' + X + '|' + X + '\n\n'
        return reply
    elif correct == 5:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += symbol + '|' + symbol + '|' + symbol + '|' + symbol + '|' + symbol + '\n'
        reply += X + '|' + X + '|' + X + '|' + X + '|' + X + '\n'
        reply += X + '|' + X + '|' + X + '|' + X + '|' + X + '\n\n'
        return reply

def showPayLine2(symbol, correct):
    reply = ''
    if correct == 3:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += X + '|' + X + '|' + X + '|' + X + '|' + X + '\n'
        reply += symbol + '|' + symbol + '|' + symbol + '|' + X + '|' + X + '\n'
        reply += X + '|' + X + '|' + X + '|' + X + '|' + X + '\n\n'
        return reply
    elif correct == 4:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += X + '|' + X + '|' + X + '|' + X + '|' + X + '\n'
        reply += symbol + '|' + symbol + '|' + symbol + '|' + symbol + '|' + X + '\n'
        reply += X + '|' + X + '|' + X + '|' + X + '|' + X + '\n\n'
        return reply
    elif correct == 5:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += X + '|' + X + '|' + X + '|' + X + '|' + X + '\n'
        reply += symbol + '|' + symbol + '|' + symbol + '|' + symbol + '|' + symbol + '\n'
        reply += X + '|' + X + '|' + X + '|' + X + '|' + X + '\n\n'
        return reply

def showPayLine3(symbol, correct):
    reply = ''
    if correct == 3:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += X + '|' + X + '|' + X + '|' + X + '|' + X + '\n'
        reply += X + '|' + X + '|' + X + '|' + X + '|' + X + '\n'
        reply += symbol + '|' + symbol + '|' + symbol + '|' + X + '|' + X + '\n\n'
        return reply
    elif correct == 4:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += X + '|' + X + '|' + X + '|' + X + '|' + X + '\n'
        reply += X + '|' + X + '|' + X + '|' + X + '|' + X + '\n'
        reply += symbol + '|' + symbol + '|' + symbol + '|' + symbol + '|' + X + '\n\n'
        return reply
    elif correct == 5:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += X + '|' + X + '|' + X + '|' + X + '|' + X + '\n'
        reply += X + '|' + X + '|' + X + '|' + X + '|' + X + '\n'
        reply += symbol + '|' + symbol + '|' + symbol + '|' + symbol + '|' + symbol + '\n\n'
        return reply

def showPayLine4(symbol, correct):
    reply = ''
    if correct == 3:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += symbol + '|' + X + '|' + symbol + '|' + X + '|' + X + '\n'
        reply += X + '|' + symbol + '|' + X + '|' + X + '|' + X + '\n'
        reply += X + '|' + X + '|' + X + '|' + X + '|' + X + '\n\n'
        return reply
    elif correct == 4:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += symbol + '|' + X + '|' + symbol + '|' + X + '|' + X + '\n'
        reply += X + '|' + symbol + '|' + X + '|' + symbol + '|' + X + '\n'
        reply += X + '|' + X + '|' + X + '|' + X + '|' + X + '\n\n'
        return reply
    elif correct == 5:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += symbol + '|' + X + '|' + symbol + '|' + X + '|' + symbol + '\n'
        reply += X + '|' + symbol + '|' + X + '|' + symbol + '|' + X + '\n'
        reply += X + '|' + X + '|' + X + '|' + X + '|' + X + '\n\n'
        return reply

def showPayLine5(symbol, correct):
    reply = ''
    if correct == 3:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += X + '|' + X + '|' + symbol + '|' + X + '|' + X + '\n'
        reply += X + '|' + symbol + '|' + X + '|' + X + '|' + X + '\n'
        reply += symbol + '|' + X + '|' + X + '|' + X + '|' + X + '\n\n'
        return reply
    elif correct == 4:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += X + '|' + X + '|' + symbol + '|' + X + '|' + X + '\n'
        reply += X + '|' + symbol + '|' + X + '|' + symbol + '|' + X + '\n'
        reply += symbol + '|' + X + '|' + X + '|' + X + '|' + X + '\n\n'
        return reply
    elif correct == 5:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += X + '|' + X + '|' + symbol + '|' + X + '|' + X + '\n'
        reply += X + '|' + symbol + '|' + X + '|' + symbol + '|' + X + '\n'
        reply += symbol + '|' + X + '|' + X + '|' + X + '|' + symbol + '\n\n'
        return reply

def showPayLine6(symbol, correct):
    reply = ''
    if correct == 3:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += X + '|' + X + '|' + symbol + '|' + X + '|' + X + '\n'
        reply += symbol + '|' + X + '|' + X + '|' + X + '|' + X + '\n'
        reply += X + '|' + symbol + '|' + X + '|' + X + '|' + X + '\n\n'
        return reply
    elif correct == 4:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += X + '|' + X + '|' + symbol + '|' + X + '|' + X + '\n'
        reply += symbol + '|' + X + '|' + X + '|' + X + '|' + X + '\n'
        reply += X + '|' + symbol + '|' + X + '|' + symbol + '|' + X + '\n\n'
        return reply
    elif correct == 5:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += X + '|' + X + '|' + symbol + '|' + X + '|' + X + '\n'
        reply += symbol + '|' + X + '|' + X + '|' + X + '|' + symbol + '\n'
        reply += X + '|' + symbol + '|' + X + '|' + symbol + '|' + X + '\n\n'
        return reply

def showPayLine7(symbol, correct):
    reply = ''
    if correct == 3:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += symbol + '|' + X + '|' + X + '|' + X + '|' + X + '\n'
        reply += X + '|' + symbol + '|' + X + '|' + X + '|' + X + '\n'
        reply += X + '|' + X + '|' + symbol + '|' + X + '|' + X + '\n\n'
        return reply
    elif correct == 4:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += symbol + '|' + X + '|' + X + '|' + symbol + '|' + X + '\n'
        reply += X + '|' + symbol + '|' + X + '|' + X + '|' + X + '\n'
        reply += X + '|' + X + '|' + symbol + '|' + X + '|' + X + '\n\n'
        return reply
    elif correct == 5:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += symbol + '|' + X + '|' + X + '|' + symbol + '|' + X + '\n'
        reply += X + '|' + symbol + '|' + X + '|' + X + '|' + X + '\n'
        reply += X + '|' + X + '|' + symbol + '|' + X + '|' + symbol + '\n\n'
        return reply

def showPayLine8(symbol, correct):
    reply = ''
    if correct == 3:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += X + '|' + X + '|' + X + '|' + X + '|' + X + '\n'
        reply += X + '|' + X + '|' + symbol + '|' + X + '|' + X + '\n'
        reply += symbol + '|' + symbol + '|' + X + '|' + X + '|' + X + '\n\n'
        return reply
    elif correct == 4:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += X + '|' + X + '|' + X + '|' + symbol + '|' + X + '\n'
        reply += X + '|' + X + '|' + symbol + '|' + X + '|' + X + '\n'
        reply += symbol + '|' + symbol + '|' + X + '|' + X + '|' + X + '\n\n'
        return reply
    elif correct == 5:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += X + '|' + X + '|' + X + '|' + symbol + '|' + symbol + '\n'
        reply += X + '|' + X + '|' + symbol + '|' + X + '|' + X + '\n'
        reply += symbol + '|' + symbol + '|' + X + '|' + X + '|' + X + '\n\n'
        return reply

def showPayLine9(symbol, correct):
    reply = ''
    if correct == 3:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += X + '|' + symbol + '|' + X + '|' + X + '|' + X + '\n'
        reply += symbol + '|' + X + '|' + X + '|' + X + '|' + X + '\n'
        reply += X + '|' + X + '|' + symbol + '|' + X + '|' + X + '\n\n'
        return reply
    elif correct == 4:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += X + '|' + symbol + '|' + X + '|' + symbol + '|' + X + '\n'
        reply += symbol + '|' + X + '|' + X + '|' + X + '|' + X + '\n'
        reply += X + '|' + X + '|' + symbol + '|' + X + '|' + X + '\n\n'
        return reply
    elif correct == 5:
        reply += '||||||\n'
        reply += ':-:|:-:|:-:|:-:|:-:\n'
        reply += X + '|' + symbol + '|' + X + '|' + symbol + '|' + X + '\n'
        reply += symbol + '|' + X + '|' + X + '|' + X + '|' + X + '\n'
        reply += X + '|' + X + '|' + symbol + '|' + X + '|' + symbol + '\n\n'
        return reply


findSlotGame('EMOJI_TEST')

"""
slotString += '     ------  ------  ------\n'
slotString += '    |  ' + res1 + '  |  ' + res2 + '  |  ' + res3 + '  |\n'
slotString += '     ------  ------  ------\n'

![slotType] [betAmount]
!musicslot 10

simpleSlot (no theme)
Bell, "Gem Stone", "Pool 8 ball", watermelon, tangerine
"""
