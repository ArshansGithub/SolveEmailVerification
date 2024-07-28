# SolveEmailVerification

This repository provides a plug-and-play solution for bypassing email verification using the IMAP protocol. It features a `Verifier` class that connects to an email server, searches for specific emails, fetches them, and extracts verification codes.

## Features

- **IMAP Integration**: Easily connect to any IMAP-supported email server.
- **Catchall Support**: Use a catchall email to streamline the verification process.
- **Automated Email Handling**: Search and fetch emails based on specific criteria.
- **Verification Code Extraction**: Extract and manage verification codes from email bodies.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ArshansGithub/SolveEmailVerification.git
   cd SolveEmailVerification
   ```

2. **Install dependencies:**
   Make sure to install the required Python packages:
   ```bash
   pip install aioimaplib email
   ```

## Usage

1. **Initialize the Verifier:**
   ```python
   from verifier import Verifier

   verifier = Verifier()
   ```

2. **Connect to the email server:**
   ```python
   await verifier.connect('your-email@example.com', 'your-password')
   ```

3. **Fetch and process emails:**
   ```python
   await verifier.fetch_emails('from-email@example.com', 'Target Subject')
   ```

4. **Access the verification codes:**
   ```python
   print(verifier.emails)
   ```

5. **Close the connection:**
   ```python
   await verifier.close()
   ```

## Example

Here's a brief example of how to use the `Verifier` class:

```python
import asyncio
from verifier import Verifier

async def main():
    verifier = Verifier()
    await verifier.connect('your-email@example.com', 'your-password')
    await verifier.fetch_emails('from-email@example.com', 'Target Subject')
    print(verifier.emails)
    await verifier.close()

asyncio.run(main())
```

A more robust example can be seen in the examples directory.

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

This project is intended for educational and testing purposes only. Please use responsibly and in accordance with all relevant laws and terms of service.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas or improvements.

## Acknowledgments

Special thanks to the developers and communities that make open-source software possible.
