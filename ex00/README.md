# ex00 — Superposition

Introduction à la superposition quantique avec la porte **Hadamard**.

## Principe

Un qubit peut exister dans une superposition de |0⟩ et |1⟩ simultanément.
La porte Hadamard crée cet état :

```
H|0⟩ = |+⟩ = 1/√2 (|0⟩ + |1⟩)
```

La mesure effondre la superposition : on observe |0⟩ ou |1⟩ avec une probabilité de 50 % chacun.

## Circuit

```
|0⟩ ──H──M
          ↓
          c0
```

| Porte | Effet |
|-------|-------|
| H | |0⟩ → 1/√2 (|0⟩ + |1⟩) |
| M | Mesure, résultat stocké dans le bit classique c0 |

## Exécution

```bash
uv run ex00/main.py
```

**Sortie attendue (500 shots) :**
```
     ┌───┐┌─┐
  q: ┤ H ├┤M├
     └───┘└─┘

Counts: {'0': ~250, '1': ~250}
```

La distribution est quasi-uniforme — c'est le comportement attendu de |+⟩.
Les légères variations viennent du caractère aléatoire de la mesure quantique.

## Résultat

Histogramme sauvegardé dans `figure.png` montrant environ 50 % pour |0⟩ et 50 % pour |1⟩.
