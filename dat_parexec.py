import webbrowser
# me - this DAT
# par - the Par object that has changed
# val - the current value
# prev - the previous value
# 
# Make sure the corresponding toggle is enabled in the Parameter Execute DAT.

def onValueChange(par, prev):
	# use par.eval() to get current value
    # print(par.name + ' changed from ' + str(prev) + ' to ' + str(par.eval()))
    if par.name == 'Port' and parent.FloraInParent.par.Active.eval() == True:
        # print('Port changed, resetting server')
        parent.FloraInParent.Start()
	
    if par.name == 'Active':
        if par.eval() == True:
            # print('Starting server')
            parent.FloraInParent.Start()
            parent.FloraInParent.par.Port.enable = False
        else:
            # print('Stopping server')
            parent.FloraInParent.Stop()
            parent.FloraInParent.par.Port.enable = True

    return

# Called at end of frame with complete list of individual parameter changes.
# The changes are a list of named tuples, where each tuple is (Par, previous value)
def onValuesChanged(changes):
	for c in changes:
		# use par.eval() to get current value
		par = c.par
		prev = c.prev
	return

def onPulse(par):
    if (par.name == 'Site'):
        webbrowser.open('https://florafauna.ai/app')
    elif (par.name == 'Help'):
        webbrowser.open('https://discord.gg/Ccencznk5f')
    elif (par.name == 'Docs'):
        webbrowser.open('https://docs.florafauna.ai')
    return

def onExpressionChange(par, val, prev):
	return

def onExportChange(par, val, prev):
	return

def onEnableChange(par, val, prev):
	return

def onModeChange(par, val, prev):
	return
	