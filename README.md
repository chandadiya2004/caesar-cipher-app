# Caesar Cipher App

A simple Streamlit web app to encrypt and decrypt text files using the Caesar cipher.

- Encryption mode: generates a random key (0–25) and shifts letters to produce an encrypted file.
- Decryption mode: brute-forces all 26 possible shifts and produces a file containing the output for each key so the user can inspect which plaintext is correct.

Built with Python and Streamlit.

## Table of contents

- [Demo](#demo)
- [Features](#features)
- [Repository structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the app](#running-the-app)
- [Usage](#usage)
- [How it works (implementation details)](#how-it-works-implementation-details)
- [Examples](#examples)
- [Testing & validation](#testing--validation)
- [Deployment suggestions](#deployment-suggestions)
- [Contributing](#contributing)
- [Security & privacy](#security--privacy)
- [License](#license)
- [Contact](#contact)

## Demo

The app is an interactive Streamlit application. Upload a `.txt` file, choose Encryption (random key) or Decryption (try all 26 combinations), and download the result.

## Features

- Encrypts a plain text file using a randomly chosen Caesar cipher key (0–25).
- Decrypts an encrypted or unknown text by producing all 26 shifted results so you can visually inspect which one is meaningful.
- Preserves non-alphabet characters (spaces, punctuation, numbers).
- Produces downloadable `.txt` outputs.

## Repository structure

- `app.py` — Main Streamlit application (UI + encryption/decryption logic)
- `requirement.txt` — Python package requirements (Streamlit)
- `LICENSE` — MIT license
- `README.md` — Original minimal README (this file is a more detailed documentation you can use)

## Prerequisites

- Python 3.8+ (recommended)
- pip

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/chandadiya2004/caesar-cipher-app.git
   cd caesar-cipher-app
   ```

2. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .venv\Scripts\activate      # Windows (PowerShell)
   ```

3. Install dependencies:

   ```bash
   pip install -r requirement.txt
   ```

   Or install Streamlit directly:

   ```bash
   pip install streamlit
   ```

## Running the app

Start the Streamlit app:

```bash
streamlit run app.py
```

This will open the app in your browser (usually at http://localhost:8501).

## Usage

1. Open the app in your browser.
2. Choose one of the options:
   - "Encryption (Random Key)" — uploads a `.txt` file, the app picks a random key between 0 and 25, encrypts alphabetic characters, and shows the random key used. A download button is available for `encrypted.txt`.
   - "Decryption (Try all 26 combinations)" — uploads a `.txt` file and the app produces the 26 possible decryptions (Key 0 through Key 25) in a single downloadable `decrypted.txt` file so you can find the readable plaintext.
3. Upload a `.txt` file using the uploader.
4. Click the download button to save the result.

Notes:
- Uppercase and lowercase letters are shifted preserving case.
- Non-letter characters (spaces, punctuation, numbers) are left unchanged.

## How it works (implementation details)

The Caesar cipher shifts alphabetic characters by a numeric key (k). This app's logic follows these rules:

- For uppercase letters: shift in the range `'A'..'Z'` (ASCII 65–90).
  - Encryption: result = chr((ord(ch) - 65 + key) % 26 + 65)
  - Decryption: result = chr((ord(ch) - 65 - key) % 26 + 65)
- For lowercase letters: shift in the range `'a'..'z'` (ASCII 97–122).
  - Encryption: result = chr((ord(ch) - 97 + key) % 26 + 97)
  - Decryption: result = chr((ord(ch) - 97 - key) % 26 + 97)
- Characters that are not alphabetic are kept as-is.

Key code excerpts (from `app.py`):

```python
# Encryption (random key)
key = random.randint(0, 25)
encrypted = ""
for ch in text:
    if ch.isupper():
        encrypted += chr((ord(ch) - 65 + key) % 26 + 65)
    elif ch.islower():
        encrypted += chr((ord(ch) - 97 + key) % 26 + 97)
    else:
        encrypted += ch

# Decryption (try all keys)
output = ""
for key in range(26):
    decrypted = ""
    for ch in text:
        if ch.isupper():
            decrypted += chr((ord(ch) - 65 - key) % 26 + 65)
        elif ch.islower():
            decrypted += chr((ord(ch) - 97 - key) % 26 + 97)
        else:
            decrypted += ch

    output += f"Key {key}:\n{decrypted}\n\n"
```

This logic ensures case preservation and handles wrap-around using modulo 26 arithmetic.

## Examples

Input file `message.txt`:

```
Hello, World! 123
```

- Encryption with key 3 => `Khoor, Zruog! 123` (app chooses a random key; this is a sample)
- Decryption: the app provides 26 keys; Key 23 (equivalently -3) will return `Hello, World! 123`

Typical workflow:
- If you encrypted with the app, use the displayed random key to decrypt manually (or re-run with key if you add manual-key feature).
- If you received a ciphertext and don't know the key, use "Decryption (Try all 26 combinations)" and pick the readable result.

## Testing & validation

This repository does not include automated tests. Suggested tests to add:

- Unit tests for shifting functions:
  - Verify encryption and decryption are inverses for all keys 0–25 for a sample set of strings containing uppercase, lowercase, and non-letters.
- Edge cases:
  - Empty file
  - File containing non-ASCII characters (the current code shifts only ASCII A–Z / a–z; non-ASCII characters are preserved as-is)
- Integration test:
  - Run the Streamlit UI in a headless environment and ensure upload and download buttons are present (or test the core logic functions directly).

Example unit test (pytest style, suggestion):

```python
def caesar_shift(text, key, encrypt=True):
    out = ""
    for ch in text:
        if ch.isupper():
            out += chr((ord(ch) - 65 + (key if encrypt else -key)) % 26 + 65)
        elif ch.islower():
            out += chr((ord(ch) - 97 + (key if encrypt else -key)) % 26 + 97)
        else:
            out += ch
    return out

def test_roundtrip_all_keys():
    s = "Hello, World!"
    for k in range(26):
        enc = caesar_shift(s, k, encrypt=True)
        dec = caesar_shift(enc, k, encrypt=False)
        assert dec == s
```

## Deployment suggestions

- Streamlit Cloud: Push the repo to GitHub and deploy using Streamlit sharing. Ensure `requirement.txt` is present (it contains `streamlit`).
- Docker: Create a small Dockerfile to run the app in a container. Example:

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirement.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

- Add a GitHub Actions workflow to run unit tests (if added) on push/PR.

## Possible improvements / roadmap

- Add an option to enter a custom key for encryption/decryption.
- Add unit tests and a CI workflow.
- Support for other encodings (e.g., UTF-8 non-Latin characters) or specify behavior clearly.
- Add page to display the random key history or allow saving keys.
- Add CLI mode for batch processing without Streamlit UI.
- Provide optional file previews before/after.

## Contributing

Contributions are welcome. Suggested process:

1. Fork the repo.
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Implement code, add tests, and update documentation.
4. Open a pull request explaining the change.

Be sure to follow consistent code formatting and add tests for new logic.

## Security & privacy

- The app performs client-side file processing on the machine where Streamlit runs. If deployed as a public service, uploaded data may be processed on the server — do not upload sensitive data to public instances.
- There is no authentication built into the app. Add access controls when deploying to shared environments.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Contact

Repository: [chandadiya2004/caesar-cipher-app](https://github.com/chandadiya2004/caesar-cipher-app)

Author: DIYA CHANDA (see LICENSE)
