# ft_quantum

Série de 5 exercices progressifs d'introduction à l'informatique quantique avec **Qiskit** et **IBM Quantum**.

## Prérequis

- Python ≥ 3.14
- [uv](https://github.com/astral-sh/uv)
- Un compte [IBM Quantum](https://quantum.ibm.com/) (requis à partir de ex02)

**Installation :**
```bash
uv sync
```

**Token IBM Quantum** (ex02, ex03, ex04) :
```bash
echo "IBM_QUANTUM_TOKEN=<votre_token>" > .env
```

---

## Vue d'ensemble

| Exercice | Concept | Qubits | Exécution |
|----------|---------|--------|-----------|
| [ex00](#ex00--superposition) | Superposition | 1 | Simulateur |
| [ex01](#ex01--intrication-état-de-bell) | Intrication (état de Bell) | 2 | Simulateur |
| [ex02](#ex02--simulateur-vs-vrai-qpu) | Simulateur vs QPU | 2 | Simulateur + QPU |
| [ex03](#ex03--algorithme-deutsch-jozsa) | Deutsch-Jozsa | 3 + 1 ancilla | QPU |
| [ex04](#ex04--algorithme-de-grover) | Grover | 4 | QPU |

---

## ex00 — Superposition

**Fichier :** [ex00/main.py](ex00/main.py)

Introduction à la superposition quantique avec la porte **Hadamard**.

```
|0⟩ ──H──M
```

La porte H transforme |0⟩ en |+⟩ = 1/√2 (|0⟩ + |1⟩).
En mesurant 500 fois, on observe environ 50 % de |0⟩ et 50 % de |1⟩.

```bash
uv run ex00/main.py
```

---

## ex01 — Intrication (état de Bell)

**Fichier :** [ex01/main.py](ex01/main.py)

Création d'un **état de Bell** Φ⁺ = 1/√2 (|00⟩ + |11⟩) via H + CNOT.

```
q0 ──H──●──M
q1 ──────X──M
```

Les deux qubits sont intriqués : mesurer l'un détermine instantanément l'état de l'autre.
On observe uniquement |00⟩ et |11⟩, jamais |01⟩ ni |10⟩.

```bash
uv run ex01/main.py
```

---

## ex02 — Simulateur vs vrai QPU

**Fichier :** [ex02/main.py](ex02/main.py)

Même circuit que ex01 (état de Bell), exécuté en **parallèle** sur :
- un simulateur d'état quantique (résultat idéal, sans bruit)
- un vrai QPU IBM (résultat bruité, avec erreurs de portes et de mesure)

L'histogramme comparatif met en évidence le **bruit quantique** : de petites probabilités parasites apparaissent sur |01⟩ et |10⟩.

```bash
uv run ex02/main.py
```

---

## ex03 — Algorithme Deutsch-Jozsa

**Fichier :** [ex03/main.py](ex03/main.py)

L'algorithme de **Deutsch-Jozsa** détermine en **un seul appel** si une fonction booléenne f : {0,1}³ → {0,1} est *constante* ou *balancée*, là où un algorithme classique nécessiterait jusqu'à 2ⁿ⁻¹ + 1 appels.

**Circuit (3 qubits d'entrée + 1 ancilla) :**
```
|0⟩ ──H──[U_f]──H──M
|0⟩ ──H──[U_f]──H──M
|0⟩ ──H──[U_f]──H──M
|1⟩ ──H──[U_f]──────
```

**Interprétation de la mesure :**
- `|000⟩` → f est **constante**
- tout autre résultat → f est **balancée**

**Oracles testés :**

| Oracle | Type | f(x) |
|--------|------|-------|
| `constant_0` | Constant | 0 pour tout x |
| `constant_1` | Constant | 1 pour tout x |
| `balanced_q0` | Balancé | x₀ |
| `balanced_q1` | Balancé | x₁ |
| `balanced_xor` | Balancé | x₀ XOR x₁ |
| `balanced_parity` | Balancé | x̄₀ XOR x̄₁ XOR x̄₂ |

```bash
uv run ex03/main.py
```

---

## ex04 — Algorithme de Grover

**Fichier :** [ex04/main.py](ex04/main.py) · [ex04/README.md](ex04/README.md)

L'algorithme de **Grover** retrouve un élément marqué dans un espace de N = 2ⁿ états en **O(√N)** itérations (contre O(N) classiquement).

**Circuit (4 qubits, 3 itérations) :**
```
|0⟩ ──H──[Oracle]──[Diffuseur]── × 3 ──M
|0⟩ ──H──[Oracle]──[Diffuseur]── × 3 ──M
|0⟩ ──H──[Oracle]──[Diffuseur]── × 3 ──M
|0⟩ ──H──[Oracle]──[Diffuseur]── × 3 ──M
```

Le nombre optimal d'itérations est ⌊π/4 · √N⌋ = 3 pour N = 16.

**Oracles testés :**

| Oracle | État cible | Valeur |
|--------|------------|--------|
| `oracle_101` | \|0101⟩ | 5 |
| `oracle_011` | \|0011⟩ | 3 |
| `oracle_000` | \|0000⟩ | 0 |
| `oracle_110` | \|0110⟩ | 6 |

```bash
uv run ex04/main.py
```

---

## Dépendances

| Paquet | Usage |
|--------|-------|
| `qiskit` | Construction et simulation des circuits quantiques |
| `qiskit-ibm-runtime` | Connexion et exécution sur les QPU IBM |
| `matplotlib` | Visualisation des histogrammes |
| `python-dotenv` | Chargement du token depuis `.env` |
