nzb-indexer
===========

Scott Metoyer
scott.metoyer@gmail.com
01/24/2013

Simple Usenet NZB indexer in Python

Requirements

Python 2.7.x
MongoDB


Setup

To install, copy and rename config_default.py to config_local.py and edit to specify your configuration values.


Usage

Run index.py to build an index. Run it again as needed to update your indexes with the latest NZB posts.

The groups to crawl are specified in groups.txt, one group name per line. There are a few in there to get you started.


