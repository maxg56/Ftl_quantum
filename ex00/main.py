from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt


def main():
    # Circuit 1 qubit, 1 bit classique
    qc = QuantumCircuit(1, 1)
    qc.h(0)         # Porte Hadamard : |0⟩ → 1/√2 (|0⟩ + |1⟩)
    qc.measure(0, 0)

    # Visualisation du circuit
    print(qc.draw(output='text'))

    # Simulation : 500 shots
    sampler = StatevectorSampler()
    job = sampler.run([qc], shots=500)
    result = job.result()

    # Extraction des counts (registre classique 'c')
    counts = result[0].data.c.get_counts()
    print("Counts:", counts)

    # Histogramme
    plot_histogram(counts, title="Superposition |+⟩ — 500 shots")
    plt.savefig("figure.png")



if __name__ == "__main__":
    main()
