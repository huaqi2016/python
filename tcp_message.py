#!/bin/env python
# -*- coding: UTF-8 -*-
import threading
import errno
import logging

import message_pb2 as pb_msg
#import internal_message_pb2 as ipb_msg

logging.basicConfig(level=logging.DEBUG)

MSG_HEADER_LEN = 4

def HeaderBuilder(msgType, msgLen):
    buff = bytearray(MSG_HEADER_LEN)
    buff[0] = msgLen/256
    buff[1] = msgLen%256
    buff[2] = msgType/256
    buff[3] = msgType%256
    return buff

def HeaderParser(headBuff):
    if len(headBuff) < MSG_HEADER_LEN:
        return None
    buff = bytearray(headBuff)
    msgType = buff[2]*256+buff[3]
    msgLen = buff[0]*256+buff[1]
    return [msgType, msgLen]

class Builder:
    def __init__(self):
        self.lock = threading.RLock()
        self.msgBuff = bytearray()

    def Build(self, msgType, msg):
        msgLen = len(msg)
        msgHead = HeaderBuilder(msgType, msgLen)
        self.lock.acquire()
        self.msgBuff += msgHead
        self.msgBuff += bytearray(msg)
        self.lock.release()

    def Empty(self):
        rv = False
        self.lock.acquire()
        if 0 == len(self.msgBuff):
            rv = True
        self.lock.release()
        return rv

    def Front(self, frontLen):
        buff = None
        self.lock.acquire()
        buff = self.msgBuff[:frontLen]
        self.lock.release()
        return buff

class Parser:
    def __init__(self):
        self.lock = threading.RLock()
        self.msgBuff = bytearray()
        self.msgs = []
        self.nextReadLen = MSG_HEADER_LEN

    def Parse(self, buff):
        self.msgBuff += buff
        self.header = HeaderParser(self.msgBuff)
        self.lock.acquire()
        while True:
            if not self.header:
                self.nextReadLen = MSG_HEADER_LEN-len(self.msgBuff)
                break
            if len(self.msgBuff) >= self.header[1] + MSG_HEADER_LEN:
                self.msgs += [(self.header[0], self.msgBuff[MSG_HEADER_LEN:MSG_HEADER_LEN+self.header[1]])]
                self.msgBuff = self.msgBuff[MSG_HEADER_LEN+self.header[1]:]
                self.header = HeaderParser(self.msgBuff)
            else:
                self.nextReadLen = self.header[1]+MSG_HEADER_LEN-len(self.msgBuff)
                break
        self.lock.release()

    def NextReadLen(self):
        nextReadLen = 0
        self.lock.acquire()
        nextReadLen = self.nextReadLen
        self.lock.release()
        return nextReadLen

    def MsgCount(self):
        msgCount = 0
        self.lock.acquire()
        msgCount = len(self.msgs)
        self.lock.release()
        return msgCount

    def Pop(self):
        msg = None
        self.lock.acquire()
        if len(self.msgs) > 0:
            msg = self.msgs[0]
            self.msgs = self.msgs[1:]
        self.lock.release()
        return msg
        
if __name__ == "__main__":
    msgType = 257
    msgLen = 257
    msgHead = HeaderBuilder(msgType, msgLen)
    if 1 != msgHead[0]:
        logging.error("msgLen first byte encode error, expect={0} actual={1}".format(1, msgHead[0]))
    if 1 != msgHead[1]:
        logging.error("msgLen second byte encode error, expect={0} actual={1}".format(1, msgHead[1]))
    if 1 != msgHead[2]:
        logging.error("msgType first byte encode error, expect={0} actual={1}".format(1, msgHead[2]))
    if 1 != msgHead[3]:
        logging.error("msgType second byte encode error, expect={0} actual={1}".format(1, msgHead[3]))
    if MSG_HEADER_LEN != len(msgHead):
        logging.error("encode msg header length error, expect={0} actual={1}".format(4, len(msgHead)))

    msgInfo = HeaderParser(msgHead)
    if msgType != msgInfo[0]:
        logging.error("Parser msg type error, expect={0} actual={1}".format(msgType, msgInfo[0]))
    if msgLen != msgInfo[1]:
        logging.error("Parser msg len error, expect={0} actual={1}".format(msgLen, msgInfo[1]))
    emptyHead = []
    msgInfoNone = HeaderParser(emptyHead)
    if None != msgInfoNone:
        logging.error("Parser msg error, expect=None actual={0}".format(msgInfoNone))

    # Test class Builder
    msgBuilder = Builder()
    msgType = 257
    msg = "yupeng test class builder"
    msgBuilder.Build(msgType, msg)
    if False != msgBuilder.Empty():
        logging.error("Msg builder build msg error, expect=False actual=True") 
    msgBuff = msgBuilder.Front(1000)
    if MSG_HEADER_LEN+len(msg) != len(msgBuff):
        logging.error("Msg builder front msg error, expect={0} actual={1}".format(MSG_HEADER_LEN+len(msg), len(msgBuff)))


    # Test class Parser
    msgParser = Parser()
    # Reuse the msgBuff
    if MSG_HEADER_LEN != msgParser.NextReadLen():
        logging.error("Empty msg parser return invalid read length, expect={0} actual={1}".format(MSG_HEADER_LEN, msgParser.NextReadLen()))
    msgParser.Parse(msgBuff[:2])
    if MSG_HEADER_LEN-2 != msgParser.NextReadLen():
        logging.error("Msg parser return invalid read length, expect={0} actual={1}".format(MSG_HEADER_LEN-2, msgParser.NextReadLen()))
    msgParser.Parse(msgBuff[2:])
    if 1 != msgParser.MsgCount():
        logging.error("Msg parser return wrong msg count, expect={0} actual={1}".format(1, msgParser.MsgCount()))
    parsedMsg = msgParser.Pop()
    if 0 != msgParser.MsgCount():
        logging.error("Msg parser return wrong msg count after pop, expect={0} actual={1}".format(0, msgParser.MsgCount()))
    if msgType != parsedMsg[0]:
        logging.error("Msg parser parsed wrong msgType, expect={0} actual={1}".format(msgType, parsedMsg[0]))
    if msg != parsedMsg[1]:
        logging.error("Msg parser parsed wrong msg, expect={0} actual={1}".format(msg, parsedMsg[1]))
    if MSG_HEADER_LEN != msgParser.NextReadLen():
        logging.error("Msg parser return invalid read length after pop, expect={0} actual={1}".format(MSG_HEADER_LEN, msgParser.NextReadLen()))
