<h1 align="center">
  <img src="https://github.com/user-attachments/assets/bad7edad-e5f6-4f28-9fab-5722a173f6ab" alt="Obsor" width="420">
</h1>

<p align="center">
  <b>Advanced multi-layer Python obfuscation framework</b><br>
  AES-256 encryption · 23+ techniques · Preset profiles · Executable builder
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7%2B-blue?style=flat-square&logo=python&logoColor=white">
  <img src="https://img.shields.io/github/license/g0w6y/obsor?style=flat-square&color=green">
  <img src="https://img.shields.io/github/stars/g0w6y/obsor?style=flat-square&color=yellow">
  <img src="https://img.shields.io/github/last-commit/g0w6y/obsor?style=flat-square&color=blue">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square">
</p>

---

## What is Obsor?

Obsor is an open-source Python code obfuscation framework that makes your source code extremely difficult to reverse-engineer — while keeping it fully functional at runtime.

It supports **23+ obfuscation and encryption techniques**, preset protection profiles, standalone executable building, and built-in self-testing.

---

## Features

| Category | Techniques |
|---|---|
| **Encoding** | Base64, Base32, Base85, Hex, Octal, URL, UUEncode, Charcode |
| **Encryption** | AES-256-CBC, XOR, RC4, Vigenère, Caesar, Atbash, Polybius |
| **Compression** | zlib (DEFLATE), bz2 (BZIP2) |
| **Bytecode** | Marshal serialization |
| **Transform** | Minify, Reverse, Split, Whitespace encoding, ROT13 |

- Multi-layer stacking (unlimited depth)
- Automatic random key generation
- Optional custom keys
- 4 built-in preset profiles
- PyInstaller executable builder
- Built-in obfuscated script self-test
- Colored CLI with progress animation

---

## Installation

```bash
git clone https://github.com/g0w6y/obsor
cd obsor
pip install -r requirements.txt
```

**Requirements:** Python 3.7+

Optional dependencies:
- `pycryptodome` — required for AES-256
- `pyinstaller` — required for executable building
- `colorama` — colored terminal output

---

## Quick Start

```bash
# Basic obfuscation
python main.py -i script.py -o protected.py -m base64,zlib

# Use a preset
python main.py -i script.py --preset military

# Test that obfuscated output still works
python main.py -i script.py --preset max --test

# Build a standalone executable
python main.py -i script.py --preset military --build-exe
```

---

## Preset Profiles

| Preset | Pipeline | Use Case |
|---|---|---|
| `military` | `minify → aes → zlib → base85 → split → reverse → marshal → vigenere` | Maximum protection |
| `max` | `minify → aes → marshal → bz2 → base64 → xor → whitespace → rc4` | Heavy multi-layer |
| `stealth` | `whitespace → split → charcode → hex → url` | Evade static analysis |
| `light` | `base64 → reverse` | Quick / lightweight |

```bash
python main.py -i script.py --preset military
python main.py -i script.py --preset stealth
python main.py -i script.py --preset light
```

---

## CLI Reference

```
python main.py [-h]
    -i INPUT                     Input Python script
    [-o OUTPUT]                  Output file (default: obfuscated_<input>)
    [-m METHODS]                 Comma-separated methods (e.g. aes,base64,zlib)
    [--preset {military,max,light,stealth}]
    [-k KEY]                     Custom key for supported methods
    [--chunk-size CHUNK_SIZE]    Chunk size for split method
    [--list-methods]             List all available obfuscation methods
    [--build-exe]                Build standalone executable via PyInstaller
    [--exe-onefile]              Single-file executable
    [--exe-console]              Console mode executable
    [--exe-icon EXE_ICON]        Icon file for executable
    [--test]                     Run and verify the obfuscated output
    [--save-keys]                Save generated keys to a file
```

---

## Examples

See [`examples/`](examples/) for ready-to-use sample scripts.

```bash
# Try obsor on the included sample script
python main.py -i examples/sample_input.py --preset military --test

# AES with a custom key
python main.py -i examples/sample_input.py -m aes,base85 -k "MySecretKey123"

# Save keys + build exe
python main.py -i examples/sample_input.py --preset max --build-exe --save-keys
```

The file `obsor.py` in the root is `main.py` obfuscated with the `military` preset — a live demo of what Obsor produces.

---

## Project Structure

```
obsor/
├── main.py               # Main obfuscation engine
├── obsor.py              # main.py obfuscated (military preset demo)
├── examples/
│   ├── sample_input.py   # Sample script for testing
│   └── README.md         # Example usage guide
├── requirements.txt
├── README.md
├── LICENSE               # Apache 2.0
└── NOTICE
```

---

## Cross-Platform Notes

- Windows, macOS, and Linux all supported
- Generated executables are OS-specific (build on the target OS)
- `marshal` output is Python version-dependent — obfuscate and run on the same Python version
- AES requires `pycryptodome` on the machine running the obfuscated script

---

## Contributing

Contributions, issues, and feature requests are welcome.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add: my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## Disclaimer

This tool is intended for **educational purposes, security research, and legitimate code protection only.**

Do **not** use Obsor to distribute malware, bypass security systems, or for any illegal activity. The author is not responsible for misuse.

---

## License

Licensed under the [Apache License 2.0](LICENSE).

Built by [g0w6y](https://github.com/g0w6y)
