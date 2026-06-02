package com.modernwarfare.config;

public record ModConfig(boolean serverAuthoritativeDamage, int maxProjectilesPerPlayer, double projectileTickSeconds,
                        boolean enableDistantGunshots, boolean enableSupersonicCracks, boolean enableThermals) {
    public static ModConfig defaults() {
        return new ModConfig(true, 256, 0.05, true, true, true);
    }
}
