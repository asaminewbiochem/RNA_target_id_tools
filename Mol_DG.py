import pandas as pnds
import sys
import os
import subprocess
from typing import List, Dict, Set
import math
import random

import numpy as nmpy

class MedRateMol:
    def __rate__(self):
        ratings = input("Molecule ratings: (g/m/b) ")
        print("You rated: {ratings}")
        MedRateMol.__rate__(self)
    def __check__(self):
        while True:
            mol = input("Checked for mol? (y/n)")
            if mol == "y":
                mol = random.randrange(1, 100)
                print("Mol this! {mol}")
                MedRateMol.__check__(self)
                continue
            else:
                print("Kshhhhhh!!!")
                break

def mol(removed):
    moling = int(input("What is your .mol file? "))
    print("Mol is: {moling}")