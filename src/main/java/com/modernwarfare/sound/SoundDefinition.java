package com.modernwarfare.sound;

import com.modernwarfare.registry.RegistryEntry;

public record SoundDefinition(String id, String path, SoundDistance distance, SoundEnvironment environment) implements RegistryEntry {
}
