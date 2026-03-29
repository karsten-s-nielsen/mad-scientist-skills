---
name: c4
description: Creates interactive C4 model architecture diagrams using Structurizr DSL — the official C4 notation by Simon Brown. Produces self-contained single-file HTML visualizations with embedded SVGs rendered locally via Java 21+ and the Structurizr export pipeline (structurizr.war + plantuml.jar). Generates System Context, Container, Component, Dynamic, and Deployment diagrams with tabbed navigation, DSL panel, and copyable Structurizr DSL source. Requires Java 21+. Use when the user asks for architecture diagrams, C4 diagrams, system diagrams, or wants to visualize software architecture.
---

# C4 Architecture Diagram Builder

A C4 diagram is a self-contained HTML file that visualizes software architecture at multiple zoom levels using the C4 model. This skill uses [Structurizr DSL](https://docs.structurizr.com/dsl) — the official C4 model notation created by Simon Brown — as the source language. Diagrams are rendered locally via a two-stage pipeline: Structurizr exports DSL to PlantUML C4, then plantuml.jar renders SVGs. SVGs are embedded directly in the HTML — making the output fully self-contained and offline-capable.

## Why Structurizr DSL?

- **Official format** — Structurizr DSL is the canonical C4 authoring language by the creator of C4
- **Model-first** — Define the model once, create multiple views from it (no duplication)
- **Portable** — DSL files can be imported into Structurizr tools and other C4-compatible software
- **Cleaner syntax** — No `@startuml`/`@enduml` wrappers or `!include` directives

## When to use this skill

When the user asks for:
- Architecture diagrams or system diagrams
- C4 model diagrams (Context, Container, Component)
- Software structure visualization
- "How does this system fit together?"
- Deployment or dynamic interaction diagrams
- Codebase architecture overview

## How to use this skill

1. **Understand the system.** Read relevant code, configs, and docs to understand the architecture. If the user describes a system verbally, capture the key elements.
2. **Identify the diagram type** from the user's request.
3. **Load the matching template** from `templates/`:
   - `templates/system-context.md` — Level 1: People, systems, and high-level interactions
   - `templates/container.md` — Level 2: Applications, data stores, and their communication
   - `templates/component.md` — Level 3: Internal structure of a single container
   - `templates/dynamic.md` — Numbered interaction sequences between elements
   - `templates/deployment.md` — Infrastructure nodes and deployed containers
4. **If no specific level requested**, build a multi-level explorer that includes System Context + Container diagrams with tab switching.
5. **Generate Structurizr DSL source** for each diagram level following the template syntax.
6. **Render each diagram** locally via the two-stage pipeline (see rendering workflow below).
7. **Assemble the HTML file** with embedded SVGs, tabbed navigation, DSL panel, and copy button.
8. **Save the `.dsl` source file** alongside the HTML for version control.
9. **Open in browser.** After writing the HTML file, run `open <filename>.html` (macOS) or `start <filename>.html` (Windows) to launch it.

## Core requirements (every C4 diagram)

- **Single HTML file.** Inline all CSS and JS. No external dependencies — SVGs are embedded at generation time.
- **Embedded SVGs.** Each diagram is a pre-rendered SVG embedded directly in the HTML. No CDN, no runtime rendering, no JavaScript module imports.
- **Tabbed navigation.** Level switching shows/hides diagram panels instantly via vanilla JS (no re-rendering needed).
- **DSL output panel.** Shows the raw Structurizr DSL source for the current view. Updates when switching levels.
- **Copy button.** Clipboard copy of the Structurizr DSL source with brief "Copied!" feedback.
- **Dark theme.** Dark background (#1a1a2e or similar), light text. System font for UI, monospace for DSL output.
- **Diagram legend.** Styling in the DSL provides automatic legend rendering via the C4-PlantUML export pipeline.
- **Companion `.dsl` file.** Save the complete workspace DSL file alongside the HTML for version control and Structurizr tool import.

## File naming convention

Use consistent names across all projects:

| File | Name | Purpose |
|------|------|---------|
| HTML viewer | `architecture.html` | Self-contained diagram viewer — commit so viewers need zero setup |
| DSL source | `architecture.dsl` | Structurizr DSL workspace — the editable source of truth |

Always use these exact names. Do not prefix with the project name or use uppercase. This ensures every repo has a predictable location for architecture diagrams.

## Structurizr DSL syntax reference

### Workspace structure

Every Structurizr DSL file is wrapped in a `workspace` block containing `model` and `views`:

```
# Structurizr DSL
workspace "Name" "Description" {

    model {
        // People, systems, containers, components, relationships
    }

    views {
        // Diagram views: systemContext, container, component, dynamic, deployment
    }

}
```

### People

```
# Structurizr DSL
<identifier> = person "Name" "Description" "Tags"
```

Example:
```
# Structurizr DSL
user = person "End User" "A user of the system who places orders"
admin = person "Administrator" "Manages configuration and users"
```

### Software systems

```
# Structurizr DSL
<identifier> = softwareSystem "Name" "Description" "Tags"
```

Example:
```
# Structurizr DSL
system = softwareSystem "My System" "Core business system that handles orders"
email = softwareSystem "Email Service" "Sendgrid" "External"
idp = softwareSystem "Identity Provider" "Auth0" "External"
```

### Containers (nested inside a software system)

```
# Structurizr DSL
<identifier> = container "Name" "Description" "Technology" "Tags"
```

Example:
```
# Structurizr DSL
system = softwareSystem "My System" "Handles orders" {
    spa = container "Web App" "Delivers the user experience via the browser" "React, TypeScript"
    api = container "API Service" "Handles business logic, exposes REST endpoints" "Node.js, Express"
    db = container "Database" "Stores users, orders, products" "PostgreSQL 15" "Database"
    cache = container "Cache" "Session storage and query caching" "Redis 7" "Database"
    queue = container "Message Queue" "Decouples API from async processing" "RabbitMQ" "Queue"
}
```

### Components (nested inside a container)

```
# Structurizr DSL
<identifier> = component "Name" "Description" "Technology" "Tags"
```

Example:
```
# Structurizr DSL
api = container "API Service" "Handles business logic" "Node.js, Express" {
    authMw = component "Auth Middleware" "Validates JWT tokens" "Express Middleware"
    userCtrl = component "User Controller" "Handles /api/users/* requests" "Express Router"
    userSvc = component "User Service" "Business logic for users" "TypeScript Class"
    userRepo = component "User Repository" "Data access for users" "TypeScript Class"
}
```

### Relationships

Relationships are defined using the `->` operator:

```
# Structurizr DSL
<source> -> <destination> "Description" "Technology"
```

Example:
```
# Structurizr DSL
user -> system "Uses" "HTTPS"
system -> email "Sends notifications" "SMTP/API"
api -> db "Reads from and writes to" "SQL/TCP"
```

Relationships can be defined:
- At the model level (between any elements)
- Inside element scope (implicitly from that element)

```
# Structurizr DSL
system = softwareSystem "My System" {
    api = container "API" "Business logic" "Node.js" {
        -> db "Reads/writes" "SQL"    // implicitly from api
    }
}
```

### Tags

Tags control styling. Built-in tags: `Element`, `Person`, `Software System`, `Container`, `Component`, `Relationship`. Custom tags are added as the last parameter or via `tags`:

```
# Structurizr DSL
db = container "Database" "Stores data" "PostgreSQL" "Database"
queue = container "Queue" "Message transport" "RabbitMQ" "Queue"
```

Or using the `tags` keyword inside scope:
```
# Structurizr DSL
db = container "Database" "Stores data" "PostgreSQL" {
    tags "Database"
}
```

### Views

Views are defined in the `views` block. Each view selects elements from the model to display.

**Omit the description parameter** on view definitions. The Structurizr exporter auto-generates a title from the view type and scope element name (e.g., "System Context View: My System"). Adding a description creates a redundant second title line in the rendered diagram.

#### System Context view

```
# Structurizr DSL
systemContext <softwareSystem> "key" {
    include *
    autoLayout
}
```

#### Container view

```
# Structurizr DSL
container <softwareSystem> "key" {
    include *
    autoLayout
}
```

#### Component view

```
# Structurizr DSL
component <container> "key" {
    include *
    autoLayout
}
```

#### Dynamic view

```
# Structurizr DSL
dynamic <scope> "key" {
    user -> spa "Submits order form"
    spa -> api "POST /api/orders"
    api -> db "INSERT order"
    api -> queue "Publish OrderCreated event"
    autoLayout
}
```

In dynamic views, relationships are rendered as numbered steps in the order they appear. **Do not include manual numbering** (e.g., "1. Load data", "2. Process request") in the relationship descriptions — Structurizr auto-numbers each step, so manual numbers produce duplicated labels like "3: 3. Extract text".

The `<scope>` can be:
- A software system identifier (shows containers)
- A container identifier (shows components)
- `*` (no scope restriction)

#### Deployment view

```
# Structurizr DSL
deployment <softwareSystem> <environment> "key" {
    include *
    autoLayout
}
```

### Deployment model

Deployment elements are defined inside the `model` block:

```
# Structurizr DSL
model {
    // ... elements ...

    production = deploymentEnvironment "Production" {
        deploymentNode "AWS" "Amazon Web Services" "Cloud" {
            deploymentNode "us-east-1" "US East" "AWS Region" {
                deploymentNode "ECS Cluster" "Container orchestration" "AWS Fargate" {
                    containerInstance api
                    containerInstance worker
                }
                deploymentNode "RDS" "Managed database" "Multi-AZ" {
                    containerInstance db
                }
            }
        }
    }
}
```

#### Infrastructure nodes

For infrastructure elements that aren't container instances:

```
# Structurizr DSL
deploymentNode "Public Subnet" "Internet-facing" "VPC" {
    infrastructureNode "Load Balancer" "Routes traffic, terminates TLS" "AWS ALB"
}
```

#### Container instances

Place containers from the model into deployment nodes:

```
# Structurizr DSL
containerInstance <containerIdentifier>
```

### View keywords

| Keyword | Description |
|---------|-------------|
| `include *` | Include all elements reachable from the scope |
| `include <element>` | Include a specific element |
| `exclude <element>` | Exclude a specific element |
| `autoLayout` | Automatic layout (default: top-bottom) |
| `autoLayout lr` | Left-to-right layout |
| `autoLayout tb` | Top-to-bottom layout (default) |
| `default` | Mark this view as the default when opening |

### Styling

Styles are defined in the `views` block:

```
# Structurizr DSL
views {
    // ... view definitions ...

    styles {
        element "Person" {
            shape Person
            background #08427B
            color #ffffff
        }
        element "Software System" {
            background #1168BD
            color #ffffff
        }
        element "External" {
            background #999999
            color #ffffff
        }
        element "Container" {
            background #438DD5
            color #ffffff
        }
        element "Database" {
            shape Cylinder
        }
        element "Queue" {
            shape Pipe
        }
        element "Component" {
            background #85BBF0
            color #000000
        }
        relationship "Relationship" {
            color #707070
        }
    }
}
```

Available shapes: `Box`, `RoundedBox`, `Circle`, `Ellipse`, `Hexagon`, `Cylinder`, `Pipe`, `Person`, `Robot`, `Folder`, `WebBrowser`, `MobileDeviceLandscape`, `MobileDevicePortrait`, `Component`.

## Rendering workflow

Diagrams are rendered locally via a two-stage pipeline: Structurizr exports DSL to PlantUML C4, then plantuml.jar renders PlantUML to SVG. Java 21+ is required for both stages.

**Tools used:**

| Tool | Purpose | Location | Download |
|------|---------|----------|----------|
| structurizr.war | Exports DSL to PlantUML C4 | `~/.claude/tools/structurizr.war` | `download.structurizr.com` |
| plantuml.jar | Renders PlantUML to SVG | `~/.claude/tools/plantuml.jar` | GitHub releases |

### Step 1: Write Structurizr DSL source

Write the complete workspace DSL (see syntax reference above). Save the `.dsl` file to disk — the export pipeline reads from the file.

### Step 2: Check Java availability

```bash
java -version
```

- **Java found** (exit code 0, version 21+) -> proceed to Step 3 (local rendering)
- **Java NOT found** or **version < 21** -> see "Java Not Found" section below

**Important:** Structurizr v6+ requires **Java 21 or later**. Earlier Java versions will not work.

### Step 3: Local rendering pipeline

#### 3a. Check for structurizr.war

- **Windows:** `%USERPROFILE%\.claude\tools\structurizr.war`
- **macOS/Linux:** `~/.claude/tools/structurizr.war`

If not found, download it. The WAR file is hosted at `download.structurizr.com` with a versioned filename. To find the current version and download URL, fetch the [binaries page](https://docs.structurizr.com/binaries) and extract the WAR link:

```bash
# Windows (PowerShell):
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\tools"
# Fetch the binaries page, extract the WAR filename, and download
$page = Invoke-WebRequest -Uri "https://docs.structurizr.com/binaries" -UseBasicParsing
$warUrl = ($page.Links | Where-Object { $_.href -match 'structurizr-.*\.war$' } | Select-Object -First 1).href
Invoke-WebRequest -Uri $warUrl -OutFile "$env:USERPROFILE\.claude\tools\structurizr.war"

# macOS/Linux:
mkdir -p ~/.claude/tools
WAR_URL=$(curl -s https://docs.structurizr.com/binaries | grep -oP 'https://download\.structurizr\.com/structurizr-[0-9.]+\.war' | head -1)
curl -L -o ~/.claude/tools/structurizr.war "$WAR_URL"
```

If the binaries page is unavailable, find the current `.war` download URL at https://docs.structurizr.com/binaries and substitute it into the curl/Invoke-WebRequest command above.

The file is saved as `structurizr.war` (without version in the filename) for simpler commands.

#### 3b. Check for plantuml.jar

- **Windows:** `%USERPROFILE%\.claude\tools\plantuml.jar`
- **macOS/Linux:** `~/.claude/tools/plantuml.jar`

If not found, download it:

```bash
# Windows (PowerShell):
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\tools"
Invoke-WebRequest -Uri "https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar" -OutFile "$env:USERPROFILE\.claude\tools\plantuml.jar"

# macOS/Linux:
mkdir -p ~/.claude/tools
curl -L -o ~/.claude/tools/plantuml.jar https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar
```

#### 3c. Export DSL to PlantUML C4

```bash
# Windows (PowerShell):
java -jar "$env:USERPROFILE\.claude\tools\structurizr.war" export -workspace <name>.dsl -format plantuml/c4plantuml -output <temp-dir>

# macOS/Linux:
java -jar ~/.claude/tools/structurizr.war export -workspace <name>.dsl -format plantuml/c4plantuml -output <temp-dir>
```

This produces one `.puml` file per view defined in the DSL. Each file corresponds to a view (e.g., `structurizr-SystemContext.puml`, `structurizr-Container.puml`).

#### 3d. Render PlantUML to SVG

```bash
# Windows (PowerShell):
java -jar "$env:USERPROFILE\.claude\tools\plantuml.jar" <temp-dir>\*.puml -tsvg

# macOS/Linux:
java -jar ~/.claude/tools/plantuml.jar <temp-dir>/*.puml -tsvg
```

This produces one SVG per `.puml` file. Read each SVG and embed in the HTML.

#### 3e. Clean and embed SVGs in HTML

Before embedding, strip the following from each SVG:

1. **Processing instructions** — Remove `<?plantuml ...?>` and `<?plantuml-src ...?>` tags
2. **Title element** — Remove `<title>...</title>` element (contains encoded text like `&lt;size:24&gt;System Context View...`)
3. **Auto-generated title blocks** — Remove the `<g class="title"...>...</g>` group. **IMPORTANT:** The opening tag includes extra attributes (e.g., `<g class="title" data-source-line="1">`), so the regex MUST match any attributes after `class="title"` — use `<g class="title"[^>]*>.*?</g>` (with `[^>]*` to match extra attributes and DOTALL flag). A regex like `<g class="title">...</g>` without the attribute wildcard will silently fail to match.

**Verification step (mandatory):** After cleaning, grep each SVG for `class="title"` — if any match remains, the cleaning failed and must be fixed before embedding.

Then place each cleaned SVG directly in its diagram panel `<div>` (see HTML template below).

#### 3f. Assembler script (recommended)

This skill includes a reusable Python script `c4_assemble.py` that handles SVG cleaning, verification, and HTML assembly. **Use this script instead of writing ad-hoc cleaning code.** It correctly handles all edge cases (extra attributes on title groups, multiline processing instructions, etc.) and includes mandatory verification.

```bash
# Find the script in the skill directory
SKILL_DIR="$(dirname "$(find ~/.claude -name c4_assemble.py -path '*/skills/c4/*' 2>/dev/null | head -1)")"

# Or on Windows:
# SKILL_DIR found via: Get-ChildItem -Recurse -Path "$env:USERPROFILE\.claude" -Filter c4_assemble.py | Where-Object { $_.DirectoryName -match 'skills[\\/]c4' } | Select -First 1

# Run: auto-detects views from SVG filenames in temp dir
python "$SKILL_DIR/c4_assemble.py" /path/to/project --svg-dir /tmp/c4-render

# Or specify views explicitly
python "$SKILL_DIR/c4_assemble.py" /path/to/project --svg-dir /tmp/c4-render \
    --views "system-context:System Context:structurizr-SystemContext.svg" \
    --views "containers:Containers:structurizr-Containers.svg"
```

The script auto-detects views from SVG filenames, extracts the system name from the DSL workspace declaration, cleans all SVGs with verification, and writes `architecture.html` alongside the DSL file. If any SVG still contains title content after cleaning, the script aborts with an error.

### Java Not Found — Installation Guidance

When Java is not detected, **stop and inform the user**:

> Java 21+ is required for Structurizr DSL rendering. Structurizr v6+ and PlantUML are both Java applications. There is no server fallback for Structurizr DSL — Java must be installed.

**Installation commands by platform:**

| Platform | Command |
|----------|---------|
| Windows | `winget install Microsoft.OpenJDK.21` |
| macOS | `brew install openjdk@21` |
| Linux (Debian/Ubuntu) | `sudo apt install openjdk-21-jre` |
| Linux (Fedora) | `sudo dnf install java-21-openjdk` |

Then **ask the user** whether to:
1. Install Java now (guide through installation, then continue with local rendering)
2. Cancel and save the `.dsl` file only (they can render later with any Structurizr-compatible tool)

**Note:** There is no server fallback for this skill. Structurizr's export command is a Java tool. If the user cannot install Java 21+, save the `.dsl` file and inform them it can be rendered with any tool that supports Structurizr DSL (e.g., the Structurizr web editor at structurizr.com).

### Important notes

- Always save the `.dsl` file to disk first — the export pipeline reads from disk
- The export produces intermediate `.puml` files in a temp directory — these are not kept
- Both structurizr.war and plantuml.jar are auto-downloaded to `~/.claude/tools/` on first use
- If Java is unavailable, save the `.dsl` file and inform the user they can render it with Structurizr Lite, Structurizr Cloud, or any compatible tool
- **Use HTML entities for special characters** in the generated HTML — never embed literal Unicode characters like `—` (em dash) or `→` (arrow). Use `&mdash;` and `&rarr;` instead. Literal Unicode characters can get corrupted when the HTML is assembled via shell scripts or multi-step encoding chains (e.g., PowerShell on Windows), producing garbled text like `â€"`.

## C4 color conventions

The C4-PlantUML stdlib (used in the intermediate export) automatically applies the standard C4 color palette. For reference:

| Element | Background | Text |
|---------|-----------|------|
| Person | #08427B | white |
| Software System (internal) | #1168BD | white |
| Software System (external) | #999999 | white |
| Container | #438DD5 | white |
| Container (database) | #438DD5 | white |
| Component | #85BBF0 | black |
| Relationship arrows | #707070 | -- |

The `styles` block in the DSL can override these defaults. Include the standard C4 styles in the DSL to ensure consistent coloring.

## HTML template pattern

The HTML viewer uses **pill-style tabs** for navigation with the **DSL source as a separate tab** (not a permanent sidebar). Diagrams render at their **natural size** inside a white card — if the viewport is narrower than the diagram, a horizontal scrollbar appears instead of shrinking the image.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[System Name] &mdash; C4 Architecture</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; }

    body {
      background: #1a1a2e;
      color: #e0e0e0;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      margin: 0;
      padding: 24px 32px;
      line-height: 1.6;
    }

    h1 {
      font-size: 1.8rem;
      font-weight: 700;
      margin: 0 0 8px 0;
      color: #ffffff;
    }

    p {
      margin: 0 0 24px 0;
      color: #a0a0b8;
      font-size: 0.95rem;
    }

    code {
      background: #16213e;
      padding: 2px 6px;
      border-radius: 4px;
      font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
      font-size: 0.9em;
      color: #7ec8e3;
    }

    /* --- Pill-style tabs --- */
    .tabs {
      display: flex;
      gap: 8px;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }

    .tab {
      background: #16213e;
      color: #a0a0b8;
      border: 1px solid #2a2a4a;
      border-radius: 24px;
      padding: 8px 20px;
      font-size: 0.9rem;
      font-family: inherit;
      cursor: pointer;
      transition: all 0.2s ease;
      outline: none;
    }

    .tab:hover {
      background: #1f2b4d;
      color: #e0e0e0;
      border-color: #3a3a5a;
    }

    .tab.active {
      background: #438DD5;
      color: #ffffff;
      border-color: #438DD5;
    }

    /* --- Tab content panels --- */
    .tab-content {
      display: none;
    }

    .tab-content.active {
      display: block;
    }

    /* --- SVG diagram container (natural size, scroll if wider than viewport) --- */
    .svg-container {
      background: #ffffff;
      border-radius: 8px;
      padding: 16px;
      overflow-x: auto;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
      border: 1px solid #2a2a4a;
    }

    .svg-container svg {
      display: block;
      margin: 0 auto;
      height: auto;
    }

    /* --- DSL source panel --- */
    .dsl-panel {
      position: relative;
      background: #16213e;
      border-radius: 8px;
      border: 1px solid #2a2a4a;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
      overflow: hidden;
    }

    .dsl-panel pre {
      margin: 0;
      padding: 20px;
      overflow-x: auto;
      font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
      font-size: 0.85rem;
      line-height: 1.6;
      color: #c8d0e0;
      tab-size: 4;
    }

    .dsl-panel code {
      background: none;
      padding: 0;
      border-radius: 0;
      color: inherit;
      font-size: inherit;
    }

    .copy-btn {
      position: absolute;
      top: 12px;
      right: 12px;
      background: #2a2a4a;
      color: #a0a0b8;
      border: 1px solid #3a3a5a;
      border-radius: 6px;
      padding: 6px 14px;
      font-size: 0.8rem;
      font-family: inherit;
      cursor: pointer;
      transition: all 0.2s ease;
      z-index: 10;
    }

    .copy-btn:hover {
      background: #3a3a5a;
      color: #e0e0e0;
    }

    .copy-btn.copied {
      background: #2e7d32;
      color: #ffffff;
      border-color: #2e7d32;
    }

    @media (max-width: 600px) {
      body { padding: 16px; }
      h1 { font-size: 1.4rem; }
      .tab { padding: 6px 14px; font-size: 0.8rem; }
    }
  </style>
</head>
<body>
  <h1>[System Name] &mdash; C4 Architecture</h1>
  <p>Generated from <code>architecture.dsl</code> using the Structurizr &rarr; PlantUML rendering pipeline.</p>

  <div class="tabs">
    <!-- One pill tab per diagram level, plus DSL tab last -->
    <button class="tab active" data-tab="system-context">System Context</button>
    <button class="tab" data-tab="containers">Containers</button>
    <!-- ... more levels as needed ... -->
    <button class="tab" data-tab="dsl">Structurizr DSL</button>
  </div>

  <!-- One tab-content per diagram level -->
  <div id="system-context" class="tab-content active">
    <div class="svg-container">
      <!-- Embedded SVG goes here -->
      <svg xmlns="http://www.w3.org/2000/svg">...</svg>
    </div>
  </div>

  <div id="containers" class="tab-content">
    <div class="svg-container">
      <svg xmlns="http://www.w3.org/2000/svg">...</svg>
    </div>
  </div>

  <!-- DSL source tab -->
  <div id="dsl" class="tab-content">
    <div class="dsl-panel">
      <button class="copy-btn" id="copyBtn" onclick="copyDSL()">Copy</button>
      <pre><code id="dsl-source"><!-- HTML-escaped DSL source goes here --></code></pre>
    </div>
  </div>

  <script>
    // Tab switching
    document.querySelectorAll('.tab').forEach(function(tab) {
      tab.addEventListener('click', function() {
        document.querySelectorAll('.tab').forEach(function(t) { t.classList.remove('active'); });
        document.querySelectorAll('.tab-content').forEach(function(c) { c.classList.remove('active'); });
        tab.classList.add('active');
        document.getElementById(tab.getAttribute('data-tab')).classList.add('active');
      });
    });

    // Copy DSL to clipboard
    function copyDSL() {
      var dslText = document.getElementById('dsl-source').textContent;
      var btn = document.getElementById('copyBtn');
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(dslText).then(function() {
          btn.textContent = 'Copied!';
          btn.classList.add('copied');
          setTimeout(function() {
            btn.textContent = 'Copy';
            btn.classList.remove('copied');
          }, 2000);
        });
      } else {
        var textarea = document.createElement('textarea');
        textarea.value = dslText;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        btn.textContent = 'Copied!';
        btn.classList.add('copied');
        setTimeout(function() {
          btn.textContent = 'Copy';
          btn.classList.remove('copied');
        }, 2000);
      }
    }
  </script>
</body>
</html>
```

**Key design decisions:**

- **Pill tabs** — Rounded filled buttons are more visually distinct and easier to target than underline tabs
- **DSL as a separate tab** — Keeps the diagram view uncluttered; the DSL source is one click away, not always consuming horizontal space
- **Natural SVG size** — Diagrams render at their intrinsic dimensions. No `max-width: 100%` or `width: 100%`. If the viewport is narrower, the `.svg-container` provides a horizontal scrollbar via `overflow-x: auto`
- **White SVG card** — C4-PlantUML renders with a white background, so the white card provides a seamless look. The dark border and shadow separate it from the dark page background
- **Clipboard fallback** — The copy function includes a `document.execCommand('copy')` fallback for contexts where `navigator.clipboard` is unavailable

**Note:** The DSL panel shows the complete Structurizr DSL workspace source (not the intermediate PlantUML). Since Structurizr DSL is model-first, the full workspace is the canonical source. The Copy button copies the Structurizr DSL.

## Source file generation

Save the complete Structurizr DSL workspace in a `.dsl` file alongside the HTML:

```
# Structurizr DSL
workspace "System Name" "Core description" {

    model {
        user = person "End User" "A user of the system"

        system = softwareSystem "System Name" "What the system does" {
            spa = container "Web App" "User interface" "React, TypeScript"
            api = container "API Service" "Business logic" "Node.js, Express"
            db = container "Database" "Data storage" "PostgreSQL 15" "Database"
        }

        user -> spa "Uses" "HTTPS"
        spa -> api "Makes API calls to" "HTTPS/JSON"
        api -> db "Reads from and writes to" "SQL/TCP"
    }

    views {
        systemContext system "SystemContext" {
            include *
            autoLayout
        }

        container system "Containers" {
            include *
            autoLayout
        }

        styles {
            element "Person" {
                shape Person
                background #08427B
                color #ffffff
            }
            element "Software System" {
                background #1168BD
                color #ffffff
            }
            element "External" {
                background #999999
                color #ffffff
            }
            element "Container" {
                background #438DD5
                color #ffffff
            }
            element "Database" {
                shape Cylinder
            }
            element "Component" {
                background #85BBF0
                color #000000
            }
        }
    }

}
```

This file is versionable, diffable, and can be imported directly into Structurizr Lite, Structurizr Cloud, or any tool that supports Structurizr DSL.

## Pre-populating from a real codebase

When analyzing actual code:
- **System Context:** Identify users/actors, the main system, and external systems it talks to (APIs, SaaS, databases)
- **Container:** Map deployable units — frontend apps, backend services, databases, message queues, caches
- **Component:** For a specific container, map its internal modules, controllers, services, repositories
- **Dynamic:** Trace a key user flow through the system (e.g., "user logs in", "order is placed")
- **Deployment:** Map infrastructure — cloud regions, clusters, servers, CDNs, load balancers

## Common mistakes to avoid

- **Missing `workspace` wrapper** — Every DSL file must be wrapped in `workspace { }` at the top level
- **Forward references** — Both source and destination elements must be defined before they can be referenced in a relationship. Relationships can be interleaved with element definitions, or defined inside element scope blocks using implicit source (`-> target "desc"`).
- **Relationships outside model** — All relationships must be inside the `model { }` block, not in `views { }`
- **Missing `autoLayout`** — Without `autoLayout` in a view, the diagram may render with overlapping elements. Always include it.
- **Containers outside software system scope** — Containers must be nested inside a `softwareSystem { }` block
- **Components outside container scope** — Components must be nested inside a `container { }` block
- **Missing view definitions** — The model alone doesn't produce diagrams. You must define views in `views { }` to generate output.
- **Using PlantUML syntax** — This skill uses Structurizr DSL, not PlantUML. Don't use `@startuml`, `!include`, `Rel()`, or PlantUML macros.
- **Identifier conflicts** — Each element needs a unique identifier within its scope. Use descriptive names like `webApp`, `apiService`, not `a`, `b`.
- **Mixing abstraction levels** — Don't put components directly in views meant for containers. Use the appropriate view type.
- **Too many elements** — Keep each level to 5-15 elements for readability
- **Missing descriptions** — Every element and relationship should have a meaningful description
- **No external systems** — Context diagrams must show what's OUTSIDE your system boundary
- **Skipping the technology tag** on containers/components — always specify (e.g., "React SPA", "PostgreSQL", "Spring Boot")
- **Adding descriptions to views** — Omit the description parameter on `systemContext`, `container`, `component`, `dynamic`, and `deployment` views. The exporter auto-generates a title from the view type and scope element. A description adds a redundant second line that overlaps with the auto-generated title.
- **Manual numbering in dynamic views** — Never prefix dynamic view descriptions with "1.", "2.", etc. Structurizr auto-numbers steps sequentially, so manual numbers produce duplicated labels like "3: 3. Extract text".
