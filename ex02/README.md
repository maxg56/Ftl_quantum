# ex02 — Simulateur vs vrai QPU

Même circuit qu'en ex01 (état de Bell), exécuté en parallèle sur un simulateur et sur un **vrai ordinateur quantique IBM**.

## Principe

Les simulateurs sont parfaits — ils n'ont pas de bruit.
Les vrais QPU souffrent de plusieurs sources d'erreur :

| Source d'erreur | Effet |
|-----------------|-------|
| Erreurs de portes | Les portes ne sont pas appliquées parfaitement |
| Erreur de mesure | La mesure peut retourner le mauvais résultat |
| Décohérence | Le qubit perd son état quantique avec le temps |
| Diaphonie (crosstalk) | Un qubit perturbe ses voisins |

Résultat : de petites probabilités parasites apparaissent sur |01⟩ et |10⟩.

## Circuit

```
q0 ──H──●──M
         │
q1 ──────X──M
```

Identique à ex01, mais transpilé (`transpile`) pour le backend IBM cible avant envoi.

## Prérequis

```bash
IBM_QUANTUM_TOKEN=<votre_token>   # dans .env
```

## Exécution

```bash
uv run ex02/main.py
```

**Sortie attendue :**
```
Backend sélectionné : ibm_xxx
Job ID : cxxxxx — en attente...

Simulateur  : {'00': 250, '11': 250}
Vrai QPU    : {'00': 231, '11': 244, '01': 14, '10': 11}
```

Le QPU retourne occasionnellement |01⟩ ou |10⟩ à cause du bruit — typiquement 3–5 % d'erreur.

## Fonctions

### `build_circuit() → QuantumCircuit`
Construit le circuit état de Bell (H + CNOT + mesure).

### `run_simulator(qc, shots=500) → dict`
Exécute le circuit sur `StatevectorSampler` (simulateur idéal, sans bruit).

### `run_real_hardware(qc, shots=500) → dict`
Sélectionne le QPU IBM le moins occupé avec au moins 2 qubits, transpile le circuit, envoie le job et retourne les counts.

## Résultat

`figure.png` contient deux histogrammes côte à côte : simulateur (idéal) et QPU (bruité).
