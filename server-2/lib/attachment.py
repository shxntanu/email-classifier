import PyPDF2
import os

def extract_attachments(email_message):
    extracted_texts = []

    for part in email_message.walk():
        if part.get_content_disposition() == 'attachment':
            # Save the attachment to a file
            filename = part.get_filename()
            with open(filename, 'wb') as f:
                f.write(part.get_payload(decode=True))

            # Extract text from the file
            file_extension = os.path.splitext(filename)[1]

            if file_extension == '.pdf':
                pdf_file_obj = open(filename, 'rb')
                pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
                text = ''
                for page_num in range(len(pdf_reader.pages)):
                    page_obj = pdf_reader.pages[page_num]
                    text += page_obj.extract_text()
                pdf_file_obj.close()
            else:
                text = None

            os.remove(filename)

            if text is not None:
                extracted_texts.append(text)

    return extracted_texts

# example usage
# print(fetch_latest_mail_extract_attachments('imap.gmail.com', "mail@gmail.com", "your app pswd"))