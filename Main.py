"""
File: main.py
Description: <Runs all test scenarios. Creates hackers and rigs, runs attacks, upgrades, encryption, and trace tests.>
Author: <Amy Lukan>
ID: <110458803>
Username: <LUKAY008>
This is my own work as defined by the University's Academic Misconduct Policy.
"""
from Hacker import Hacker
from Rig import Rig
from Asset import Asset

def print_separator():
    print("\n" + "="*60 + "\n")

def scenario_basic_flow():
    print_separator()
    print("/n--- basic test: to acquire and upgrade ---")
    alice = Hacker("Nyx")
    print(alice)
    # try to get rig (costs 1 CryptoToken)
    alice.acquire_rig()  # uses initial CryptoToken
    print(alice)
    # generate a few assets on rig
    alice.rig.generate_asset()
    alice.rig.generate_asset()
    print(alice.rig)
    # store generated asset into hacker inventory by retrieving
    alice.retrieve_from_rig(all_items=True)
    print(alice)
    # attempt upgrade without patch
    alice.upgrade_rig()  # it should fail
    # give hardware patch and upgrade
    alice.inventory.append(Asset("Hardware Patch", "Used to upgrade rigs"))
    alice.upgrade_rig()
    print(alice.rig)

def scenario_attack_and_extract():
    print_separator()
    print("/n--- attack and extract test ---")
    attacker = Hacker("ZeroCool")
    defender = Hacker("CrashOverride")
    # both get rigs
    attacker.acquire_rig(Rig("ZeroRig"))
    defender.acquire_rig(Rig("CrashBox"))
    # attacker rig already has 2 data spikes. Launch twice
    attacker.launch_data_spike(defender.rig)
    print(defender.rig)
    attacker.launch_data_spike(defender.rig)
    print(defender.rig)
    # defender rig should now be broken and attacker tries to extract
    # ensure attacker has a removable drive
    attacker.extract_from_broken_rig(defender.rig)
    print(attacker)
    print(defender.rig)

def scenario_encryption_edge_cases():
    print_separator()
    print("/n--- encryption stuff ---")
    h = Hacker("Cipher")
    h.acquire_rig()
    # add a security chip to inventory
    h.inventory.append(Asset("Security Chip", "Used to encrypt/decrypt"))
    # add a valuable asset to inventory
    h.inventory.append(Asset("Secret Data", "Sensitive file"))
    # encrypt it
    h.encrypt_asset("Secret Data", use_from="inventory")
    # try to store encrypted asset to rig (should fail)
    h.store_asset_to_rig("Secret Data")
    # decrypt it using security chip from rig storage (don't have one there)
    # put chip into rig storage to test using rig chip
    chip = h.pop_item("Security Chip")
    h.rig.storage.append(chip)
    # now decrypt (should fail because asset not in rig), then decrypt from inventory
    # add another security chip to inventory to decrypt
    h.inventory.append(Asset("Security Chip", "Used to encrypt/decrypt"))
    h.decrypt_asset("Secret Data", use_from="inventory")
    print(h)

def scenario_trace_limit():
    print_separator()
    print("/n--- trace test ---")
    a = Hacker("Tracer")
    b = Hacker("Target")
    a.acquire_rig()
    b.acquire_rig()
    # artificially increase a's trace above threshold
    a.trace_level = Hacker.TRACE_THRESHOLD + 1
    success = a.launch_data_spike(b.rig)  # should be blocked
    print("success?", success)
    a.reduce_trace(3)  # lower trace a bit
    # still might be over threshold
    success = a.launch_data_spike(b.rig)
    print("success after lowering trace:", success)

if __name__ == "__main__":
    scenario_basic_flow()
    scenario_attack_and_extract()
    scenario_encryption_edge_cases()
    scenario_trace_limit()
