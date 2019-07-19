import io
import os
import sys
import twitter
from .web_scraper import find_first_tweet

def generate_link_to_tweet(path):

    input_dict = sanitize(detect_text(path))

    username = input_dict.get('username')
    text = input_dict['text']

    if len(text.replace(" ", "")) > 160:
        text = reformat_text(text)

    text = text.replace(" ", "%20")
    if username:
        URL = "https://twitter.com/search?l=&q={}%20from%3A{}&src=typd".format(text, username)
    else:
        URL = "https://twitter.com/search?l=&q={}&src=typd".format(text)

    return find_first_tweet(URL)

def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    return texts[0].description.split("\n")



def sanitize(text):
    lines_after_username = 0  # Counter to keep track of how far we are after finding the username line

    input_dictionary = {"text": ""}
    line_num = 0
    for line in text:
        print(line)
        if line_num == 0 and "@" in line:
            lines_after_username += 1
            continue
        if line == "Following" or line == "Follow" or line == '':
            continue
        if lines_after_username == 1 and line.startswith("Replying to"):
            # If the line after the username begins with "Replying to", ignore it
            continue
        if line[0] == "@" and lines_after_username == 0: # We have found the username line
            lines_after_username += 1
            input_dictionary["username"] = line[1:]
            continue
        if is_end_of_text(line):
            break
        elif lines_after_username > 0:
            input_dictionary["text"] += " " + line
        line_num += 1
    print(input_dictionary)
    return input_dictionary


def is_end_of_text(line):
    """
    Determines whether a line of text from a tweet image is no longer part of the body of the tweet.
    """

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    digits = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    blacklist = ["More", "Favorite", "Reply", "Retweet"]
    line_list = line.split(" ")
    if (":" in line) and ("/" in line) and (any([char in digits for char in line])):
        return True
    if (":" in line) and (("AM" in line) or ("PM" in line)) and (any([char in digits for char in line])):
        return True
    if ("Reply" in line) and ("Retweet" in line) and ("Favorite" in line) and ("More" in line):
        return True
    if ("@" in line) and ("/" in line) and any([char in digits for char in line]):
        return True
    if all([char in digits for char in line]):
        print(line)
        print("got to digits")
        return True
    if all([word in blacklist for word in line_list]):
        return True
    return False

def reformat_text(text):
    """
    Due to strange constraints on the number of words in the search parameter,
    this function truncates the text at the next space character after 170
    characters (not including spaces)
    """
    num_letters = 0
    new_text = ""
    for i in range(len(text)):
        char = text[i]
        if num_letters > 160 and char == " ":
            new_text = text[0:i]
            break
        if char != " ":
            num_letters += 1
    return new_text


def get_embed_html(link):
    consumer_token = os.environ['TWT_CONSUMER_TOKEN']
    consumer_secret = os.environ['TWT_CONSUMER_SECRET']
    access_token = os.environ['TWT_ACCESS_TOKEN']
    access_secret = os.environ['TWT_ACCESS_SECRET']
    api = twitter.Api(consumer_key=consumer_token,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token,
                  access_token_secret=access_secret)
    print("This is link: " + link)
    html = api.GetStatusOembed(url=link)
    return html['html']

# get_embed_html('https://twitter.com/BobWulff/status/1151642928286187525')
# generate_link_to_tweet(sys.argv[1])
#detect_text(sys.argv[1])
