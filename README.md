# SolveEmailVerification

This Python script provides a simple, plug-and-play solution for bypassing email verification processes by leveraging the IMAP protocol. It allows you to dynamically filter emails and extract codes or links, perfect for automating tasks that require email verification.

## Features

- **IMAP4 SSL**: Secure connection to your email server.
- **Dynamic Filtering**: Customize how emails are filtered and what data is extracted.
- **Asynchronous Operation**: Efficient handling of email fetching and processing using asyncio.
- **Support for Any Email Server**: Although configured for Outlook, it can be easily adapted to any email server.

## Usage

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/ArshansGithub/SolveEmailVerification.git
   ```
2. Install dependencies:
   ```sh
   pip install aioimaplib email
   ```

### Example

Here's a basic example of how to use the `Verifier` class:

```python
import aioimaplib
import email
from email.header import decode_header
import asyncio
import traceback


class EmailVerifier:
    def __init__(self, host='outlook.office365.com', port=993):
        # Initialize the IMAP client with the specified host and port
        self.client = aioimaplib.IMAP4_SSL(host, port)
        self.emails = {}  # Dictionary to store fetched emails

    async def connect(self, email, password):
        # Connect and log in to the email server
        await self.client.wait_hello_from_server()
        try:
            await self.client.login(email, password)
        except aioimaplib.IMAP4.error as e:
            print("Failed to login")
            print(e)
            return
        # Select the INBOX folder
        await self.client.select('INBOX')

    async def close(self):
        # Log out and close the connection
        await self.client.logout()

    async def search_emails(self, from_email):
        # Search for emails from the specified sender
        search_criteria = f'(FROM "{from_email}")'
        return await self.client.search(search_criteria, charset='US-ASCII')

    async def fetch_email(self, email_id):
        # Fetch the email by its ID
        return await self.client.fetch(email_id, '(RFC822)')

    async def fetch_emails(self, from_email, subject_filter=None, body_filter=None, code_extractor=None):
        """
        Fetch emails based on dynamic filtering and extraction criteria.

        :param from_email: The email address to filter the sender.
        :param subject_filter: A function to filter email subjects. Should return True if the subject is a match.
        :param body_filter: A function to filter email bodies. Should return True if the body is a match.
        :param code_extractor: A function to extract the code or link from the email body; otherwise, the body is returned.
        """
        print("Fetching emails...")
        search_result, data = await self.search_emails(from_email)
        email_ids = data[0].split()

        for email_id in email_ids:
            fetch_result = await self.fetch_email(int(email_id))
            raw_email = fetch_result[1][1]
            msg = email.message_from_bytes(raw_email)

            # Decode the subject and determine the recipient email address
            to_email = msg["To"]
            subject, encoding = decode_header(msg["Subject"])[0]

            if isinstance(subject, bytes):
                subject = subject.decode(encoding or 'utf-8')

            # Apply the subject filter if provided
            if subject_filter and not subject_filter(subject):
                print(f"Skipping email with subject: {subject}")
                continue

            # Decode the body of the email
            body = msg.get_payload(decode=True).decode()

            # Apply the body filter if provided
            if body_filter and not body_filter(body):
                print(f"Skipping email with body: {body}")
                continue

            # Extract the code or link using the provided extractor function
            code = code_extractor(body) if code_extractor else body
            if code:
                # Mark the email as deleted after processing
                await self.client.store(int(email_id), '+FLAGS', '\\Deleted')
                self.emails[to_email] = code


# Function to extract a specific code or link from the email body
def extract_code(body):
    # Example code extraction logic. Modify as needed based on the email content.
    return (
        body.split('href="')[1].split('"')[0].strip()
    )


async def monitorEmails():
    # Continuously monitor the inbox for new emails
    while True:
        print(f"Monitoring: Email count: {len(verifier.emails)}")
        await asyncio.sleep(3)  # Wait for 3 seconds before checking again
        try:
            # Fetch emails with specific criteria
            await verifier.fetch_emails(
                "from_email@domain.com",
                subject_filter=lambda subject: "Subject to filter by" in subject,
                body_filter=lambda body: "This text must be in the body of the email" in body,
                code_extractor=extract_code
            )
            await verifier.client.expunge()  # Remove deleted emails
        except:
            print(traceback.format_exc())
            continue


async def someTask():
    email = "someemail@domain.com"

    # Insert logic to send email

    # Wait for the email to be received

    code = None
    while code is None:
        if email in verifier.emails:
            code = verifier.emails[email]
            verifier.emails.pop(email)
            break

        await asyncio.sleep(3)  # Check every 3 seconds

    print(f"Found code/link: {code}")


async def main():
    global verifier

    verifier = EmailVerifier()

    await verifier.connect('email@domain.com', 'password')

    # Start the email monitoring task
    asyncio.create_task(monitorEmails())

    # Start your tasks here

    while True:
        try:
            await asyncio.sleep(5)
        except KeyboardInterrupt:
            break

    await verifier.close()


if __name__ == "__main__":
    asyncio.run(main())
```

### Fetching Emails Dynamically

To fetch emails dynamically, specify the `from_email`, and optionally, provide `subject_filter`, `body_filter`, and `code_extractor` functions:

```python
await verifier.fetch_emails(
    "from_email@domain.com",
    subject_filter=lambda subject: "Subject to filter by" in subject,
    body_filter=lambda body: "This text must be in the body of the email" in body,
    code_extractor=extract_code
)
```

The `extract_code` function defines how to extract the desired code or link from the email body.

### Asynchronous Monitoring

The `monitorEmails` function continuously monitors the inbox for new emails that match the criteria and extracts the codes.

### Using the Extracted Code

To retrieve the extracted code, use:

```python
code = None
while code is None:
    if email in verifier.emails:
        code = verifier.emails[email]
        verifier.emails.pop(email)
        break

    await asyncio.sleep(3)

print(f"Found code/link: {code}")
```

This code snippet waits until the desired code or link is found in the inbox.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Feel free to fork this repository, make improvements, and submit pull requests. Contributions are welcome!
