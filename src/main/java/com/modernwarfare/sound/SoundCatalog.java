package com.modernwarfare.sound;

import com.modernwarfare.registry.Registry;
import com.modernwarfare.weapon.WeaponDefinition;

public final class SoundCatalog {
    private SoundCatalog() {}

    public static void registerAll(Registry<SoundDefinition> sounds, Registry<WeaponDefinition> weapons) {
        for (WeaponDefinition weapon : weapons.values()) {
            for (SoundDistance distance : SoundDistance.values()) {
                sounds.register(new SoundDefinition(weapon.id() + "_fire_" + distance.name().toLowerCase(),
                        "modernwarfare:weapon/" + weapon.id() + "/fire_" + distance.name().toLowerCase(), distance, SoundEnvironment.OUTDOOR));
            }
            sounds.register(new SoundDefinition(weapon.id() + "_reload", "modernwarfare:weapon/" + weapon.id() + "/reload", SoundDistance.NEAR, SoundEnvironment.INDOOR));
            sounds.register(new SoundDefinition(weapon.id() + "_bolt", "modernwarfare:weapon/" + weapon.id() + "/bolt", SoundDistance.NEAR, SoundEnvironment.INDOOR));
            sounds.register(new SoundDefinition(weapon.id() + "_empty", "modernwarfare:weapon/" + weapon.id() + "/empty", SoundDistance.NEAR, SoundEnvironment.INDOOR));
            sounds.register(new SoundDefinition(weapon.id() + "_mag_insert", "modernwarfare:weapon/" + weapon.id() + "/mag_insert", SoundDistance.NEAR, SoundEnvironment.INDOOR));
        }
        sounds.register(new SoundDefinition("supersonic_crack", "modernwarfare:bullet/supersonic_crack", SoundDistance.MID, SoundEnvironment.OUTDOOR));
        sounds.register(new SoundDefinition("bullet_whiz", "modernwarfare:bullet/whiz", SoundDistance.NEAR, SoundEnvironment.OUTDOOR));
        sounds.register(new SoundDefinition("suppressor_tail", "modernwarfare:weapon/common/suppressor_tail", SoundDistance.MID, SoundEnvironment.FOREST));
    }
}
