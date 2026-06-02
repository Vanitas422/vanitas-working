package com.modernwarfare.networking;

import java.util.LinkedHashSet;
import java.util.Set;

public final class NetworkSystem {
    private final String channel;
    private final Set<String> packetTypes = new LinkedHashSet<>();

    public NetworkSystem(String channel) { this.channel = channel; }

    public void registerDefaultPackets() {
        register("weapon_fire");
        register("projectile_spawn");
        register("particle_event");
        register("animation_event");
        register("vehicle_state");
        register("sound_event");
    }

    public void register(String type) { packetTypes.add(type); }
    public boolean accepts(Packet packet) { return packetTypes.contains(packet.type()); }
    public String channel() { return channel; }
    public Set<String> packetTypes() { return Set.copyOf(packetTypes); }
}
