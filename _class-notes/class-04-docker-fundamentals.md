# Class 4 — Docker Fundamentals (catalog-api)

> **Date:** April 28, 2026
> **Goal:** Containerize the first ShopWave microservice (`catalog-api`) and master the Docker workflow used in production at FAANG-grade companies.
> **Cost:** ₹0 (everything ran on local Docker Desktop)

---

## 1. Why Docker?

| Problem before Docker | How Docker fixes it |
|---|---|
| "Works on my machine" — different Python/OS/lib versions break apps in prod | Image bundles app + runtime + libs into one immutable artifact |
| VMs are heavy (full OS, GBs, slow boot) | Containers share host kernel — MBs, boot in ms |
| Ops manually installs apps on servers | `docker run image` — done. Same command everywhere. |
| Scaling = provisioning new VMs | Scaling = `docker run` 100 more containers |

**One-liner:** Docker is the standard unit of deployment in modern infra. Kubernetes, Azure Container Apps, AWS ECS — all run Docker images.

---

## 2. Mental Model

| Concept | Analogy |
|---|---|
| **Dockerfile** | Recipe (instructions) |
| **Image** | Frozen, ready-to-cook meal kit (immutable) |
| **Container** | The meal currently being eaten (running process) |
| **Registry (ACR/Docker Hub)** | The grocery store where meal kits are stored/shared |

One image → many containers. Containers are ephemeral; images are versioned.

---

## 3. The Dockerfile We Wrote

```dockerfile
# syntax=docker/dockerfile:1.7
FROM python:3.13-slim AS base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Line-by-line WHY

| Line | Why this, why here |
|---|---|
| `# syntax=docker/dockerfile:1.7` | Pins BuildKit syntax version → enables modern features (cache mounts, secrets) |
| `FROM python:3.13-slim AS base` | `slim` = ~150MB, balanced size vs compatibility. `AS base` = named stage for future multi-stage builds (Class 5) |
| `WORKDIR /app` | Sets default dir AND creates it. Better than `RUN mkdir + cd`. |
| `COPY requirements.txt .` BEFORE `COPY . .` | **Layer caching.** Deps change rarely; code changes constantly. Putting deps first means `pip install` cache survives code edits. |
| `RUN pip install --no-cache-dir` | `--no-cache-dir` skips pip's wheel cache → smaller image |
| `COPY . .` | Copies app code AFTER deps installed |
| `RUN useradd ... && chown` | Creates non-root user. Backslash + `&&` chains commands into ONE layer (smaller image) |
| `USER appuser` | All subsequent commands + the running container use this user. Defense in depth. |
| `EXPOSE 8000` | **Documentation only** — does NOT publish the port |
| `CMD [...]` (exec form) | JSON array = exec form → uvicorn runs as PID 1, signals propagate, `docker stop` works gracefully |

---

## 4. Alternatives Considered

| Choice | Alternative | Why we picked ours |
|---|---|---|
| `python:3.13-slim` | `python:3.13` (full) | Full = ~1GB, too big |
| `python:3.13-slim` | `python:3.13-alpine` | Alpine uses musl libc → many Python C-extension wheels break or recompile slowly |
| `python:3.13-slim` | `distroless` | Distroless is smaller + safer but harder to debug. We'll move there in Class 5. |
| Single-stage | Multi-stage | Multi-stage is for Class 5 — we wanted to nail single-stage first |
| `CMD` (exec form) | `CMD` (shell form) | Shell form runs via `/bin/sh -c` → signals don't propagate → `docker stop` waits 10s then kills |
| Non-root `appuser` | Default `root` | CIS Docker Benchmark 4.1 — never run as root |

---

## 5. Daily-driver commands

```powershell
# Build
docker build -t catalog-api:1.0.0 .

# Run (detached, named, port-mapped)
docker run -d --name catalog-api -p 8000:8000 catalog-api:1.0.0

# Inspect
docker ps                       # running
docker ps -a                    # all (including stopped)
docker images                   # list images
docker logs catalog-api         # logs
docker logs -f catalog-api      # follow logs
docker exec -it catalog-api /bin/bash   # shell inside container
docker inspect catalog-api      # full JSON metadata

# Lifecycle
docker stop catalog-api         # SIGTERM, then SIGKILL after 10s
docker start catalog-api
docker restart catalog-api
docker rm catalog-api           # delete container (must be stopped)
docker rmi catalog-api:1.0.0    # delete image
```

---

## 6. WHAT BREAKS HERE — Bugs I created and fixed

### Drill 1 — `127.0.0.1` vs `0.0.0.0` (the #1 trap)
- **Symptom:** `docker ps` shows container Up. Browser → "connection refused".
- **Diagnose:** `docker logs` showed `Uvicorn running on http://127.0.0.1:8000`.
- **Root cause:** `127.0.0.1` = loopback INSIDE the container only. `-p 8000:8000` forwards traffic to the container's network interface, not its loopback.
- **Fix:** Bind to `0.0.0.0` (all interfaces) inside containers. **Always.**

### Drill 2 — Layer caching speed
- Changed one product name. Rebuild took **~2 seconds** instead of ~30s.
- Build log showed `=> CACHED [base 4/6] RUN pip install` — the slow layer was reused.
- **Lesson:** Order Dockerfile instructions from least-changing (base, deps) to most-changing (app code).

### Drill 3 — Wrong port mapping
- Ran with `-p 9000:8000`. App still listened on 8000 internally; host now exposed it on 9000.
- **Lesson:** `-p HOST:CONTAINER`. Left = your laptop. Right = inside container. Same idea as K8s `Service.port` vs `targetPort`.

### Bonus — Backslash mid-line bug
- Original Dockerfile had `RUN useradd ... \ && chown ...` on one line.
- Backslash followed by space + `&&` is invalid → backslash escapes the space, breaks parser.
- **Fix:** `\` must be the LAST character on the line. Zero trailing whitespace.

---

## 7. Interview Q&A (memorize)

| Q | A |
|---|---|
| Image vs container? | Image = read-only template. Container = running instance. One→many. |
| Why slim, not full or alpine? | Slim = balanced ~150MB. Full too big. Alpine breaks many Python wheels (musl vs glibc). |
| CMD vs ENTRYPOINT? | CMD = default args, easy to override. ENTRYPOINT = fixed binary. Best practice: combine — ENTRYPOINT for the binary, CMD for default flags. |
| Exec form vs shell form? | Exec form (JSON array) → app is PID 1, signals work. Shell form → wrapped in /bin/sh, breaks `docker stop` graceful shutdown. |
| Why non-root user? | Container escape → attacker doesn't land as root on host. CIS Docker 4.1. |
| Why COPY requirements.txt first? | Layer caching. Deps change rarely; code constantly. |
| What does EXPOSE do? | Documentation + metadata for `docker run -P`. Does NOT publish ports. |
| What does .dockerignore do? | Excludes files from the build context sent to daemon. Smaller, faster, prevents secret leaks. |
| Why bind to 0.0.0.0 not 127.0.0.1 inside containers? | Loopback inside container is unreachable from host. Bind to all interfaces. |
| How is a container different from a VM? | VM virtualizes hardware (full guest OS). Container shares the host kernel (just isolated processes via namespaces + cgroups). |

---

## 8. CONNECT — How this maps to the rest of the curriculum

- **Class 5:** Multi-stage builds, distroless, Trivy scanning, cosign signing → makes this image production-grade
- **Class 7:** Push this image to ACR (Azure Container Registry)
- **Class 12-14:** Deploy this image to AKS via Kubernetes Deployment + Service
- **Class 20-22:** Build this image automatically in Azure DevOps pipelines on every commit

---

## 9. Verified Outcomes

- [x] Wrote Dockerfile from scratch
- [x] Built image with `docker build -t catalog-api:1.0.0 .`
- [x] Ran container with `-d --name -p`
- [x] Hit all 4 endpoints in browser successfully
- [x] Ran `docker logs`, `docker exec`, `docker stop`
- [x] Completed all 3 debugging drills
- [x] Understood layer caching (rebuild was seconds, not minutes)
- [x] Container ran as `appuser`, NOT root (verified inside `docker exec`)

---

## 10. Cost Check

- This entire class: **₹0** (local Docker Desktop)
- No Azure resources created in Class 4
- AKS still stopped, RG still has only the budget+lock from Class 2

---

**Status:** ✅ Class 4 complete. Ready for Class 5: Multi-stage builds, distroless images, Trivy scanning, image signing.
