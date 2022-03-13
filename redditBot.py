import praw
from praw.models import MoreComments

#import list of phrases, save in substring
# will use to iterate through substring to find matching phrases in top level comments
# then when match is found, will go through the users comments and again iterate through
# substrings to find more matching phrases
listFile = open("list.txt", "r")
substrings = []
for lines in listFile:
    commonPhrases = lines[:-1]
    substrings.append(commonPhrases)
    
# set up reddit login credentials
reddit = praw.Reddit(
        user_agent="commonPhrasesBot",
        client_id="",
        client_secret="",
        username="commonPhrasesBot",
        password="",
    )

#will return false if authentication worked
print("failed authentication: " + str(reddit.read_only))

#use results from r/popular
subreddit = reddit.subreddit("popular")

user = "none"
#browse however many submissions from r/popular
for submission in subreddit.hot(limit=100):
    #get the comment tree
    all_comments = submission.comments
    print("total top level comments to parse: " + str(len(all_comments)))
    for top_level_comment in all_comments:
        # for simplicity just get top level comments
        if isinstance(top_level_comment, MoreComments):
            continue
        #print(top_level_comment.body.lower())
        #print(top_level_comment.author)
        user = top_level_comment.author
        # bool we can assign if match found to allow reply
        shouldReply = False
        # count how many matches we get from a users comments in event of one match
        count = 0

        # iterate through the list of common phrases
        for s in substrings:
            # convert to lowercase and check for string, also check that post wordcount is short and lacks real substance
            if s in top_level_comment.body.lower() and len(top_level_comment.body.split()) < 14:
                shouldReply = True
                count += 1
                print("found matching string in submission: " + str(submission.title))
                print("userName: " + str(top_level_comment.author))
                print("top level comment: " + top_level_comment.body)
                usedStr = s
                # now check all the users comments, since we found one match
                for comment in reddit.redditor(str(user)).comments.new(limit=None):
                    # check each comment for each common phrase
                    for moreStrings in substrings:
                        if moreStrings in comment.body.lower():
                            print("match: " + moreStrings)
                            count += 1
                print("userName: " + str(top_level_comment.author) + " - total matches: " + str(count))
        # now reply if bool is true and the poster has made it past certain threshold of comments with phrases
        # (its not really interesting to post if they only have done it once or twice)
        if (shouldReply) and (count > 10):
            print("conditions met, replying.")
            part1 = "Hi there!\n\n\n\n You used the phrase '" + usedStr + "' in your comment, a common reddit-ism!\n\n"
            part2 = "I looked through your recent comments and found you used common reddit-isms " + str(count) + " times.\n\n"
            part3 = "I am a bot and check for common phrases like 'they understood the assignment', 'SHUT UP AND TAKE MY MONEY', or 'I also choose this guys wife'. \n\n"
            part4 = "I am mostly curious about pointing out potential karma farming accounts, and hope to occasionally get a laugh.\n\n "
            part5 = "Sorry if you just like using these phrases occasionally!"
            top_level_comment.reply(part1 + part2 + part3 + part4 + part5)
