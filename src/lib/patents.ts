/* ── Achala IT Solutions patented-intelligence registry ───────────────────────────
   Distilled from the eight patent complete specifications filed by
   Strategemist Global Pvt. Ltd. (Hyderabad) — the intellectual-property
   foundation beneath the Achala platform portfolio. Only delivery-relevant
   capability summaries are surfaced on the site (no claims language).     */

export type Patent = {
  ref: string; // short cite, e.g. "Patent 2 / GNN contextual core"
  title: string;
  oneLiner: string;
  capabilities: string[];
  towers: string[]; // service tower slugs it powers
  platforms: string[]; // platform slugs it powers
};

export const PATENTS: Patent[] = [
  {
    ref: "GNN-Contextual",
    title: "Contextual Intelligence Processing Using Graph Neural Networks",
    oneLiner:
      "The graph core of Achala Nexus: dynamic heterogeneous graphs, hypergraph tensors, quantum-inspired embedding and deterministic streaming for real-time contextual reasoning.",
    capabilities: [
      "Dynamic graph representations with continuous edge rewiring",
      "Hypergraph tensor encoding (CANDECOMP/PARAFAC, Tucker)",
      "Persistent homology for structural anomaly detection",
      "Fractal graph compression for billion-node scale",
      "Deterministic micro-batch streaming with conflict resolution",
    ],
    towers: ["data-analytics-lakehouse", "applied-ai-generative-ai"],
    platforms: ["nexus", "quanta"],
  },
  {
    ref: "Quantum-Workflow",
    title: "Optimizing Computational Workflows Using Quantum-Inspired Algorithms",
    oneLiner:
      "Tensor-manifold processing, quantum-walk exploration and logarithmic-complexity scheduling executed across TPU/FPGA fabric — the Achala Quanta and Forge optimization core.",
    capabilities: [
      "Tensor manifold processing units (TMPUs)",
      "Quantum-walk state-space exploration",
      "Logarithmic complexity scaling for enterprise workloads",
      "Non-Euclidean (Riemannian) clustering and segmentation",
      "Abstract-interpretation + temporal-logic verification",
    ],
    towers: ["quantum-advanced-compute", "cloud-edge-platform-engineering"],
    platforms: ["quanta", "forge"],
  },
  {
    ref: "Federated-Distributed",
    title: "Distributed Intelligence Using Federated Learning in Enterprise Networks",
    oneLiner:
      "Privacy-preserving collaborative intelligence: ZHNE homomorphic encryption, Multi-Scale Asynchronous Byzantine Consensus and swarm-based self-healing clusters — the Achala Sentinel trust fabric.",
    capabilities: [
      "Zero-Knowledge Homomorphic Neural Encryption (ZHNE)",
      "Multi-Scale Asynchronous Byzantine Consensus (MABC)",
      "Swarm-intelligence adaptive node clustering",
      "Blockchain-integrated self-healing workload recovery",
      "Neuromorphic accelerators for edge deployments",
    ],
    towers: ["cybersecurity-zero-trust", "iot-digital-twin-robotics"],
    platforms: ["sentinel", "ledger"],
  },
  {
    ref: "Ethical-Decision",
    title: "Ethical Decision Processing With Multi-Layer Algorithmic Validation",
    oneLiner:
      "Hierarchical validation — rule graphs, Bayesian refinement and cascading-impact simulation — that makes every automated decision explainable, auditable and bias-tested.",
    capabilities: [
      "Hierarchical ethical-graph ontology validation",
      "Bayesian probabilistic refinement of decision vectors",
      "Recursive cascading-impact simulation",
      "Multi-modal explainability (DAG decision pathways)",
      "Synthetic adversarial resilience testing",
    ],
    towers: ["agentic-ai-hyperautomation", "applied-ai-generative-ai"],
    platforms: ["sentinel", "compass"],
  },
  {
    ref: "GenAI-Workflows",
    title: "Automating Knowledge Workflows Using Generative Artificial Intelligence",
    oneLiner:
      "Self-improving orchestration: transformer workflow blueprints, temporal reasoning, knowledge-liquidity protocols and multi-agent reinforcement learning — the Achala Swarm engine.",
    capabilities: [
      "Generative AI orchestration blueprints (DAG synthesis)",
      "Probabilistic temporal-logic scheduling",
      "Knowledge-liquidity protocol for cross-platform workflows",
      "Multi-agent RL with shared-reward credit assignment",
      "zk-SNARK validated decentralized execution",
    ],
    towers: ["agentic-ai-hyperautomation", "applied-ai-generative-ai"],
    platforms: ["swarm", "forge"],
  },
  {
    ref: "Pattern-Recognition",
    title: "Adaptive Pattern Recognition Using Quantum-Enhanced Neural Networks",
    oneLiner:
      "Real-time multimodal perception — vision, audio, text and sensor fusion with quantum feedback loops and probabilistic ensemble learning — the Achala Twinverse perception layer.",
    capabilities: [
      "Multimodal fusion across sensor, video, text and audio streams",
      "Quantum feedback loop recalibration without retraining",
      "Probabilistic ensemble learning with Bayesian averaging",
      "Edge-cloud hybrid deployment with latency-aware routing",
      "Biometric, document and anomaly recognition at scale",
    ],
    towers: ["iot-digital-twin-robotics", "applied-ai-generative-ai"],
    platforms: ["twinverse", "nexus"],
  },
  {
    ref: "Energy-Workload",
    title: "AI-Driven Energy-Efficient Workload Optimization in Distributed Computing",
    oneLiner:
      "Grid-aware orchestration: tensor workload decomposition, reinforcement-learned scheduling and power-state modulation that cut datacenter energy per decision — the Achala Forge economics engine.",
    capabilities: [
      "Tensor-based workload decomposition (SVD, low-rank)",
      "Double-Q-learning execution scheduling",
      "Grid-stability-aware power synchronization",
      "Photonic-electronic node arbitration",
      "Fault-tolerant checkpointing and recovery",
    ],
    towers: ["cloud-edge-platform-engineering", "quantum-advanced-compute"],
    platforms: ["forge", "quanta"],
  },
  {
    ref: "Adaptive-Learning",
    title: "Adaptive Learning Using Reinforcement Optimization and Self-Evolving Frameworks",
    oneLiner:
      "Self-evolving decision systems: neural architecture search, temporal-spatial feature extraction and knowledge-graph decision support synced by Raft consensus — the Achala Compass intelligence loop.",
    capabilities: [
      "Dynamic reinforcement learning framework (DRLF)",
      "Temporal Fusion Transformers + Fourier cyclical modeling",
      "Knowledge-graph-driven decision support (KGD-DSS)",
      "Raft-consensus distributed coherence",
      "Explainable AI (SHAP/LIME) stakeholder outputs",
    ],
    towers: ["applied-ai-generative-ai", "data-analytics-lakehouse"],
    platforms: ["compass", "nexus"],
  },
];

export function patentsForPage(url: string, title: string): Patent[] {
  const hay = (url + " " + title).toLowerCase();
  const scored = PATENTS.map((p) => {
    let score = 0;
    for (const t of p.towers) if (hay.includes(t.replace(/-/g, "-"))) score += 2;
    for (const t of p.towers) {
      const words = t.split("-");
      if (words.every((w) => hay.includes(w))) score += 2;
    }
    for (const pl of p.platforms) if (hay.includes(pl)) score += 3;
    return { p, score };
  })
    .filter((s) => s.score > 0)
    .sort((a, b) => b.score - a.score);
  return scored.slice(0, 3).map((s) => s.p);
}
