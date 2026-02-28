import os
from dotenv import load_dotenv
from qiskit import QuantumCircuit, transpile
from qiskit.primitives import StatevectorSampler
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
import matplotlib.pyplot as plt


def build_circuit() -> QuantumCircuit:
    qc = QuantumCircuit(2, 2)
    qc.h(0)      # |0⟩ → 1/√2 (|0⟩ + |1⟩)
    qc.cx(0, 1)  # CNOT → état de Bell 1/√2 (|00⟩ + |11⟩)
    qc.measure([0, 1], [0, 1])
    return qc


def run_simulator(qc: QuantumCircuit, shots: int = 500) -> dict:
    sampler = StatevectorSampler()
    result = sampler.run([qc], shots=shots).result()
    return result[0].data.c.get_counts()

def run_real_hardware(qc: QuantumCircuit, shots: int = 500) -> dict:
    load_dotenv()
    token = os.environ.get("IBM_QUANTUM_TOKEN")
    if not token:
        raise RuntimeError(
            "Token IBM Quantum manquant.\n"
            "Exporter la variable d'environnement : export IBM_QUANTUM_TOKEN=<token>"
        )

    service = QiskitRuntimeService(channel="ibm_quantum_platform", token=token)
    
    # Choisir le backend le moins chargé avec au moins 2 qubits
    backend = service.least_busy(operational=True, simulator=False, min_num_qubits=2)
    print(f"Backend sélectionné : {backend.name}")

    isa_circuit = transpile(qc, backend=backend)

    sampler = Sampler(backend)
    job = sampler.run([isa_circuit], shots=shots)
    print(f"Job ID : {job.job_id()} — en attente...")
    result = job.result()
    return result[0].data.c.get_counts()


def main():
    qc = build_circuit()   
    print(qc.draw(output='text'))

    # --- Simulateur (référence idéale) ---
    sim_counts = run_simulator(qc, shots=500)
    print(f"\nSimulateur  : {sim_counts}")

    # --- Vrai ordinateur quantique ---
    hw_counts = run_real_hardware(qc, shots=500)
    print(f"Vrai QPU    : {hw_counts}")

    # --- Comparaison ---
    _, axes = plt.subplots(1, 2, figsize=(10, 4))
    plot_histogram(sim_counts, title="Simulateur (idéal)", ax=axes[0])
    plot_histogram(hw_counts,  title="Vrai QPU (bruité)",  ax=axes[1])
    plt.tight_layout()
    plt.savefig("figure.png")
    print("\nFigure sauvegardée dans figure.png")


if __name__ == "__main__":
    main()
