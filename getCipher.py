import time, random, json
import timeStampGenerator as tsg
import matrixOperation as mop
import fileManager as fm

jsonData = fm.getFile('generalConstants.json', 'r')
jsonParse = json.loads(jsonData)

def checkLength(num):
	state = False
	if(len(num)<=jsonParse['checkLength']):
		while(len(num)<jsonParse['checkLength']):
			num = '0' + num
		state = True
	else:
		state = False
	return (num, state)

def embedCipher(cipherVector, messageByteVector):
	cipherMessageVector = []
	messageLen, index = len(messageByteVector), 0
	for element in cipherVector:
		if(index >= messageLen):
			numAssetStr = element
		else:
			numAssetStr = str(int(element) + messageByteVector[index])
		numAssetStr, status = checkLength(numAssetStr)
		if(status):
			cipherMessageVector.append(numAssetStr)
		index += 1
	return cipherMessageVector

def makeCipherVector(messageByteVector, timeStampVector):
	cipherVector, cipherMessageVector = [], []
	while(len(cipherVector) != jsonParse['lengthMessage']):
		num = random.randint(jsonParse['startConstant'], jsonParse['infinityConstant'])
		numStr, stateNumStr = checkLength(str(num))
		if(stateNumStr):
			cipherVector.append(numStr)
	cipherMessageVector += embedCipher(cipherVector, messageByteVector)
	cipherMessageVector += embedCipher(cipherVector, timeStampVector)
	return cipherVector + cipherMessageVector

def getCipherMessage(joinedCipher):
	index, length = 0, jsonParse['selectLength']
	cipherList = []
	while(len(joinedCipher) != 0):
		numSubstring = int(joinedCipher[index : index + length])
		status1 = (numSubstring >=jsonParse['Const1'] and numSubstring<=jsonParse['Const2']) 
		status2 = (numSubstring>=jsonParse['Const3'] and numSubstring<=jsonParse['Const4'])
		if(status1 or status2):
			cipherList.append(chr(numSubstring))
			joinedCipher = joinedCipher[index + length : len(joinedCipher)]
		else:
			cipherList.append(joinedCipher[index])
			joinedCipher = joinedCipher[index + 1 : len(joinedCipher)]
	return "".join(cipherList)

def getCipher():
	messageByteVector = fm.getFile('messageCopy.txt', 'rb')
	timeStampVector = [ord(element) for element in tsg.getTimeStamp()]
	print('Message laid!')
	finalCipherVector = makeCipherVector(messageByteVector, timeStampVector)
	cipherMatrix = mop.matrixTransposer(mop.squareMatrixMakerOnList(finalCipherVector)) 
	finalCipher = getCipherMessage("".join(mop.matrixToVector(cipherMatrix)))
	print('Cipher created!')
	return finalCipher