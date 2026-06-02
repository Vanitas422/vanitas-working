package com.modernwarfare.vehicle;

public final class VehicleDamageSystem {
    public double applyHit(VehicleDefinition vehicle, double penetration, boolean frontalAspect) {
        double armor = frontalAspect ? vehicle.armorFront() : vehicle.armorSide();
        double overmatch = Math.max(0.0, penetration - armor);
        return overmatch == 0.0 ? 0.0 : Math.min(100.0, overmatch * 1.35);
    }
}
