# Obfuscator - Python Code Obfuscation Tool

![Obfuscator](https://github.com/user-attachments/assets/db5233be-dc59-41ee-ad4e-d81c728c5b6d)

## 🛠 Tool Information

- **Tool Name:** Obfuscator  
- **Author:** g0w6y  
- **Description:** A Python-based tool designed to **obfuscate Python scripts** using multiple encoding and encryption techniques.  
- **Purpose:** Helps **protect Python code** by making it harder to read and analyze.  

---

## 🚀 Features
✔ Multiple **Obfuscation Techniques**:  
   - **Base64 Encoding** (Simple)  
   - **XOR Encryption** (Medium)  
   - **ROT13 Encoding** (Medium-High)  
   - **Reverse Code Obfuscation** (Medium)  
   - **Whitespace Obfuscation** (High)  

✔ **Fast and Secure Execution**  
✔ **Customizable Output File Name**  
✔ **No False Positives in Execution**  
✔ **Smooth User Experience with Animated Loading**  

---

## 📥 Installation

### **🔹 Clone the Repository**
```sh
git clone https://github.com/g0w6y/obfuscator
cd obfuscator
```

### **🔹 Install Dependencies**
```sh
pip install -r requirements.txt
```

---

## ⚡ Usage

### **Run the Tool**
```sh
python3 main.py
```

### **Obfuscation Process**
1️⃣ Choose the obfuscation method from the menu.  
2️⃣ Enter the Python file you want to obfuscate.  
3️⃣ Specify the output filename for the obfuscated script.  
4️⃣ Wait for the obfuscation process to complete.  

💡 **Example:**
```
[1] Base64 Encoding (Simple)
[2] XOR Encryption (Medium)
[3] ROT13 Encoding (Medium-High)
[4] Reverse Code Obfuscation (Medium)
[5] Whitespace Obfuscation (High)
[0] Exit

[?] Choose an option: 2
[?] Enter Python file to obfuscate: script.py
[?] Enter output filename (e.g., obfuscated.py): obfuscated_script.py
[✔] Obfuscating your code... Please wait.
[✔] Obfuscated.
```

---

## 🔑 Obfuscation Techniques Explained

| Method                  | Complexity | Description |
|-------------------------|------------|-------------|
| **Base64 Encoding**      | Simple     | Encodes code using Base64, reversible with `base64.b64decode()` |
| **XOR Encryption**       | Medium     | Encrypts using XOR with a random key, making it harder to decode |
| **ROT13 Encoding**       | Medium-High | Substitutes characters using ROT13 encoding |
| **Reverse Obfuscation**  | Medium     | Reverses the script text, requiring reversal to execute |
| **Whitespace Obfuscation** | High      | Converts script into binary, using whitespace characters (space/tab) |

---

## ⚠ Disclaimer
This tool is intended for **educational and security research purposes only**.  
Do **NOT** use it for malicious activities. The author is **not responsible** for any misuse.

---

## 🤝 Contributing
💡 Contributions, issues, and feature requests are welcome!  
To contribute, fork the repository, make changes, and submit a pull request.

---

## 📜 License
This project is licensed under the **MIT License**. See the `LICENSE` file for more details.

---
