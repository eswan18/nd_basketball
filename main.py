#!/usr/bin/python

from DataPuller import DataPuller
from DataParser import DataParser

puller = DataPuller()
puller.pull(19)
parser = DataParser()
parser.parse()
