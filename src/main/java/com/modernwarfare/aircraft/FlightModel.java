package com.modernwarfare.aircraft;

public record FlightModel(double liftCoefficient, double dragCoefficient, double thrust, double radarCrossSection) {
    public double climbRate(double speed, double mass) {
        return Math.max(0.0, (liftCoefficient * speed * speed + thrust - mass * 9.81) / Math.max(1.0, mass));
    }
}
