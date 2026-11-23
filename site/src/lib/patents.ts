/* ── Achala IT Solutions method-family registry (proprietary IP) ──────────────────
   Distilled from the eight complete specifications held by the Achala IT Solutions
   research programme — the intellectual-property foundation beneath the
   Achala platform portfolio. Only delivery-relevant capability summaries are
   surfaced on the site (no claims language, no applicant details).        */

export type Patent = {
  ref: string; // short cite, e.g. "Patent 2 / GNN contextual core"
  title: string;
  oneLiner: string;
  outcome: string; // A-29: the buyer-facing "what this buys you" line
  capabilities: string[];
  expertise: string[]; // expertise domain slugs it powers
  platforms: string[]; // platform slugs it powers
};

export const PATENTS: Patent[] = [
  {
    ref: "GNN-Contextual",
    title: "Contextual Intelligence Processing Using Graph Neural Networks",
    oneLiner:
      "The graph core of EEMS Platform: dynamic heterogeneous graphs, hypergraph tensors, quantum-inspired embedding and deterministic streaming for real-time contextual reasoning.",
    outcome:
      "Means: decisions that cite their full context — the replay trail your auditor asks for.",
    capabilities: [
      "Dynamic graph representations with continuous edge rewiring",
      "Hypergraph tensor encoding (CANDECOMP/PARAFAC, Tucker)",
      "Persistent homology for structural anomaly detection",
      "Fractal graph compression for billion-node scale",
      "Deterministic micro-batch streaming with conflict resolution",
    ],
    expertise: ["data-analytics-lakehouse", "applied-ai-generative-ai"],
    platforms: ["nexus", "quanta"],
  },
  {
    ref: "Quantum-Workflow",
    title: "Optimizing Computational Workflows Using Quantum-Inspired Algorithms",
    oneLiner:
      "Tensor-manifold processing, quantum-walk exploration and logarithmic-complexity scheduling executed across TPU/FPGA fabric — the Token Management System and Forge optimization core.",
    outcome:
      "Means: scheduling and optimization that stays near-log-cost as the estate grows.",
    capabilities: [
      "Tensor manifold processing units (TMPUs)",
      "Quantum-walk state-space exploration",
      "Logarithmic complexity scaling for enterprise workloads",
      "Non-Euclidean (Riemannian) clustering and segmentation",
      "Abstract-interpretation + temporal-logic verification",
    ],
    expertise: ["quantum-advanced-compute", "cloud-edge-platform-engineering"],
    platforms: ["quanta", "forge"],
  },
  {
    ref: "Federated-Distributed",
    title: "Distributed Intelligence Using Federated Learning in Enterprise Networks",
    oneLiner:
      "Privacy-preserving collaborative intelligence: ZHNE homomorphic encryption, Multi-Scale Asynchronous Byzantine Consensus and swarm-based self-healing clusters — the Tele Medicine Platform trust fabric.",
    outcome:
      "Means: partner analytics without sharing raw data — the control your DPO will ask about.",
    capabilities: [
      "Zero-Knowledge Homomorphic Neural Encryption (ZHNE)",
      "Multi-Scale Asynchronous Byzantine Consensus (MABC)",
      "Swarm-intelligence adaptive node clustering",
      "Blockchain-integrated self-healing workload recovery",
      "Neuromorphic accelerators for edge deployments",
    ],
    expertise: ["cybersecurity-zero-trust", "iot-digital-twin-robotics"],
    platforms: ["sentinel", "ledger"],
  },
  {
    ref: "Ethical-Decision",
    title: "Ethical Decision Processing With Multi-Layer Algorithmic Validation",
    oneLiner:
      "Hierarchical validation — rule graphs, Bayesian refinement and cascading-impact simulation — that makes every automated decision explainable, auditable and bias-tested.",
    outcome:
      "Means: every automated decision explainable and bias-tested — the answer when the regulator asks why.",
    capabilities: [
      "Hierarchical ethical-graph ontology validation",
      "Bayesian probabilistic refinement of decision vectors",
      "Recursive cascading-impact simulation",
      "Multi-modal explainability (DAG decision pathways)",
      "Synthetic adversarial resilience testing",
    ],
    expertise: ["agentic-ai-hyperautomation", "applied-ai-generative-ai"],
    platforms: ["sentinel", "compass"],
  },
  {
    ref: "GenAI-Workflows",
    title: "Automating Knowledge Workflows Using Generative Artificial Intelligence",
    oneLiner:
      "Self-improving orchestration: transformer workflow blueprints, temporal reasoning, knowledge-liquidity protocols and multi-agent reinforcement learning — the KYC Management System engine.",
    outcome:
      "Means: digital workers that improve on the job under guardrails — every action logged and reversible.",
    capabilities: [
      "Generative AI orchestration blueprints (DAG synthesis)",
      "Probabilistic temporal-logic scheduling",
      "Knowledge-liquidity protocol for cross-platform workflows",
      "Multi-agent RL with shared-reward credit assignment",
      "zk-SNARK validated decentralized execution",
    ],
    expertise: ["agentic-ai-hyperautomation", "applied-ai-generative-ai"],
    platforms: ["swarm", "forge"],
  },
  {
    ref: "Pattern-Recognition",
    title: "Adaptive Pattern Recognition Using Quantum-Enhanced Neural Networks",
    oneLiner:
      "Real-time multimodal perception — vision, audio, text and sensor fusion with quantum feedback loops and probabilistic ensemble learning — the BI & Analytics Platform perception layer.",
    outcome:
      "Means: one perception layer across sensor, video and text — recalibrated without retraining pauses.",
    capabilities: [
      "Multimodal fusion across sensor, video, text and audio streams",
      "Quantum feedback loop recalibration without retraining",
      "Probabilistic ensemble learning with Bayesian averaging",
      "Edge-cloud hybrid deployment with latency-aware routing",
      "Biometric, document and anomaly recognition at scale",
    ],
    expertise: ["iot-digital-twin-robotics", "applied-ai-generative-ai"],
    platforms: ["twinverse", "nexus"],
  },
  {
    ref: "Energy-Workload",
    title: "AI-Driven Energy-Efficient Workload Optimization in Distributed Computing",
    oneLiner:
      "Grid-aware orchestration: tensor workload decomposition, reinforcement-learned scheduling and power-state modulation that cut datacenter energy per decision — the Fleet Management System economics engine.",
    outcome:
      "Means: compute cost and energy per decision fall together — visible on your infrastructure bill.",
    capabilities: [
      "Tensor-based workload decomposition (SVD, low-rank)",
      "Double-Q-learning execution scheduling",
      "Grid-stability-aware power synchronization",
      "Photonic-electronic node arbitration",
      "Fault-tolerant checkpointing and recovery",
    ],
    expertise: ["cloud-edge-platform-engineering", "quantum-advanced-compute"],
    platforms: ["forge", "quanta"],
  },
  {
    ref: "Adaptive-Learning",
    title: "Adaptive Learning Using Reinforcement Optimization and Self-Evolving Frameworks",
    oneLiner:
      "Self-evolving decision systems: neural architecture search, temporal-spatial feature extraction and knowledge-graph decision support synced by Raft consensus — the Driisti Smart Vision Glasses intelligence loop.",
    outcome:
      "Means: systems that keep learning under governance — explained to stakeholders, synced by consensus.",
    capabilities: [
      "Dynamic reinforcement learning framework (DRLF)",
      "Temporal Fusion Transformers + Fourier cyclical modeling",
      "Knowledge-graph-driven decision support (KGD-DSS)",
      "Raft-consensus distributed coherence",
      "Explainable AI (SHAP/LIME) stakeholder outputs",
    ],
    expertise: ["applied-ai-generative-ai", "data-analytics-lakehouse"],
    platforms: ["compass", "nexus"],
  },
];

export function patentsForPage(url: string, title: string): Patent[] {
  const hay = (url + " " + title).toLowerCase();
  const scored = PATENTS.map((p) => {
    let score = 0;
    for (const t of p.expertise) if (hay.includes(t.replace(/-/g, "-"))) score += 2;
    for (const t of p.expertise) {
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
