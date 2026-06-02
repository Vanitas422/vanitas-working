package com.modernwarfare.armor;

import com.modernwarfare.registry.RegistryEntry;

public record ArmorDefinition(String id, String displayName, ArmorKind kind, ArmorClass armorClass, double weight,
                              double durability) implements RegistryEntry {
}
