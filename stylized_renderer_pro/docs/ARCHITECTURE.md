# Stylized Renderer Pro — Architecture Design

Stylized Renderer Pro is a modular Blender 5.1+ add-on that switches a scene between game-inspired and animation-inspired non-photorealistic rendering (NPR) looks. It targets Eevee Next and Cycles through Python, `bpy`, shader nodes, compositor-ready render settings, Geometry Nodes modifiers, and JSON style presets.

## Goals

- Provide one-click style application through a unified NPR shader architecture.
- Keep every style as data (`styles/presets/*.json`) instead of hard-coding one shader per look.
- Support Blender 5.x evolution by isolating direct `bpy` calls inside managers and operators.
- Offer production tools: material classification, outline mode switching, lighting rigs, world skies, style mixing, import/export, batch rendering, Asset Browser marking, and user configuration persistence.
- Reserve AI style generation behind an abstract provider interface with OpenAI and DeepSeek provider modules.

## Package Layout

```text
stylized_renderer_pro/
├── __init__.py                  # Blender add-on registration entry point
├── docs/ARCHITECTURE.md         # This architecture document
├── ai/                          # AI prompt-to-style generation
│   ├── base.py                  # Provider interface and deterministic fallback parser
│   ├── generator.py             # Provider selection and generated-preset normalization
│   └── providers/
│       ├── deepseek.py          # DeepSeek-compatible HTTP provider
│       └── openai.py            # OpenAI-compatible HTTP provider
├── lighting/manager.py          # Anime/studio/outdoor/night light rigs
├── materials/                   # Material recognition and shader assignment
│   ├── applier.py
│   └── classifier.py
├── operators/                   # Blender operators used by the N-panel
│   ├── ai_ops.py
│   ├── asset_ops.py
│   ├── batch_ops.py
│   ├── light_ops.py
│   ├── material_ops.py
│   ├── outline_ops.py
│   ├── preset_ops.py
│   ├── render_ops.py
│   └── sky_ops.py
├── outline/manager.py           # Inverted hull, Freestyle, Geometry Nodes outlines
├── shaders/npr_shader.py        # Shared node-tree shader builder
├── sky/manager.py               # World node presets
├── styles/                      # Style dataclasses, loading, mixing, import/export
│   ├── manager.py
│   ├── preset.py
│   └── presets/*.json
├── ui/panel.py                  # Stylized Renderer Pro N-panel
└── utils/                       # Constants, properties, logging, config singleton, I/O
    ├── addon_properties.py
    ├── constants.py
    ├── file_io.py
    ├── logger.py
    └── settings.py
```

## Data Model

All styles share `StyleParameters`, a dataclass containing:

- `outline_width`, `outline_color`
- `shadow_steps`, `shadow_color`
- `rim_light`, `rim_light_color`
- `specular_strength`
- `saturation`, `contrast`
- `ambient_occlusion`, `bloom`, `depth_of_field`, `fog`
- `color_grading`
- optional per-category material overrides for skin, hair, eyes, metal, cloth, weapon, and environment.

The add-on loads each preset JSON into a `StylePreset` dataclass. The active preset is serialized into the scene property group so UI controls, operators, and render settings remain synchronized.

## Unified NPR Shader

`shaders/npr_shader.py` builds one reusable node architecture for all visual styles:

1. Principled BSDF provides Blender 5.x compatibility and works in Eevee Next/Cycles.
2. Color ramps quantize diffuse shading into toon-like bands based on `shadow_steps`.
3. Emission/rim controls are represented as custom material properties and node values.
4. Material category overrides adjust saturation, contrast, roughness, metallic, and specular inputs without changing the node topology.

No preset creates a unique shader graph. Style JSON only changes parameters.

## Material Recognition

The classifier uses material and object names plus shader hints to assign one of seven categories:

- Skin
- Hair
- Eyes
- Metal
- Cloth
- Weapon
- Environment

The applier stores `srp_material_category` on materials, applies category overrides, and rebuilds the shared NPR node tree.

## Outline Modes

`outline/manager.py` supports three switchable modes:

- **Inverted Hull Outline**: creates/updates duplicate outline objects with flipped normals material and Solidify modifier.
- **Freestyle Outline**: enables render-layer Freestyle and uses line color/thickness from the active style.
- **Geometry Nodes Outline**: creates a reusable Geometry Nodes modifier placeholder and stores all outline parameters for future node-group upgrades.

## Lighting and Sky Systems

Lighting rigs are generated as named collections so they can be removed/rebuilt safely. Supported rigs:

- Anime Lighting
- Studio Lighting
- Outdoor Lighting
- Night Lighting

World presets create a procedural node setup for:

- Anime Sky
- Sunset Sky
- Night Sky
- Cyberpunk Sky

## AI Generator

The AI layer is intentionally provider-agnostic:

- `AIProvider` is the abstract base.
- `OpenAIStyleProvider` and `DeepSeekStyleProvider` implement compatible REST calls.
- `HeuristicStyleProvider` provides an offline deterministic generator so the add-on remains usable without API keys.

Generated output is normalized into style parameters and can be applied immediately or exported as a new JSON preset.

## Registration Flow

`__init__.py` registers:

1. Scene and WindowManager properties.
2. Operators.
3. N-panel UI classes.
4. Loads default presets and user config through the singleton settings manager.

Unregister reverses the order to avoid dangling Blender RNA classes.

## Packaging

The folder is directly zip-installable:

```bash
zip -r stylized_renderer_pro.zip stylized_renderer_pro
```

Install in Blender through **Edit → Preferences → Add-ons → Install...** and select the ZIP.
