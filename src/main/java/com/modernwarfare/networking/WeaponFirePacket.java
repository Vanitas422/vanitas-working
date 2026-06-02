package com.modernwarfare.networking;

public record WeaponFirePacket(String shooterId, String weaponId, String ammoId, double x, double y, double z) implements Packet {
    @Override public String type() { return "weapon_fire"; }
    @Override public String encode() { return shooterId + ";" + weaponId + ";" + ammoId + ";" + x + ";" + y + ";" + z; }
}
