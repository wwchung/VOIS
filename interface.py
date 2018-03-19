'''
Team VOIS
Won-Woo Chung, Guangyu Li, Daniel u, Akihiro Ota
EECS 498 Section 9
'''
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from threading import Thread
import time
import vois_phone
import vois_email
import vois_documents
import vois_websearch
import boto3
import datetime
import ast

# Load kv file
Builder.load_file('interface.kv')


#Builder.load_file('documents.kv')


# Define home screen
class HomeScreen(Screen):
    pass


# Define loading screen
class LoadingScreen(Screen):
    pass


# Create screen manager
sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(LoadingScreen(name='loading'))

# Add all phone screens
sm.add_widget(vois_phone.PhoneScreen(name='phone'))
sm.add_widget(vois_phone.CallScreen(name='call'))
sm.add_widget(vois_phone.TextScreen(name='text'))

# Add all email screens
sm.add_widget(vois_email.EmailScreen(name='email'))
sm.add_widget(vois_email.ComposeScreen(name='compose'))
sm.add_widget(vois_email.InboxScreen(name='inbox'))
sm.add_widget(vois_email.SentScreen(name='sent'))
sm.add_widget(vois_email.MessageScreen(name='message'))

# Add all document screens
sm.add_widget(vois_documents.documentHomeScreen(name='documentHome'))


#sm.add_widget(vois_documents.newDocsScreen(name='newDocs'))
#sm.add_widget(vois_documents.prevDocsScreen(name='prevDocs'))
sm.add_widget(vois_documents.documentResultsScreen(name='documentResults'))

# Add all web screens
sm.add_widget(vois_websearch.WebScreen(name='web'))
sm.add_widget(vois_websearch.ResultScreen(name='result'))

def execute(data):
    action_type = data['ActionType'].lower()
    context = data['Context']

    print('')
    print('Action:',action_type)
    print('Context', context)

    if action_type == 'navigate':
        destination_screen = context['DestinationScreen'].lower()

        if destination_screen == 'home':
            sm.current = 'home'

        elif destination_screen == 'phone':
            sm.current = 'phone'

        elif destination_screen == 'email':
            sm.current = 'email'

        elif destination_screen == 'doc':
            sm.current = 'documentHome'

        elif destination_screen == 'web':
            sm.current = 'web'

        else:
            print('Error: Invalid destination screen')

    elif action_type == 'phonecall':
        destination_number = context['DestinationNumber']
        current_screen = sm.current

        sm.current = 'call'
        screen = vois_phone.CallScreen()
        screen.call(destination_number)
        time.sleep(1)
        sm.current = current_screen

    elif action_type == 'phonetext':
        destination_number = context['DestinationNumber']
        message = context['Message']
        current_screen = sm.current

        sm.current = 'text'
        screen = vois_phone.TextScreen()
        screen.text(destination_number, message)
        time.sleep(1)
        sm.current = current_screen

    elif action_type == 'emailcompose':
        to = context['To']
        subject = context['Subject']
        message = context['Message']
        sm.current = 'compose'
        screen = vois_email.ComposeScreen()
        screen.compose_email(to, subject, message)

    elif action_type == 'emailreply':
        to = vois_email.reply_msg['to']
        subject = vois_email.reply_msg['subject']
        message = context['Message'] + vois_email.reply_msg['body']
        sm.current = 'compose'
        screen = vois_email.ComposeScreen()
        screen.compose_email(to, subject, message)
    
    elif action_type == 'emailforward':
        to = context['To']
        subject = vois_email.forward_msg['subject']
        message = context['Message'] + vois_email.forward_msg['body']
        sm.current = 'compose'
        screen = vois_email.ComposeScreen()
        screen.compose_email(to, subject, message)

    elif action_type == 'emailsend':
        screen = vois_email.ComposeScreen()
        screen.send_email()
        sm.current = 'email'

    elif action_type == 'emailinbox':
        sm.current = 'loading'
        time.sleep(0.5)
        sm.current = 'inbox'
        screen = vois_email.InboxScreen()
        screen.get_inbox_emails()

    elif action_type == 'emailsent':
        sm.current = 'loading'
        time.sleep(0.5)
        sm.current = 'sent'
        screen = vois_email.SentScreen()
        screen.get_sent_emails()
    
    elif action_type == 'emailopen':
        message_number = int(context['MessageNumber'])

        if sm.current == 'inbox':
            msg = vois_email.inbox_messages[message_number - 1]
            sm.current = 'message'
            screen = vois_email.MessageScreen()
            screen.open_message(msg, True)

        elif sm.current == 'sent':
            msg = vois_email.sent_messages[message_number - 1]
            sm.current = 'message'
            screen = vois_email.MessageScreen()
            screen.open_message(msg, False)


    elif action_type == 'documentcreate':

        #Extract file and folder name
        file_name = context['FileName'].lower()
        folder_name = context['FolderName'].lower()

        #Create new document
        vois_documents.newDoc(folder_name,file_name)


    elif action_type == 'documentsearch':

        #Extract folder name
        folder_name = context['FolderName'].lower()

        #Search Folder and load document results
        sm.get_screen('documentResults').byFolder(folder_name)
        sm.transition.direction = 'left'
        sm.current = 'documentResults'


    elif action_type == 'documentrecent':
        
        #Call top ten function
        sm.get_screen('documentResults').topTen()
        sm.transition.direction = 'left'
        sm.current = 'documentResults'


    elif action_type == 'documentopen':
        
        #Construct document id 
        doc_num = int(context['DocumentNumber'])
        doc_id = 'doc_' + str(doc_num - 1)

        #Get the file
        file = sm.get_screen('documentResults').ids[doc_id].text
        #Remove the number from the file name
        file = file.replace(str(doc_num) + '. ','') 
        #Open the document
        sm.get_screen('documentResults').openDoc(file)

        #Return to the home screen
        sm.current = 'home'
        sm.transition.direction = 'left'


        

    elif action_type == 'websearch':
        query = context['Query']

        if query == '':
            print('Error: Empty query')
            return
        
        sm.current = 'loading'
        time.sleep(0.5)
        sm.current = 'result'
        screen = vois_websearch.ResultScreen()
        screen.search(query)

    elif action_type == 'webopen':
        result_number = context['ResultNumber']

        screen = vois_websearch.ResultScreen()

        if int(result_number) > min(5, len(screen.results)):
            print('Error: Invalid result number')
            return

        screen.open_url(result_number)

    elif action_type == 'exit':
        App.get_running_app().stop()


def error_check(image):
    action_type = image['ActionType']['S'].lower()
    context = ast.literal_eval(image['Context']['S'])
    data = {
        'ActionType': '',
        'Context': {}
    }

    if action_type == 'navigate':
        destionation_screen = context['DestinationScreen']
        
        data['ActionType'] = 'Navigate'
        data['Context'] = {
            'DestinationScreen': destionation_screen
        }

    elif action_type == 'phonecall':
        destination_number = str(context['DestinationNumber'])

        data['ActionType'] = 'PhoneCall'
        data['Context'] = {
            'DestinationNumber': destination_number
        }

    elif action_type == 'phonetext':
        destination_number = str(context['DestinationNumber'])
        message = context['Message']

        data['ActionType'] = 'PhoneText'
        data['Context'] = {
            'DestinationNumber': destination_number,
            'Message': message
        }

    elif action_type == 'emailcompose':
        to = context['To']
        subject = context['Subject']
        message = context['Message']

        data['ActionType'] = 'EmailCompose'
        data['Context'] = {
            'To': to,
            'Subject': subject,
            'Message': message
        }

    elif action_type == 'emailinbox':
        data['ActionType'] = 'EmailInbox'

    elif action_type == 'emailsend':
        if sm.current != 'compose':
            print('Error: Invalid action type')
            return
        data['ActionType'] = 'EmailSend'

    elif action_type == 'emailsent':
        data['ActionType'] = 'EmailSent'

    elif action_type == 'emailreply':
        if sm.current != 'message':
            print('Error: Invalid action type')
            return

        message = context['Message']

        data['ActionType'] = 'EmailReply'
        data['Context'] = {
            'Message': message
        }

    elif action_type == 'emailforward':
        if sm.current != 'message':
            print('Error: Invalid action type')
            return

        to = context['To']
        message = context['Message']

        data['ActionType'] = 'EmailForward'
        data['Context'] = {
            'To': to,
            'Message': message
        }
        
    elif action_type == 'emailopen':
        if sm.current != 'inbox' and sm.current != 'sent':
            print('Error: Invalid action type')
            return

        message_number = context['EmailNumber']

        data['ActionType'] = 'EmailOpen'
        data['Context'] = {
            'MessageNumber': message_number
        }

    elif action_type == 'documentcreate':
        file_name = context['FileName']
        folder_name = context['FolderName']
        
        data['ActionType'] = 'DocumentCreate'
        data['Context'] = {
            'FileName': file_name,
		    'FolderName': folder_name
        }

    elif action_type == 'documentsearch':
        folder_name = context['FolderName']
        
        data['ActionType'] = 'DocumentSearch'
        data['Context'] = {
            'FolderName': folder_name
        }

    elif action_type == 'documentrecent':
        data['ActionType'] = 'DocumentRecent'

    elif action_type == 'documentopen':
        document_number = context['DocumentNumber']
        
        data['ActionType'] = 'DocumentOpen'
        data['Context'] = {
		    'DocumentNumber': document_number
        }

    elif action_type == 'websearch':
        query = context['Query']

        data['ActionType'] = 'WebSearch'
        data['Context'] = {
            'Query': query
        }

    elif action_type == 'webopen':
        if sm.current != 'result':
            print('Error: Invalid action type')
            return

        result_number = context['ResultNumber']

        data['ActionType'] = 'WebOpen'
        data['Context'] = {
            'ResultNumber': result_number
        }

    elif action_type == 'exit':
        data['ActionType'] = 'Exit'
    
    else:
        print('Error: Invalid action type')
        return

    execute(data)


#connect to stream by ARN, and then get shards from description
def listenToDB():
    client = boto3.client('dynamodbstreams')
    arn = 'arn:aws:dynamodb:us-east-1:166631308062:table/Commands/stream/2018-03-17T00:48:45.175'
    description = client.describe_stream(StreamArn=arn)
    shardsList = description['StreamDescription']['Shards']

    print("Number of shards in stream:", len(shardsList))

    for shard in shardsList:

        shardID = shard['ShardId']

        #skip shard if it's closed (it will not be receiving any new records)
        if 'EndingSequenceNumber' in shard['SequenceNumberRange']:
            print("Shard ID ending in ", shardID[-8:], "is closed")
            continue

        print("Shard open, processing shard ID:", shardID[-8:])

        #get an iterator result for the open shard
        #this iterator looks at records that appear only after this function has been called

        getShardIteratorResult = client.get_shard_iterator(
            StreamArn=arn,
            ShardId=shardID,
            ShardIteratorType='LATEST'
        )

        shardIterator = getShardIteratorResult['ShardIterator']

        print("\nListening for new records...")

        #begin iterating through shards from the parent 
        while shardIterator is not None:


            #get any new records that may appear
            getRecordsResult = client.get_records(ShardIterator=shardIterator)
            recordsList = getRecordsResult['Records']


            #usually recordsList is a single record, but sometimes multiple records may have been modified
            for record in recordsList:

                creationDateTime = record['dynamodb']['ApproximateCreationDateTime']
                tzinfo = creationDateTime.tzinfo
                diff = datetime.datetime.now(tzinfo) - creationDateTime

                #double checks that any new records are ACTUALLY new
                if diff < datetime.timedelta(minutes = 1):
                    # print("> New Event Record of type", record['eventName'], "<")

                    #Checks to see if the new event record is an insertion
                    if record['eventName'] != "INSERT":
                        print("Record is not a new insertion, skipping")
                        print("\nListening for new records...")
                        continue

                    #prints the attributes of the new record
                    image = record['dynamodb']['NewImage']
                    # for attr in image:
                    #     print("\t",attr, image[attr])

                    error_check(image)

                #this shouldn't happen
                else:
                    print("ERROR: Old Record")

                print("\nListening for new records...")

            #move on to the next shard iterator
            if 'NextShardIterator' in getRecordsResult:
                shardIterator = getRecordsResult['NextShardIterator']

                #print("Moving to shard iterator ending in", shardIterator[-8:])
            else: 
                #reached the end of a shard sequence, which means it has closed.
                shardIterator = None
                break

        print("Reached end of shardIterators for shardID ", shardID, ", stopped listening.")


class VOIS(App):

    def build(self):
        return sm


if __name__ == '__main__':
    t = Thread(target=listenToDB)
    t.daemon = True     # Stop thread at shutdown
    t.start()
    VOIS().run()
