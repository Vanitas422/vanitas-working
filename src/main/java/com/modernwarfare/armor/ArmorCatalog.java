package com.modernwarfare.armor;

import com.modernwarfare.registry.Registry;
import com.modernwarfare.util.Json;

import java.io.IOException;
import java.util.Map;

public final class ArmorCatalog {
    private ArmorCatalog() {}

    public static void load(Registry<ArmorDefinition> registry) throws IOException {
        for (Object value : Json.asArray(Json.parseResource("/data/modernwarfare/armor/armor.json"))) {
            Map<String, Object> map = Json.asObject(value);
            registry.register(new ArmorDefinition(Json.string(map, "id"), Json.string(map, "displayName"),
                    ArmorKind.valueOf(Json.string(map, "kind")), ArmorClass.valueOf(Json.string(map, "armorClass")),
                    Json.number(map, "weight"), Json.number(map, "durability")));
        }
    }
}
