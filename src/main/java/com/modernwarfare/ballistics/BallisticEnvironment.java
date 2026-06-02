package com.modernwarfare.ballistics;

public record BallisticEnvironment(double gravity, double dragCoefficient, double ricochetHardnessThreshold) {
    public static BallisticEnvironment overworld() {
        return new BallisticEnvironment(9.81, 0.00018, 0.72);
    }
}
