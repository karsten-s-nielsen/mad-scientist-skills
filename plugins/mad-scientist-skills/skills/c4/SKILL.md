---
name: c4
description: Creates interactive C4 model architecture diagrams using Structurizr DSL — the official C4 notation by Simon Brown. Produces self-contained single-file HTML visualizations with embedded SVGs rendered locally via Java 21+ and the Structurizr export pipeline (structurizr.war + plantuml.jar). Generates System Context, Container, Component, Dynamic, and Deployment diagrams with tabbed navigation, DSL panel, and copyable Structurizr DSL source. Requires Java 21+ and Graphviz — verify Graphviz with `java -jar plantuml.jar -testdot`, never with `which dot` (PlantUML resolves dot through its own search paths, so an installed Graphviz that is absent from PATH still works). Use when the user asks for architecture diagrams, C4 diagrams, system diagrams, or wants to visualize software architecture.
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

## Readability & Navigation

Large diagrams become unreadable two ways: individual boxes grow too wide, and a
single view holds too many elements. Three tunable levers (defaults chosen from
empirical render measurements) address both, plus bidirectional drill-down ties
the views together.

| Constant | Unit | Governs | Default |
|---|---|---|---|
| `MAX_BOX_DESCR_CHARS` | characters | Authoring cap on each element description — keeps text human-readable; warned at assemble time | `200` |
| `BOX_WRAP_WIDTH_PX` | pixels | Render wrap — pixel width at which box text wraps to the next line | `200` |
| `MAX_ELEMENTS_PER_VIEW` | elements | Subdivision guideline — split a view when it exceeds this | `15` |

**Character cap vs pixel wrap are different levers.** The character cap
(`MAX_BOX_DESCR_CHARS`) stops a box from holding an essay; the pixel wrap
(`BOX_WRAP_WIDTH_PX`) stops even a capped 200-char line from rendering as one
ultra-wide row. `200` matches C4's stock wrap for fairly square boxes; lower it
(e.g. `150`) for narrower, taller boxes.

- **Authoring rule:** cap each element `description` at `MAX_BOX_DESCR_CHARS` (200)
  characters. A box cannot shrink below its widest unbreakable token (a long word,
  URL, or the `<<stereotype>>` label) — the pixel wrap helps typical prose, not a
  single long identifier. The assembler **measures** this and prints a non-fatal
  `WARN` per breach, worst first:

  ```
  Authoring lint: 3 element description(s) exceed the 200-character cap …
    WARN: 'documentation-audit Skill' (documentationAuditSkill) has a
          317-character description.
  ```

  The rule went unmeasured for a long time and drifted accordingly: a scan of 18
  real workspaces found **14 descriptions over the cap, the worst at 664
  characters** — including three in this plugin's own diagram, since fixed.
- **Subdivision rule:** when a container view would exceed ~`MAX_ELEMENTS_PER_VIEW`
  (15) *boxes* (people/systems/containers/components in scope — relationships and
  boundary clusters do not count), emit **one `Component_<containerId>` view per
  container** instead of a single combined `Components` view. Splitting remains a
  modeling decision you (or Claude) make, but the assembler now **counts** the
  boxes and prints a non-fatal `WARN` for any view above the guideline:

  ```
  WARN: structurizr-Containers.svg has 41 element nodes — the readability
        guideline is 15; consider splitting it.
  ```

  It warns rather than fails because a legitimately flat system can exceed 15.
  Treat the warning as a prompt to re-read the view, not as an error to silence.
- **View-key naming convention** (powers grouping *and* drill-down):

  ```
  SystemContext
  Containers                     # single software system
  Containers_<systemId>          # one per system when the workspace has several
  Component_<containerId>
  Dynamic_<flowId>
  Deployment_<envId>
  ```

  Structurizr exports `structurizr-<ViewKey>.svg`; the assembler groups tabs by
  the key prefix and drills from a container box into its `Component_<id>` view.
  A small system may keep the combined `Components` key — it is still navigable.

  **Multi-system workspaces must use the `Containers_<systemId>` form.** Structurizr
  view keys are unique across the workspace, so N software systems need N distinct
  container-view keys; the bare `Containers` key can only ever name one of them.
  Any key the prefix table does not recognise becomes **its own top-level tab**, so
  a bespoke name like `CIContainers` advertises an architectural level that does not
  exist. Both separators (`Containers_CI`, `Containers-CI`) and the singular DSL
  spelling (`Container_CI`) group correctly.

- **Drill-down (single software system):** in the generated HTML, clicking a
  container box that has a deeper Component view switches to that view; each detail
  view shows a breadcrumb (`Context › Containers › api`) to navigate back up. Only
  boxes with a target are clickable. The drill axis is `SystemContext → Containers
  → Component_<id>`; Deployment tabs are navigation leaves.

  A **multi-system** workspace groups and breadcrumbs correctly (each
  `Containers_<systemId>` panel gets its `Context ›` crumb), but click-through
  drill-down remains single-system: the `Containers` crumb on a Component panel
  resolves against the bare key, which a multi-system workspace does not have, so
  that one crumb is omitted rather than pointed at a missing panel.

- **Coverage lint (automated, non-fatal):** the assembler flags modeled detail
  that renders in no diagram, at **both** levels. This is the mirror image of
  subdivision: subdivision splits an over-full view; the lint catches a
  decomposition that was modeled and then forgotten.

  | Level | Flagged when | Warning |
  |-------|--------------|---------|
  | 2 | a `softwareSystem` declares `container` children but has **no `container` view scoped to it** | `WARN: software system '<name>' (<id>) has N container(s) but no container <id> "Containers_<id>" view.` |
  | 3 | a `container` declares `component` children but has **no `component` view scoped to it** | `WARN: container '<name>' (<id>) has N component(s) but no component <id> "Component_<id>" view.` |

  Neither fails the build (the model stays internally consistent — an uncovered
  container is correctly left inert for drill-down). Resolve either by adding the
  missing view (`container <id> "Containers_<id>" { include * autoLayout }`) or, if
  that subtree genuinely does not warrant its own view, deleting the child
  declarations so the model does not carry invisible detail.

  **The Level-2 case is the damaging one** — a missing component view hides one
  container's internals; a missing container view hides an entire subsystem. It is
  also the easier one to miss, because nothing else in the pipeline complains: the
  DSL is valid, the export succeeds, and the elements show up in the DSL panel.

  Coverage means **a view scoped to that element and nothing else**. In particular
  `include <containerId>` inside *another* system's container view does not count:
  a container view may only hold containers of its own scope, so the exporter drops
  the foreign include and the element still renders nowhere. The lint deliberately
  keeps warning in that case.

- **Do not verify coverage by grepping the output.** Searching `architecture.html`
  or the `.puml` files for an element's name gives both false passes and false
  failures:

  - PlantUML splits label text across `<text>` nodes, so `CVE Review` appears as
    `>CVE<` + `>Review<` and greps for the whole phrase find nothing.
  - The assembled HTML embeds the **DSL source panel**, so a name "found" in the
    page may only be the model text — the element itself may render nowhere.
  - `.puml` files carry generated aliases (`Sys.APIService`), not DSL identifiers,
    so an identifier grep returns nothing even for elements that did render.

  The reliable key in a `.puml` is the element **name**. Better still, trust the
  coverage lint above — it is a structural check against the DSL, immune to label
  wrapping and to what happens to be quoted in a panel.

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

#### 3c-2. Inject the pixel wrap width (readability)

Before rendering, narrow the boxes by injecting `skinparam wrapWidth` into each
exported `.puml`. This MUST happen after export and before render, and the
assembler places the directive after the **last** `!include <C4/...>` line — every
C4 sub-include re-emits the stock `wrapWidth 200`, so an earlier placement (or the
`plantuml.skinparams` view property) is silently clobbered.

```bash
# macOS/Linux (SKILL_DIR resolved as in Step 3f):
python "$SKILL_DIR/c4_assemble.py" . --inject-wrap-width <temp-dir>
```

This rewrites every `<temp-dir>/*.puml` in place (default 200px, matching C4's
stock wrap; override with `--wrap-width N`). Lower `--wrap-width` for narrower,
taller boxes.

#### 3d. Render PlantUML to SVG

**First, verify Graphviz is available to PlantUML** (the entire C4 pipeline needs
it — see "Graphviz Not Found" below). Gate on PlantUML's own check, NOT `dot -V`
or `which dot` (PlantUML resolves `dot` via its own search paths, not `$PATH`):

```bash
# macOS/Linux:
java -jar ~/.claude/tools/plantuml.jar -testdot
```

Exit 0 with "Installation seems OK. File generation OK" → proceed. Any other
result → see "Graphviz Not Found". Without `dot`, PlantUML does NOT fall back: it
emits a green "Cannot find Graphviz" placeholder SVG **with exit code 0**, which
`c4_assemble.py` will then reject (0 element nodes). Fix Graphviz, don't bypass.

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

# Or specify views explicitly (one --views flag, space-separated specs;
# repeating --views would clobber all but the last because it is nargs="*")
python "$SKILL_DIR/c4_assemble.py" /path/to/project --svg-dir /tmp/c4-render \
    --views "SystemContext:System Context:structurizr-SystemContext.svg" \
            "Containers:Containers:structurizr-Containers.svg"
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

### Graphviz Not Found — Installation Guidance

Graphviz (`dot`) is a **hard prerequisite on par with Java 21+**. The **entire** C4
pipeline — SystemContext, Containers, Component, Dynamic, and Deployment views, not
just Container/Component — routes through PlantUML's `dot`-based layout. Without it,
PlantUML silently emits a "Cannot find Graphviz" placeholder (exit code 0), which
the assembler rejects.

**Installation commands by platform:**

| Platform | Command |
|----------|---------|
| Windows | `winget install -e --id Graphviz.Graphviz` |
| macOS | `brew install graphviz` |
| Linux (Debian/Ubuntu) | `sudo apt install graphviz` |
| Linux (Fedora) | `sudo dnf install graphviz` |

After installing, confirm with `java -jar ~/.claude/tools/plantuml.jar -testdot`
(expect "Installation seems OK"). There is **no** `!pragma layout smetana` fallback
in this skill — Graphviz is required so checked-in diagrams keep full layout
fidelity.

### Checking whether an element actually rendered

Grepping the generated HTML for an element name is **not** a valid check. Three
ways it returns a confident wrong answer:

1. **The DSL panel embeds the entire `.dsl` source**, so every element name appears
   in the page whether or not it rendered. Match each tab panel to its own `<svg>`
   block first and search inside that block only.
2. **`wrapWidth` splits a label across several `<text>` elements**, one per word.
   Searching for `"StatsBomb Orchestrator"` returns zero hits on a diagram that
   renders it perfectly. Extract the `<text>` nodes of one SVG, collapse
   whitespace, and match against that.
3. **Collapsed text matches descriptions too**, not just element labels — one
   container's description mentioning another component is a false positive.

The authoritative roster is the per-panel `data-qualified-name` attribute list
(`_ENTITY_OPEN_RE` in `c4_assemble.py`), which names exactly the elements that
rendered as boxes. Cross-check against that, not against page text.

Because `hoist_text_styles` moves `fill`/`font-*` onto classes, do not grep for a
literal `font-family="sans-serif"` to find text either — match `<text` itself.

### Important notes

- Always save the `.dsl` file to disk first — the export pipeline reads from disk
- **The export and render steps each take longer than 30 s on Windows.** Some
  harnesses kill a foreground shell call at that threshold, which looks exactly
  like a toolchain failure. Background the call (or run it from PowerShell) rather
  than concluding Java or Graphviz is broken.
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

The viewer is **generated** by `c4_assemble.py` (the `TEMPLATE` string plus `build_html`), not hand-authored. `c4_assemble.py` is the single source of truth for the exact markup, CSS, and JS; this section describes the structure it emits so you can recognize and reason about the output. If you change the layout, change the template in `c4_assemble.py` and update this section — do not paste a competing copy here.

### Layout: two-level grouped tabs + breadcrumbs + drill-down

The old single row of flat pills was replaced by a two-level navigation that scales past ~6 views:

- **Group row** (`.grp` buttons, `role="tab"`) — top-level C4 levels in a fixed order (`GROUP_ORDER`): Context, Containers, Components, Dynamic, Deployment, then a synthetic **DSL** group. Clicking a group calls `c4ShowGroup(g)`, which activates that group's first view. Unrecognised keys sort after the canonical levels; `TAIL_GROUPS` (currently just `DSL`) then sorts *after those*, so the synthetic source panel is always the last tab rather than sliding mid-row whenever a bespoke key exists.
- **Sub-tab row** (`.subrow` / `.subtab`) — shown only for a group with **more than one** view (e.g. several split `Component_<container>` views under **Components**). A single-view group renders an empty `.subrow` placeholder and no sub-tabs. Sub-tab labels resolve in this order: an explicit `--views` label wins, then the container's DSL display name (via `build_view_labels`), then the raw key suffix. That ordering matters — auto-detection synthesizes a label from the view key, so letting *any* label win unconditionally would drop a Component tab from `Analytics & SAM` back to the bare suffix `analytics`.
- **Breadcrumbs** (`.breadcrumb`) — a Component panel shows `Context › Containers › <current>`; a Container panel shows `Context › <current>`. Crumbs are emitted only for ancestor views that actually rendered (`build_breadcrumbs` gates on the existing view keys), so a crumb never points at a missing panel.
- **Panels** (`.tab-content`, one per view + the DSL panel) — the active panel is shown; others are `display:none`. Each panel is focusable (`tabindex="-1"`) and focused on activation for keyboard users.

### View keys, tab ids, and grouping

- `parse_view_key(raw_key)` maps a Structurizr view key to `(group, sub_label)` — e.g. `SystemContext → (Context, "System Context")`, `Component_api → (Components, "api")`, `Containers_CI → (Containers, "CI")`. Both `_` and `-` work as the separator. Unknown keys become their own group, which is why a multi-system workspace must name its container views `Containers_<systemId>` (see "View-key naming convention").
- `view_key_to_tab_id(raw_key)` is the **single source of truth** for the DOM id / `data-tab` / `c4ShowTab('…')` argument: lowercase, `_→-`, strip to `[a-z0-9-]`. It is emitted **unescaped** into attribute and JS-string contexts, so it must be a safe slug. A degenerate key with no alphanumerics falls back to a stable `view-<hash>` id (never an empty id).
- **Tab order follows the DSL.** The five well-known views keep their fixed order; any project-specific view is then ordered by where its key appears in the DSL's `views` block, so a deliberately sequenced set of split views reads in the order the author wrote. Keys with no DSL declaration (and every key when the DSL fails to parse) fall back to filename order, so the result is deterministic either way. Ordering by filename alone was stable but arbitrary: it silently re-sorted a narrative into alphabetical order.
- The synthetic DSL panel reserves tab id `dsl` (see the `_DSL_VIEW` constant). Two guards warn instead of silently shadowing a panel: `find_tab_id_collisions` (run over the rendered views **plus** `_DSL_VIEW`) catches two *distinct* keys colliding on any id, and `find_reserved_id_shadow` catches a user view claiming a reserved id — including the exact `raw_key='DSL'` case that the collision check's per-id key-set would otherwise dedup away.

### Drill-down (click-through between levels)

`build_drilldown_map` maps each container's dotted alias to the Component view scoped to it; `wire_drilldown` attaches `role="button"`, `tabindex="0"`, keyboard handlers, and an `onclick="c4ShowTab('<component-tab>')"` to the matching entity `<g>` in the **container** SVG. Clickable boxes carry a persistent dashed outline (`.svg-container [role="button"]`) so they read as clickable without hovering. Only views that actually rendered a panel are wired (the injected `c4ShowTab` target can never dangle). Non-ASCII scope names, empty aliases, and whole-model alias collisions are skipped with a warning.

### JS runtime

Two embedded JSON maps drive navigation: `C4_TAB_GROUP` (tab id → group) and `C4_GROUP_TABS` (group → ordered tab ids). Both are emitted via `_json_for_script` (which `\uXXXX`-escapes `<`, `>`, `&` so a view key containing `</script>` cannot break out of the block). `c4ShowGroup` / `c4ShowTab` toggle the `active` class across groups, sub-rows, sub-tabs, and panels, and set `aria-selected`. The DSL panel's **Copy** button (`copyDSL`) uses `navigator.clipboard` with a `document.execCommand('copy')` fallback.

### Escaping contract (why several escapes differ)

- **Tab ids** — slugified by `view_key_to_tab_id`; safe in `id=`, `data-tab=`, `onclick=`, and as a JS map key.
- **Group `onclick` argument** — a group name flows into `onclick="c4ShowGroup('<g>')"`, a JS-string-inside-an-HTML-attribute. HTML-escaping is **wrong** there (the browser HTML-decodes `&#x27;` to `'` before the JS parser runs), so `_js_str_in_attr` emits `\uXXXX` for anything outside a conservative safe set. The `data-group=` attribute and visible text use ordinary `html.escape`.
- **System name, labels, breadcrumb text** — ordinary `html.escape` (plain HTML text/attribute context).
- **Embedded SVG** — cleaned by `clean_svg` (strips title/PI/active content) and verified by `verify_clean` before embedding; see *SVG Cleaning* in the `c4_assemble.py` docstring.

### Output size: hoisted `<text>` styling

PlantUML positions and justifies **every word individually**, emitting one `<text>`
element per word with the whole font stack repeated inline. On a dense multi-view
page that is thousands of `<text>` elements re-declaring the same handful of
attribute combinations, and it dominates the file: measured across real projects,
`<text>` markup ran to roughly 70% of the bytes.

Two passes cut that without changing a pixel:

- `clean_svg` drops `lengthAdjust="spacing"`. `spacing` **is** the SVG initial
  value, so the attribute is pure repetition (~12% of a page). It is matched on the
  value, never blanket-stripped — a real `lengthAdjust="spacingAndGlyphs"` survives.
- `hoist_text_styles` collects the CSS-inheritable presentation attributes
  (`fill`, `font-family`, `font-size`, `font-style`, `font-weight`, …) into
  generated `.c4tN` classes appended to the page's own `<style>` block. `x`, `y`
  and `textLength` stay inline because they are genuinely per-element.

Together these cut a typical page by **~35%** (1.16 MB → 0.74 MB on an 17-view
model), verified pixel-identical against the pre-change output.

Two constraints worth knowing before touching this code:

- **It must stay a document-wide pass, not a per-SVG one.** Every SVG is embedded
  in a single HTML document, so `.c4tN` names share one namespace; numbering per
  SVG would make the same class mean different things in different panels.
- **`lengthAdjust` cannot move into a class.** It is not a CSS property in SVG 1.1,
  and it is not inherited from a parent `<g>` either — which is why it is *dropped*
  when redundant rather than hoisted.
- **`verify_clean` cannot be re-run after the hoist.** The pipeline order is
  `clean_svg` → `verify_clean` → `wire_drilldown` → `hoist_text_styles`, and
  `wire_drilldown` deliberately injects the `onclick`/`onkeydown` handlers that
  make boxes clickable. `verify_clean` rejects `on*=` handlers by design — it
  guards PlantUML's *raw* output, before wiring — so re-verifying at the end would
  abort every build that has drill-down. The hoist instead checks its own
  invariant: angle-bracket counts per SVG must be unchanged, and a violation falls
  back to the un-hoisted SVGs with a `WARN`. The end-of-run sweep that *does*
  cover the final bytes is `verify_embedded_svgs` — see below.

### Final page verification

`verify_clean` guards each SVG as it comes off PlantUML, but two stages run after
it. `verify_embedded_svgs` therefore re-checks every embedded `<svg>` region **in
the form it actually ships**, and aborts the build on:

- a title element or `class="title"` group, a `<?plantuml` processing instruction,
  `<script>`, or `<foreignObject>`;
- an active-scheme href, matched on the **normalized** value (entities decoded,
  tabs/newlines stripped) so `jav&#x61;script:` cannot slip past a substring scan;
- any event handler outside the allowlist of what `wire_drilldown` itself injects
  — `onclick="c4ShowTab(…"` and `onkeydown="if(event.key===…"`. A correctly-named
  `onclick` with a foreign payload, an unquoted handler, and a `/`-separated
  `<rect/onload=…>` are all rejected.

Two scoping decisions worth not "fixing" later:

- **SVG regions, not the whole page.** The page's own chrome legitimately contains
  a head `<title>` and the inline `<script>` runtime. A whole-page scan for those
  is permanently red, and a check that always fails is a check nobody reads.
- **A raw hit is always a violation — never subtract escaped occurrences.** Every
  author-supplied string (DSL source, system name, labels) is html-escaped before
  it reaches the page, so the raw and escaped forms are disjoint. The predecessor
  subtracted one count from the other, which masked one real violation per escaped
  mention in the DSL panel.

The saving is in raw bytes, which is what matters for a file opened straight from
disk. Compressed, the same change is worth only ~6% (these pages gzip to about an
eighth of their size either way), so do not expect a proportional drop in repo size.

### Visual conventions (unchanged)

- **Pill tabs** on a dark page; the active group/sub-tab is filled (`#438DD5` / `#2a5a8a`).
- **Natural SVG size** inside a white card — no `max-width`/`width` scaling; `.svg-container` scrolls horizontally (`overflow-x:auto`) when the diagram is wider than the viewport.
- **DSL as its own group/panel**, not a permanent sidebar — the diagram view stays uncluttered and the full Structurizr workspace source is one click away, with a Copy button.
- **HTML entities for special characters** (`&mdash;`, `&rarr;`) — never literal Unicode, which can corrupt through shell/encoding chains.

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
- **Too many elements** — Keep each view to ~15 element boxes (`MAX_ELEMENTS_PER_VIEW`); split a dense system into per-container `Component_<id>` views (see "Readability & Navigation")
- **Missing descriptions** — Every element and relationship should have a meaningful description
- **No external systems** — Context diagrams must show what's OUTSIDE your system boundary
- **Skipping the technology tag** on containers/components — always specify (e.g., "React SPA", "PostgreSQL", "Spring Boot")
- **Adding descriptions to views** — Omit the description parameter on `systemContext`, `container`, `component`, `dynamic`, and `deployment` views. The exporter auto-generates a title from the view type and scope element. A description adds a redundant second line that overlaps with the auto-generated title.
- **Manual numbering in dynamic views** — Never prefix dynamic view descriptions with "1.", "2.", etc. Structurizr auto-numbers steps sequentially, so manual numbers produce duplicated labels like "3: 3. Extract text".
