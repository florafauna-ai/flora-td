import time

table = op('info_table')
img_data = op('img_data')

# Initialize counter and start time
message_count = 0
fps = 0
total_time = 0
start_time = time.time()
time_intervals = []

def onConnect(dat):
    global start_time, total_time, message_count, fps
    start_time = time.time()
    total_time = 0
    message_count = 0
    fps = 0
    
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
    global message_count, start_time, table, img_data, fps, total_time, time_intervals
    
    # Increment the message count
    message_count += 1
    img_data.text = message
    
    # Calculate the time since the last call
    current_time = time.time()
    elapsed_time = current_time - start_time
    total_time += elapsed_time
    start_time = current_time
    
    # Store the time interval
    time_intervals.append(elapsed_time)
    
    # Maintain a list of the last N intervals (for a moving average)
    N = 200  # Adjust N to control the smoothing window
    if len(time_intervals) > N:
        time_intervals.pop(0)
    
    # Calculate FPS as the inverse of the average time interval
    if len(time_intervals) > 0:
        average_time = sum(time_intervals) / len(time_intervals)
        fps = 1.0 / average_time if average_time > 0 else 0
    
    # Update table with FPS and other stats
    table.replaceRow('fps', ['fps', int(fps)])
    table.replaceRow('frames', ['frames', message_count])
    table.replaceRow('total_time', ['total_time', round(total_time, 2)])
    
    return

# me - this DAT
# dat - the DAT that received a message
# contents - a byte array of the message contents
# 
# Only binary frame messages will be handled in this function.

def onReceiveBinary(dat, contents):
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