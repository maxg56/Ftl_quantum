import math
import os
from dotenv import load_dotenv
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
import matplotlib.pyplot as plt

# Nombre de qubits de recherche (minimum 2, sans modification pour changer d'oracle)
N_INPUT = 4
# Nombre optimal d'itérations : ⌊π/4 · √N⌋ avec N = 2^n
N_ITERS = max(1, round(math.pi / 4 * math.sqrt(2 ** N_INPUT)))


# ---------------------------------------------------------------------------
# Helpers bas niveau
# ---------------------------------------------------------------------------

def _phase_flip_all_ones(qc: QuantumCircuit) -> None:
    """Inversion de phase de |11...1⟩ via multi-controlled Z (H·MCX·H)."""
    qc.h(N_INPUT - 1)
    qc.mcx(list(range(N_INPUT - 1)), N_INPUT - 1)
    qc.h(N_INPUT - 1)


# ---------------------------------------------------------------------------
# Oracles — marquage par inversion de phase de l'état cible
# ---------------------------------------------------------------------------

def make_oracle(target: int):
    """
    Retourne un oracle qui marque l'état |target⟩ par inversion de phase :
      U_ω|target⟩ = −|target⟩,  U_ω|x⟩ = |x⟩  pour x ≠ target.

    Méthode : transformer |target⟩ en |11...1⟩ (X sur les bits à 0),
    appliquer le flip de phase de |11...1⟩, puis défaire.
    """
    def oracle(qc: QuantumCircuit) -> None:
        for i in range(N_INPUT):
            if not (target >> i) & 1:
                qc.x(i)
        _phase_flip_all_ones(qc)
        for i in range(N_INPUT):
            if not (target >> i) & 1:
                qc.x(i)
    return oracle


# Oracles prédéfinis pour 3 qubits (états de 0 à 7)
oracle_101 = make_oracle(0b101)   # cherche |101⟩ = 5
oracle_011 = make_oracle(0b011)   # cherche |011⟩ = 3
oracle_000 = make_oracle(0b000)   # cherche |000⟩ = 0
oracle_110 = make_oracle(0b110)   # cherche |110⟩ = 6


# ---------------------------------------------------------------------------
# Construction du circuit de Grover
# ---------------------------------------------------------------------------

def build_grover_circuit(oracle_fn, n_iterations: int = N_ITERS) -> QuantumCircuit:
    """
    Circuit de Grover sur N_INPUT qubits.

    Étapes :
      1. Initialisation  — superposition uniforme : H⊗ⁿ|0⟩
      2. × n_iterations :
         a. Oracle    — inversion de phase de l'état cible
         b. Diffuseur — amplification d'amplitude : 2|ψ⟩⟨ψ| − I
      3. Mesure de tous les qubits d'entrée
    """
    qc = QuantumCircuit(N_INPUT, N_INPUT)

    # 1. Superposition uniforme
    qc.h(range(N_INPUT))
    qc.barrier()

    for _ in range(n_iterations):
        # 2a. Oracle
        oracle_fn(qc)
        qc.barrier()

        # 2b. Diffuseur : H·X·MCZ·X·H  (≡ 2|ψ⟩⟨ψ| − I à une phase globale près)
        qc.h(range(N_INPUT))
        qc.x(range(N_INPUT))
        _phase_flip_all_ones(qc)
        qc.x(range(N_INPUT))
        qc.h(range(N_INPUT))
        qc.barrier()

    # 3. Mesure
    qc.measure(range(N_INPUT), range(N_INPUT))
    return qc


# ---------------------------------------------------------------------------
# Interprétation
# ---------------------------------------------------------------------------

def interpret(counts: dict) -> str:
    dominant = max(counts, key=counts.get)
    value = int(dominant, 2)
    total = sum(counts.values())
    prob = counts[dominant] / total
    return f"|{dominant}⟩ (={value}, {prob:.0%})"


# ---------------------------------------------------------------------------
# Exécution hardware (batch unique)
# ---------------------------------------------------------------------------

def run_real_hardware(circuits: list[QuantumCircuit], shots: int = 500) -> list[dict]:
    """Envoie tous les circuits en un seul job sur le vrai QPU."""
    load_dotenv()
    token = os.environ.get("IBM_QUANTUM_TOKEN")
    if not token:
        raise RuntimeError(
            "Token IBM Quantum manquant.\n"
            "Définir IBM_QUANTUM_TOKEN dans .env ou en variable d'environnement."
        )

    service = QiskitRuntimeService(channel="ibm_quantum_platform", token=token)
    backend = service.least_busy(operational=True, simulator=False, min_num_qubits=N_INPUT)
    print(f"Backend sélectionné : {backend.name}")

    isa_circuits = [transpile(qc, backend=backend) for qc in circuits]

    sampler = Sampler(backend)
    job = sampler.run(isa_circuits, shots=shots)
    print(f"Job ID : {job.job_id()} — en attente...")
    result = job.result()

    return [result[i].data.c.get_counts() for i in range(len(circuits))]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"Grover — {N_INPUT} qubits (N={2**N_INPUT} états), {N_ITERS} itération(s)\n")

    oracles = {
        "target |101⟩=5": oracle_101,
        "target |011⟩=3": oracle_011,
        "target |000⟩=0": oracle_000,
        "target |110⟩=6": oracle_110,
    }

    circuits = {name: build_grover_circuit(fn) for name, fn in oracles.items()}

    # Afficher un circuit représentatif
    print(next(iter(circuits.values())).draw(output='text'))

    # --- Vrai QPU ---
    print("\n--- Vrai QPU ---")
    results = run_real_hardware(list(circuits.values()), shots=500)
    hw_counts = dict(zip(circuits.keys(), results))
    for name, counts in hw_counts.items():
        print(f"  {name:22s} → {interpret(counts)}  {counts}")

    # --- Figure ---
    _, axes = plt.subplots(1, len(oracles), figsize=(4 * len(oracles), 4))
    for col, name in enumerate(oracles):
        plot_histogram(
            hw_counts[name],
            title=f"{name}\n{interpret(hw_counts[name])}",
            ax=axes[col],
        )

    plt.tight_layout()
    plt.savefig("figure.png")
    print("\nFigure sauvegardée dans figure.png")


if __name__ == "__main__":
    main()
