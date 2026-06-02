package com.modernwarfare.weapon;

import com.modernwarfare.ammo.AmmoDefinition;
import com.modernwarfare.registry.Registry;
import com.modernwarfare.util.Json;

import java.io.IOException;
import java.util.List;
import java.util.Map;

public final class WeaponCatalog {
    private WeaponCatalog() {}

    public static void load(Registry<WeaponDefinition> weapons, Registry<AmmoDefinition> ammo) throws IOException {
        for (Object value : Json.asArray(Json.parseResource("/data/modernwarfare/weapons/weapons.json"))) {
            Map<String, Object> map = Json.asObject(value);
            Map<String, Object> stats = Json.asObject(map.get("stats"));
            List<String> slots = Json.asArray(map.get("attachmentSlots")).stream().map(String::valueOf).toList();
            String caliber = Json.string(map, "caliber");
            boolean caliberAvailable = ammo.values().stream().anyMatch(profile -> profile.caliber().equals(caliber));
            if (!caliberAvailable) {
                throw new IllegalArgumentException("Weapon " + Json.string(map, "id") + " uses undefined caliber " + caliber);
            }
            weapons.register(new WeaponDefinition(
                    Json.string(map, "id"),
                    Json.string(map, "displayName"),
                    WeaponCategory.valueOf(Json.string(map, "category")),
                    caliber,
                    new WeaponStats(Json.number(stats, "damage"), Json.number(stats, "fireRate"), Json.number(stats, "verticalRecoil"),
                            Json.number(stats, "horizontalRecoil"), Json.number(stats, "accuracy"), Json.number(stats, "velocity"),
                            Json.number(stats, "reloadTime"), Json.number(stats, "weight"), Json.integer(stats, "magazineSize"),
                            Json.number(stats, "effectiveRange"), Json.number(stats, "maxRange"), Json.number(stats, "penetration")),
                    slots,
                    Json.string(map, "fireSound")
            ));
        }
    }
}
