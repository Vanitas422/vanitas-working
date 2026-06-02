package com.modernwarfare.attachment;

import com.modernwarfare.registry.Registry;
import com.modernwarfare.util.Json;

import java.io.IOException;
import java.util.Map;

public final class AttachmentCatalog {
    private AttachmentCatalog() {}

    public static void load(Registry<AttachmentDefinition> registry) throws IOException {
        for (Object value : Json.asArray(Json.parseResource("/data/modernwarfare/attachments/attachments.json"))) {
            Map<String, Object> map = Json.asObject(value);
            registry.register(new AttachmentDefinition(Json.string(map, "id"), Json.string(map, "displayName"),
                    AttachmentSlot.valueOf(Json.string(map, "slot")), Json.number(map, "recoilMultiplier"),
                    Json.number(map, "accuracyBonus"), Json.integer(map, "magazineDelta"), Json.number(map, "weightDelta"),
                    Json.bool(map, "suppressor"), Json.number(map, "zoom")));
        }
    }
}
