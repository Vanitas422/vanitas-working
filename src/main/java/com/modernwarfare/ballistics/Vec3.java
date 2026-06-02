package com.modernwarfare.ballistics;

public record Vec3(double x, double y, double z) {
    public Vec3 add(Vec3 other) { return new Vec3(x + other.x, y + other.y, z + other.z); }
    public Vec3 scale(double scalar) { return new Vec3(x * scalar, y * scalar, z * scalar); }
    public double length() { return Math.sqrt(x * x + y * y + z * z); }
    public Vec3 normalize() {
        double length = length();
        return length == 0.0 ? new Vec3(0.0, 0.0, 0.0) : scale(1.0 / length);
    }
}
