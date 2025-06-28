# Afula

**Afula** is a microservices-based system for tracking and renovating Git repositories at scale.

It stores metadata about repositories in a database and coordinates renovation tasks using Kubernetes.

---

## 🧩 Architecture

- **PostgreSQL** – stores repository metadata
- **Manager**
- **Processor**
