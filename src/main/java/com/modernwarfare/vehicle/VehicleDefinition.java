package com.modernwarfare.vehicle;

import com.modernwarfare.registry.RegistryEntry;

public record VehicleDefinition(String id, String displayName, VehicleRole role, double armorFront, double armorSide,
                                double maxSpeed, boolean turret, boolean thermal, String primaryWeapon,
                                String secondaryWeapon) implements RegistryEntry {
}
