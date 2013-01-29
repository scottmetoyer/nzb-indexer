# test.py
# Scott Metoyer, 2013
# Retrieves a list of new NZB's from the newsgroups specified in a config file
from nntplib import *
from config import config
from yenc import yenc_decode
import pymongo

group = 'alt.binaries.movies'

print('Connecting to ' + config["usenet_server"] + '...')
#server = NNTP(config["usenet_server"], config["usenet_port"], config["usenet_username"], config["usenet_password"])

print('Grabbing fragments...')
#server.body('<1ddee$4fd75543$5ed4fe1c$32589@4ux.nl>', 'fragment1')
#server.body('<8f9f5$4fd75546$5ed4fe1c$32589@4ux.nl>', 'fragment2')
#server.body('<999b8$4fd75548$5ed4fe1c$32589@4ux.nl>', 'fragment3')

print('Decoding...')
f = open('fragment1', 'r')
data = yenc_decode(f)
f.close()

f = open('fragment2', 'r')
data += yenc_decode(f)
f.close()

f = open('fragment3', 'r')
data += yenc_decode(f)
f.close()

print('Writing output file...')
f = open('output.nzb', 'w')
for s in data:
    f.write(s)
f.close()