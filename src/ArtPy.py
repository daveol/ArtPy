PORT = 6454

ID = b'Art-Net\x00'
VER = 14 # 14

OPCODE_ARTPOLL      = bytes([0x00, 0x20])
OPCODE_ARTPOLLREPLY = bytes([0x00, 0x21])
OPCODE_ARTDMX       = bytes([0x00, 0x50])

TALK_VLC_DISABLE_BIT  = 0b00010000
TALK_DIAG_UNICAST_BIT = 0b00001000
TALK_DIAG_ENABLE_BIT  = 0b00000100
TALK_REPLY_CHANGE_BIT = 0b00000010

def decode(data):
    if data[:8] != ID:
        raise RuntimeError('Not a Art-Net packet')

    elif data[8:10] == OPCODE_ARTPOLL:
        return {
            'type': 'ArtPoll',
            'data': {
                'vlc': not bool(data[12] & TALK_VLC_DISABLE_BIT),
                'diag':{
                    'unicast': bool(data[12] & TALK_DIAG_UNICAST_BIT),
                    'enable': bool(data[12] & TALK_DIAG_ENABLE_BIT),
                    'priority': data[13]
                },
                'replychange': bool(data[12] & TALK_REPLY_CHANGE_BIT)
            }
        }

    elif data[8:10] == OPCODE_ARTPOLLREPLY:
        return {
            'type': 'ArtPollReply',
            'data':{
                'ip': (data[10], data[11], data[12], data[13]),
                'port': data[14],
                'version': data[15:17]
            }
        }

    elif data[8:10] == OPCODE_ARTDMX:
        return {
            'type': 'ArtDmx'
        }

    else:
        raise NotImplementedError("OpCode not recognized: {}".format(data[8:10].hex()))