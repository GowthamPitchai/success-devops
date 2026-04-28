# Class 2 - Azure Foundations & Governance

**Date:** 2026-04-28
**Status:** COMPLETE
**Cost incurred:** Rs.0
**Cost saved:** ~Rs.85/day (deleted runaway AKS cluster)

---

## What I built

| Item | Name / Value |
|------|--------------|
| Resource Group | `rg-shopwave-dev-eastus` |
| Location | `eastus` |
| Tags | `Owner=gowtham, Project=shopwave, Env=dev, CostCenter=learning, ManagedBy=manual` |
| Budget | `budget-shopwave-monthly` = Rs.2,000/month INR |
| Budget alerts | 50%, 80%, 100% to `gowthammurugaiyan94156@gmail.com` |
| Resource Lock | `lock-shopwave-dev-nodelete` (CanNotDelete) |

---

## Subscription details (always good to have handy)

- Subscription ID: `1ee36dd3-5126-42b3-b979-d28523f6e67e`
- Tenant ID: `92ed01cd-899d-4ad2-a0e8-17c161459fd3`
- Billing currency: **INR** (MCA - Invoice section model)
- Login: `gowthammurugaiyan94156@gmail.com`

---

## The 3 most important things I learned

1. **Azure hierarchy** = Tenant -> Subscription -> Resource Group -> Resource. Tenant holds identities, subscription pays bills, RG is a folder, resources are the things.
2. **CAF naming convention** = `<type>-<workload>-<env>-<region>-<instance>` so resources are self-documenting.
3. **5 mandatory tags** = Owner, Project, Env, CostCenter, ManagedBy - critical for FinOps cost allocation.

---

## Where I got stuck and how I escaped

1. **Old AKS cluster was running, costing Rs.85/day** -> stopped it (`az aks stop`), then deleted parent RG. The `MC_*` RG auto-cleared.
2. **Confused about USD vs INR in budget form** -> the form's "US$ suggested" hint was misleading; actual amount field used INR because my subscription is on MCA Invoice section model.
3. **`az lock list --output table` returned empty** -> known propagation quirk; verified via JSON output instead.

---

## The interview answer in 60 seconds

> "I followed Microsoft's CAF naming pattern with five mandatory tags - Owner, Project, Env, CostCenter, ManagedBy - then layered three controls. First, a CanNotDelete lock prevents accidental teardown. Second, a multi-tier budget alert at 50/80/100% gives graduated warnings. Third, the RG itself acts as a single-blast-radius cleanup unit. The currency model matters too - my subscription is MCA with an INR invoice section, so my budget is genuine INR, not converted-from-USD."

---

## What broke and how I fixed it

| Problem | Fix |
|---------|-----|
| AKS cluster running silently, burning ~Rs.85/day | `az aks stop` + `az group delete` of `devops-bootcamp-rg` |
| Forgot the `MC_*` resource group existed | Realized AKS auto-creates a sibling RG for worker nodes; gets cleaned up when parent RG is deleted |
| Portal UI didn't match my mental model | Used direct URL + verified via CLI for source-of-truth |

---

## What I'd do differently in production

- Use **Azure Policy** to ENFORCE the 5 mandatory tags - block resource creation without them
- Use **management groups** to apply policies across multiple subscriptions
- Codify the budget + lock + tags via **Terraform** (`azurerm_consumption_budget_subscription`, `azurerm_management_lock`) so they're reproducible
- Set up an **action group** that triggers an automation runbook at 100% threshold to auto-stop expensive resources (not just email)
- Use **separate subscriptions** for dev vs prod, not just RGs

---

## Interview Q&A I can now answer cold

1. Walk me through the Azure resource hierarchy
2. How do you prevent accidental RG deletion in production?
3. Difference between a tag and a resource group?
4. Why is my Key Vault name unavailable after I deleted it? (soft-delete, 90 days)
5. How do you stop someone from spending more than Rs.X in a subscription?
6. What's CAF naming convention?
7. Why does my Indian Azure subscription bill in USD vs INR? (MCA vs PAYG)

---

## Connection to next class

**Class 3 = Git Strategy.** Every file we write from here goes into a git repo with branch protection, PR workflow, and the right CI/CD hooks. The governance discipline I built today (naming, tagging, locks) carries into branch naming, commit message conventions, and PR titles.
