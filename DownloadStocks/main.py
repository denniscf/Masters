__author__ = 'DCFURLA'

from Stocks import Stocks

#Download IBOVESPA stocks timeseries
if __name__ == '__main__':
    s = Stocks(['BVMF:BBAS3', 'BVMF:BBDC3', 'BVMF:BBDC4',
                'BVMF:BRAP4', 'BVMF:BRKM5', 'BVMF:BRML3',
                'BVMF:CCRO3', 'BVMF:CESP6', 'BVMF:CIEL3', 'BVMF:CMIG4', 'BVMF:CPFE3', 'BVMF:CPLE6',
                'BVMF:CRUZ3', 'BVMF:CSNA3', 'BVMF:CTIP3', 'BVMF:CYRE3', 'BVMF:DTEX3',
                'BVMF:ELET3', 'BVMF:ELET6', 'BVMF:EMBR3', 'BVMF:ENBR3', 'BVMF:ESTC3',
                'BVMF:EVEN3', 'BVMF:FIBR3', 'BVMF:GGBR4', 'BVMF:GOAU4', 'BVMF:GOLL4',
                'BVMF:HGTX3', 'BVMF:HYPE3', 'BVMF:ITSA4', 'BVMF:ITUB4', 'BVMF:JBSS3',
                'BVMF:LAME4', 'BVMF:LIGT3', 'BVMF:LREN3', 'BVMF:MRFG3', 'BVMF:MRVE3',
                'BVMF:MULT3', 'BVMF:NATU3', 'BVMF:OIBR4', 'BVMF:PCAR4', 'BVMF:PDGR3', 'BVMF:PETR3',
                'BVMF:PETR4', 'BVMF:POMO4', 'BVMF:RENT3', 'BVMF:SANB11', 'BVMF:SBSP3',
                'BVMF:SUZB5', 'BVMF:TBLE3', 'BVMF:TIMP3', 'BVMF:USIM5', 'BVMF:VALE3',
                'BVMF:VALE5', 'BVMF:VIVT4'])
    start = '12/31/2009'
    end = '12/31/2014'
    #ABEV3, ALLL3, BRF3, BBSE3, BRPR3, BVMF3, CSAN3, CFSA3, ECOR3, KLBN11, KROT3, QUAL3, UGPA3 - Removed from processing
    #Reason: Not enough days

    s.DownloadStocks(start,end)
    s.OutputDataToCsv()