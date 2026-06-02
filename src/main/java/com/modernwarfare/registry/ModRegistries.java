package com.modernwarfare.registry;

import com.modernwarfare.ammo.AmmoDefinition;
import com.modernwarfare.armor.ArmorDefinition;
import com.modernwarfare.attachment.AttachmentDefinition;
import com.modernwarfare.sound.SoundDefinition;
import com.modernwarfare.vehicle.VehicleDefinition;
import com.modernwarfare.weapon.WeaponDefinition;

public final class ModRegistries {
    private final Registry<WeaponDefinition> weapons = new Registry<>("weapon");
    private final Registry<AmmoDefinition> ammo = new Registry<>("ammo");
    private final Registry<AttachmentDefinition> attachments = new Registry<>("attachment");
    private final Registry<ArmorDefinition> armors = new Registry<>("armor");
    private final Registry<VehicleDefinition> vehicles = new Registry<>("vehicle");
    private final Registry<SoundDefinition> sounds = new Registry<>("sound");

    public Registry<WeaponDefinition> weapons() { return weapons; }
    public Registry<AmmoDefinition> ammo() { return ammo; }
    public Registry<AttachmentDefinition> attachments() { return attachments; }
    public Registry<ArmorDefinition> armors() { return armors; }
    public Registry<VehicleDefinition> vehicles() { return vehicles; }
    public Registry<SoundDefinition> sounds() { return sounds; }
}
