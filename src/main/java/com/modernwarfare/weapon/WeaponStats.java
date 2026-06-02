package com.modernwarfare.weapon;

public record WeaponStats(double damage, double fireRate, double verticalRecoil, double horizontalRecoil,
                          double accuracy, double velocity, double reloadTime, double weight,
                          int magazineSize, double effectiveRange, double maxRange, double penetration) {
    public WeaponStats modified(double damageMultiplier, double recoilMultiplier, double accuracyBonus, int magazineDelta, double weightDelta) {
        return new WeaponStats(damage * damageMultiplier, fireRate, verticalRecoil * recoilMultiplier,
                horizontalRecoil * recoilMultiplier, accuracy + accuracyBonus, velocity, reloadTime,
                weight + weightDelta, magazineSize + magazineDelta, effectiveRange, maxRange, penetration);
    }
}
