# Pedagogical Scaffolding Reference

## Purpose

Answer: "Does this documentation teach effectively, or does it merely present information?"

## Pre-audit checklist

Before auditing, identify:

- [ ] The reader's expected prior knowledge for each document
- [ ] Which documents are procedural (tutorials, how-tos) vs. reference
- [ ] Whether verification commands exist after complex procedures
- [ ] The reading order assumed by the documentation

Documentation that merely describes a system is an encyclopedia. Documentation that teaches is a curriculum. This template provides frameworks from instructional design research to audit whether documentation builds competence or just transfers text.

## Carroll's Minimalism (1990)

John Carroll's minimalist instruction theory (MIT Press, 1990) emerged from studying how people actually learn software — they skip ahead, try things, ignore manuals. Effective documentation works WITH this behavior instead of fighting it.

### Principle 1: Immediate Meaningful Tasks

**Statement**: Get the reader doing real work immediately. People learn by doing, not by reading about doing.

**Documentation interpretation**: The first section of any guide should produce a visible, meaningful result. Not "understanding the architecture" — actually running something, seeing output, creating a resource.

**Audit question**: How many paragraphs appear before the first actionable step? If the answer is more than two, the document front-loads theory over practice.

### Principle 2: Minimize Passive Instruction

**Statement**: Cut preamble before action. Every sentence of explanation that precedes an action step is a sentence the reader will skip.

**Documentation interpretation**: Explanation should follow action, not precede it. "Run this command. Here's what it does" outperforms "This command does X. Now run it." Readers who have just seen the output are primed to understand the explanation.

**Audit question**: What percentage of the document is explanation vs. action? If explanation exceeds 60% in a tutorial or guide, the balance is wrong. (Reference documentation is exempt — its purpose IS explanation.)

### Principle 3: Error Recognition and Recovery

**Statement**: Anticipate failures and guide recovery. Users will encounter errors. Documentation that pretends they won't is documentation that abandons users at the moment they need help most.

**Documentation interpretation**: Every step that can fail should say what failure looks like and what to do about it. "If you see `ECONNREFUSED`, the database isn't running — start it with `docker compose up -d db`." This is not optional polish; it is core content.

**Audit question**: Are common errors documented? Is there a troubleshooting section? For each step that involves external dependencies (network, database, filesystem), is the failure mode addressed?

### Principle 4: Self-Contained Modules

**Statement**: Each section should be usable independently. Readers arrive via search, links, and bookmarks — not by reading from page one.

**Documentation interpretation**: Every section should establish its own context. If Section 5 requires state from Section 3, it must say so explicitly: "This section assumes you have a running database (see Section 3: Database Setup)." A reader who lands on Section 5 from a Google search should know immediately what they need.

**Audit question**: Can a reader land on any section via search and understand it without reading from the beginning? Pick three sections at random — do they stand alone?

## Cognitive Load Theory (Sweller 1988)

John Sweller's cognitive load theory (published in *Cognitive Science*, 1988) identifies three types of cognitive load. Documentation design directly controls two of them.

### Three-Type Taxonomy

| Load Type | Source | Documentation Design Implication |
|-----------|--------|----------------------------------|
| **Intrinsic load** | Domain complexity — inherent to the subject matter | Cannot reduce. Scaffold with progressive disclosure: simple cases first, edge cases later. Break complex topics into sequential sections that each introduce one concept. |
| **Extraneous load** | Poor design — imposed by the documentation itself | **ELIMINATE.** This is the audit's primary target. Sources: split attention (code here, explanation there), redundancy (saying the same thing three ways), lack of structure (wall of text with no headings), inconsistent formatting, jargon without definition. |
| **Germane load** | Productive learning — effort spent building mental models | **MAXIMIZE.** Consistent patterns across docs (every API endpoint documented the same way), worked examples that connect to prior knowledge, explicit connections between concepts ("this uses the same retry pattern from Chapter 3"). |

### Split-Attention Effect (Chandler & Sweller 1992)

Split attention occurs when the reader must mentally integrate information from physically separated sources. This is the single most common pedagogical failure in technical documentation.

**Anti-patterns**:
- Code block on page, explanation in a separate paragraph 3 screens away
- Diagram with numbered labels, legend on a different page
- Configuration file shown in full, individual settings explained in a separate table below the fold
- "See Appendix B for parameter descriptions" next to a function call with 6 arguments

**Fixes**:
- Inline code comments for complex blocks
- Adjacent annotations — explanation directly above or below each code section
- Integrated explanation — interleave code and prose in alternating blocks
- Self-contained diagrams with labels and explanations embedded

**Audit check**: For each code block longer than 5 lines, is the explanation within visual proximity (immediately before, after, or via inline comments)? If the reader must scroll to connect code to its explanation, this is a split-attention violation.

### Guidance Fading Effect (Sweller)

The appropriate level of scaffolding depends on reader expertise. Documentation must calibrate its support level correctly.

| Audience Level | Scaffolding Style | Documentation Pattern | Example |
|---------------|-------------------|----------------------|---------|
| **Novice** | Explicit step-by-step with verification at each stage | Every command shown, every output verified, every decision explained | "Run this command. You should see this output. If you see X instead, do Y." |
| **Intermediate** | Guided examples with some open-ended elements | Key steps shown, peripheral decisions left to reader | "Configure the retry policy. See the reference for available options." |
| **Expert** | Reference-style, minimal scaffolding | API signatures, configuration tables, terse descriptions | `retry(max_attempts=3, backoff=exponential)` — no walkthrough needed |

**Anti-pattern**: A tutorial that says "explore the API" for first-time users. This applies expert-mode scaffolding to novices. Novices don't know what to explore, what's important, or what's safe to ignore.

### Expertise Reversal Effect

Scaffolding that helps novices actively hurts experts by adding extraneous load. Step-by-step instructions that orient a beginner are noise to an expert who just wants the API signature.

**Implication**: The same document cannot optimally serve both novices and experts. The solution is either:
1. **Separate paths**: "New to X? Start with the Tutorial. Already familiar? Jump to the API Reference."
2. **Progressive disclosure**: Collapsible detail sections, tabbed interfaces (Beginner / Advanced), expandable "Why?" blocks.

**Audit check**: Does the documentation identify its target audience? If it tries to serve everyone, does it use progressive disclosure to avoid the expertise reversal trap?

## Merrill's First Principles of Instruction (2002)

David Merrill's synthesis (published in *Educational Technology Research and Development*, 2002) distilled decades of instructional design research into five principles. Each maps directly to a documentation audit check.

### Principle 1: Task-Centered

**Principle**: Learning is promoted when learners are engaged in solving real-world problems.

**Audit check**: Is the documentation organized around user problems (what they want to accomplish), not system features (how the code is structured)?

**Anti-pattern**: Documentation structured by module, class, or file rather than by what users want to accomplish. A "Database Module" page that describes every method alphabetically instead of a "Storing and Retrieving Data" guide that walks through common workflows.

### Principle 2: Activation

**Principle**: Learning is promoted when existing knowledge is activated as a foundation for new knowledge.

**Audit check**: Does the documentation connect to what the reader already knows? Does it use analogies, comparisons, or references to familiar tools?

**Anti-pattern**: Introducing a completely novel concept without anchoring it. Compare: "The middleware pipeline processes requests sequentially" (meaningless to a newcomer) vs. "If you've used Express.js, this will be familiar — the middleware pattern works the same way. Each function receives the request, can modify it, and passes it to the next handler."

### Principle 3: Demonstration

**Principle**: Learning is promoted when new knowledge is demonstrated to the learner, not just described.

**Audit check**: Are worked examples provided (not just described)? Does the reader see concrete instances, not just abstract rules?

**Anti-pattern**: "You can use the retry decorator to add retry logic to any function." This describes the capability without demonstrating it. The reader still doesn't know the syntax, the import, the parameters, or what the output looks like.

### Principle 4: Application

**Principle**: Learning is promoted when new knowledge is applied by the learner.

**Audit check**: Is the reader required to produce output? Does the documentation include exercises, challenges, or "try it yourself" sections?

**Anti-pattern**: A tutorial with no exercises — only "read and observe." The reader follows along passively, finishes the tutorial, and cannot reproduce what they read because they never practiced.

### Principle 5: Integration

**Principle**: Learning is promoted when new knowledge is integrated into the learner's world.

**Audit check**: Does the documentation help connect new knowledge to existing practice? Does it show where this fits in the larger workflow?

**Anti-pattern**: A guide that ends abruptly after the last step. Compare: "Done." vs. "Now that you've set up CI, consider adding the linting step from the Contributing Guide. You can also configure Slack notifications — see the Integrations page."

## Lemov Content Quality Techniques

Doug Lemov's techniques (adapted from classroom instruction to documentation authoring) provide concrete, assessable quality criteria. Each technique below includes a deficient and exemplar annotated work sample.

### Begin with the End (4 Ms)

Effective documentation states measurable outcomes up front so the reader knows what they will be able to DO, not just what they will read ABOUT.

**Deficient**:
> This guide covers authentication.

Diagnosis: Vague scope. Not measurable. The reader cannot tell what they will be able to do after reading, nor whether they've succeeded. "Covers" is a document-centric verb (what the doc does), not a learner-centric verb (what the reader can do).

**Exemplar**:
> After completing this guide, you will be able to: (1) authenticate API requests using OAuth 2.0 tokens, (2) implement token refresh to maintain long-lived sessions, and (3) handle authentication errors gracefully with user-facing messages.

Diagnosis: Manageable scope (three specific outcomes). Measurable (each can be verified). Made of the most important concepts (OAuth flow, refresh, error handling). Stated first so the reader can decide immediately if this is the right document.

### Knowledge Organizers (#5)

Prerequisites and required context must appear BEFORE the reader encounters them, not inline when it's too late.

**Deficient**:
> Step 7 of a 10-step tutorial: "You'll need Redis installed and running on port 6379."

Diagnosis: The reader is 70% through the tutorial before discovering a hard dependency. They must now stop, install Redis, configure it, verify it, and try to find their place again. Every prerequisite discovered mid-tutorial is a context switch that damages learning.

**Exemplar**:
> **Prerequisites** — Before you begin, ensure you have:
> - Python 3.9+ (`python --version` — must show 3.9 or higher)
> - Redis 6.0+ running on port 6379 (`redis-cli ping` — must respond `PONG`; see [Installing Redis](./installing-redis.md) if needed)
> - A GitHub account with admin access to the target repository

Diagnosis: All dependencies surfaced before step 1. Each includes a verification command so the reader can confirm readiness. The Redis prerequisite links to setup instructions for readers who don't have it yet.

### Take the Steps / Guidance Fading (#21)

Complex operations must be decomposed into individual, verifiable steps. Each step should produce observable output the reader can check.

**Deficient**:
> Configure the database connection and set up migrations.

Diagnosis: Two complex operations compressed into one sentence. No indication of what "configure" means (which file? what values?). No verification — the reader has no way to know if they succeeded before moving on. When step 4 fails, they can't tell if the problem is in the connection or the migration.

**Exemplar**:
> **Step 1: Create the database configuration file.**
> Copy the following into `config/database.yml`:
> ```yaml
> development:
>   adapter: postgresql
>   host: localhost
>   port: 5432
>   database: myapp_dev
>   username: admin
>   password: <%= ENV['DB_PASSWORD'] %>
> ```
>
> **Step 2: Verify the connection.**
> Run: `rails db:ping`
> You should see: `Database connection successful.`
> If you see `FATAL: role "admin" does not exist`, create the role: `createuser -s admin`
>
> **Step 3: Run the initial migration.**
> Run: `rails db:migrate`
> You should see: `Migrated 3 files successfully.`

Diagnosis: Each step is atomic (one action). Each has explicit expected output ("You should see..."). Step 2 includes error recovery for the most common failure. The reader can verify success at each checkpoint.

### Retrieval Practice / Elaborative Hooks (#7)

Effective documentation connects new content to previously encountered concepts and adjacent guides, reinforcing learning and building a knowledge graph.

**Deficient**:
> Procedure lists steps 1 through 8 with no connection to concepts, related guides, or the reader's prior experience. Each step exists in isolation.

Diagnosis: The reader completes the procedure but builds no mental model. They can follow the steps but cannot adapt them, debug them, or explain them. The documentation is a recipe without culinary understanding.

**Exemplar**:
> This uses the same connection pooling pattern described in the [Database Setup guide](./database-setup.md#connection-pooling). If your pool size seems too small under load, see [Tuning Connection Pools](./tuning-pools.md) for the calculation method.
>
> **Why 10 connections?** This default assumes 4 web workers with 2 threads each, plus 2 for background jobs. If you changed your worker count in the previous section, adjust this proportionally.

Diagnosis: Links to prior learning (Database Setup guide). Provides a "why" explanation that connects the specific value to the reader's own configuration. Offers a path to deeper understanding (Tuning Connection Pools) without requiring it.

### Right Is Right (#16)

Technical documentation must be precisely correct. Approximations, vague descriptions, and "close enough" statements cause bugs in production.

**Deficient**:
> The function returns a list of objects.

Diagnosis: Rounds up — what type of objects? Ordered how? How many? What happens when there are no results? What happens when there are too many? Every ambiguity in this sentence is a potential production bug.

**Exemplar**:
> Returns a `List[User]` ordered by `created_at` descending. Maximum 100 items per page (configure via `page_size` parameter, range 1–500). Returns an empty list `[]` (not `None`) when no results match the query. Raises `ValueError` if `page_size` is outside the valid range.

Diagnosis: Precise return type (`List[User]`). Explicit ordering. Documented limits with configuration option. Empty-case behavior stated (prevents `NoneType` errors). Error behavior documented. A developer can write correct calling code from this description alone.

## Worked Example Quality Assessment

Not all examples serve the same purpose. The type of example must match the complexity and structure of the task being taught.

| Example Type | When Required | Audit Check | Anti-Pattern |
|-------------|---------------|-------------|-------------|
| **Product-oriented** (shows final result only) | Simple, well-structured tasks with clear correct answers. Configuration files, API calls with expected responses, template usage. | Does the reader need to understand WHY, or just WHAT? If just what, product-oriented is sufficient. | Using product-oriented examples for architectural decisions — showing the final `docker-compose.yml` without explaining why services are structured that way. |
| **Process-oriented** (shows reasoning + decisions) | Complex, ill-structured tasks with multiple valid approaches. System design, debugging workflows, migration strategies. | Does the example narrate the decision process? Does it explain rejected alternatives? | Code dump without explanation of choices — a complete Terraform module with no commentary on why these instance types, these availability zones, these scaling thresholds. |

**Audit rule**: If a task has multiple valid solutions, the example MUST be process-oriented. Showing only the final answer for a decision-rich task teaches the reader to copy without understanding.

## Verification Command Checklist

Every procedural step that changes system state should include a verification command. The reader should never have to guess whether a step succeeded.

| Technology | Verification Pattern | Example |
|-----------|---------------------|---------|
| **Web server** | HTTP request with expected status and body snippet | `curl -s http://localhost:3000/health \| jq .status` should return `"ok"` |
| **Database** | Query with expected result | `psql -U admin -c "SELECT count(*) FROM users"` should return `(1 row)` |
| **Container** | Process check with expected state | `docker ps --filter name=app` should show `STATUS: Up 30 seconds (healthy)` |
| **API endpoint** | Authenticated request with response body | `curl -H "Authorization: Bearer $TOKEN" https://api.example.com/me` should return `{"id": 1, "email": "..."}` |
| **Config file** | Validation command with expected output | `nginx -t` should return `syntax is ok` |
| **Build** | Build command with expected artifacts | `npm run build` should produce `Successfully compiled 42 modules` |
| **General** | Any step that modifies state | "You should see..." followed by the specific expected output. If the output is variable, specify the invariant: "You should see a UUID (36 characters, format `xxxxxxxx-xxxx-...`)." |

**Audit rule**: For every step in a tutorial or guide, ask: "If this step failed silently, would the reader know?" If the answer is no, a verification command is missing.
