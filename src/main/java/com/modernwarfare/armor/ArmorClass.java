package com.modernwarfare.armor;

public enum ArmorClass {
    IIIA(35),
    III(70),
    IV(105);

    private final double resistance;

    ArmorClass(double resistance) { this.resistance = resistance; }
    public double resistance() { return resistance; }
}
