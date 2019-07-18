import io
import os
import sys
import twitter

def generate_link_to_tweet(path):
   input_dict = sanitize(detect_text(path))

   username = input_dict['username']
   text = input_dict['text'].replace(" ", "%20")
   print(username)
   print("https://twitter.com/search?l=&q={}%20from%3A{}&src=typd".format(text, username))

def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations


    #print(sanitize(texts[0].description.split("\n")))
    return texts[0].description.split("\n")

def sanitize(text):
    lines_after_username = 0  # Counter to keep track of how far we are after finding the username line

    input_dictionary = {"text": ""}
    for line in text:
        if line == "Following" or line == '':
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
    return input_dictionary


def is_end_of_text(line):
    '''
    Determines whether a line of text from a tweet image is no longer part of the body of the tweet.
    '''

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    digits = ["1", "2", "3", "4", "5", "6", "7", "8", "9","0"]
    blacklist = ["More", "Favorite", "Reply", "Retweet"]
    line_list = line.split(" ")
    if (":" in line) and ("/" in line) and (any([char in digits for char in line])):
        return True
    if (":" in line) and ("-" in line) and ("AM" in line or "PM" in line) and (any([char in digits for char in line])):
        return True
    if ("Reply" in line) and ("Retweet" in line) and ("Favorite" in line) and ("More" in line):
        return True
    if all([word in blacklist for word in line_list]):
        return True
    return False

def get_embed_html(url):
    consumer_token = os.environ['TWT_CONSUMER_TOKEN']
    consumer_secret = os.environ['TWT_CONSUMER_SECRET']
    access_token = os.environ['TWT_ACCESS_TOKEN']
    access_secret = os.environ['TWT_ACCESS_SECRET']
    api = twitter.Api(consumer_key=consumer_token,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token,
                  access_token_secret=access_secret)
    html = api.GetStatusOembed(url=url)
    print(html)

get_embed_html('https://twitter.com/BobWulff/status/1151642928286187525')
# generate_link_to_tweet(sys.argv[1])
#detect_text(sys.argv[1])
