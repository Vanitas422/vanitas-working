package com.modernwarfare.ballistics;

import com.modernwarfare.ammo.AmmoDefinition;
import com.modernwarfare.weapon.WeaponDefinition;

import java.util.UUID;

public final class BallisticsEngine {
    public BallisticProjectile fireServerAuthoritative(WeaponDefinition weapon, AmmoDefinition ammo, Vec3 muzzle, Vec3 direction) {
        double muzzleVelocity = weapon.stats().velocity() * ammo.muzzleVelocityMultiplier();
        Vec3 velocity = direction.normalize().scale(muzzleVelocity);
        double energy = 0.5 * (ammo.massGrams() / 1000.0) * muzzleVelocity * muzzleVelocity;
        return new BallisticProjectile(UUID.randomUUID().toString(), weapon, ammo, muzzle, velocity, 0.0, energy);
    }

    public boolean penetrates(BallisticProjectile projectile, double armorResistance) {
        return projectile.weapon().stats().penetration() * projectile.ammo().penetrationMultiplier() * projectile.energyJoules() / 1000.0 > armorResistance;
    }

    public boolean ricochets(double incidenceCosine, double surfaceHardness, BallisticEnvironment environment) {
        return incidenceCosine < 0.22 && surfaceHardness >= environment.ricochetHardnessThreshold();
    }
}
