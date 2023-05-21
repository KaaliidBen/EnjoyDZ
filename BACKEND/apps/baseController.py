from starlette.responses import JSONResponse

#Response sent in case of a successful request
def sendResponse(data, message):
    return JSONResponse({
        'result' : True,
        'message' : message,
        'data' : data
    })

#Response sent in cas eof an error
def sendErrorMessage(ErrorMessage):
    return JSONResponse({
        'result' : False,
        'message' : ErrorMessage
    })