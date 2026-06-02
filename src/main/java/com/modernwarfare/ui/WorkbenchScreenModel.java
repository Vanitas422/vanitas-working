package com.modernwarfare.ui;

import java.util.List;

public record WorkbenchScreenModel(WorkbenchType type, String titleKey, List<String> slotKeys) {
    public static WorkbenchScreenModel weaponModding() {
        return new WorkbenchScreenModel(WorkbenchType.WEAPON_MODDING_TABLE, "screen.modernwarfare.weapon_modding", 
                List.of("optic", "muzzle", "grip", "laser", "light", "stock", "magazine", "rail"));
    }
}
