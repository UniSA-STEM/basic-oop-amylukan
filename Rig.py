"""
File: rig.py
Description: <Defines the Rig class. Handles rig storage, damage, and upgrades. Can be broken or improved with patches.>
Author: <Amy Lukan>
ID: <110458803>
Username: <LUKAY008>
This is my own work as defined by the University's Academic Misconduct Policy.
"""
from typing import List
import random
from Asset import Asset

class Rig:
 # basic rig class
 # keeps track of the damage, items and upgrade level
    def __init__(self, name: str):
        self.name = name
        self.damage = 0
        self.broken = False
        self.storage = []
        self.upgrade_level = 0

        # the start inventory: 2 Data Spikes and 1 Removable Drive
        self.storage.append(Asset("Data Spike", "Used in battles"))
        self.storage.append(Asset("Data Spike", "Used in battles"))
        self.storage.append(Asset("Removable Drive", "Used for extraction"))

    # the capacity increases with upgrade level
    @property
    def storage_capacity(self) -> int:
        base = 5
        return base + (self.upgrade_level * 2)

    def is_full(self):
        return len(self.storage) >= self.storage_capacity

    def condition_string(self) -> str:
        if self.broken:
            return f"Broken (Level {self.upgrade_level})"
        # map damage and level to description
        if self.damage == 0:
            return f"Pristine (Level {self.upgrade_level})"
        if self.damage == 1:
            return f"Damaged (Level {self.upgrade_level})"
        return f"Critical (Level {self.upgrade_level})"

    def __str__(self) -> str:
        stored = ", ".join(str(a) for a in self.storage) or "Empty"
        return f"{self.name} - {self.condition_string()} - Stored: [{stored}]"

    def take_hit(self, amount=1):
        # increases the damage
        # the threshold grows with the upgrade level

        if self.broken:
            return
        # rigs with a higher upgrade level are slightly tougher
        threshold = 2 + self.upgrade_level  # level 0 -> 2, level1 ->3, etc.
        self.damage += amount
        if self.damage >= threshold:
            self.broken = True

    def repair(self, token):
        # reset damage if its broken
        if token.name != "CryptoToken":
            return False
        if self.damage == 0 and not self.broken:
            return False
        # reset the damage
        self.damage = 0
        self.broken = False
        return True

    def upgrade(self, patch):
        # upgrading the rig and increase upgrade level

        if patch.name != "Hardware Patch":
            return False
        self.upgrade_level += 1
        return True

    def generate_asset(self) -> Asset:
        # create a random core asset and add it to the storage is there is room
        # if there is no room, return the asset

        pool = [
            ("CryptoToken", "Used to acquire or repair rigs"),
            ("Data Spike", "Used in battles"),
            ("Removable Drive", "Used for extraction"),
            ("Security Chip", "Used to encrypt/decrypt assets"),
            ("Hardware Patch", "Used to upgrade rigs")
        ]
        choice = random.choice(pool)
        new_asset = Asset(choice[0], choice[1])
        if not self.is_full():
            self.storage.append(new_asset)
            return new_asset
        # if full, return but not stored
        return new_asset

    def remove_asset_by_name(self, name: str) -> Asset | None:
        # get rid of the first non-encrytped asset by name and return it
        # if the asset was encrypted, don't return it

        for i, a in enumerate(self.storage):
            if a.name == name:
                if a.encrypted:
                    return None
                return self.storage.pop(i)
        return None

    def list_non_encrypted(self) -> list[Asset]:
        return [a for a in self.storage if not a.encrypted]
