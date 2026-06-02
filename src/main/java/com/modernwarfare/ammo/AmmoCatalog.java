package com.modernwarfare.ammo;

import com.modernwarfare.registry.Registry;
import com.modernwarfare.util.Json;

import java.io.IOException;
import java.util.Map;

public final class AmmoCatalog {
    private AmmoCatalog() {}

    public static void load(Registry<AmmoDefinition> registry) throws IOException {
        for (Object value : Json.asArray(Json.parseResource("/data/modernwarfare/ammo/ammo.json"))) {
            Map<String, Object> map = Json.asObject(value);
            registry.register(new AmmoDefinition(
                    Json.string(map, "id"),
                    Json.string(map, "caliber"),
                    AmmoType.valueOf(Json.string(map, "type")),
                    Json.number(map, "massGrams"),
                    Json.number(map, "muzzleVelocityMultiplier"),
                    Json.number(map, "penetrationMultiplier"),
                    Json.number(map, "damageMultiplier"),
                    Json.bool(map, "tracer")
            ));
        }
    }
}
