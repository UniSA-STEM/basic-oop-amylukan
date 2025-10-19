"""
File: hacker.py
Description: <Main logic file with the Hacker class. Manages inventory, rig actions, trace level, and encrypt/decrypt functions.>
Author: <Amy Lukan>
ID: <110458803>
Username: <LUKAY008>
This is my own work as defined by the University's Academic Misconduct Policy.
"""
from typing import List
from Asset import Asset
from Rig import Rig

class Hacker:
 # main player class
 # it handles the inventory, trace system and rig control
 # it is used to manage most of the games actions

    TRACE_THRESHOLD = 5

    def __init__(self, name: str):
        self.name = name
        self.inventory = []
        # start with single CryptoToken
        self.inventory.append(Asset("CryptoToken", "Used to acquire or repair rigs"))
        self.rig: Rig | None = None
        self.trace_level = 0

    def __str__(self) -> str:
        inv = ", ".join(str(a) for a in self.inventory) or "Empty"
        rig_name = self.rig.name if self.rig else "None"
        return f"Hacker {self.name} - Rig: {rig_name} - Trace: {self.trace_level} - Inventory: [{inv}]"

    def has_item(self, name: str):
        return any(a.name == name for a in self.inventory)

    def pop_item(self, name: str) -> Asset | None:
        for i, a in enumerate(self.inventory):
            if a.name == name:
                return self.inventory.pop(i)
        return None

    def acquire_rig(self, rig: Rig | None = None):
        # get a rig by using one CryptoToken

        if self.rig is not None:
            # already has a rig
            return False
        token = self.pop_item("CryptoToken")
        if token is None:
            return False
        if rig is None:
            rig = Rig(f"{self.name}'s Rig")
        self.rig = rig
        print(self.name, "activated rig", self.rig.name)
        return True

    def launch_data_spike(self, target_rig):
        # attack the target rig using a data spike from its storage
        # increase own trace and if the traces exceeds the threshold, block the action

        if self.trace_level > Hacker.TRACE_THRESHOLD:
            print(self.name, "too traced to attack")
            return False
        if self.rig is None:
            print("No rig found")
            return False
        # find a Data spike in this rig storage
        for i, a in enumerate(self.rig.storage):
            if a.name == "Data Spike":
                # use it
                self.rig.storage.pop(i)
                # apply the hit
                # damage reduction due to upgrade level
                damage_amount = 1
                # the spec said upgrade reduces damage taken
                target_rig.take_hit(damage_amount)
                self.trace_level += 1
                print(self.name, "spiked", target_rig.name)
                return True
        print("no data spike left")
        return False

    def encrypt_asset(self, asset_name, use_from="inventory"):
        # encrypt an asset in either the hacker inventory or the rig using a security chip.

        # find security chip in either inventory or rig storage
        chip = None
        # chip can be used from either inventory or rig storage
        chip_source = None
        # search hacker inventory
        for i, a in enumerate(self.inventory):
            if a.name == "Security Chip":
                chip = self.inventory.pop(i)
                chip_source = "inventory"
                break
        if chip is None and self.rig:
            for i, a in enumerate(self.rig.storage):
                if a.name == "Security Chip":
                    chip = self.rig.storage.pop(i)
                    chip_source = "rig"
                    break
        if chip is None:
            print("no chip found")
            return False

        # find the asset to encrypt
        if use_from == "inventory":
            for a in self.inventory:
                if a.name == asset_name and not a.encrypted:
                    a.encrypt()
                    print(asset_name, "encrypted in hacker inventory")
                    return True
        elif use_from == "rig":
            if not self.rig:
                print("No rig.")
                # return chip to its original location because we used it early
                if chip_source == "inventory":
                    self.inventory.append(chip)
                else:
                    self.rig.storage.append(chip)
                return False
            for a in self.rig.storage:
                if a.name == asset_name and not a.encrypted:
                    a.encrypt()
                    print(asset_name, "encrypted in rig storage")
                    return True
        # if we reach here asset not found or its already encrypted: return chip back
        if chip_source == "inventory":
            self.inventory.append(chip)
        elif chip_source == "rig" and self.rig:
            self.rig.storage.append(chip)
        print(asset_name," not found/unable to encrypt")
        return False

    def decrypt_asset(self, asset_name: str, use_from: str = "inventory"):
        # decrypt the asset using a security chip

        # find the security chip
        chip = None
        chip_source = None
        for i, a in enumerate(self.inventory):
            if a.name == "Security Chip":
                chip = self.inventory.pop(i)
                chip_source = "inventory"
                break
        if chip is None and self.rig:
            for i, a in enumerate(self.rig.storage):
                if a.name == "Security Chip":
                    chip = self.rig.storage.pop(i)
                    chip_source = "rig"
                    break
        if chip is None:
            print("No chip available to decrypt")
            return False

        # find asset to decrypt
        if use_from == "inventory":
            for a in self.inventory:
                if a.name == asset_name and a.encrypted:
                    a.decrypt()
                    print(asset_name, "decrypted in hacker inventory")
                    return True
        elif use_from == "rig":
            if not self.rig:
                print("No rig.")
                if chip_source == "inventory":
                    self.inventory.append(chip)
                else:
                    self.rig.storage.append(chip)
                return False
            for a in self.rig.storage:
                if a.name == asset_name and a.encrypted:
                    a.decrypt()
                    print(asset_name, "decrypted in rig storage")
                    return True
        # return chip
        if chip_source == "inventory":
            self.inventory.append(chip)
        elif chip_source == "rig" and self.rig:
            self.rig.storage.append(chip)
        print(asset_name, "not found/unable to decrypt")
        return False

    def upgrade_rig(self):
        # upgrade rig using a hardware patch

        if not self.rig:
            print("No rig to upgrade.")
            return False
        patch = self.pop_item("Hardware Patch")
        if patch is None:
            print("No Hardware Patch found in inventory")
            return False
        self.rig.upgrade(patch)
        print(self.rig.name, "upgraded to level", self.rig.upgrade_level)
        return True

    def repair_rig(self):
        # repair the rig using a cryptoToken

        if not self.rig:
            print("No rig.")
            return False
        token = self.pop_item("CryptoToken")
        if token is None:
            print("No CryptoToken to fix")
            return False
        success = self.rig.repair(token)
        if success:
            print(self.rig.name, "repaired")
            return True
        else:
            # if there was no repair needed, return the token to inventory
            self.inventory.append(token)
            print("Repair not needed")
            return False

    def store_asset_to_rig(self, asset_name: str, all_items: bool = False):
        # move an asset (or more) from the hacker inventory to the rig storage

        if not self.rig:
            print("No rig.")
            return False
        if all_items:
            moved = False
            # attempt to move each transferable asset individuallly
            for a in self.inventory[:]:
                if len(self.rig.storage) >= self.rig.storage_capacity:
                    break
                if not a.encrypted:
                    self.inventory.remove(a)
                    self.rig.storage.append(a)
                    moved = True
            print("Moved all possible items to rig" if moved else "Nothing to move")
            return moved
        else:
            for i, a in enumerate(self.inventory):
                if a.name == asset_name:
                    if a.encrypted:
                        print("Cannot move encrypted item")
                        return False
                    if len(self.rig.storage) >= self.rig.storage_capacity:
                        print("Rig storage full")
                        return False
                    self.rig.storage.append(self.inventory.pop(i))
                    print(asset_name, "moved to rig storage")
                    return True
            print(asset_name, "not found in inventory")
            return False

    def retrieve_from_rig(self, asset_name: str | None = None, all_items: bool = False):
        # more asset (or more) from rig storage to hacker inventory
        # the encrypted assets can't be moved

        if not self.rig:
            print("No rig")
            return False
        if all_items:
            moved = False
            for a in self.rig.storage[:]:
                if a.encrypted:
                    continue
                self.rig.storage.remove(a)
                self.inventory.append(a)
                moved = True
            print("Got all items from rig" if moved else "No items")
            self.trace_level += 1  # retrieving may increase trace slightly
            return moved
        else:
            for i, a in enumerate(self.rig.storage):
                if a.name == asset_name:
                    if a.encrypted:
                        print("Cannot take encrypted item")
                        return False
                    self.inventory.append(self.rig.storage.pop(i))
                    self.trace_level += 1
                    print(asset_name, "taken from rig")
                    return True
            print(asset_name, "missing in rig storage")
            return False

    def scan_inventory_for(self, asset_name: str) -> Asset | None:
        # find and remove an asset (by name) from the inventory

        for i, a in enumerate(self.inventory):
            if a.name == asset_name:
                return self.inventory.pop(i)
        return None

    def extract_from_broken_rig(self, target_rig):
        # if the target rig is broken, use a removable drive from own rig storage (or own inventory)
        # to extract all the unencrypted assets from target rig into hacker inventory

        if not target_rig.broken:
            print("Target rig is not broken")
            return False
        # find removable drive in own rig storage first, else then in inventory
        removable = None
        # prefer rig storage if exists
        if self.rig:
            for i, a in enumerate(self.rig.storage):
                if a.name == "Removable Drive":
                    removable = self.rig.storage.pop(i)
                    break
        if removable is None:
            # look in hacker inventory
            for i, a in enumerate(self.inventory):
                if a.name == "Removable Drive":
                    removable = self.inventory.pop(i)
                    break
        if removable is None:
            print("No Removable drive to extract.")
            return False
        # extract unencrypted assets from target rig
        extracted = []
        for a in target_rig.storage[:]:
            if not a.encrypted:
                extracted.append(a)
                target_rig.storage.remove(a)
        if extracted:
            self.inventory.extend(extracted)
            self.trace_level += 2  # extraction is risky
            print("Pulled", len(extracted), "items from", target_rig.name)
            return True
        else:
            print("Nothing to extract")
            return False

    def reduce_trace(self, amount=1):
        # reduce the trace level
        # it can't go below 0

        self.trace_level = max(0, self.trace_level - amount)
        print("Trace now", self.trace_level)
