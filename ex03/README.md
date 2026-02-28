# ex03 — Algorithme Deutsch-Jozsa

L'algorithme de **Deutsch-Jozsa** détermine en **un seul appel** si une fonction booléenne est constante ou balancée — là où un algorithme classique nécessiterait jusqu'à 2ⁿ⁻¹ + 1 appels.

## Principe

Soit f : {0,1}ⁿ → {0,1}. On garantit que f est soit :
- **Constante** : f(x) = 0 pour tout x, ou f(x) = 1 pour tout x
- **Balancée** : f retourne 0 pour exactement la moitié des entrées, 1 pour l'autre moitié

L'algorithme exploite l'**interférence quantique** : en superposant toutes les entrées simultanément, les amplitudes s'annulent ou se renforcent de façon à révéler la nature de f en une seule mesure.

## Circuit

```
|0⟩ ──H──[U_f]──H──M
|0⟩ ──H──[U_f]──H──M
|0⟩ ──H──[U_f]──H──M
|1⟩ ──H──[U_f]──────   ← ancilla (non mesurée)
```

**Étapes :**
1. Ancilla initialisée à |1⟩ (X gate)
2. Hadamard sur tous les qubits → |+⟩⊗ⁿ ⊗ |−⟩
3. Oracle U_f (kick-back de phase)
4. Hadamard sur les qubits d'entrée
5. Mesure des n qubits d'entrée

**Interprétation :**
- Résultat `|000⟩` → f est **constante**
- Tout autre résultat → f est **balancée**

## Oracles

| Oracle | Type | Implémentation |
|--------|------|----------------|
| `oracle_constant_0` | Constant | Rien (identité) |
| `oracle_constant_1` | Constant | X sur l'ancilla |
| `oracle_balanced_q0` | Balancé | CNOT(q0 → ancilla) |
| `oracle_balanced_q1` | Balancé | CNOT(q1 → ancilla) |
| `oracle_balanced_xor` | Balancé | CNOT(q0) + CNOT(q1) → ancilla |
| `oracle_balanced_parity` | Balancé | X·CNOT·X sur q0, q1, q2 → ancilla |

> Le **kick-back de phase** : avec l'ancilla en |−⟩ = 1/√2 (|0⟩ − |1⟩), appliquer CNOT(qᵢ → ancilla) revient à appliquer une phase −1 sur qᵢ si qᵢ = |1⟩, sans modifier l'ancilla.

## Prérequis

```bash
IBM_QUANTUM_TOKEN=<votre_token>   # dans .env
```

## Exécution

```bash
uv run ex03/main.py
```

**Sortie attendue :**
```
--- Vrai QPU ---
  constant_0           → CONSTANT  {'000': 498, ...}
  constant_1           → CONSTANT  {'000': 491, ...}
  balanced_q0          → BALANCÉ   {'100': 234, '000': 12, ...}
  balanced_q1          → BALANCÉ   {'010': 251, '000': 8, ...}
  balanced_xor         → BALANCÉ   {'110': 229, ...}
  balanced_parity      → BALANCÉ   {'111': 241, ...}
```

Les quelques mesures erronées sur `|000⟩` pour les oracles balancés sont dues au bruit du QPU.

## Résultat

`figure.png` contient un histogramme par oracle (6 au total).
