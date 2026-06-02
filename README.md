# Modern Warfare Reforged

Modern Warfare Reforged is a Java 21, data-driven modern military warfare mod scaffold targeting Minecraft Java Edition 26.1 and NeoForge 26.1.x.

The project is organized into common, client, server, weapon, ammo, attachment, armor, vehicle, aircraft, sound, animation, particle, networking, UI, crafting, config, rendering, registry, and data modules.

## Current implementation phases

- Phase 1: Gradle project, main mod bootstrap, registries, networking, and config.
- Phase 2: JSON-driven weapons and ammunition definitions.
- Phase 3: Tarkov-style attachment slots and effective-stat calculation.
- Phase 4: server-authoritative projectile ballistics with gravity, drag, penetration, ricochet, speed decay, tracer visibility, and flight time.
- Phase 5: ground vehicle, armor, aircraft, turret, thermal, and damage data models.
- Phase 6: sound event catalog, GeckoLib animation bridge, and particle event catalog.
- Phase 7: packet type registry and server combat ticking primitives for multiplayer synchronization.

## Build

```bash
gradle build
```

The produced jar is emitted under `build/libs/`.
