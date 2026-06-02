package com.modernwarfare.particle;

import java.util.EnumMap;
import java.util.Map;

public final class ParticleSystem {
    private final Map<ParticleEvent, Integer> lifetimes = new EnumMap<>(ParticleEvent.class);

    public ParticleSystem() {
        lifetimes.put(ParticleEvent.MUZZLE_FLASH, 3);
        lifetimes.put(ParticleEvent.MUZZLE_SMOKE, 35);
        lifetimes.put(ParticleEvent.EJECTED_CASING, 100);
        lifetimes.put(ParticleEvent.PENETRATION_SPARK, 12);
        lifetimes.put(ParticleEvent.EXPLOSION_SHOCKWAVE, 45);
        lifetimes.put(ParticleEvent.TANK_DUST, 70);
        lifetimes.put(ParticleEvent.MISSILE_TRAIL, 55);
    }

    public int lifetimeTicks(ParticleEvent event) { return lifetimes.get(event); }
}
