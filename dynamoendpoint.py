import boto3
import datetime

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
                    print("> New Event Record of type", record['eventName'], "<")

                    #Checks to see if the new event record is an insertion
                    if record['eventName'] != "INSERT":
                        print("Record is not a new insertion, skipping")
                        print("\nListening for new records...")
                        continue

                    #prints the attributes of the new record
                    image = record['dynamodb']['NewImage']
                    for attr in image:
                        print("\t",attr, image[attr])

                    #parseRecord(record)

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




