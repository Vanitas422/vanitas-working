package com.modernwarfare.server;

import com.modernwarfare.ballistics.BallisticEnvironment;
import com.modernwarfare.ballistics.BallisticProjectile;

public final class ServerCombatSystem {
    public BallisticProjectile tickProjectile(BallisticProjectile projectile) {
        return projectile.step(0.05, BallisticEnvironment.overworld());
    }
}
