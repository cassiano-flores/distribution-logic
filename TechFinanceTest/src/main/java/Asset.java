public class Asset {
    private final String name;
    private final double price;
    private double quantity;
    private final double targetPercent;
    private final double minimumTick;

    public Asset(String name, double price, double quantity, double targetPercent, double minimumTick) {
        this.name = name;
        this.price = price;
        this.quantity = quantity;
        this.targetPercent = targetPercent;
        this.minimumTick = minimumTick;
    }

    public String getName() {
        return name;
    }

    public double getPrice() {
        return price;
    }

    public double getQuantity() {
        return quantity;
    }

    public void setQuantity(double quantity) {
        this.quantity = quantity;
    }

    public double getTargetPercent() {
        return targetPercent;
    }

    public double getMinimumTick() {
        return minimumTick;
    }
}
