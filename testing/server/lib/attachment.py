from email.message import EmailMessage

def extract_attachment_text(email_message: EmailMessage):
    """
    Extracts text content from attachments in an email.

    Args:
        email_message (email.message.EmailMessage): Email message object.

    Returns:
        list: List of text content extracted from attachments.
    """
    attachment_texts = []

    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        filename = part.get_filename()
        if filename:
            attachment_text = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
            attachment_texts.append(attachment_text)
            print("Attachment text:", attachment_text)

    return attachment_texts

# Example usage
# email_message = ...  # Your email message object
# attachment_texts = extract_attachment_text(email_message)
# print(attachment_texts)