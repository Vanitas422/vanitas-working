package com.modernwarfare.attachment;

import com.modernwarfare.weapon.WeaponDefinition;
import com.modernwarfare.weapon.WeaponStats;

import java.util.Collection;

public final class WeaponModification {
    private final WeaponDefinition baseWeapon;
    private final Collection<AttachmentDefinition> attachments;

    public WeaponModification(WeaponDefinition baseWeapon, Collection<AttachmentDefinition> attachments) {
        this.baseWeapon = baseWeapon;
        this.attachments = attachments;
    }

    public WeaponStats effectiveStats() {
        double recoil = 1.0;
        double accuracy = 0.0;
        int magazine = 0;
        double weight = 0.0;
        for (AttachmentDefinition attachment : attachments) {
            recoil *= attachment.recoilMultiplier();
            accuracy += attachment.accuracyBonus();
            magazine += attachment.magazineDelta();
            weight += attachment.weightDelta();
        }
        return baseWeapon.stats().modified(1.0, recoil, accuracy, magazine, weight);
    }

    public boolean suppressed() {
        return attachments.stream().anyMatch(AttachmentDefinition::suppressor);
    }
}
