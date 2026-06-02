package com.modernwarfare.attachment;

import com.modernwarfare.registry.RegistryEntry;

public record AttachmentDefinition(String id, String displayName, AttachmentSlot slot, double recoilMultiplier,
                                   double accuracyBonus, int magazineDelta, double weightDelta,
                                   boolean suppressor, double zoom) implements RegistryEntry {
}
