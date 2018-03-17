import base64
import email
from googleapiclient import errors
from bs4 import BeautifulSoup

def GetMessage(service, msg_id, user_id="me", format="full"):
      """Get a Message with given ID.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        msg_id: The ID of the Message required.

      Returns:
        A Message.
      """
      try:
          message = service.users().messages().get(userId=user_id, id=msg_id,
                                                   format=format).execute()
          return message
      except errors.HttpError as error:
          print ('An error occurred: %s' % error)


def GetLabelMessages(service, user_id="me", label_ids=["INBOX"], numResults=7):
    """List all Messages of the user's mailbox with label_ids applied.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    label_ids: Only return Messages with these labelIds applied.

    Returns:
    List of Messages that have all required Labels applied. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate id to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId=user_id,
                                                   labelIds=label_ids,
                                                   maxResults=numResults)\
                                                   .execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])
        return messages
    except errors.HttpError as error:
        print ('An error occurred: %s' % error)


def ModifyMessage(service, msg_id, msg_labels, user_id='me'):
      """Modify the Labels on the given Message.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        msg_id: The id of the message required.
        msg_labels: The change in labels.

      Returns:
        Modified message, containing updated labelIds, id and threadId.
      """
      try:
          message = service.users().messages().modify(userId=user_id, id=msg_id,
                                                      body=msg_labels).execute()

      except errors.HttpError as error:
          print ('An error occurred: %s', error)


def cleanMe(html):
    soup = BeautifulSoup(html, "lxml") # create a new bs4 object from the html data loaded
    for script in soup(["script", "style"]): # remove all javascript and stylesheet code
        script.extract()
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text


def GetInboxMessages(service, num_msg=6):
    messages = GetLabelMessages(service, numResults=num_msg)
    messages_info = []
    for msg in messages:
        msg_id = msg.get('id')
        msg_details = GetMessage(service, msg_id)
        message_info = {'msg_id': msg_id,
                        'snippet': msg_details.get('snippet'),
                        'timestamp': int(msg_details.get('internalDate'))/1000,
                        'labels': msg_details.get('labelIds')}

        for entry in msg_details.get('payload').get('headers'):
            name = entry.get('name').lower()
            value = entry.get('value')
            if name == 'from':
                message_info['from'] = value
            elif name == 'reply-to':
                message_info['reply'] = value
            elif name == 'subject':
                message_info['subject'] = value
        try:
            if msg_details.get('payload').get('parts'):
                body_msg = msg_details.get('payload').get('parts')[-1]\
                           .get('body').get('data')
            else:
                body_msg = msg_details.get('payload').get('body').get('data')
            body_str = base64.urlsafe_b64decode(body_msg.encode('ASCII'))
            html_str = body_str.decode('UTF-8')
            message_info['body'] = cleanMe(html_str)
        except:
            message_info['body'] = "Failed to retrieve the email body, \
                                    please view it on the web./n"
        messages_info.append(message_info)
    return messages_info


def GetSentMessages(service, num_msg=6):
    messages = GetLabelMessages(service, label_ids=["SENT"], numResults=num_msg)
    messages_info = []
    for msg in messages:
        msg_id = msg.get('id')
        msg_details = GetMessage(service, msg_id)
        message_info = {'msg_id': msg_id,
                        'snippet': msg_details.get('snippet'),
                        'timestamp': int(msg_details.get('internalDate'))/1000}

        for entry in msg_details.get('payload').get('headers'):
            name = entry.get('name').lower()
            value = entry.get('value')
            if name == 'to':
                message_info['to'] = value
            elif name == 'subject':
                message_info['subject'] = value
        try:
            if msg_details.get('payload').get('parts'):
                body_msg = msg_details.get('payload').get('parts')[-1]\
                           .get('body').get('data')
            else:
                body_msg = msg_details.get('payload').get('body').get('data')
            body_str = base64.urlsafe_b64decode(body_msg.encode('ASCII'))
            html_str = body_str.decode('UTF-8')
            message_info['body'] = cleanMe(html_str)
        except:
            message_info['body'] = "Failed to retrieve the email body, \
                                    please view it on the web./n"
        messages_info.append(message_info)
    return messages_info
