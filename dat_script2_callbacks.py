# me - this DAT
# scriptOp - the OP which is cooking

import numpy as np
import cv2
import ast
import base64

def readb64(encoded_data):
    # Remove the prefix if it exists
    if encoded_data.startswith('data:image/jpeg;base64,'):
        encoded_data = encoded_data.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # Convert BGR to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Flip the image along both axes
    img = cv2.flip(img, 0)
    return img

# press 'Setup Parameters' in the OP to call this function to re-create the parameters.
def onSetupParameters(scriptOp):
	data = op('img_data').text
	img = readb64(data)
	
	try:
		scriptOp.copyNumpyArray(img)
	except:
		debug("Error occured processing image. most likely invalid prompt")

	
	#if parent().par.Autosaveimages:
		#op('moviefileout1').par.addframe.pulse()
	return

# called whenever custom pulse parameter is pushed
def onPulse(par):
	return


def onCook(scriptOp):
	#a = numpy.random.randint(0, high=255, size=(2, 2, 4), dtype='uint8')
	#scriptOp.copyNumpyArray(a)
	return
