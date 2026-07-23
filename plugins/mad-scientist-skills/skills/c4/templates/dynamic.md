# Dynamic Diagram Template (C4 Supplementary) — Structurizr DSL

Shows a **specific interaction flow** between elements over time, with numbered steps. This is the diagram you use during design reviews, incident post-mortems, and when explaining "how does X actually work end-to-end?"

## Purpose

Answer: "What happens when a user does [specific action]? What's the sequence of calls across the system?"

## Architect's checklist

Before building this diagram, identify:

- [ ] **The scenario** — One specific user action or system event (e.g., "User places an order")
- [ ] **The trigger** — Who/what initiates the flow?
- [ ] **The participants** — Which elements (from any C4 level) are involved?
- [ ] **The steps** — Ordered sequence of interactions
- [ ] **The data** — What payload/information moves at each step?
- [ ] **Happy path first** — Document the success case. Error paths can be separate diagrams.

## Layout

```
+--------------------------------------------------+
|  Tab bar: [Context] [Container] ... [Dynamic*]    |
+--------------------------------------------------+
|                                                    |
|  Scenario: "User Places an Order"                  |
|                                                    |
|  +------+  1. POST /orders  +----------+           |
|  | User |------------------>| Web App  |           |
|  +------+                   +----------+           |
|                                  |                  |
|                        2. POST   |                  |
|                        /api/order|                  |
|                                  v                  |
|                             +----------+            |
|                             | API      |            |
|                             +----------+            |
|                              |    |    |            |
|                    3. INSERT |    |    | 5. publish  |
|                              v    |    v            |
|                     +------+ | +--------+           |
|                     |  DB  | | | Queue  |           |
|                     +------+ | +--------+           |
|                              |      |               |
|                   4. validate|      | 6. consume    |
|                              v      v               |
|                         +------+ +--------+         |
|                         | Auth | | Worker |         |
|                         +------+ +--------+         |
|                                      |              |
|                             7. send  |              |
|                                      v              |
|                                 +--------+          |
|                                 | Email  |          |
|                                 +--------+          |
|                                                    |
+--------------------------------------------------+
|  Structurizr DSL Source                    [Copy]  |
+--------------------------------------------------+
```

## Structurizr DSL syntax for this level

```
workspace "System Name" "Dynamic diagram" {

    model {
        user = person "End User" "Customer placing an order"

        system = softwareSystem "System Name" "Order management" {
            spa = container "Web App" "Browser-based UI" "React"
            api = container "API Service" "Order processing logic" "Node.js"
            db = container "Database" "Order and product data" "PostgreSQL" "Database"
            queue = container "Message Queue" "Async job transport" "RabbitMQ" "Queue"
            worker = container "Background Worker" "Processes async tasks" "Node.js"
        }

        idp = softwareSystem "Auth Provider" "Auth0" "External"
        email = softwareSystem "Email Service" "Sendgrid" "External"
    }

    views {
        dynamic system "Dynamic_PlaceOrder" "User Places an Order" {
            user -> spa "Submits order form"
            spa -> api "POST /api/orders with cart payload"
            api -> idp "Validates auth token"
            api -> db "INSERT order + line items"
            api -> queue "Publish OrderCreated event"
            worker -> queue "Consume OrderCreated event"
            worker -> email "Send confirmation email"
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
            element "Queue" {
                shape Pipe
            }
            relationship "Relationship" {
                color #707070
            }
        }
    }

}
```

**Note:** In Structurizr DSL dynamic views, relationships are automatically numbered in the order they appear. The sequence of relationship declarations defines the flow order. The scope (here `system`) determines which elements can participate.

### Dynamic view scoping

| Scope | Elements available | Use when |
|-------|-------------------|----------|
| `<softwareSystem>` | Containers of that system + external | Cross-container flows within a system |
| `<container>` | Components of that container + external | Internal flow within a single container |
| `*` | Any element in the model | Cross-system flows |

Example with container scope (component-level flow):

```
dynamic api "Dynamic_AuthFlow" "Authentication Flow" {
    authMw -> idp "Validates JWT token"
    authMw -> userCtrl "Passes authenticated request"
    userCtrl -> userSvc "Delegates to service layer"
    userSvc -> userRepo "Queries user data"
    userRepo -> db "SELECT user WHERE id = ?"
    autoLayout
}
```

## Best practices for Dynamic diagrams

| Practice | Why |
|----------|-----|
| **One scenario per diagram** | "User logs in" and "User places order" are separate diagrams |
| **Name the scenario in the view description** | `"User Places an Order"` — makes intent clear |
| **Relationship labels describe the action + data** | "POST /api/orders with cart payload" not "sends request" |
| **Order matters** | Relationship declaration order = step numbering. Put them in chronological sequence. |
| **Include the protocol** | Shows how the interaction actually happens |
| **Choose the right scope** | Use system scope for container interactions, container scope for component interactions |
| **Keep to 5-12 steps** | More becomes unreadable. Split complex flows into sub-scenarios. |

## Scenario selection guide

Good scenarios to diagram dynamically:

| Category | Examples |
|----------|---------|
| **Core user journeys** | Login, signup, place order, make payment |
| **Integration flows** | Webhook received, file import processed, external sync |
| **Async processing** | Job queued -> processed -> notification sent |
| **Error/recovery** | Payment fails -> retry -> dead letter -> alert |
| **Security-critical** | Token refresh, permission escalation, data export |

## Step labeling format

Each relationship label should follow this pattern:

```
[HTTP method + endpoint] OR [action] + [data description]
```

| Bad | Good |
|-----|------|
| "Sends request" | "POST /api/orders with cart items" |
| "Reads data" | "SELECT orders WHERE user_id = ?" |
| "Publishes" | "Publish OrderCreated event {orderId, items, total}" |
| "Notifies" | "Send order confirmation email with receipt PDF" |

## Anti-patterns to avoid

- **Showing all flows in one diagram** — Each diagram is ONE scenario. Create multiple dynamic views.
- **Vague data descriptions** — "Sends data" tells nothing. Name the endpoint, event, or query.
- **Including error handling in happy path** — Diagram the happy path first. Separate error paths.
- **Too many participants** — If you have 15+ elements, the flow is too complex for one diagram. Decompose.
- **Wrong scope** — Using `*` scope when `system` scope would be cleaner. Match the scope to the level of detail needed.
