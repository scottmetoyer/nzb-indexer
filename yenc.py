# yenc.py
# Decode a yenc encoded file and return a list of string fragments
import string

yenc42 = string.join(map(lambda x: chr((x-42) & 255), range(256)), "")
yenc64 = string.join(map(lambda x: chr((x-64) & 255), range(256)), "")

def yenc_decode(file):
    # Find the body
    while 1:
        line = file.readline()
        if not line:
            return None
        if line[:7] == "=ybegin":
            break
    # Extract data
    buffer = []
    while 1:
        line = file.readline()
        if not line or line[:5] == "=yend":
            break
        if line[-2:] == "\r\n":
            line = line[:-2]
        elif line[-1:] in "\r\n":
            line = line[:-1]
        data = string.split(line, "=")
        buffer.append(string.translate(data[0], yenc42))
        
        # What is this doing? It inserted a bunch of gibberish at the start of each article fragment.
        #for data in data[1:]:
            #data = string.translate(data, yenc42)
            #buffer.append(string.translate(data[0], yenc64))
            #buffer.append(data[1:])
    return buffer