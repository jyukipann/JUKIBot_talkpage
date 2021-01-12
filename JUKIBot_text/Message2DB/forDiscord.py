import csv
import itertools
from collections import deque
import hashlib
from . import _createDB
import sqlite3

def tohash(data):
	hashId = hashlib.md5()
	hashId.update(repr(data).encode("utf-8"))
	return hashId.digest()
