package com.modernwarfare.weapon;

import com.modernwarfare.registry.RegistryEntry;

import java.util.List;

public record WeaponDefinition(String id, String displayName, WeaponCategory category, String caliber,
                               WeaponStats stats, List<String> attachmentSlots, String fireSound) implements RegistryEntry {
}
