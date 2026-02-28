from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt


def main():
    # Circuit 2 qubits, 2 bits classiques
    qc = QuantumCircuit(2, 2)
    qc.h(0)         # Hadamard sur q0 : |0⟩ → 1/√2 (|0⟩ + |1⟩)
    qc.cx(0, 1)     # CNOT (q0=contrôle, q1=cible) → état de Bell 1/√2 (|00⟩ + |11⟩)
    qc.measure([0, 1], [0, 1])

    # Visualisation du circuit
    print(qc.draw(output='text'))

    # Simulation : 500 shots
    sampler = StatevectorSampler()
    job = sampler.run([qc], shots=500)
    result = job.result()

    # Extraction des counts
    counts = result[0].data.c.get_counts()
    print("Counts:", counts)

    # Histogramme
    plot_histogram(counts, title="État de Bell 1/√2 (|00⟩ + |11⟩) — 500 shots")
    plt.savefig("figure.png")


if __name__ == "__main__":
    main()
