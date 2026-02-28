
Obsor – Python Obfuscation Framework
<img width="720" height="720" alt="obsor" src="https://github.com/user-attachments/assets/bad7edad-e5f6-4f28-9fab-5722a173f6ab" />

Obsor is an advanced, multi-layer Python code obfuscation framework designed for
code protection, intellectual property security, and security research. It supports
over 20 obfuscation and encryption techniques, preset protection profiles, executable
building, and automated testing.

This tool focuses on making Python source code difficult to analyze while maintaining
full runtime compatibility.

------------------------------------------------------------

Features
--------

- 23+ obfuscation and encoding techniques
- Multi-layer obfuscation (unlimited stacking)
- Preset protection modes (military, max, light, stealth)
- AES-256-CBC encryption using pycryptodome
- Pure-Python RC4 implementation
- Classical cipher support (Vigenère, Caesar, Atbash, Polybius)
- Compression-based obfuscation (zlib, bz2)
- Bytecode serialization using marshal
- Automatic random key generation
- Optional custom keys for supported methods
- Executable builder using PyInstaller
- Built-in obfuscated script testing
- Cross-platform support (Windows, macOS, Linux)
- Colored CLI output and progress animation

------------------------------------------------------------

Obfuscation Techniques Explained
--------------------------------

Encoding:
- Base64 / Base32 / Base85
- Hexadecimal
- Octal
- URL percent encoding
- UUEncode
- Character code conversion

Encryption:
- AES-256-CBC (secure symmetric encryption)
- XOR (single-byte)
- RC4 stream cipher
- Vigenère cipher
- Caesar cipher
- Atbash cipher
- Polybius square cipher

Compression:
- zlib (DEFLATE)
- bz2 (BZIP2)

Bytecode:
- Marshal serialization (Python bytecode)

Layering / Transformation:
- Minify (remove comments and extra whitespace)
- Reverse
- Split (chunk-based reconstruction)
- Whitespace encoding (tabs/spaces)
- ROT13

------------------------------------------------------------

Preset Modes
------------

military  
`minify → aes → zlib → base85 → split → reverse → marshal → vigenere `

max  
`minify → aes → marshal → bz2 → base64 → xor → whitespace → rc4  `

light  
base64 → reverse  

stealth  
`whitespace → split → charcode → hex → url `

------------------------------------------------------------

Installation
------------

Clone the repository:
```
git clone https://github.com/g0w6y/obsor
cd obsor
```
Install dependencies:
```
pip install -r requirements.txt
```
------------------------------------------------------------

Requirements
------------

- Python 3.7 or newer

Optional:
- pycryptodome (required for AES)
- pyinstaller (required for executable building)
- colorama (for colored output)

------------------------------------------------------------

Basic Usage
-----------
```
python obsor.py -i input_script.py -o output.py
```
------------------------------------------------------------

Command Line Interface
----------------------
```
python obsor.py [-h]
    -i INPUT
    [-o OUTPUT]
    [-m METHODS]
    [--preset {military,max,light,stealth}]
    [-k KEY]
    [--chunk-size CHUNK_SIZE]
    [--list-methods]
    [--build-exe]
    [--exe-onefile]
    [--exe-console]
    [--exe-icon EXE_ICON]
    [--test]
    [--save-keys]
```
------------------------------------------------------------

Usage Examples
--------------

Basic obfuscation:
```
python obsor.py -i script.py -o obfuscated.py -m base64,zlib
```
Military-grade preset with executable:
```
python obsor.py -i script.py --preset military --build-exe
```
AES encryption with custom key:
```
python obsor.py -i script.py -m aes,base85 -k "MySecretKey123"
```
Test obfuscated script:
```
python obsor.py -i script.py -m base64,zlib --test
```
List available methods:
```
python obsor.py --list-methods
```
Create standalone executable with icon:
```
python obsor.py -i script.py --preset max --build-exe --exe-icon icon.ico
```
------------------------------------------------------------

Cross-Platform Notes
--------------------

- Fully compatible with Windows, macOS, and Linux
- Generated executables are OS-specific
- Marshal output depends on Python version
- AES requires pycryptodome to be installed on the target system

------------------------------------------------------------

Project Structure
-----------------
```
obsor/
├── obsor.py
├── requirements.txt
├── README.md
├── LICENSE
└── dist/
```
------------------------------------------------------------

⚠ Disclaimer
------------

This tool is intended for educational purposes, security research,
and legitimate code protection only.

Do NOT use for:
- Malicious code distribution
- Bypassing security measures
- Illegal activities
- Hiding malware or viruses

The author g0w6y is not responsible for any misuse or damage caused by this tool.
Users are solely responsible for complying with all applicable local, state,
and federal laws.

------------------------------------------------------------

Contributing
------------

Contributions, issues, and feature requests are welcome.

Steps:
- Fork the repository
- Create a feature branch
- Commit your changes
- Push to the branch
- Open a pull request

------------------------------------------------------------

## ⚖️ Attribution & Licensing

This project is licensed under the **Apache License 2.0**. 

If you use this framework in your own projects, redistribution, or security research, you **must** provide credit by linking back to the original author:
- **Project:** Obsor Python Obfuscator  
- **Author:** [g0w6y](https://github.com/g0w6y)  
- **Repository:** [https://github.com/g0w6y/obsor](https://github.com/g0w6y/obsor)

![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=flat-square)

Built by g0w6y
