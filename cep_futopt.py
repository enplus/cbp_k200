from cep_adaptor import *

import pythoncom

# @CpRqRp('CpSysDib.EurexJpbid')

import CpUtil
g_STKCODE = CpUtil.CpStockCode()


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
                    time.sleep(0.5)
                    # MessagePump(10000)

            else:
                com_obj.SetInputValue(0, self.itm_cod)
                com_obj.Request()
                # com_obj.BlockRequest()

    def response(self, com_obj):
        # pythoncom.PumpWaitingMessages()
        itm_cod = com_obj.GetHeaderValue(0)
        undr = com_obj.GetHeaderValue(112)
        undr_name = g_STKCODE.code2name(undr)

        out = undr + ',' + undr_name

        if undr[:1] == 'A':
            self.eproc.push(key='#%s' % itm_cod, data=out)
        elif undr == 'U180':
            self.eproc.push(key='K200_%s' % itm_cod, data=out)
        else:
            self.eproc.push(key='FUTURE_%s' % itm_cod, data=out)


# 호가구조 (가격,잔량,건수) * 1~5
@CpSbPb('CpSysDib.FutureJpBid')
class FutureJpbid:
    def __init__(self):
        self.itm_cod = None
        self.eproc = None

    def setInitData(self, itm_cod=None, evntProc=None):
        self.itm_cod = itm_cod
        self.eproc = evntProc
        print('# FutBid Init: %s' % self.itm_cod)

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
        itm_cod = com_obj.GetHeaderValue(0)
        time = com_obj.GetHeaderValue(1)

        bidpr = [
            com_obj.GetHeaderValue(2),
            com_obj.GetHeaderValue(3),
            com_obj.GetHeaderValue(4),
            com_obj.GetHeaderValue(5),
            com_obj.GetHeaderValue(6),
            ]

        bidqty = [
            com_obj.GetHeaderValue(7),
            com_obj.GetHeaderValue(8),
            com_obj.GetHeaderValue(9),
            com_obj.GetHeaderValue(10),
            com_obj.GetHeaderValue(11),
            ]

        bidcnt = [
            com_obj.GetHeaderValue(13),
            com_obj.GetHeaderValue(14),
            com_obj.GetHeaderValue(15),
            com_obj.GetHeaderValue(16),
            com_obj.GetHeaderValue(17),
            ]

        askpr = [
            com_obj.GetHeaderValue(19),
            com_obj.GetHeaderValue(20),
            com_obj.GetHeaderValue(21),
            com_obj.GetHeaderValue(22),
            com_obj.GetHeaderValue(23),
            ]

        askqty = [
            com_obj.GetHeaderValue(24),
            com_obj.GetHeaderValue(25),
            com_obj.GetHeaderValue(26),
            com_obj.GetHeaderValue(27),
            com_obj.GetHeaderValue(28),
            ]

        askcnt = [
            com_obj.GetHeaderValue(30),
            com_obj.GetHeaderValue(31),
            com_obj.GetHeaderValue(32),
            com_obj.GetHeaderValue(33),
            com_obj.GetHeaderValue(34),
            ]

        bids, asks = [], []
        for p, q, c in zip(bidpr, bidqty, bidcnt):
            bids.append((int(p*100), q, c, 0))

        for p, q, c in zip(askpr, askqty, askcnt):
            asks.append((int(p*100), q, c, 0))

        data = {'time': time, 'bids': bids, 'asks': asks}
        print('%s) %s %s' % (time, itm_cod, data))

        # # 이벤트 처리기에 전달

        # # # 이벤트 처리기에 전달
        if self.eproc is not None:
            self.eproc.push(key='stkbid_%s' % itm_cod, data=data)


@CpSbPb('CpSysDib.OptionJpBid')
class OptionJpbid:
    def __init__(self):
        self.itm_cod = None
        self.eproc = None

    def setInitData(self, itm_cod=None, evntProc=None):
        self.itm_cod = itm_cod
        self.eproc = evntProc
        print('# OptBid Init: %s' % self.itm_cod)

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
        # itm_cod = com_obj.GetHeaderValue(0)
        # bid1 = com_obj.GetHeaderValue(2)

        # for i in range(3, 23, 4):
        #     itm = (
        #         com_obj.GetHeaderValue(i+0),
        #         com_obj.GetHeaderValue(i+1),
        #         com_obj.GetHeaderValue(i+2),
        #         com_obj.GetHeaderValue(i+3)
        #     )
        #     tlist.append(itm)

        # 이벤트 처리기에 전달
        if self.eproc is not None:
            self.eproc.push('stkbid_%s' % itm_cod, tlist)

@CpSbPb('dscbo1.FutureCurr')
class FutureCur:
    def __init__(self):
        self.itm_cod = None
        self.eproc = None

    def setInitData(self, itm_cod=None, evntProc=None):
        self.itm_cod = itm_cod
        self.eproc = evntProc
        print('# XXXX Init: %s' % self.itm_cod)

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
        # itm_cod = com_obj.GetHeaderValue(0)
        # bid1 = com_obj.GetHeaderValue(2)

        # for i in range(3, 23, 4):
        #     itm = (
        #         com_obj.GetHeaderValue(i+0),
        #         com_obj.GetHeaderValue(i+1),
        #         com_obj.GetHeaderValue(i+2),
        #         com_obj.GetHeaderValue(i+3)
        #     )
        #     tlist.append(itm)

        # 이벤트 처리기에 전달
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
