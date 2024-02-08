/*
    ÚNICO ARQUIVO QUE SERÁ MODIFICADO!
    A MEDIDA QUE COMPRAR/VENDER ATIVOS, INSERIR AQUI COM SUA RESPECTIVA QUANTIDADE E PERCENTUAL DESEJADO
*/

public enum MyAssets {
    BBAS3(5, (0.4 * 0.28 * ((double) 1 / 3))),
    BBDC3(35, (0.4 * 0.28 * ((double) 1 / 3))),
    SANB3(31, (0.4 * 0.28 * ((double) 1 / 3))),
    AESB3(20, (0.4 * 0.45 * ((double) 1 / 5))),
    AURE3(35, (0.4 * 0.45 * ((double) 1 / 5))),
    CMIG4(28, (0.4 * 0.45 * ((double) 1 / 5))),
    TAEE3(37, (0.4 * 0.45 * ((double) 1 / 5))),
    TRPL4(17, (0.4 * 0.45 * ((double) 1 / 5))),
    BBSE3(10, (0.4 * 0.18 * ((double) 1 / 2))),
    CXSE3(20, (0.4 * 0.18 * ((double) 1 / 2))),
    SAPR3(41, (0.4 * 0.09 * ((double) 1))),
    KNRI11(4, (0.25 * 0.5 * ((double) 1 / 2))),
    MXRF11(70, (0.25 * 0.5 * ((double) 1 / 2))),
    HGLG11(1, (0.25 * 0.18 * ((double) 1 / 2))),
    VILG11(1, (0.25 * 0.18 * ((double) 1 / 2))),
    BRCR11(1, (0.25 * 0.18 * ((double) 1 / 2))),
    HGRE11(1, (0.25 * 0.18 * ((double) 1 / 2))),
    MALL11(1, (0.25 * 0.14 * ((double) 1 / 2))),
    XPML11(2, (0.25 * 0.14 * ((double) 1 / 2)))/*,
    DLR(1),
    O(1),
    STAG(1),
    SPG(1),
    AMT(1),
    ARR(1),
    VOO(1),
    BTC(1),
    ETH(1),
    RE(1)*/;

    private final double quantity;
    private final double targetPercent;

    MyAssets(double quantity, double targetPercent) {
        this.quantity = quantity;
        this.targetPercent = targetPercent;
    }

    public double getQuantity() {
        return quantity;
    }

    public double getTargetPercent() {
        return targetPercent;
    }
}
