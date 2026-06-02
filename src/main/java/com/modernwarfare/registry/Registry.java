package com.modernwarfare.registry;

import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Optional;

public final class Registry<T extends RegistryEntry> {
    private final String name;
    private final Map<String, T> entries = new LinkedHashMap<>();

    public Registry(String name) {
        this.name = name;
    }

    public void register(T entry) {
        if (entries.containsKey(entry.id())) {
            throw new IllegalArgumentException("Duplicate " + name + " id: " + entry.id());
        }
        entries.put(entry.id(), entry);
    }

    public Optional<T> get(String id) {
        return Optional.ofNullable(entries.get(id));
    }

    public Collection<T> values() {
        return entries.values();
    }

    public int size() {
        return entries.size();
    }
}
