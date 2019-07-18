import io
import sys

def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    #print(texts[0].description.split("\n"))
    #print(texts[0].description)
    print(sanitize(texts[0].description.split("\n")))
    return str(texts[0].description.split("\n"))

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
            input_dictionary["username"] = line
            continue
        if is_end_of_text(line):
            break
        elif lines_after_username > 0:
            input_dictionary["text"] += " " + line
    return input_dictionary


def is_end_of_text(line):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    digits = ["1", "2", "3", "4", "5", "6", "7", "8", "9","0"]
    if (":" in line) and ("/" in line) and (any([char in digits for char in line])):
        return True
    if ("Reply" in line) and ("Retweet" in line) and ("Favorite" in line) and ("More" in line):
        return True
    return False




detect_text(sys.argv[1])
