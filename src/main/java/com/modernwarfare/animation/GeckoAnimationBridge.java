package com.modernwarfare.animation;

public final class GeckoAnimationBridge {
    public String controllerName(AnimationEvent event, boolean firstPerson) {
        return (firstPerson ? "first_person_" : "third_person_") + event.name().toLowerCase();
    }
}
