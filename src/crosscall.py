import sys, base64, json

def receive_request(stream):
    '''
    从指定的流接收一个请求
    '''
    obj = json.loads(base64.b64decode(stream.readline()).decode())
    return obj.get('Command', None), obj.get('Payload', None)

def send_response(stream, status, payload):
    '''
    往指定的流发送一个响应
    '''
    stream.write(base64.b64encode(json.dumps({
        "Status": status, 
        "Payload": payload
    }).encode()).decode())
    stream.write("\n")
    stream.flush()

def send_request(stream, command, payload):
    '''
    往指定的流发送一个请求
    '''
    stream.write(base64.b64encode(json.dumps({
        "Command": command,
        "Payload": payload
    }).encode()).decode())
    stream.write("\n")
    stream.flush()

def receive_response(stream):
    '''
    从指定的流接收一个响应
    '''
    obj = json.loads(base64.b64decode(stream.readline()).decode())
    return obj.get('Status', None), obj.get('Payload', None)

def receive_request_loop(stream, handler):
    '''
    持续从指定的流接收请求
    '''
    try:
        while (True):
            command, payload = receive_request(stream)
            if not handler(command, payload):
                break
    except KeyboardInterrupt:
        pass

def receive_response_loop(stream, handler):
    '''
    持续从指定的流接收响应
    '''
    try:
        while (True):
            command, payload = receive_request(stream)
            if not handler(command, payload):
                break
    except KeyboardInterrupt:
        pass
