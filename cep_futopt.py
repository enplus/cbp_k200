from cep_adaptor import *

import pythoncom

# @CpRqRp('CpSysDib.EurexJpbid')

@CpSbPb('CpSysDib.EurexJpbid')
class EurexJpbid:
    def __init__(self):
        self.itm_cod = None
        self.eproc = None

    def setInitData(self, itm_cod=None, evntProc=None):
        self.itm_cod = itm_cod
        self.eproc = evntProc
        print('# STKBID Init: %s' % self.itm_cod)

    def subscribe(self, com_obj):
        com_obj.Unsubscribe()

        if self.itm_cod is None:
            print('itmCode is None')
        else:
            if type(self.itm_cod) == list:
                for x in self.itm_cod:
                    com_obj.SetInputValue(0, x)
                    com_obj.Subscribe()
            else:
                com_obj.SetInputValue(0, self.itm_cod)
                com_obj.Subscribe()

    def publish(self, com_obj):
        tlist = []
        itm_cod = com_obj.GetHeaderValue(0)
        bid1 = com_obj.GetHeaderValue(2)

        print(itm_cod, bid1)

        # for i in range(3, 23, 4):
        #     itm = (
        #         com_obj.GetHeaderValue(i+0),
        #         com_obj.GetHeaderValue(i+1),
        #         com_obj.GetHeaderValue(i+2),
        #         com_obj.GetHeaderValue(i+3)
        #     )
        #     tlist.append(itm)

        # # 이벤트 처리기에 전달
        # if self.eproc is not None:
        #     self.eproc.push('stkbid_%s' % itm_cod, tlist)


@CpRqRp('dscbo1.FutureMst')
class FutOptMst:
    def __init__(self):
        self.itm_cod = None
        self.eproc = None

    def setInitData(self, itm_cod=None, evntProc=None):
        self.itm_cod = itm_cod
        self.eproc = evntProc
        print('# foMst Init: %s' % self.itm_cod)

    def request(self, com_obj):
        if self.itm_cod is None:
            print('itmCode is None')
        else:
            if type(self.itm_cod) == list:
                for x in self.itm_cod:
                    com_obj.SetInputValue(0, x)
                    # com_obj.BlockRequest()
                    com_obj.BlockRequest()
                    # MessagePump(10000)

            else:
                com_obj.SetInputValue(0, self.itm_cod)
                com_obj.Request()
                # com_obj.BlockRequest()

    def response(self, com_obj):
        # pythoncom.PumpWaitingMessages()
        itm_cod = com_obj.GetHeaderValue(0)
        out = com_obj.GetHeaderValue(2)
        undr = com_obj.GetHeaderValue(112)

        if undr[:1] == 'A':
            self.eproc.push(key = 'SFUT_%s' % itm_cod, data=out)
        elif undr == 'U180':
            self.eproc.push(key = 'K200_%s' % itm_cod, data=out)
        else:
            self.eproc.push(key = 'FUTURE_%s' % itm_cod, data=out)


@CpSbPb('CpSysDib.EurexJpbid')
class FutOptJpbid:
    def __init__(self):
        self.itm_cod = None
        self.eproc = None

    def setInitData(self, itm_cod=None, evntProc=None):
        self.itm_cod = itm_cod
        self.eproc = evntProc
        print('# STKBID Init: %s' % self.itm_cod)

    def subscribe(self, com_obj):
        com_obj.Unsubscribe()

        if self.itm_cod is None:
            print('itmCode is None')
        else:
            if type(self.itm_cod) == list:
                for x in self.itm_cod:
                    com_obj.SetInputValue(0, x)
                    com_obj.Subscribe()
            else:
                com_obj.SetInputValue(0, self.itm_cod)
                com_obj.Subscribe()

    def publish(self, com_obj):
        tlist = []
        itm_cod = com_obj.GetHeaderValue(0)
        bid1 = com_obj.GetHeaderValue(2)

        print(itm_cod, bid1)

        # for i in range(3, 23, 4):
        #     itm = (
        #         com_obj.GetHeaderValue(i+0),
        #         com_obj.GetHeaderValue(i+1),
        #         com_obj.GetHeaderValue(i+2),
        #         com_obj.GetHeaderValue(i+3)
        #     )
        #     tlist.append(itm)

        # # 이벤트 처리기에 전달
        if self.eproc is not None:
            self.eproc.push('stkbid_%s' % itm_cod, tlist)

# @CpSbPb('')
# class XXXX:
#     def __init__(self):
#         self.itm_cod = None
#         self.eproc = None
#
#     def setInitData(self, itm_cod=None, evntProc=None):
#         self.itm_cod = itm_cod
#         self.eproc = evntProc
#         print('# XXXX Init: %s' % self.itm_cod)
#
#     def subscribe(self, com_obj):
#         com_obj.Unsubscribe()
#
#         if self.itm_cod is None:
#             print('itmCode is None')
#         else:
#             if type(self.itm_cod) == list:
#                 for x in self.itm_cod:
#                     com_obj.SetInputValue(0, x)
#                     com_obj.Subscribe()
#             else:
#                 com_obj.SetInputValue(0, self.itm_cod)
#                 com_obj.Subscribe()
#
#     def publish(self, com_obj):
#         tlist = []
#         # itm_cod = com_obj.GetHeaderValue(0)
#         # bid1 = com_obj.GetHeaderValue(2)
#
#         # for i in range(3, 23, 4):
#         #     itm = (
#         #         com_obj.GetHeaderValue(i+0),
#         #         com_obj.GetHeaderValue(i+1),
#         #         com_obj.GetHeaderValue(i+2),
#         #         com_obj.GetHeaderValue(i+3)
#         #     )
#         #     tlist.append(itm)
#
#         # 이벤트 처리기에 전달
#         if self.eproc is not None:
#             self.eproc.push('stkbid_%s' % itm_cod, tlist)
