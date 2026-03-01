#!/usr/bin/env python3
import os
import sys
import base64
import zlib
import bz2
import uu
import io
import random
import argparse
import threading
import time
import marshal
import subprocess
import string
from pathlib import Path
from colorama import Fore, init

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
    from Crypto.Random import get_random_bytes
    AES_AVAILABLE = True
except ImportError:
    AES_AVAILABLE = False

init(autoreset=True)

AUTHOR = "g0w6y"
TOOL_NAME = "Obsor"
VERSION = "2.0"

BANNER = r"""
        _                         
   __.  \ ___    ____   __.  .___ 
 .'   \ |/   \  (     .'   \ /   \ 
 |    | |    `  `--.  |    | |   '
  `._.' `___,' \___.'  `._.' /    
"""

PRESETS = {
    'military': ['minify', 'aes', 'zlib', 'base85', 'split', 'reverse', 'marshal', 'vigenere'],
    'max': ['minify', 'aes', 'marshal', 'bz2', 'base64', 'xor', 'whitespace', 'rc4'],
    'light': ['base64', 'reverse'],
    'stealth': ['whitespace', 'split', 'charcode', 'hex', 'url'],
}

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show_banner():
    clear_screen()
    print(Fore.CYAN + BANNER)
    print(Fore.YELLOW + f"Author: {AUTHOR} | Version: {VERSION}\n")

def animate_obfuscation(stop_event):
    chars = ["|", "/", "-", "\\"]
    while not stop_event.is_set():
        for c in chars:
            sys.stdout.write(f"\r{Fore.CYAN}[⏳] Obfuscating... {c} ")
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write("\r" + " " * 50 + "\r")

class ObfuscationMethod:
    name = "base"
    description = "Base method"
    @staticmethod
    def apply(code, **kwargs):
        raise NotImplementedError

class Base64Method(ObfuscationMethod):
    name = "base64"
    description = "Base64 encoding"
    @staticmethod
    def apply(code, **kwargs):
        encoded = base64.b64encode(code.encode()).decode()
        return f'''import base64
exec(compile(base64.b64decode({repr(encoded)}).decode(), '<string>', 'exec'))
'''

class XORMethod(ObfuscationMethod):
    name = "xor"
    description = "XOR encryption (single byte)"
    @staticmethod
    def apply(code, **kwargs):
        key = kwargs.get('key')
        if key is None:
            key = random.randint(1, 255)
            print(Fore.YELLOW + f"[!] Generated random XOR key: {key}")
        elif isinstance(key, str):
            key = ord(key[0]) if key else random.randint(1, 255)
        elif not isinstance(key, int):
            key = random.randint(1, 255)
        
        encrypted = ''.join(chr(ord(c) ^ key) for c in code)
        encoded = base64.b64encode(encrypted.encode()).decode()
        return f'''import base64
_xor_key = {key}
_xor_data = base64.b64decode({repr(encoded)}).decode()
exec(compile(''.join(chr(ord(c) ^ _xor_key) for c in _xor_data), '<string>', 'exec'))
'''

class ROT13Method(ObfuscationMethod):
    name = "rot13"
    description = "ROT13 encoding"
    @staticmethod
    def apply(code, **kwargs):
        trans = str.maketrans(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm"
        )
        encoded = code.translate(trans)
        return f'''def _rot13(s):
    return s.translate(str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm"
    ))
exec(compile(_rot13({repr(encoded)}), '<string>', 'exec'))
'''

class ReverseMethod(ObfuscationMethod):
    name = "reverse"
    description = "Reverse entire code"
    @staticmethod
    def apply(code, **kwargs):
        rev = code[::-1]
        return f'''exec(compile({repr(rev)}[::-1], '<string>', 'exec'))
'''

class WhitespaceMethod(ObfuscationMethod):
    name = "whitespace"
    description = "Whitespace (tabs/spaces) encoding"
    @staticmethod
    def apply(code, **kwargs):
        binary = ''.join(format(ord(c), '08b') for c in code)
        ws = binary.replace('0', ' ').replace('1', '\t')
        return f'''def _ws_decode(s):
    b = ''.join(['0' if c == ' ' else '1' for c in s])
    return ''.join(chr(int(b[i:i+8], 2)) for i in range(0, len(b), 8))
exec(compile(_ws_decode({repr(ws)}), '<string>', 'exec'))
'''

class ZlibMethod(ObfuscationMethod):
    name = "zlib"
    description = "zlib compression + Base64"
    @staticmethod
    def apply(code, **kwargs):
        compressed = zlib.compress(code.encode())
        encoded = base64.b64encode(compressed).decode()
        return f'''import zlib, base64
exec(compile(zlib.decompress(base64.b64decode({repr(encoded)})).decode(), '<string>', 'exec'))
'''

class BZ2Method(ObfuscationMethod):
    name = "bz2"
    description = "bz2 compression + Base64"
    @staticmethod
    def apply(code, **kwargs):
        compressed = bz2.compress(code.encode())
        encoded = base64.b64encode(compressed).decode()
        return f'''import bz2, base64
exec(compile(bz2.decompress(base64.b64decode({repr(encoded)})).decode(), '<string>', 'exec'))
'''

class MarshalMethod(ObfuscationMethod):
    name = "marshal"
    description = "Marshal bytecode"
    @staticmethod
    def apply(code, **kwargs):
        code_obj = compile(code, '<string>', 'exec')
        marshaled = marshal.dumps(code_obj)
        encoded = base64.b64encode(marshaled).decode()
        return f'''import marshal, base64
exec(marshal.loads(base64.b64decode({repr(encoded)})))
'''

class AESMethod(ObfuscationMethod):
    name = "aes"
    description = "AES-256 CBC (requires pycryptodome)"
    @staticmethod
    def apply(code, **kwargs):
        if not AES_AVAILABLE:
            raise ImportError("pycryptodome not installed")
        key = kwargs.get('key')
        if key is None:
            key = get_random_bytes(32)
            print(Fore.YELLOW + f"[!] Generated random AES key (base64): {base64.b64encode(key).decode()}")
        else:
            from hashlib import sha256
            if isinstance(key, str):
                key = sha256(key.encode()).digest()
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded = pad(code.encode(), AES.block_size)
        encrypted = cipher.encrypt(padded)
        encoded_key = base64.b64encode(key).decode()
        encoded_iv = base64.b64encode(iv).decode()
        encoded_data = base64.b64encode(encrypted).decode()
        return f'''import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
_key = base64.b64decode({repr(encoded_key)})
_iv = base64.b64decode({repr(encoded_iv)})
_cipher = AES.new(_key, AES.MODE_CBC, _iv)
_data = base64.b64decode({repr(encoded_data)})
_decrypted = unpad(_cipher.decrypt(_data), AES.block_size)
exec(compile(_decrypted.decode(), '<string>', 'exec'))
'''

class MinifyMethod(ObfuscationMethod):
    name = "minify"
    description = "Remove comments and extra whitespace"
    @staticmethod
    def apply(code, **kwargs):
        import ast
        try:
            tree = ast.parse(code)
            minified = ast.unparse(tree)
        except:
            lines = code.splitlines()
            new_lines = []
            for line in lines:
                stripped = line.strip()
                if stripped and not stripped.startswith('#'):
                    new_lines.append(line.rstrip())
            minified = '\n'.join(new_lines)
        return minified

class SplitMethod(ObfuscationMethod):
    name = "split"
    description = "Split code into chunks and reassemble"
    @staticmethod
    def apply(code, **kwargs):
        chunk_size = kwargs.get('chunk_size', 50)
        chunks = [code[i:i+chunk_size] for i in range(0, len(code), chunk_size)]
        encoded = [base64.b64encode(c.encode()).decode() for c in chunks]
        return f'''import base64
_chunks = {repr(encoded)}
_code = ''.join(base64.b64decode(c).decode() for c in _chunks)
exec(compile(_code, '<string>', 'exec'))
'''

class HexMethod(ObfuscationMethod):
    name = "hex"
    description = "Hexadecimal encoding"
    @staticmethod
    def apply(code, **kwargs):
        hexed = code.encode().hex()
        return f'''exec(compile(bytes.fromhex({repr(hexed)}).decode(), '<string>', 'exec'))
'''

class Base32Method(ObfuscationMethod):
    name = "base32"
    description = "Base32 encoding"
    @staticmethod
    def apply(code, **kwargs):
        encoded = base64.b32encode(code.encode()).decode()
        return f'''import base64
exec(compile(base64.b32decode({repr(encoded)}).decode(), '<string>', 'exec'))
'''

class Base85Method(ObfuscationMethod):
    name = "base85"
    description = "Base85 encoding (Python 3.4+)"
    @staticmethod
    def apply(code, **kwargs):
        encoded = base64.b85encode(code.encode()).decode()
        return f'''import base64
exec(compile(base64.b85decode({repr(encoded)}).decode(), '<string>', 'exec'))
'''

class CharCodeMethod(ObfuscationMethod):
    name = "charcode"
    description = "Convert to ASCII codes"
    @staticmethod
    def apply(code, **kwargs):
        codes = [str(ord(c)) for c in code]
        codes_str = ','.join(codes)
        return f'''exec(compile(''.join(chr(int(i)) for i in [{codes_str}]), '<string>', 'exec'))
'''

class UUMethod(ObfuscationMethod):
    name = "uu"
    description = "UUEncode (Unix-to-Unix encoding)"
    @staticmethod
    def apply(code, **kwargs):
        data = code.encode()
        out = io.BytesIO()
        uu.encode(io.BytesIO(data), out, name="data", mode=0o666)
        encoded = out.getvalue().decode()
        return f'''import uu, io
_in = io.BytesIO({repr(encoded)}.encode())
_out = io.BytesIO()
uu.decode(_in, _out)
exec(compile(_out.getvalue().decode(), '<string>', 'exec'))
'''

class AtbashMethod(ObfuscationMethod):
    name = "atbash"
    description = "Atbash cipher (reverse alphabet mapping)"
    @staticmethod
    def apply(code, **kwargs):
        def atbash_char(c):
            if 'a' <= c <= 'z':
                return chr(ord('a') + (25 - (ord(c) - ord('a'))))
            elif 'A' <= c <= 'Z':
                return chr(ord('A') + (25 - (ord(c) - ord('A'))))
            else:
                return c
        encoded = ''.join(atbash_char(c) for c in code)
        return f'''def _atbash(s):
    res = []
    for c in s:
        if 'a' <= c <= 'z':
            res.append(chr(ord('a') + (25 - (ord(c) - ord('a')))))
        elif 'A' <= c <= 'Z':
            res.append(chr(ord('A') + (25 - (ord(c) - ord('A')))))
        else:
            res.append(c)
    return ''.join(res)
exec(compile(_atbash({repr(encoded)}), '<string>', 'exec'))
'''

class CaesarMethod(ObfuscationMethod):
    name = "caesar"
    description = "Caesar cipher with random shift (1-25)"
    @staticmethod
    def apply(code, **kwargs):
        shift = random.randint(1, 25)
        def caesar_char(c):
            if 'a' <= c <= 'z':
                return chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
            elif 'A' <= c <= 'Z':
                return chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
            else:
                return c
        encoded = ''.join(caesar_char(c) for c in code)
        return f'''_caesar_shift = {shift}
def _caesar_decode(s):
    res = []
    for c in s:
        if 'a' <= c <= 'z':
            res.append(chr((ord(c) - ord('a') - _caesar_shift) % 26 + ord('a')))
        elif 'A' <= c <= 'Z':
            res.append(chr((ord(c) - ord('A') - _caesar_shift) % 26 + ord('A')))
        else:
            res.append(c)
    return ''.join(res)
exec(compile(_caesar_decode({repr(encoded)}), '<string>', 'exec'))
'''

class VigenereMethod(ObfuscationMethod):
    name = "vigenere"
    description = "Vigenère cipher with random keyword"
    @staticmethod
    def apply(code, **kwargs):
        keyword = kwargs.get('key')
        if keyword is None:
            keyword = ''.join(random.choices(string.ascii_uppercase, k=8))
            print(Fore.YELLOW + f"[!] Generated random Vigenère keyword: {keyword}")
        elif isinstance(keyword, bytes):
            keyword = keyword.decode('latin1')
        elif not isinstance(keyword, str):
            keyword = ''.join(random.choices(string.ascii_uppercase, k=8))
        
        keyword = keyword.upper()
        encoded = []
        key_index = 0
        for c in code:
            if c.isalpha():
                shift = ord(keyword[key_index % len(keyword)]) - ord('A')
                if c.islower():
                    encoded.append(chr((ord(c) - ord('a') + shift) % 26 + ord('a')))
                else:
                    encoded.append(chr((ord(c) - ord('A') + shift) % 26 + ord('A')))
                key_index += 1
            else:
                encoded.append(c)
        encoded_str = ''.join(encoded)
        return f'''_keyword = {repr(keyword)}
def _vigenere_decode(s):
    res = []
    key_index = 0
    for c in s:
        if c.isalpha():
            shift = ord(_keyword[key_index % len(_keyword)]) - ord('A')
            if c.islower():
                res.append(chr((ord(c) - ord('a') - shift) % 26 + ord('a')))
            else:
                res.append(chr((ord(c) - ord('A') - shift) % 26 + ord('A')))
            key_index += 1
        else:
            res.append(c)
    return ''.join(res)
exec(compile(_vigenere_decode({repr(encoded_str)}), '<string>', 'exec'))
'''

class RC4Method(ObfuscationMethod):
    name = "rc4"
    description = "RC4 stream cipher (pure Python)"
    @staticmethod
    def apply(code, **kwargs):
        key = kwargs.get('key')
        if key is None:
            key_bytes = bytes([random.randint(0,255) for _ in range(16)])
            print(Fore.YELLOW + f"[!] Generated random RC4 key (base64): {base64.b64encode(key_bytes).decode()}")
        elif isinstance(key, str):
            key_bytes = key.encode('latin1')
        else:
            key_bytes = key
        
        def rc4(data, key):
            S = list(range(256))
            j = 0
            for i in range(256):
                j = (j + S[i] + key[i % len(key)]) % 256
                S[i], S[j] = S[j], S[i]
            i = j = 0
            result = []
            for byte in data:
                i = (i + 1) % 256
                j = (j + S[i]) % 256
                S[i], S[j] = S[j], S[i]
                k = S[(S[i] + S[j]) % 256]
                result.append(byte ^ k)
            return bytes(result)
        
        data = code.encode()
        encrypted = rc4(data, key_bytes)
        encoded_data = base64.b64encode(encrypted).decode()
        encoded_key = base64.b64encode(key_bytes).decode()
        return f'''import base64
_key = base64.b64decode({repr(encoded_key)})
_data = base64.b64decode({repr(encoded_data)})
def _rc4(data, key):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    result = []
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        k = S[(S[i] + S[j]) % 256]
        result.append(byte ^ k)
    return bytes(result)
_decrypted = _rc4(_data, _key)
exec(compile(_decrypted.decode(), '<string>', 'exec'))
'''

class PolybiusMethod(ObfuscationMethod):
    name = "polybius"
    description = "Polybius square cipher (A-Z, I/J combined)"
    @staticmethod
    def apply(code, **kwargs):
        square = [['A','B','C','D','E'],
                  ['F','G','H','I','K'],
                  ['L','M','N','O','P'],
                  ['Q','R','S','T','U'],
                  ['V','W','X','Y','Z']]
        encode_map = {}
        for r in range(5):
            for c in range(5):
                ch = square[r][c]
                encode_map[ch] = f"{r+1}{c+1}"
                if ch == 'I':
                    encode_map['J'] = f"{r+1}{c+1}"
        encoded = []
        for ch in code.upper():
            if ch in encode_map:
                encoded.append(encode_map[ch])
            else:
                encoded.append(ch)
        encoded_str = ''.join(encoded)
        return f'''def _polybius_decode(s):
    square = [['A','B','C','D','E'],
              ['F','G','H','I','K'],
              ['L','M','N','O','P'],
              ['Q','R','S','T','U'],
              ['V','W','X','Y','Z']]
    res = []
    i = 0
    while i < len(s):
        if s[i].isdigit() and i+1 < len(s) and s[i+1].isdigit():
            r = int(s[i]) - 1
            c = int(s[i+1]) - 1
            if 0 <= r < 5 and 0 <= c < 5:
                res.append(square[r][c])
                i += 2
            else:
                res.append(s[i])
                i += 1
        else:
            res.append(s[i])
            i += 1
    return ''.join(res)
exec(compile(_polybius_decode({repr(encoded_str)}), '<string>', 'exec'))
'''

class OctalMethod(ObfuscationMethod):
    name = "octal"
    description = "Octal encoding"
    @staticmethod
    def apply(code, **kwargs):
        octal = ''.join(format(ord(c), '03o') for c in code)
        return f'''def _octal_decode(s):
    return ''.join(chr(int(s[i:i+3], 8)) for i in range(0, len(s), 3))
exec(compile(_octal_decode({repr(octal)}), '<string>', 'exec'))
'''

class URLMethod(ObfuscationMethod):
    name = "url"
    description = "URL percent-encoding"
    @staticmethod
    def apply(code, **kwargs):
        import urllib.parse
        encoded = urllib.parse.quote(code)
        return f'''import urllib.parse
exec(compile(urllib.parse.unquote({repr(encoded)}), '<string>', 'exec'))
'''

METHODS = {
    'base64': Base64Method,
    'xor': XORMethod,
    'rot13': ROT13Method,
    'reverse': ReverseMethod,
    'whitespace': WhitespaceMethod,
    'zlib': ZlibMethod,
    'bz2': BZ2Method,
    'marshal': MarshalMethod,
    'aes': AESMethod,
    'minify': MinifyMethod,
    'split': SplitMethod,
    'hex': HexMethod,
    'base32': Base32Method,
    'base85': Base85Method,
    'charcode': CharCodeMethod,
    'uu': UUMethod,
    'atbash': AtbashMethod,
    'caesar': CaesarMethod,
    'vigenere': VigenereMethod,
    'rc4': RC4Method,
    'polybius': PolybiusMethod,
    'octal': OctalMethod,
    'url': URLMethod,
}

def apply_layers(original_code, methods, **kwargs):
    current = original_code
    applied = []
    for m in methods:
        if m not in METHODS:
            raise ValueError(f"Unknown method: {m}")
        meth = METHODS[m]
        if m == 'minify':
            current = meth.apply(current, **kwargs)
            applied.append('minify')
        else:
            current = meth.apply(current, **kwargs)
            applied.append(m)
    return current, applied

def build_executable(script_path, onefile=True, console=True, icon=None):
    print(Fore.YELLOW + "\n[⚙] Building executable...")
    cmd = ["pyinstaller"]
    if onefile:
        cmd.append("--onefile")
    if not console:
        cmd.append("--noconsole")
    if icon:
        cmd.extend(["--icon", icon])
    cmd.append(str(script_path))
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(Fore.GREEN + "[✔] Executable created in dist/")
        else:
            print(Fore.RED + "[!] PyInstaller failed:\n" + res.stderr)
    except FileNotFoundError:
        print(Fore.RED + "[!] PyInstaller not found. Install: pip install pyinstaller")

def test_obfuscated(script_path):
    print(Fore.YELLOW + f"\n[🧪] Testing obfuscated script: {script_path}")
    try:
        res = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=10)
        if res.returncode == 0:
            print(Fore.GREEN + "[✔] Test passed: script executed successfully")
            if res.stdout:
                print(Fore.CYAN + "Output:\n" + res.stdout[:500] + "..." if len(res.stdout) > 500 else res.stdout)
        else:
            print(Fore.RED + f"[!] Test failed with return code {res.returncode}")
            if res.stderr:
                print(Fore.RED + "Error:\n" + res.stderr)
    except subprocess.TimeoutExpired:
        print(Fore.RED + "[!] Test timed out - trying direct execution...")
        try:
            exec(open(script_path).read())
        except Exception as e:
            print(Fore.RED + f"[!] Direct execution error: {e}")
    except Exception as e:
        print(Fore.RED + f"[!] Test error: {e}")

def save_keys(key_data, output_base):
    key_file = output_base + ".keys"
    with open(key_file, 'w') as f:
        f.write(key_data)
    print(Fore.YELLOW + f"[🔑] Keys saved to {key_file}")

def parse_args():
    p = argparse.ArgumentParser(description="Advanced Python Obfuscator - Military Grade Obfuscation Available")
    p.add_argument('-i', '--input', required=True, help="Input Python file")
    p.add_argument('-o', '--output', default='obfuscated.py', help="Output file")
    p.add_argument('-m', '--methods', default='base64', help="Comma-separated methods (use --preset to override)")
    p.add_argument('--preset', choices=['military', 'max', 'light', 'stealth'], 
                   help="Use predefined obfuscation preset (overrides -m)")
    p.add_argument('-k', '--key', help="Global key for methods that support it (XOR, AES, Vigenère, RC4). If not provided, random keys are generated per method.")
    p.add_argument('--chunk-size', type=int, default=50, help="Chunk size for split method")
    p.add_argument('--list-methods', action='store_true', help="List all available methods")
    p.add_argument('--build-exe', action='store_true', help="Build executable with PyInstaller after obfuscation")
    p.add_argument('--exe-onefile', action='store_true', default=True, help="PyInstaller one-file mode (default)")
    p.add_argument('--exe-console', action='store_true', default=True, help="PyInstaller console mode (default)")
    p.add_argument('--exe-icon', help="Icon file for executable")
    p.add_argument('--test', action='store_true', help="Test obfuscated script by running it")
    p.add_argument('--save-keys', action='store_true', help="Save generated keys to a file")
    return p.parse_args()

def list_methods():
    print(Fore.CYAN + "\nAvailable methods:\n")
    for name, meth in METHODS.items():
        req = " (requires pycryptodome)" if name == 'aes' and not AES_AVAILABLE else ""
        print(Fore.YELLOW + f"  {name:12} - {meth.description}{req}")
    print("\nPresets:")
    for preset, methods in PRESETS.items():
        print(Fore.GREEN + f"  {preset:10} -> {', '.join(methods)}")
    print()

def main():
    args = parse_args()
    show_banner()
    if args.list_methods:
        list_methods()
        return
    in_path = Path(args.input)
    if not in_path.is_file():
        print(Fore.RED + f"[!] File not found: {args.input}")
        return
    
    if args.preset:
        method_list = PRESETS[args.preset]
        print(Fore.CYAN + f"[*] Using preset '{args.preset}': {', '.join(method_list)}")
        if any(m in ['aes', 'vigenere', 'rc4', 'xor'] for m in method_list) and args.key is None:
            print(Fore.YELLOW + "[!] Some methods will generate random keys")
    else:
        method_list = [m.strip() for m in args.methods.split(',') if m.strip()]
    
    for m in method_list:
        if m not in METHODS:
            print(Fore.RED + f"[!] Unknown method: {m}")
            list_methods()
            return
    
    with open(in_path, 'r', encoding='utf-8') as f:
        original = f.read()
    
    stop = threading.Event()
    anim = threading.Thread(target=animate_obfuscation, args=(stop,))
    anim.start()
    try:
        obf_code, applied = apply_layers(original, method_list, key=args.key, chunk_size=args.chunk_size)
    except Exception as e:
        stop.set()
        anim.join()
        print(Fore.RED + f"\n[!] Error: {e}")
        import traceback
        traceback.print_exc()
        return
    stop.set()
    anim.join()
    
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(obf_code)
    print(Fore.GREEN + f"\n[✔] Saved to {args.output}")
    print(Fore.CYAN + f"    Layers: {' → '.join(applied)}")
    
    if args.test:
        test_obfuscated(args.output)
    
    if args.build_exe:
        build_executable(args.output, args.exe_onefile, args.exe_console, args.exe_icon)

if __name__ == "__main__":
    main()
