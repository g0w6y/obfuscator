# Examples

This directory contains sample scripts to test and demonstrate Obsor.

## sample_input.py

A ready-to-use sample Python script with real logic (functions, loops, secrets).
Use it to test any obfuscation preset:

```bash
# Basic
python main.py -i examples/sample_input.py -o output.py -m base64,zlib

# Military preset
python main.py -i examples/sample_input.py --preset military

# Stealth preset with self-test
python main.py -i examples/sample_input.py --preset stealth --test

# AES + custom key
python main.py -i examples/sample_input.py -m aes,base85 -k "MyKey123"

# Build executable
python main.py -i examples/sample_input.py --preset max --build-exe
```

## obsor.py (in root)

The root  is  obfuscated with the  preset — a live demonstration
of what Obsor produces when applied to itself.
