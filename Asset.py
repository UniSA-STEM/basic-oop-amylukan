"""
File: asset.py
Description: <Holds the Asset class. Used for items like Data Spikes or Patches. Tracks name, description, and if it’s encrypted.>
Author: <Amy Lukan>
ID: <110458803>
Username: <LUKAY008>
This is my own work as defined by the University's Academic Misconduct Policy.
"""
from dataclasses import dataclass

@dataclass
class Asset:
   # used for all items such as CryptoToken, DataSpike etc.
    name: str
    description: str
    encrypted: bool = False

    def encrypt(self):
        if self.encrypted:
            return False
        self.encrypted = True
        return True

    def decrypt(self):
        if not self.encrypted:
            return False
        self.encrypted = False
        return True

    def __str__(self):
        return self.name

