# ex04 — Algorithme de Grover

Implémentation de l'**algorithme de recherche de Grover** sur un vrai QPU IBM Quantum.

## Principe

L'algorithme de Grover permet de trouver un élément marqué dans une base de données non triée de **N = 2ⁿ** états en **O(√N)** itérations, contre O(N) classiquement.

Il repose sur deux opérateurs appliqués en alternance :

| Opérateur | Rôle |
|-----------|------|
| **Oracle U_ω** | Inverse la phase de l'état cible : U_ω\|ω⟩ = −\|ω⟩ |
| **Diffuseur** | Amplification d'amplitude : 2\|ψ⟩⟨ψ\| − I |

Après **⌊π/4 · √N⌋** itérations, la probabilité de mesurer l'état cible est maximale.

## Structure du circuit

```
|0⟩ ──H──[Oracle]──[Diffuseur]── × n_iters ──M
|0⟩ ──H──[Oracle]──[Diffuseur]── × n_iters ──M
...
```

**Étapes :**
1. **Superposition uniforme** — H⊗ⁿ\|0⟩ crée l'état \|ψ⟩ = 1/√N Σ\|x⟩
2. **Oracle** — inverse de phase de \|ω⟩ (X sur les bits à 0, MCZ, X inverse)
3. **Diffuseur** — H·X·MCZ·X·H (réflexion par rapport à \|ψ⟩)
4. **Mesure** — les n qubits d'entrée

## Paramètres

| Constante | Valeur par défaut | Description |
|-----------|-------------------|-------------|
| `N_INPUT` | `4` | Nombre de qubits de recherche (espace de 2⁴ = 16 états) |
| `N_ITERS` | `⌊π/4 · √16⌋ = 3` | Nombre optimal d'itérations |

## Oracles prédéfinis

| Oracle | État cible | Valeur décimale |
|--------|------------|-----------------|
| `oracle_101` | \|0101⟩ | 5 |
| `oracle_011` | \|0011⟩ | 3 |
| `oracle_000` | \|0000⟩ | 0 |
| `oracle_110` | \|0110⟩ | 6 |

> **Ajouter un oracle** : `make_oracle(target)` génère l'oracle pour n'importe quel entier `target` dans [0, 2^N_INPUT − 1].

## Fonctions clés

### `make_oracle(target: int) → Callable`
Retourne une fonction oracle qui marque `|target⟩` par inversion de phase.
Algorithme : transforme `|target⟩` en `|11...1⟩` via des portes X sur les bits à 0, applique un flip multi-contrôlé, puis inverse la transformation.

### `build_grover_circuit(oracle_fn, n_iterations) → QuantumCircuit`
Construit le circuit de Grover complet sur `N_INPUT` qubits avec le nombre d'itérations spécifié.

### `run_real_hardware(circuits, shots=500) → list[dict]`
Envoie tous les circuits en un **seul batch job** sur le QPU IBM le moins occupé disposant d'au moins `N_INPUT` qubits.
Nécessite `IBM_QUANTUM_TOKEN` dans `.env`.

### `interpret(counts: dict) → str`
Retourne l'état dominant sous la forme `|1010⟩ (=10, 87%)`.

## Prérequis

```bash
# Variable d'environnement
IBM_QUANTUM_TOKEN=<votre_token>   # dans .env ou l'environnement
```

## Exécution

```bash
uv run ex04/main.py
```

**Sortie attendue :**
```
Grover — 4 qubits (N=16 états), 3 itération(s)

--- Vrai QPU ---
  target |101⟩=5        → |0101⟩ (=5, 91%)  {'0101': 455, ...}
  target |011⟩=3        → |0011⟩ (=3, 89%)  {'0011': 445, ...}
  ...

Figure sauvegardée dans figure.png
```

## Résultat

Un histogramme par oracle est sauvegardé dans `figure.png`.
L'état cible doit ressortir avec une probabilité proche de 1 après le nombre optimal d'itérations.
