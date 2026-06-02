package com.modernwarfare.vehicle;

import com.modernwarfare.registry.Registry;
import com.modernwarfare.util.Json;

import java.io.IOException;
import java.util.Map;

public final class VehicleCatalog {
    private VehicleCatalog() {}

    public static void load(Registry<VehicleDefinition> registry) throws IOException {
        for (String path : new String[]{"/data/modernwarfare/vehicles/vehicles.json", "/data/modernwarfare/aircraft/aircraft.json"}) {
            for (Object value : Json.asArray(Json.parseResource(path))) {
                Map<String, Object> map = Json.asObject(value);
                registry.register(new VehicleDefinition(Json.string(map, "id"), Json.string(map, "displayName"),
                        VehicleRole.valueOf(Json.string(map, "role")), Json.number(map, "armorFront"),
                        Json.number(map, "armorSide"), Json.number(map, "maxSpeed"), Json.bool(map, "turret"),
                        Json.bool(map, "thermal"), Json.string(map, "primaryWeapon"), Json.string(map, "secondaryWeapon")));
            }
        }
    }
}
