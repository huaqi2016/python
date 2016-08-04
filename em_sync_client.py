#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import socket
import weakref
import errno
import logging

import message_pb2 as pb_msg
#import internal_message_pb2 as ipb_msg
import tcp_message as tcp_msg

logging.basicConfig(level=logging.DEBUG)

dcs = socket.socket()
dcs.connect(("yupeng.info", 9898))

s = pb_msg.SessionStart()
s.v = 1
s.uuid = "00001234567890123456789012345678901234567890"
s.sid = "00001234567890123456789012345678901234567890"
logging.info(s)

msg = s.SerializeToString()
msgBuilder = tcp_msg.Builder()
msgBuilder.Build(pb_msg.MsgType.SESSION_START, msg)
sendLen = dcs.send(msgBuilder.Front(1000))
logging.info("msgLen={0} sendLen={1}".format(len(msg), sendLen))

msgParser = tcp_msg.Parser()
msgParser.Parse(dcs.recv(msgParser.NextReadLen()))
msgParser.Parse(dcs.recv(msgParser.NextReadLen()))
msgType_, msg_ = msgParser.Pop()
logging.info("msgType={0} msg={1}".format(msgType_, msg_))
dcs.close()

