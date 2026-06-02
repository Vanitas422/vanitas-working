package com.modernwarfare.client;

import com.modernwarfare.animation.GeckoAnimationBridge;
import com.modernwarfare.particle.ParticleSystem;

public final class ClientProxy {
    private final GeckoAnimationBridge animations = new GeckoAnimationBridge();
    private final ParticleSystem particles = new ParticleSystem();

    public GeckoAnimationBridge animations() { return animations; }
    public ParticleSystem particles() { return particles; }
}
