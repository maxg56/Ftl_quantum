# ex01 — Intrication (état de Bell)

Création d'un **état de Bell** Φ⁺, le plus simple des états intriqués à deux qubits.

## Principe

Deux qubits sont **intriqués** quand leur état ne peut pas s'écrire comme le produit de deux états indépendants.
Mesurer l'un détermine instantanément l'état de l'autre, quelle que soit la distance qui les sépare.

L'état de Bell Φ⁺ :
```
|Φ⁺⟩ = 1/√2 (|00⟩ + |11⟩)
```

On observe uniquement |00⟩ et |11⟩, jamais |01⟩ ni |10⟩.

## Circuit

```
q0 ──H──●──M
         │
q1 ──────X──M
```

| Étape | Porte | Effet |
|-------|-------|-------|
| 1 | H sur q0 | |00⟩ → 1/√2 (|00⟩ + |10⟩) |
| 2 | CNOT(q0→q1) | 1/√2 (|00⟩ + |10⟩) → 1/√2 (|00⟩ + |11⟩) |
| 3 | Mesure | Effondrement corrélé |

Le CNOT inverse q1 uniquement si q0 vaut |1⟩, ce qui crée la corrélation.

## Exécution

```bash
uv run ex01/main.py
```

**Sortie attendue (500 shots) :**
```
Counts: {'00': ~250, '11': ~250}
```

Les états |01⟩ et |10⟩ n'apparaissent jamais — preuve de l'intrication parfaite.

## Résultat

Histogramme sauvegardé dans `figure.png` avec uniquement deux barres : |00⟩ et |11⟩.
