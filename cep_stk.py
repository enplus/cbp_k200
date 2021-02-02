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
        tlist = []
        itm_cod = com_obj.GetHeaderValue(0)
        for i in range(3, 23, 4):
            itm = (
                com_obj.GetHeaderValue(i+0),
                com_obj.GetHeaderValue(i+1),
                com_obj.GetHeaderValue(i+2),
                com_obj.GetHeaderValue(i+3)
            )
            tlist.append(itm)

        # 이벤트 처리기에 전달
        if self.eproc is not None:
            self.eproc.push('stkbid_%s' % itm_cod, tlist)


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

