from cep_adaptor import CpSbPb
from cep_adaptor import CpRqRp

###################################################
# Adaptors : 발생한 이벤트를 처리기에 전달하는 역할
#
###################################################
# 주식 호가잔량
@CpSbPb('dscbo1.StockJpBid')
class StkBid:
    def __init__(self):
        self.itm_cod = None
        self.eproc = None

    def setInitData(self, itm_cod=None, evntProc=None):
        self.itm_cod = itm_cod
        self.eproc = evntProc
        print('# STKBID Init: %s' % self.itm_cod)

    def subscribe(self, com_obj):
        if self.itm_cod is None:
            print('itmCode is None')
        else:
            com_obj.Unsubscribe()
            # print('ComObj: %s' % com_obj)
            # print('# STKBID Subc: %s' % self.itm_cod)

            for x in self.itm_cod:
                com_obj.SetInputValue(0, x)
                com_obj.Subscribe()

    def publish(self, com_obj):
        itm_cod = com_obj.GetHeaderValue(0)
        time = com_obj.GetHeaderValue(1) * 100

        bidpr = [
            com_obj.GetHeaderValue(4),
            com_obj.GetHeaderValue(8),
            com_obj.GetHeaderValue(12),
            com_obj.GetHeaderValue(16),
            com_obj.GetHeaderValue(20),
        ]

        bidqty = [
            com_obj.GetHeaderValue(6),
            com_obj.GetHeaderValue(10),
            com_obj.GetHeaderValue(14),
            com_obj.GetHeaderValue(18),
            com_obj.GetHeaderValue(22),
        ]

        bid_lpqty = [
            com_obj.GetHeaderValue(48),
            com_obj.GetHeaderValue(50),
            com_obj.GetHeaderValue(52),
            com_obj.GetHeaderValue(54),
            com_obj.GetHeaderValue(56),
        ]

        askpr = [
            com_obj.GetHeaderValue(3),
            com_obj.GetHeaderValue(7),
            com_obj.GetHeaderValue(11),
            com_obj.GetHeaderValue(15),
            com_obj.GetHeaderValue(19),
        ]

        askqty = [
            com_obj.GetHeaderValue(5),
            com_obj.GetHeaderValue(9),
            com_obj.GetHeaderValue(13),
            com_obj.GetHeaderValue(17),
            com_obj.GetHeaderValue(21),
        ]

        ask_lpqty = [
            com_obj.GetHeaderValue(47),
            com_obj.GetHeaderValue(49),
            com_obj.GetHeaderValue(51),
            com_obj.GetHeaderValue(53),
            com_obj.GetHeaderValue(55),
        ]

        bids, asks = [], []
        for p, q, lp in zip(bidpr, bidqty, bid_lpqty):
            bids.append((p, q, 0, lp))

        for p, q, lp in zip(askpr, askqty, ask_lpqty):
            asks.append((p, q, 0, lp))

        data = {'bids': bids, 'asks': asks}
        print('%s) %s %s' % (time, itm_cod, data))

        # # 이벤트 처리기에 전달
        # if self.eproc is not None:
        #     self.eproc.push('stkbid_%s' % itm_cod, tlist)


# 주식 현재가
@CpSbPb('dscbo1.StockCur')
class StkCur:
    def __init__(self):
        self.itm_cod = None
        self.eproc = None

    def setInitData(self, itm_cod=None, evntProc=None):
        self.itm_cod = itm_cod
        self.eproc = evntProc
        print('# STKCUR Init: %s' % self.itm_cod)

    def subscribe(self, com_obj):
        com_obj.Unsubscribe()
        com_obj.SetInputValue(0, self.itm_cod)
        com_obj.Subscribe()

    def publish(self, com_obj):
        nowpr    = com_obj.GetHeaderValue(13) # 현재가
        sellbuy  = com_obj.GetHeaderValue(14) # 매수매도구분(체결시)
        clsqty   = com_obj.GetHeaderValue(17) # 순간체결수량

        # 이벤트처리기에 전달
        self.evntproc.push('cls_%s'% (self.itm_cod), (nowpr, chr(sellbuy), clsqty))

