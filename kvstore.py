#!/usr/bin/env python3
# EUID: kjl0146
# Simple key-value store - CSCE 4350 build a database
# stores data in a file so it doesnt get lost on restart

import sys
import os

DB_FILE = "data.db"


# node for my linked list
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# using a linked list instead of a dict like the assignment says
class KVIndex:

    def __init__(self):
        self.head = None

    # just tack a new node onto the end every time
    def set(self, key, value):
        new_node = Node(key, value)
        if self.head is None:
            self.head = new_node
            return
        curr = self.head
        while curr.next is not None:
            curr = curr.next
        curr.next = new_node

    # scan the whole list, keep overwriting result so we get the latest value
    def get(self, key):
        curr = self.head
        found = None
        while curr is not None:
            if curr.key == key:
                found = curr.value
            curr = curr.next
        return found


# write to the log file
def save(key, value):
    with open(DB_FILE, "a", encoding="utf-8") as f:
        f.write(f"SET {key} {value}\n")


# read the log file on startup and rebuild the index
def load(index):
    if not os.path.exists(DB_FILE):
        return
    with open(DB_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(" ", 2)
            # skip anything thats not a SET line
            if len(parts) == 3 and parts[0] == "SET":
                index.set(parts[1], parts[2])


def main():
    index = KVIndex()
    load(index)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split(" ", 2)
        cmd = parts[0].upper()

        if cmd == "SET":
            if len(parts) < 3:
                print("ERROR: need a key and value")
            else:
                save(parts[1], parts[2])
                index.set(parts[1], parts[2])
                print("OK")

        elif cmd == "GET":
            if len(parts) < 2:
                print("ERROR: need a key")
            else:
                val = index.get(parts[1])
                if val is None:
                    print("")
                else:
                    print(val)

        elif cmd == "EXIT":
            sys.exit(0)

        else:
            print(f"ERROR: unknown command '{cmd}'")

        sys.stdout.flush()


if __name__ == "__main__":
    main()