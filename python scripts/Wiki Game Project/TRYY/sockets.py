import sys
import os
import shutil
import socket
import thread
import traceback
import StringIO
import subprocess
import glob

# simple client-server socket example
# This is a full solution for exercise 2.7 from the Gvahim networks book.

# PIL is an image processing library. get it using (in cmd.exe):
# > pip install Pillow https://pillow.readthedocs.org/en/latest/
try:
    from PIL import ImageGrab, Image
except ImportError:
    print "Could not find PIL package. screen shot command will not work"

# pyperclip is a library for inteating with the windows clipboard. get it using:
# pip install pyperclip
try:
    import pyperclip
except ImportError:
    print "Cound not find pyperclip module. clipboard commands will not work"
     
   
# define the basic protocol we run on the socket
# the client starts the session by send a 4 characters command followed by a new line
# after that the client sends a chunk and the server responds with a chunk.
# a chunk starts with a 10 digit decimal number followed by a new line.
# this number gives the size in bytes of the data that follows
class Protocol:
    def __init__(self, sock):
        # wrap a socket object
        self.sock = sock
        
    COMMAND_LEN = 4
    DATA_SIZE_LEN = 10
        
    def sendCmd(self, cmd): # client side
        assert len(cmd) == Protocol.COMMAND_LEN
        self.sock.send(cmd + "\n") # total length of the packet = 5 bytes.
        
    def recvCmd(self): # server side
        cmd = self.sock.recv(Protocol.COMMAND_LEN + 1) # +1 for the \n
        assert len(cmd) > 0, "Received empty command, other side hung up"
        assert cmd[-1] == '\n', "Unexpected command format"
        return cmd[0:Protocol.COMMAND_LEN]

    def sendChunk(self, data):
        dataSize = len(data)
        # 10 digits with zero-padding followed by \n
        self.sock.send( '{0:{fill}{length}}\n'.format(dataSize, fill='0', length=Protocol.DATA_SIZE_LEN) ) 
        if len(data) > 0:
            self.sock.send(data)
        
    def recvChunk(self):
        # read 10 chars with the size + \n
        expectSizeStr = self.sock.recv(Protocol.DATA_SIZE_LEN + 1)
        assert len(expectSizeStr) > 0, "Received empty size, other side hung up"
        assert expectSizeStr[-1] == '\n', "Unexpected size format"  # validate input
        expectSize = int(expectSizeStr)
        if expectSize == 0:
            return str()  # empty chunk, no data will follow
        # read packets from the socket and accumulate them to a single buffer
        receivedData = '' 
        sizeRemaining = expectSize
        while True:
            packet = self.sock.recv(sizeRemaining)
            if len(packet) == 0:
                break # unexpected end of data
            receivedData += packet # append to buffer
            sizeRemaining -= len(packet)
            if sizeRemaining == 0:
                break # reached the end of the expected data
        assert len(receivedData) == expectSize, "Received partial data, other side hung up %d != %d" % (len(receivedData), expectSize)
        return receivedData
        
    def sendRecvChunk(self, outData):
        # helper function for the above
        self.sendChunk(outData)
        inData = self.recvChunk()
        return inData
        
                    
#---------------------------------------------------------------------------------------
    
CLIENT_TIMEOUT_SEC = 5    
        
def clientMain(args):
    if len(args) < 3:
        print "Usage: sockets.py client <address> <port> <CMD> [cmd-args]"
        print "Example:\n   python sockets.py client 127.0.0.1` 666 ECHO Hello"
        return
    
    address = args[0] # string with IP address to connect to
    port = int(args[1])
    cmd = args[2]
    # command specific arguments from command line, if they exist
    cmdArgs = args[3:] if len(args) > 3 else []
    
    assert len(cmd) == Protocol.COMMAND_LEN, "Command must be %d characters. got `%s`" % (Protocol.COMMAND_LEN, cmd)
    sender = ClientSender()
    # in this sender object, find a method which corresponds to the name of the received command
    func = getattr(sender, "send_" + cmd, None)
    assert func is not None, "Unknown command `%s`" % cmd
    # func is a method object which will be called later

    # create a socket object, AP_INET - this is an IPv4 connection, SOCK_STREAM - this is a TCP connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # configure the socket so that if the server doesn't respond, don't hang indefinitely.
    sock.settimeout(CLIENT_TIMEOUT_SEC)
    # start the connection
    sock.connect( (address, port) ) # a tuple with the address string and port number 
    
    p = Protocol(sock)
    p.sendCmd(cmd)
    func(cmdArgs, p) # call the sender
    
    sock.close()        

# this class defines what commands the client can send
# a method starting with 'send_' represents a command
# it gets the arguments from the command line and the Protocol object that wraps the socket
# the method needs to
# - validate its input, 
# - send a chunk to the server and receive a reply chunk
# - display the reply to the user    
class ClientSender:
    def send_ECHO(self, args, protoc): 
        # just send a string to the server. example:
        # python sockets.py client 127.0.0.1 666 ECHO "Hello World!"
        assert len(args) == 1, "Missing required argument - the string to echo"
        reply = protoc.sendRecvChunk(args[0])
        print "`" + reply + "`"
    
    def send_GRAB(self, args, protoc): 
        # screenshot
        assert len(args) == 0, "No arguments needed"
        reply = protoc.sendRecvChunk('-')
        print "Got Image", len(reply), "bytes"
        im = Image.open(StringIO.StringIO(reply))
        im.show()
        
    def send_RUNX(self, args, protoc):
        # run an external process. example:
        # Example: python sockets.py client 127.0.0.1 666 RUNX cmd.exe /c dir
        assert len(args) > 0, "Missing required arguments - the command line to run"
        # may have more than one arguments, concatenate them with a space delimiter
        cmdLine = ' '.join(args)
        print "Sending command `%s`" % cmdLine
        reply = protoc.sendRecvChunk(cmdLine)
        print "Command output:", len(reply), "bytes"
        print reply
              
    def send_DIRL(self, args, protoc):
        assert len(args) == 1, "Missing required argument - remote directory to list"
        print "Sending directory listing", args[0]
        reply = protoc.sendRecvChunk(args[0])
        print reply
        
    def send_DELF(self, args, protoc):
        assert len(args) == 1, "Missing required argument - remote file to delete"
        print "Sending delete file", args[0]
        reply = protoc.sendRecvChunk(args[0])
        print reply
        
    def send_CPYF(self, args, protoc):
        assert len(args) == 2, "Missing required argument - source path, dest path"
        print "Sending copy file from", args[0], "to", args[1]
        reply = protoc.sendRecvChunk(args[0] + "\n" + args[1])
        print reply
        
    def send_CLCP(self, args, protoc):
        assert len(args) == 1, "Missing required argument - test to copy to clipboard"
        print "Sending clipboard copy of `%s`" % args[0]
        reply = protoc.sendRecvChunk(args[0])
        print reply
    
    def send_CLPS(self, args, protoc):
        assert len(args) == 0, "No arguments needed"
        reply = protoc.sendRecvChunk("-")
        print "Got paste data:"
        print reply
        
    def send_STOP(self, args, protoc):
        # cause the server to stop
        assert len(args) == 0, "No arguments needed"
        reply = protoc.sendRecvChunk("-")
        print reply
        
    def send_EXEC(self, args, protoc):
        # cause the server to run a given python script file
        assert len(args) == 1, "Missing required argument - python file to send"
        text = open(args[0]).read()
        reply = protoc.sendRecvChunk(text)
        print reply

    
#---------------------------------------------------------------------------------------

SERVER_TIMEOUT = 1
SERVER_BACKLOG_CONNECTIONS = 10

def serverMain(args):
    if len(args) < 1:
        print "Usage: sockets.py server PORT_NUMBER"
        print "Example:\n  python sockets.py server 666"
        return
    port = int(args[0])
    
    # create a socket object, AF_INET means IPv4, SOCK_STREAM means TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # configure the socket to be listening on all of the machines network interfaces
        # and the given port number. This still doesn't open the port for connections.
        # this function can fail if the port is already bound in another application
        # or if the user does not have privileges to open this port.
        sock.bind( ('0.0.0.0', port) )
    except socket.error as msg:
        print 'bind() failed' + str(msg) 
        return
        
    print "listening on port" , port
    # open the server port for incoming connections.
    # 10 is the number of pending incoming connection that are allowed to queue without being accepted
    sock.listen(SERVER_BACKLOG_CONNECTIONS)
    # setting the timeout for the following accept() call
    sock.settimeout(SERVER_TIMEOUT)
    
    # a single handler object handles all the connections
    handler = ServerHandler()
    try:
        while not handler.stop:
            # wait for an incoming connection and accept it when it comes
            # returns the a newly created socket object that will be used for the two-way communication
            # and the address of the client that made the connection
            try:
                sockNew, addr = sock.accept()
            except socket.timeout:
                # if a a connection is not received after 1 second (timeout) accept will throw an
                # exception and we will call accept() again. This is useful to not be blocking
                # inside accept indefinitely so that we would be able to receive KeyboardInterrupt (Ctrl+C)
                # if the user wants to exit the server
                continue;
                
            print "Got connection from", addr
            # further handling of this connection will be performed from a new thread started for this purpose
            # The current thread will loop again and wait for in accept() for the next connection
            thread.start_new_thread(servingThread, (sockNew, handler))
    except KeyboardInterrupt:    
        print "Got KeyboardInterrupt"
        pass 
    
    print "shutting down"
    sock.close()

    
def servingThread(sock, handler):
    # configure the socket so it won't hang if the client stop responding
    sock.settimeout(SERVER_TIMEOUT)
    try:
        protoc = Protocol(sock) # Protocol object wraps a socket object
        cmd = protoc.recvCmd()
        print 'got command', cmd
        # find the method in the handle for handling this command
        func = getattr(handler, "do_" + cmd, None)
        assert func is not None, "Unknown command `%s`" % cmd
        
        # first chunk after receiving the command is data from the client about the command
        inStr = protoc.recvChunk()
        # running the command handler to produce the command output
        try:
            outStr = func(inStr)
        except Exception as e:
            outStr = "Faild running " + cmd + " : " + str(e)
        # send the command output as a reply chunk to the client
        protoc.sendChunk(outStr)
  
    except socket.error as e:
        # timeout exception or a connection error
        print "Socket error in servingThread", str(e)
        traceback.print_exc()
    except Exception as e:
        # failed finding the command or any other error
        print "Error in servingThread", str(e)
        traceback.print_exc()
    
    # the socket object that was created in accept() is closed and the connection with this client ends
    # but the main socket of the server is still listening for the next client
    sock.close()
    

# this class defines the command the server is able to respond to.    
# the method "do_XXXX" will be called to handle the command XXXX. 
# each command method needs to:
# - parse the input string sent by the client (when relevant) 
# - process the command
# - return a reply string which will be sent to the client.
class ServerHandler:
    def __init__(self):
        self.stop = False # marks to the main server thread the server should be stopped
    
    def do_ECHO(self, inStr):
        # reverse the given string and send it as a reply
        return inStr[::-1]
    
    def do_GRAB(self, inStr):
        print "Capturing screen"
        img = ImageGrab.grab()
        sio = StringIO.StringIO() # buffer for image data
        img.save(sio, 'PNG')
        buf = sio.getvalue() 
        print "Sending", len(buf), "bytes"
        return buf
        
    def do_RUNX(self, inStr):
        print "Running process", inStr
        # create a new process with input and output redirected to python
        process = subprocess.Popen(inStr, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdoutdata, stderrdata = process.communicate() # send empty input and wait for output
        return stdoutdata
        
    def do_DIRL(self, inStr):
        print "Listing directory", inStr
        if not os.path.exists(inStr):
            return "[Not a directory]"
        # find all files in the requested directory
        filesList = glob.glob(os.path.join(inStr, '*'))
        if len(filesList) == 0:
            return "[No files found]"
        return '\n'.join(filesList)
        
    def do_DELF(self, inStr):
        print "Deleting file", inStr
        os.unlink(inStr)
        return "OK"
    
    def do_CPYF(self, inStr):
        names = inStr.splitlines()
        assert len(names) == 2, "Wrong syntax, got " + str(names)
        print "Copying", names[0], "to", names[1]
        shutil.copy(names[0], names[1])
        return "OK"
            
    def do_CLCP(self, inStr):
        print "Clipboard copy `%s`" % inStr
        pyperclip.copy(inStr)
        return "OK"
    
    def do_CLPS(self, inStr):
        print "Clipboard paste request"
        data = pyperclip.paste()
        # if the data in the clipboard is not text, this will return None
        if data is not None:
            return data
        return "[No text in clipboard]"
        
    def do_EXEC(self, inStr):
        print "Executing python"
        runGlobals = {} 
        exec(inStr, runGlobals)
        return str(runGlobals.get('retVal', '[None]'))

    def do_STOP(self, inStr):
        print "Stopping server"
        self.stop = True
        return "OK"


#---------------------------------------------------------------------------------------    
    
# start of execution from command line    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: python sockets.py <client|server>";
        sys.exit(1)
        
    if  sys.argv[1] == "server":
        serverMain(sys.argv[2:])
    elif sys.argv[1] == "client":
        clientMain(sys.argv[2:])          
