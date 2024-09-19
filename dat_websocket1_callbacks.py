import time

# Initialize counter and start time
message_count = 0
start_time = time.time()
messages_per_second = 0

# me - this DAT
# dat - the WebSocket DAT

def onConnect(dat):
    print("Connected to websocket server")
    return

# me - this DAT
# dat - the WebSocket DAT

def onDisconnect(dat):
    return

# me - this DAT
# dat - the DAT that received a message
# rowIndex - the row number the message was placed into
# message - a unicode representation of the text
# 
# Only text frame messages will be handled in this function.

def onReceiveText(dat, rowIndex, message):
    global message_count, start_time, messages_per_second
    
    # Increment the message count
    message_count += 1
    
    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    
    # Calculate messages per second
    if elapsed_time > 0:
        messages_per_second = message_count / elapsed_time
    
    # Store the message in 'img_data'
    op('img_data').text = message
    
    return

# me - this DAT
# dat - the DAT that received a message
# contents - a byte array of the message contents
# 
# Only binary frame messages will be handled in this function.

def onReceiveBinary(dat, contents):
    print(f"Received binary message")
    return

# me - this DAT
# dat - the DAT that received a message
# contents - a byte array of the message contents
# 
# Only ping messages will be handled in this function.

def onReceivePing(dat, contents):
    dat.sendPong(contents) # send a reply with same message
    return

# me - this DAT
# dat - the DAT that received a message
# contents - a byte array of the message content
# 
# Only pong messages will be handled in this function.

def onReceivePong(dat, contents):
    return

# me - this DAT
# dat - the DAT that received a message
# message - a unicode representation of the message
#
# Use this method to monitor the websocket status messages

def onMonitorMessage(dat, message):
    return