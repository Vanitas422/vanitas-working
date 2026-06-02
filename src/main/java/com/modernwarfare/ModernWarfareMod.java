package com.modernwarfare;

import com.modernwarfare.ammo.AmmoCatalog;
import com.modernwarfare.armor.ArmorCatalog;
import com.modernwarfare.attachment.AttachmentCatalog;
import com.modernwarfare.config.ModConfig;
import com.modernwarfare.networking.NetworkSystem;
import com.modernwarfare.registry.ModRegistries;
import com.modernwarfare.sound.SoundCatalog;
import com.modernwarfare.vehicle.VehicleCatalog;
import com.modernwarfare.weapon.WeaponCatalog;
import net.neoforged.fml.common.Mod;

import java.io.IOException;
import java.util.logging.Logger;

@Mod(ModernWarfareMod.MOD_ID)
public final class ModernWarfareMod {
    public static final String MOD_ID = "modernwarfare";
    public static final String MOD_NAME = "Modern Warfare Reforged";
    public static final Logger LOGGER = Logger.getLogger(MOD_NAME);

    private final ModConfig config;
    private final ModRegistries registries;
    private final NetworkSystem networkSystem;
    private boolean initialized;

    public ModernWarfareMod() {
        this.config = ModConfig.defaults();
        this.registries = new ModRegistries();
        this.networkSystem = new NetworkSystem(MOD_ID);
        bootstrap();
    }

    private void bootstrap() {
        try {
            initialize();
        } catch (IOException exception) {
            throw new IllegalStateException("Failed to initialize " + MOD_NAME, exception);
        }
    }

    public void initialize() throws IOException {
        if (initialized) {
            return;
        }

        LOGGER.info(() -> "Initializing " + MOD_NAME);
        AmmoCatalog.load(registries.ammo());
        AttachmentCatalog.load(registries.attachments());
        WeaponCatalog.load(registries.weapons(), registries.ammo());
        ArmorCatalog.load(registries.armors());
        VehicleCatalog.load(registries.vehicles());
        SoundCatalog.registerAll(registries.sounds(), registries.weapons());
        networkSystem.registerDefaultPackets();
        initialized = true;
        LOGGER.info(() -> "Loaded " + registries.weapons().size() + " weapons, "
                + registries.ammo().size() + " ammunition profiles, "
                + registries.attachments().size() + " attachments, and "
                + registries.vehicles().size() + " vehicles.");
    }

    public ModConfig config() {
        return config;
    }

    public ModRegistries registries() {
        return registries;
    }

    public NetworkSystem networkSystem() {
        return networkSystem;
    }

    public static void main(String[] args) {
        new ModernWarfareMod();
    }
}
