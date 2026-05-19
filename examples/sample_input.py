#!/usr/bin/env python3
"""
Sample script to demonstrate Obsor obfuscation.
Use this as input to test different obfuscation presets.

Usage:
  python main.py -i examples/sample_input.py -o output.py -m base64,zlib
  python main.py -i examples/sample_input.py --preset military
  python main.py -i examples/sample_input.py --preset stealth --test
"""

import os
import platform

def greet(name: str) -> str:
    return f"Hello, {name}! Running on {platform.system()} {platform.release()}"

def fibonacci(n: int) -> list:
    seq = [0, 1]
    for _ in range(n - 2):
        seq.append(seq[-1] + seq[-2])
    return seq[:n]

def secret_logic():
    key = "s3cr3t_k3y_2024"
    data = [ord(c) ^ 0x42 for c in key]
    return bytes(data).hex()

if __name__ == "__main__":
    print(greet("World"))
    print("Fibonacci(10):", fibonacci(10))
    print("Protected value:", secret_logic())
    print("CWD:", os.getcwd())
