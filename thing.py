import pickle
import base64
import os.path
from email.mime.text import MIMEText
from googleapiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def auth():
    creds = None
    # if the token already exists in token.pickle load it
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # if there aren't any valid creds log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

# Stolen from gmail api docs
def create_message(sender, to, subject, message_text):
    """Create a message for an email.
    
    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.
    
    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    print(message.as_string())
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

#Also stolen from gmail docs
def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    return message
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

def main():
    creds = auth()
    print("got here")
    service = build('gmail', 'v1', credentials=creds)
    message = create_message('sahan.reddy.58@gmail.com', 'jordanumusu@gmail.com',
                             'Bitch', 'bitch')
    send_message(service, 'me', message)

if __name__ == '__main__':
    main()
