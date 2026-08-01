workspace "Spike System" "Probe data-qualified-name and wrapWidth behavior" {

    model {
        user = person "End User" "A person who places orders through the storefront"

        system = softwareSystem "Order Platform" "Handles orders end to end" {
            web = container "Web App" "Delivers the storefront UI to the browser over HTTPS with server side rendering and a very long description to test how the pixel wrap width setting narrows this particular box when the text would otherwise render as one extremely wide single line" "React, TypeScript"
            api = container "API Service" "Handles business logic and exposes REST endpoints" "Node.js, Express" {
                authMw = component "Auth Middleware" "Validates JWT tokens on every inbound request" "Express Middleware"
                orderCtrl = component "Order Controller" "Handles /api/orders/* routes" "Express Router"
                orderSvc = component "Order Service" "Business logic for orders" "TypeScript Class"
            }
            db = container "Database" "Stores users, orders, and products" "PostgreSQL 15" "Database"
        }

        email = softwareSystem "Email Service" "Sends transactional email" "External"

        user -> web "Uses" "HTTPS"
        web -> api "Makes API calls to" "HTTPS/JSON"
        api -> db "Reads from and writes to" "SQL/TCP"
        system -> email "Sends notifications via" "SMTP/API"
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

        component api "Component_api" {
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
