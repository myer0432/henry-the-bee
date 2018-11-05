from textgenrnn import textgenrnn
import tweepy
import sys
import random
import re

##########################################################################
#  _   _ _____ _   _ ______   __  _____ _   _ _____   ____  _____ _____  #
# | | | | ____| \ | |  _ \ \ / / |_   _| | | | ____| | __ )| ____| ____| #
# | |_| |  _| |  \| | |_) \ V /    | | | |_| |  _|   |  _ \|  _| |  _|   #
# |  _  | |___| |\  |  _ < | |     | | |  _  | |___  | |_) | |___| |___  #
# |_| |_|_____|_| \_|_| \_\|_|     |_| |_| |_|_____| |____/|_____|_____| #
#                                                                        #
#                                                                        #
#  Authors: Zoey Fryhover, Sarah Myers and Melissa Wilson                #
#  Version: 2.0                                                          #
#                                                                        #
#  Thank you to minimaxir for your text-generating RNN.                  #
#  https://github.com/minimaxir/textgenrnn                               #
#                                                                        #
##########################################################################

# Temperature range for Guss (creativity level)
LOW = 0.35
HIGH = 0.65

########
# MAIN #
########
def main():
    henry = rnn("Weights/henry.hdf5", LOW, HIGH)
    henry.get_secrets()
    henry.tweet()

#######
# RNN #
#######
class rnn():
    # Constructor
    def __init__(self, weights, low, high):
        self.textgen = textgenrnn(weights)
        self.low = low
        self.high = high

    # Get authorization
    def get_secrets(self):
        with open("../../Personal/Secrets/henry.txt") as file:
            contents = file.readlines()
        contents = [x.strip() for x in contents]
        self.consumer_key = contents[0]
        self.consumer_secret = contents[1]
        self.access_token = contents[2]
        self.access_token_secret = contents[3]

    # Generate text
    def generate(self, low, high):
        hashtag = ""
        text = self.textgen.generate(1, temperature=(random.uniform(0, 1)*(high-low)+low), return_as_list=True)[0].lower()
        arr = text.split(" ")
        if len(arr) <= 3:
            hashtag += "#"
            for a in arr:
                hashtag += re.sub('[^0-9a-zA-Z]+', '', a)
            text = ""
        while len(text + hashtag) < 280:
            hashtag_more = ""
            if random.randint(0, 1) == 0:
                return text + hashtag
            more = self.textgen.generate(1, temperature=(random.uniform(0, 1)*(high-low)+low), return_as_list=True)[0].lower()
            arr = more.split(" ")
            if len(arr) <= 3:
                hashtag_more = "#"
                for a in arr:
                    if len(hashtag_more) > 1:
                        hashtag_more += re.sub('[^0-9a-zA-Z]+', '', a).capitalize()
                    else:
                        hashtag_more += re.sub('[^0-9a-zA-Z]+', '', a)
                more = ""
            if len(text + more + hashtag + hashtag_more) < 280:
                if len(more) > 0:
                    text += " " + more
                if len(hashtag_more) > 0:
                    hashtag += " " + hashtag_more
        return text + " " + hashtag

    # Send a tweet
    def tweet(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth)
        api.update_status(status=self.generate(LOW, HIGH))

if __name__ == "__main__":
    main()
