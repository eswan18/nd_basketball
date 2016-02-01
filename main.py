#!/usr/bin/python

from DataPuller import DataPuller
from DataParser import DataParser
from DataCompleter import DataCompleter

puller = DataPuller()
puller.pull(21)
parser = DataParser()
parser.parse()
completer = DataCompleter()
completer.complete()
