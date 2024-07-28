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
