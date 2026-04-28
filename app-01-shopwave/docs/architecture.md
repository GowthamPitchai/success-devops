# ShopWave — Architecture (Beginner Edition)

> This file is your "what are we building?" reference.
> Open it any time you feel lost.

---

## 1. What is ShopWave?

ShopWave is a **mini Amazon** — an online shopping platform.
Users can browse products, add them to a cart, place orders, pay, and get email confirmations.

We're building it to learn **real-world DevOps on Azure**.

---

## 2. Why microservices? (the shop analogy)

Imagine a shop with one super-employee Raju who does everything (greeting, billing, packing, delivery, SMS).
That's a **monolith** — simple but fragile. If Raju is sick, the shop closes.

Instead, we hire **6 specialists**, each doing one job. That's **microservices**.

**Benefits:**
- If one specialist is busy, the others keep working
- We can hire 5 more catalog clerks if catalog is busy (scale only what's needed)
- Each specialist can be upgraded without disturbing others

---

## 3. The 6 services of ShopWave

| # | Service | Real-life role | What it does |
|---|---------|----------------|--------------|
| 1 | `frontend` | Shop's window display | Shows the website (HTML pages) you see in browser |
| 2 | `catalog-api` | Product catalog book | Knows all products, prices, descriptions |
| 3 | `cart-api` | Shopping basket | Tracks what each user is collecting |
| 4 | `orders-api` | Cashier | Saves placed orders permanently |
| 5 | `payments-worker` | Back-room money handler | Processes payments asynchronously (in background) |
| 6 | `notifier` | Shop boy who calls you | Sends confirmation emails/SMS |

**The customer journey:**
Browse (frontend) -> See products (catalog) -> Add to basket (cart) -> Checkout (orders) -> Payment processed (payments-worker) -> Get email (notifier).

---

## 4. Azure = the building blocks we rent

Each problem we have is solved by one Azure service. We don't memorize all of these now — each will be a class:

| Problem | Azure service | What it really is |
|---------|---------------|-------------------|
| Need computers to run services | **AKS** (Azure Kubernetes Service) | Rented computers managed automatically |
| Need permanent storage for orders | **Azure Database for PostgreSQL** | Like Excel that never loses data |
| Need fast temporary storage for carts | **Redis** | Super-fast notepad |
| Services need to send messages to each other | **Azure Service Bus** | A post office between services |
| Need a public web address | **NGINX Ingress + Public IP** | The shop's address on the internet |
| Need to store passwords safely | **Azure Key Vault** | A locker for secrets |
| Need to store our app packages | **Azure Container Registry (ACR)** | A shelf for app images |
| Need a worker that wakes only when needed | **Azure Functions** | Pay-per-use background worker |
| Need to know when something breaks | **Azure Monitor + App Insights** | CCTV + alarms for the system |
| Need auto-deploy when code changes | **Azure DevOps Pipelines** | Factory line: code in, app out |

---

## 5. The simple architecture picture (in words)

```
User in browser
   |
   | HTTPS (https://shopwave.com)
   v
NGINX Ingress (the shop's main door)
   |
   +--> frontend (shows webpage)
   +--> catalog-api (returns products)
   +--> cart-api  ----> Redis (cart storage)
   +--> orders-api ----> Postgres (order storage)
                  |
                  +--> Service Bus queue
                              |
                              v
                   payments-worker (processes money)
                              |
                              v
                  Service Bus topic "order-completed"
                              |
                              v
                       notifier Function
                              |
                       Email + SMS to user

Behind the scenes:
- Key Vault holds all secrets (DB password, queue keys, etc.)
- App Insights watches everything and alerts on problems
- ACR stores our packaged services
- Azure DevOps builds and deploys everything when we push code
```

---

## 6. The journey ahead (25 classes)

| Phase | Classes | What we learn |
|-------|---------|---------------|
| Foundation | 1-4 | Understanding, Azure setup, Git, local Docker |
| Containers | 5-7 | Docker, image security, ACR |
| Infrastructure | 8-11 | Terraform, AKS, networking |
| Kubernetes | 12-16 | Pods, services, ingress, secrets, RBAC |
| Reliability | 17-19 | Auto-scaling, surviving failures, databases |
| CI/CD | 20-22 | Pipelines, blue-green deploys, GitOps |
| Observability | 23-24 | Monitoring, dashboards, alerts |
| Mastery | 25 | Chaos engineering + interview prep |

We do **one class per session**. Each class is small. No drowning.

---

## 7. What I (the learner) understand after Class 1

- A monolith is one big program; microservices are many small programs working together
- ShopWave has 6 services with clear, single responsibilities
- Azure provides one building block per problem (compute, DB, queue, secrets, etc.)
- We will build it step by step over 25 classes, learning each Azure piece deeply

---

**Status: CLASS 1 COMPLETE.** Next: Class 2 -- Azure Subscription, Resource Groups, Naming, Tags, Locks, and Cost Alerts.
