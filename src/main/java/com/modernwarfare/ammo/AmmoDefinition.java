package com.modernwarfare.ammo;

import com.modernwarfare.registry.RegistryEntry;

public record AmmoDefinition(String id, String caliber, AmmoType type, double massGrams, double muzzleVelocityMultiplier,
                             double penetrationMultiplier, double damageMultiplier, boolean tracer) implements RegistryEntry {
}
