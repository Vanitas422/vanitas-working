# Stylized Renderer Pro

Stylized Renderer Pro 是一个面向 Blender 5.1+ 的专业级 NPR 渲染插件，支持 Eevee Next 与 Cycles。插件通过统一 NPR Shader、JSON 风格预设、材质自动识别、描边系统、灯光 Rig、程序化天空和 AI 风格生成器，让用户一键切换游戏与动画风格。

## 完整项目目录

```text
stylized_renderer_pro/
├── __init__.py
├── README.md
├── docs/ARCHITECTURE.md
├── ai/
│   ├── __init__.py
│   ├── base.py
│   ├── generator.py
│   └── providers/
│       ├── __init__.py
│       ├── deepseek.py
│       └── openai.py
├── lighting/
│   ├── __init__.py
│   └── manager.py
├── materials/
│   ├── __init__.py
│   ├── applier.py
│   └── classifier.py
├── operators/
│   ├── __init__.py
│   ├── ai_ops.py
│   ├── asset_ops.py
│   ├── batch_ops.py
│   ├── light_ops.py
│   ├── material_ops.py
│   ├── outline_ops.py
│   ├── preset_ops.py
│   ├── render_ops.py
│   └── sky_ops.py
├── outline/
│   ├── __init__.py
│   └── manager.py
├── shaders/
│   ├── __init__.py
│   └── npr_shader.py
├── sky/
│   ├── __init__.py
│   └── manager.py
├── styles/
│   ├── __init__.py
│   ├── manager.py
│   ├── preset.py
│   └── presets/
│       ├── american_cartoon.json
│       ├── anime_standard.json
│       ├── arknights.json
│       ├── cyberpunk_anime.json
│       ├── delta_force.json
│       ├── genshin_impact.json
│       ├── ghibli_style.json
│       ├── honkai_star_rail.json
│       ├── makoto_shinkai_style.json
│       ├── manga_black_white.json
│       ├── neverness_to_everness.json
│       ├── painterly.json
│       ├── persona_style.json
│       ├── watercolor.json
│       └── wuthering_waves.json
├── ui/
│   ├── __init__.py
│   └── panel.py
└── utils/
    ├── __init__.py
    ├── addon_properties.py
    ├── constants.py
    ├── file_io.py
    ├── logger.py
    └── settings.py
```

## 安装

```bash
zip -r stylized_renderer_pro.zip stylized_renderer_pro
```

在 Blender 中打开 **Edit → Preferences → Add-ons → Install...**，选择生成的 ZIP 文件并启用插件。启用后在 3D Viewport 的 N 面板中打开 **Stylized Renderer Pro**。

## 已实现能力

- 15 个内置 JSON 风格预设：原神、鸣潮、异环、明日方舟、崩坏星穹铁道、女神异闻录、三角洲行动、日漫标准、吉卜力、新海诚、赛博朋克动画、美式卡通、黑白漫画、水彩、绘画风。
- 统一 NPR Shader 架构，禁止每个风格单独创建 Shader。
- 材质自动分类：Skin、Hair、Eyes、Metal、Cloth、Weapon、Environment。
- 三种描边模式：Inverted Hull、Freestyle、Geometry Nodes metadata modifier。
- 四种灯光 Rig：Anime、Studio、Outdoor、Night。
- 四种 World Sky：Anime、Sunset、Night、Cyberpunk。
- AI Generator 面板：离线启发式生成器，以及 OpenAI/DeepSeek 抽象 API 预留。
- 风格混合、导入、导出、一键应用、恢复默认、批量渲染、Asset Browser 标记、自动保存用户配置。
