import os
from dotenv import load_dotenv
from qiskit import QuantumCircuit, transpile

from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
import matplotlib.pyplot as plt

# 3 qubits d'entrée + 1 ancilla (q3)
N_INPUT = 3
ANCILLA = N_INPUT  # qubit index 3


# ---------------------------------------------------------------------------
# Oracles
# ---------------------------------------------------------------------------

def oracle_constant_0(__: QuantumCircuit) -> None:
    """f(x) = 0 pour tout x — ne fait rien."""
    pass


def oracle_constant_1(qc: QuantumCircuit) -> None:
    """f(x) = 1 pour tout x — flip l'ancilla."""
    qc.x(ANCILLA)


def oracle_balanced_q0(qc: QuantumCircuit) -> None:
    """f(x) = x0 — CNOT de q0 vers ancilla."""
    qc.cx(0, ANCILLA)


def oracle_balanced_q1(qc: QuantumCircuit) -> None:
    """f(x) = x1 — CNOT de q1 vers ancilla."""
    qc.cx(1, ANCILLA)


def oracle_balanced_xor(qc: QuantumCircuit) -> None:
    """f(x) = x0 XOR x1 — deux CNOTs vers ancilla."""
    qc.cx(0, ANCILLA)
    qc.cx(1, ANCILLA)


def oracle_balanced_parity(qc: QuantumCircuit) -> None:
    """f(x) = x̄0 XOR x̄1 XOR x̄2 — patron X-CNOT-X sur tous les qubits d'entrée.
    X retourne chaque qubit avant le CNOT (contrôle sur |0⟩), puis X remet en état.
    """
    qc.x(range(N_INPUT))               # flip tous les qubits d'entrée
    qc.cx(0, ANCILLA)                   # CNOT si q0 était |0⟩
    qc.cx(1, ANCILLA)                   # CNOT si q1 était |0⟩
    qc.cx(2, ANCILLA)                   # CNOT si q2 était |0⟩
    qc.x(range(N_INPUT))               # restaure les qubits d'entrée
    


# ---------------------------------------------------------------------------
# Construction du circuit Deutsch-Jozsa
# ---------------------------------------------------------------------------

def build_dj_circuit(oracle) -> QuantumCircuit:
    """
    Circuit Deutsch-Jozsa sur N_INPUT qubits + 1 ancilla.

    Étapes :
      1. Initialisation : ancilla à |1⟩
      2. Hadamard sur tous les qubits → |+...+⟩|−⟩
      3. Oracle U_f
      4. Hadamard sur les qubits d'entrée
      5. Mesure des qubits d'entrée
    """
    qc = QuantumCircuit(N_INPUT + 1, N_INPUT)

    # Étape 1 : ancilla → |1⟩
    qc.x(ANCILLA)

    # Étape 2 : Hadamard sur tout
    qc.h(range(N_INPUT + 1))
    qc.barrier()

    # Étape 3 : oracle
    oracle(qc)
    qc.barrier()

    # Étape 4 : Hadamard sur les qubits d'entrée
    qc.h(range(N_INPUT))

    # Étape 5 : mesure
    qc.measure(range(N_INPUT), range(N_INPUT))

    return qc


# ---------------------------------------------------------------------------
# Interprétation
# ---------------------------------------------------------------------------

def interpret(counts: dict) -> str:
    dominant = max(counts, key=counts.get)
    return "CONSTANT" if dominant == "0" * N_INPUT else "BALANCÉ"


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
    backend = service.least_busy(operational=True, simulator=False, min_num_qubits=N_INPUT + 1)
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
    oracles = {
        "constant_0":      oracle_constant_0,
        "constant_1":      oracle_constant_1,
        "balanced_q0":     oracle_balanced_q0,
        "balanced_q1":     oracle_balanced_q1,
        "balanced_xor":    oracle_balanced_xor,
        "balanced_parity": oracle_balanced_parity,
    }

    circuits = {name: build_dj_circuit(fn) for name, fn in oracles.items()}

    # Afficher un circuit représentatif
    print(next(iter(circuits.values())).draw(output='text'))

    # --- Vrai QPU ---
    print("\n--- Vrai QPU ---")
    results = run_real_hardware(list(circuits.values()), shots=500)
    hw_counts = dict(zip(circuits.keys(), results))
    for name, counts in hw_counts.items():
        print(f"  {name:20s} → {interpret(counts):8s}  {counts}")

    # --- Figure ---
    _, axes = plt.subplots(1, len(oracles), figsize=(4 * len(oracles), 4))
    for col, name in enumerate(oracles):
        plot_histogram(hw_counts[name], title=f"{name}\nQPU → {interpret(hw_counts[name])}", ax=axes[col])

    plt.tight_layout()
    plt.savefig("figure.png")
    print("\nFigure sauvegardée dans figure.png")


if __name__ == "__main__":
    main()
