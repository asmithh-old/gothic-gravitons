import random, re
import tweepy
import time
content = []
text1 = True
text2 = True
text3 = True
if text1:
    with open('text1.txt') as f:
        for line in f.readlines():
            content.append(line)
        f.close()
if text2:
    with open('text2.txt') as g:
        mystr = ''
        for line in g.readlines():
            mystr += str(re.sub('\n', ' ', line))
        for t in mystr.split('.'):
            content.append(t + '.')
        g.close()
if text3:
    with open('text3.txt') as h:
        for line in h.readlines():
            content.append(line)
        h.close()
transitions = {}
words = {}
begins = []
donttweet = []
#if your source texts contain offensive language (as my immortal and the sound and the fury both do)
#you may want to screen for this language and prevent the bot from tweeting it.
for line in content:
    try:
        if len(line.split())>3:
            begins.append(line.split()[0])
    except:
        pass
    for word in line.split():
        if word in donttweet:
            pass
        else:
            if word in words:
                words[word] = words[word] + 1
            else:
                words[word] = 1
            if line.split().index(word) + 1 < len(line.split()) :
                succ = line.split()[line.split().index(word) + 1]
                if word in transitions:
                    if succ in transitions[word]:
                        transitions[word][succ] = transitions[word][succ] + 1
                    else:
                        transitions[word][succ] = 1
                else:
                    transitions[word] = {}
                    transitions[word][succ] = 1

def make_dist(dictionary):
    res = []
    for word in dictionary.keys():
        for val in range(0, dictionary[word]):
            res.append(word)
    return res


transitionDists = {}

seedDist = make_dist(words)
def new_tweet(songLen):
    state = random.choice(begins)
    steps = 0
    song = ''
    while steps < songLen:
        song += ' '
        song += state
        steps += 1
        if state in transitionDists:
            state = random.choice(transitionDists[state])
        else:
            try:
                transitionDists[state] = make_dist(transitions[state])
                state = random.choice(transitionDists[state])
            except KeyError:
                song += '\n'
                state = random.choice(begins)
    while song[-1] != ".":
        song += ' '
        song += state
        steps += 1
        if state in transitionDists:
            state = random.choice(transitionDists[state])
        else:
            try:
                transitionDists[state] = make_dist(transitions[state])
                state = random.choice(transitionDists[state])
            except KeyError:
                song += '\n'
                state = random.choice(begins)
    return song
tweets = []
for i in range(55):
    new = new_tweet(15)
    tweets.append(new)
    #print len(new)
    print new
    print
print
print 'tweeting'
print
consumer_key = 'your consumer key here'
consumer_secret = 'your consumer secret here'
access_token = 'your access token here'
access_token_secret = 'your access token secret here'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
public_tweets = api.home_timeline()

for i in tweets:
    if len(i) <= 140:
            api.update_status(status = i)
    # else:
    #     if len(i.split('.')) == 2:
    #         tweets.append(i.split('.')[0])
    #
    #         tweets.append(i.split('.')[1])
    time.sleep(10)
