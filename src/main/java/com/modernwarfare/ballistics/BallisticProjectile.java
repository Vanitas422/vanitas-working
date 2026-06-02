package com.modernwarfare.ballistics;

import com.modernwarfare.ammo.AmmoDefinition;
import com.modernwarfare.weapon.WeaponDefinition;

public record BallisticProjectile(String id, WeaponDefinition weapon, AmmoDefinition ammo, Vec3 position,
                                  Vec3 velocity, double ageSeconds, double energyJoules) {
    public BallisticProjectile step(double seconds, BallisticEnvironment environment) {
        Vec3 gravity = new Vec3(0.0, -environment.gravity(), 0.0);
        Vec3 drag = velocity.scale(-environment.dragCoefficient() * velocity.length());
        Vec3 nextVelocity = velocity.add(gravity.add(drag).scale(seconds));
        Vec3 nextPosition = position.add(nextVelocity.scale(seconds));
        double energy = 0.5 * (ammo.massGrams() / 1000.0) * nextVelocity.length() * nextVelocity.length();
        return new BallisticProjectile(id, weapon, ammo, nextPosition, nextVelocity, ageSeconds + seconds, energy);
    }

    public boolean tracerVisible() {
        return ammo.tracer() && ageSeconds > 0.05;
    }
}
