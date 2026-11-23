import Reveal from "./Reveal";

/* ── TechDiagrams (wave-2) ──────────────────────────────────────────────────
   Animated technical architecture & flow diagrams, rendered as inline SVG.
   Pure CSS animation (dash streams, pulses, sweeps, orbits) — no client JS,
   fully static-export safe, disabled under prefers-reduced-motion.
   Each archetype is parameterized with real labels injected by the content
   engine, so no two pages show the same diagram text. */

export type DiagramKind =
  | "layered-stack"
  | "pipeline"
  | "orchestration-loop"
  | "zero-trust-mesh"
  | "twin-loop"
  | "optimization-funnel"
  | "ledger-chain"
  | "edge-topology"
  | "decision-fabric"
  | "delivery-cadence";

export const DIAGRAM_KINDS: DiagramKind[] = [
  "layered-stack",
  "pipeline",
  "orchestration-loop",
  "zero-trust-mesh",
  "twin-loop",
  "optimization-funnel",
  "ledger-chain",
  "edge-topology",
  "decision-fabric",
  "delivery-cadence",
];

/* palette — brand navy field + orange signal */
const CL = {
  line: "rgba(255,255,255,0.30)",
  soft: "rgba(255,255,255,0.14)",
  fill: "rgba(255,255,255,0.065)",
  fill2: "rgba(255,255,255,0.11)",
  stroke: "rgba(255,255,255,0.24)",
  orange: "#d20000",
  orangeSoft: "rgba(210, 0, 0,0.55)",
  txt: "rgba(255,255,255,0.94)",
  dim: "rgba(255,255,255,0.62)",
  faint: "rgba(255,255,255,0.4)",
};

const W = 880;
const H = 430;

/* ── shared primitives ─────────────────────────────────────────────────── */

function Flow({
  d,
  delay = 0,
  dur = 2.2,
  width = 2,
  color = CL.orange,
}: {
  d: string;
  delay?: number;
  dur?: number;
  width?: number;
  color?: string;
}) {
  return (
    <path
      className="td-flow"
      d={d}
      fill="none"
      stroke={color}
      strokeWidth={width}
      strokeLinecap="round"
      strokeDasharray="5 11"
      style={{ animationDelay: `${delay}s`, animationDuration: `${dur}s` }}
    />
  );
}

function Edge({
  d,
  width = 1.4,
  dashed = false,
  color = CL.line,
}: {
  d: string;
  width?: number;
  dashed?: boolean;
  color?: string;
}) {
  return (
    <path
      d={d}
      fill="none"
      stroke={color}
      strokeWidth={width}
      strokeDasharray={dashed ? "3 5" : undefined}
      strokeLinecap="round"
    />
  );
}

function Node({
  x,
  y,
  w,
  h,
  r = 9,
  hot = false,
}: {
  x: number;
  y: number;
  w: number;
  h: number;
  r?: number;
  hot?: boolean;
}) {
  return (
    <rect
      x={x}
      y={y}
      width={w}
      height={h}
      rx={r}
      fill={hot ? "rgba(210, 0, 0,0.16)" : CL.fill}
      stroke={hot ? "rgba(210, 0, 0,0.65)" : CL.stroke}
      strokeWidth={1.2}
    />
  );
}

function Label({
  x,
  y,
  children,
  size = 11.5,
  dim = false,
  anchor = "middle",
  weight = 600,
}: {
  x: number;
  y: number;
  children: string;
  size?: number;
  dim?: boolean;
  anchor?: "start" | "middle" | "end";
  weight?: number;
}) {
  return (
    <text
      x={x}
      y={y}
      fontSize={size}
      fontWeight={weight}
      fill={dim ? CL.dim : CL.txt}
      textAnchor={anchor}
      style={{ letterSpacing: "0.01em" }}
    >
      {children}
    </text>
  );
}

function Pulse({ cx, cy, r = 4, delay = 0 }: { cx: number; cy: number; r?: number; delay?: number }) {
  return (
    <circle
      className="td-pulse"
      cx={cx}
      cy={cy}
      r={r}
      fill={CL.orange}
      style={{ animationDelay: `${delay}s` }}
    />
  );
}

function Frame({ children, bg }: { children: React.ReactNode; bg?: string }) {
  return (
    <svg
      viewBox={`0 0 ${W} ${H}`}
      className="td-svg block w-full"
      role="img"
      aria-hidden="false"
      style={{ background: bg ?? undefined }}
    >
      {children}
    </svg>
  );
}

/* ── 1. layered-stack — platform strata with packet flow ────────────────── */

function LayeredStack({ labels }: { labels: string[] }) {
  const L = labels.length >= 5 ? labels : ["Experience & copilots", "Decision services", "Orchestration & policy", "Feature & model layer", "Governed data foundation"];
  const rows = L.slice(0, 6);
  const top = 58;
  const rowH = 56;
  const gap = 12;
  return (
    <Frame>
      {rows.map((r, i) => {
        const y = top + i * (rowH + gap);
        const inset = Math.max(0, 2 - i % 3) * 26;
        const x = 90 + inset;
        const w = 560 - inset * 2;
        return (
          <g key={r + i}>
            <Node x={x} y={y} w={w} h={rowH} r={10} hot={i === 1} />
            <rect x={x} y={y} width={5} height={rowH} rx={2.5} fill={CL.orange} opacity={0.9} />
            <Label x={x + 22} y={y + rowH / 2 + 4} anchor="start">{r}</Label>
            <Label x={x + w - 16} y={y + rowH / 2 + 4} anchor="end" dim size={10}>{`L${rows.length - i}`}</Label>
            {i < rows.length - 1 && (
              <>
                <Edge d={`M ${x + 60} ${y + rowH} V ${y + rowH + gap}`} width={1.2} color={CL.soft} />
                <Edge d={`M ${x + w - 60} ${y + rowH} V ${y + rowH + gap}`} width={1.2} color={CL.soft} />
                <circle className="td-drop" cx={x + 60} cy={y + rowH} r={3.2} fill={CL.orange} style={{ animationDelay: `${i * 0.5}s` }} />
                <circle className="td-drop" cx={x + w - 60} cy={y + rowH} r={3.2} fill={CL.orange} style={{ animationDelay: `${0.9 + i * 0.4}s` }} />
              </>
            )}
          </g>
        );
      })}
      <Label x={56} y={top - 22} anchor="start" dim size={10.5}>CONSUMPTION</Label>
      <Label x={56} y={top + rows.length * (rowH + gap) - 6} anchor="start" dim size={10.5}>FOUNDATION</Label>
    </Frame>
  );
}

/* ── 2. pipeline — streaming decision pipeline with feedback ────────────── */

function Pipeline({ labels }: { labels: string[] }) {
  const L = labels.length >= 5 ? labels.slice(0, 6) : ["Sources", "Ingest & contracts", "Lakehouse", "Feature store", "Realtime decision", "Action systems"];
  const n = Math.min(6, L.length);
  const bw = 108;
  const gap = (W - 60 - n * bw) / (n - 1);
  const y = 150;
  const h = 64;
  const xs = Array.from({ length: n }, (_, i) => 30 + i * (bw + gap));
  return (
    <Frame>
      {L.slice(0, n).map((s, i) => (
        <g key={s + i}>
          <Node x={xs[i]} y={y} w={bw} h={h} hot={i === n - 2} />
          <Label x={xs[i] + bw / 2} y={y + h / 2 - 3}>{`0${i + 1}`}</Label>
          <foreignObject x={xs[i] + 4} y={y + h - 26} width={bw - 8} height={44}>
            <div className="td-lbl">{s}</div>
          </foreignObject>
          {i < n - 1 && (
            <>
              <Edge d={`M ${xs[i] + bw} ${y + h / 2} H ${xs[i + 1]}`} />
              <Flow d={`M ${xs[i] + bw + 2} ${y + h / 2} H ${xs[i + 1] - 2}`} dur={1.6} delay={i * 0.28} />
            </>
          )}
        </g>
      ))}
      {/* feedback loop */}
      <Edge d={`M ${xs[n - 1] + bw / 2} ${y + h + 4} V 268 H ${xs[0] + bw / 2} V ${y + h + 4}`} dashed color={CL.soft} />
      <Flow d={`M ${xs[n - 1] + bw / 2} 268 H ${xs[0] + bw / 2}`} dur={3.2} color={CL.orangeSoft} />
      <Label x={W / 2} y={260} dim size={10.5}>OUTCOME TELEMETRY RETURNS TO BASELINE</Label>
      {/* SLA lane */}
      <rect x={30} y={318} width={W - 60} height={44} rx={9} fill={CL.fill} stroke={CL.stroke} strokeDasharray="3 5" />
      <Label x={54} y={344} anchor="start" dim size={10}>SLO</Label>
      <Label x={W / 2} y={344} dim size={11}>end-to-end decision latency budgeted per stage — every hop owns a number</Label>
      <Pulse cx={xs[n - 1] + bw / 2} cy={y + h + 2} delay={0.4} />
    </Frame>
  );
}

/* ── 3. orchestration-loop — agent fleet control loop ───────────────────── */

function OrchestrationLoop({ labels }: { labels: string[] }) {
  const L = labels.length >= 4 ? labels.slice(0, 4) : ["Plan & queue", "Bid & route", "Execute with tools", "Verify & learn"];
  const cx = W / 2;
  const cy = 208;
  const R = 118;
  const nw = 150;
  const nh = 46;
  const pos = [
    { x: cx - nw / 2, y: cy - R - nh / 2 },
    { x: cx + R - nw / 2 + 24, y: cy - nh / 2 },
    { x: cx - nw / 2, y: cy + R - nh / 2 },
    { x: cx - R - 24 - nw / 2, y: cy - nh / 2 },
  ];
  return (
    <Frame>
      {/* rotating dashed orbit */}
      <circle className="td-spin" cx={cx} cy={cy} r={R} fill="none" stroke={CL.soft} strokeWidth={1.2} strokeDasharray="4 8" />
      {/* arcs between nodes */}
      <Edge d={`M ${cx} ${cy - R} A ${R} ${R} 0 0 1 ${cx + R} ${cy}`} color={CL.soft} />
      <Edge d={`M ${cx + R} ${cy} A ${R} ${R} 0 0 1 ${cx} ${cy + R}`} color={CL.soft} />
      <Edge d={`M ${cx} ${cy + R} A ${R} ${R} 0 0 1 ${cx - R} ${cy}`} color={CL.soft} />
      <Edge d={`M ${cx - R} ${cy} A ${R} ${R} 0 0 1 ${cx} ${cy - R}`} color={CL.soft} />
      <Flow d={`M ${cx + 34} ${cy - R + 12} A ${R} ${R} 0 0 1 ${cx + R - 10} ${cy - 34}`} dur={1.8} />
      <Flow d={`M ${cx + R - 12} ${cy + 34} A ${R} ${R} 0 0 1 ${cx + 34} ${cy + R - 12}`} dur={1.8} delay={0.5} />
      <Flow d={`M ${cx - 34} ${cy + R - 12} A ${R} ${R} 0 0 1 ${cx - R + 12} ${cy + 34}`} dur={1.8} delay={1.0} />
      <Flow d={`M ${cx - R + 12} ${cy - 34} A ${R} ${R} 0 0 1 ${cx - 34} ${cy - R + 12}`} dur={1.8} delay={1.5} />
      {/* core */}
      <circle cx={cx} cy={cy} r={58} fill="rgba(210, 0, 0,0.13)" stroke="rgba(210, 0, 0,0.7)" strokeWidth={1.4} />
      <circle cx={cx} cy={cy} r={44} fill="rgba(43, 86, 114,0.9)" stroke={CL.orange} strokeWidth={1.2} />
      <Label x={cx} y={cy - 2}>Orchestration</Label>
      <Label x={cx} y={cy + 15} dim size={10}>core</Label>
      {L.map((s, i) => (
        <g key={s + i}>
          <Node x={pos[i].x} y={pos[i].y} w={nw} h={nh} hot={i === 2} />
          <foreignObject x={pos[i].x + 6} y={pos[i].y + 6} width={nw - 12} height={nh - 12}>
            <div className="td-lbl td-lbl-c">{`0${i + 1} · ${s}`}</div>
          </foreignObject>
        </g>
      ))}
      {/* human checkpoint */}
      <Node x={W - 210} y={352} w={170} h={40} r={20} />
      <Label x={W - 125} y={376} size={10.5}>Human checkpoint</Label>
      <Edge d={`M ${cx + R * 0.62} ${cy + R * 0.62} C ${cx + 120} ${cy + 120}, ${W - 250} 340, ${W - 212} 368`} dashed color={CL.soft} />
      <Pulse cx={cx} cy={cy - 58} delay={0.2} />
    </Frame>
  );
}

/* ── 4. zero-trust-mesh — radial trust gates ────────────────────────────── */

function ZeroTrustMesh({ labels }: { labels: string[] }) {
  const L = labels.length >= 6 ? labels.slice(0, 6) : ["Identity", "Device posture", "Network", "Workload", "Data", "Audit trail"];
  const cx = W / 2;
  const cy = 210;
  const R = 132;
  const gates = L.map((s, i) => {
    const a = (Math.PI * 2 * i) / L.length - Math.PI / 2;
    return { s, x: cx + R * Math.cos(a), y: cy + R * Math.sin(a), a };
  });
  return (
    <Frame>
      {/* orbit rings */}
      <circle className="td-spin" cx={cx} cy={cy} r={R} fill="none" stroke={CL.soft} strokeDasharray="2 7" />
      <circle cx={cx} cy={cy} r={R + 44} fill="none" stroke={CL.soft} strokeDasharray="2 9" opacity={0.7} />
      {/* radials + flow */}
      {gates.map((g, i) => (
        <g key={g.s + i}>
          <Edge d={`M ${g.x} ${g.y} L ${cx + 52 * Math.cos(g.a)} ${cy + 52 * Math.sin(g.a)}`} color={CL.soft} />
          <Flow
            d={`M ${g.x + (cx - g.x) * 0.28} ${g.y + (cy - g.y) * 0.28} L ${cx + 52 * Math.cos(g.a)} ${cy + 52 * Math.sin(g.a)}`}
            dur={2.4}
            delay={i * 0.36}
          />
          {/* gate diamond */}
          <rect
            className="td-breathe"
            x={g.x + (cx - g.x) * 0.62 - 7}
            y={g.y + (cy - g.y) * 0.62 - 7}
            width={14}
            height={14}
            rx={3}
            transform={`rotate(45 ${g.x + (cx - g.x) * 0.62} ${g.y + (cy - g.y) * 0.62})`}
            fill="rgba(210, 0, 0,0.2)"
            stroke={CL.orange}
            strokeWidth={1.2}
            style={{ animationDelay: `${i * 0.5}s` }}
          />
          <Node x={g.x - 52} y={g.y - 17} w={104} h={34} r={8} />
          <foreignObject x={g.x - 48} y={g.y - 14} width={96} height={28}>
            <div className="td-lbl td-lbl-c">{g.s}</div>
          </foreignObject>
        </g>
      ))}
      {/* core */}
      <circle cx={cx} cy={cy} r={52} fill="rgba(43, 86, 114,0.92)" stroke={CL.orange} strokeWidth={1.6} />
      <circle className="td-halo" cx={cx} cy={cy} r={52} fill="none" stroke={CL.orangeSoft} />
      <Label x={cx} y={cy - 4}>Policy engine</Label>
      <Label x={cx} y={cy + 14} dim size={10}>deny · verify · sign</Label>
    </Frame>
  );
}

/* ── 5. twin-loop — physical ⇄ digital mirror ───────────────────────────── */

function TwinLoop({ labels }: { labels: string[] }) {
  const L = labels.length >= 4 ? labels.slice(0, 4) : ["Physical asset", "Telemetry", "Digital twin", "Optimal control"];
  return (
    <Frame>
      {/* physical panel */}
      <Node x={44} y={92} w={250} h={190} r={14} />
      <Label x={169} y={124}>{L[0]}</Label>
      {[0, 1, 2].map((i) => (
        <g key={i}>
          <rect x={70 + i * 70} y={146} width={54} height={40} rx={7} fill={CL.fill2} stroke={CL.stroke} />
          <Pulse cx={97 + i * 70} cy={166} r={2.6} delay={i * 0.6} />
        </g>
      ))}
      <Label x={169} y={216} dim size={10}>sensors · PLCs · vision · ERP events</Label>
      {/* digital panel */}
      <Node x={586} y={92} w={250} h={190} r={14} hot />
      <Label x={711} y={124}>{L[2]}</Label>
      {[0, 1, 2].map((i) => (
        <rect key={i} x={612 + i * 70} y={146} width={54} height={40} rx={7} fill="rgba(210, 0, 0,0.14)" stroke="rgba(210, 0, 0,0.55)" />
      ))}
      <Label x={711} y={216} dim size={10}>state estimate · simulation · prediction</Label>
      {/* forward telemetry */}
      <Edge d={`M 294 150 H 586`} color={CL.soft} />
      <Flow d={`M 298 150 H 582`} dur={1.7} />
      <Label x={440} y={140} size={10.5} dim>{L[1]}</Label>
      {/* reverse control */}
      <Edge d={`M 586 224 H 294`} color={CL.soft} />
      <Flow d={`M 582 224 H 298`} dur={2.1} delay={0.6} color={CL.orangeSoft} />
      <Label x={440} y={244} size={10.5} dim>{L[3]}</Label>
      {/* sync hub */}
      <circle className="td-spin" cx={440} cy={188} r={26} fill="rgba(43, 86, 114,0.92)" stroke={CL.orange} strokeDasharray="3 5" />
      <Label x={440} y={192} size={10}>sync</Label>
      {/* analytics strip */}
      <rect x={44} y={318} width={W - 88} height={48} rx={10} fill={CL.fill} stroke={CL.stroke} />
      <Label x={W / 2} y={347} dim size={11}>calibration loop — model drift checked against plant truth every shift</Label>
      <Pulse cx={112} cy={342} delay={0.3} />
    </Frame>
  );
}

/* ── 6. optimization-funnel — quantum-inspired convergence ──────────────── */

function OptimizationFunnel({ labels }: { labels: string[] }) {
  const L = labels.length >= 3 ? labels.slice(0, 3) : ["Candidate space", "Evaluated schedules", "Committed plan"];
  return (
    <Frame>
      {/* funnel bands */}
      <path d="M 120 70 H 760 L 640 168 H 240 Z" fill="rgba(255,255,255,0.05)" stroke={CL.stroke} />
      <path d="M 240 176 H 640 L 548 268 H 332 Z" fill="rgba(255,255,255,0.07)" stroke={CL.stroke} />
      <path d="M 332 276 H 548 L 468 340 H 412 Z" fill="rgba(210, 0, 0,0.14)" stroke="rgba(210, 0, 0,0.6)" />
      <Label x={440} y={104}>{L[0]}</Label>
      <Label x={440} y={210}>{L[1]}</Label>
      <Label x={440} y={296}>{L[2]}</Label>
      {/* orbiting particles */}
      <circle className="td-orbit" cx={440} cy={120} r={0} fill={CL.orange} style={{ transformOrigin: "440px 130px" }} />
      <circle className="td-orbit td-orbit-2" cx={440} cy={120} r={0} fill="rgba(255,255,255,0.8)" style={{ transformOrigin: "440px 130px" }} />
      <ellipse cx={440} cy={130} rx={250} ry={34} fill="none" stroke={CL.soft} strokeDasharray="2 6" />
      {/* evaluation ticks */}
      {[0, 1, 2, 3, 4, 5].map((i) => (
        <g key={i}>
          <rect x={270 + i * 60} y={188} width={44} height={12} rx={4} fill={CL.fill2} stroke={CL.stroke} />
          <rect className="td-eval" x={270 + i * 60} y={188} width={0} height={12} rx={4} fill={CL.orange} opacity={0.8} style={{ animationDelay: `${i * 0.34}s` }} />
        </g>
      ))}
      {/* result node */}
      <Node x={382} y={352} w={116} h={42} r={10} hot />
      <Label x={440} y={377} size={11}>ship the plan</Label>
      <Flow d="M 440 344 V 350" dur={1} />
      <Label x={132} y={72} anchor="start" dim size={10}>10⁶–10⁹ options</Label>
      <Label x={748} y={72} anchor="end" dim size={10}>constraints · SLAs · cost</Label>
    </Frame>
  );
}

/* ── 7. ledger-chain — signed block chain with consensus bar ────────────── */

function LedgerChain({ labels }: { labels: string[] }) {
  const L = labels.length >= 5 ? labels.slice(0, 5) : ["Event", "Anchor", "Attest", "Verify", "Settle"];
  const bw = 116;
  const bh = 86;
  const gap = 44;
  const x0 = (W - (5 * bw + 4 * gap)) / 2;
  const y = 128;
  return (
    <Frame>
      {L.map((s, i) => {
        const x = x0 + i * (bw + gap);
        return (
          <g key={s + i}>
            <Node x={x} y={y} w={bw} h={bh} r={12} hot={i === 2} />
            <rect x={x} y={y} width={bw} height={26} rx={12} fill="rgba(210, 0, 0,0.16)" />
            <Label x={x + bw / 2} y={y + 17} size={10} dim>{`block ${String(i + 1).padStart(2, "0")}`}</Label>
            <Label x={x + bw / 2} y={y + 56}>{s}</Label>
            <circle className="td-pulse" cx={x + bw - 14} cy={y + bh - 14} r={2.4} style={{ animationDelay: `${i * 0.44}s` }} />
            {i < 4 && (
              <>
                <Edge d={`M ${x + bw} ${y + bh / 2} h ${gap}`} />
                <Flow d={`M ${x + bw + 3} ${y + bh / 2} h ${gap - 6}`} dur={1.4} delay={i * 0.3} />
                <circle cx={x + bw + gap / 2} cy={y + bh / 2} r={4.5} fill="#2b5672" stroke={CL.orange} strokeWidth={1.3} />
              </>
            )}
          </g>
        );
      })}
      {/* consensus bar */}
      <rect x={x0} y={268} width={5 * bw + 4 * gap} height={44} rx={10} fill={CL.fill} stroke={CL.stroke} />
      <Label x={x0 + (5 * bw + 4 * gap) / 2} y={294} dim size={11}>consensus & finality — every state transition signed, timestamped and replayable</Label>
      {/* hash tie-lines */}
      {[1, 3].map((i) => (
        <Edge key={i} d={`M ${x0 + i * (bw + gap) + bw / 2} ${y + bh} V 268`} dashed color={CL.soft} />
      ))}
    </Frame>
  );
}

/* ── 8. edge-topology — edge fleet uplinking to core ────────────────────── */

function EdgeTopology({ labels }: { labels: string[] }) {
  const L = labels.length >= 4 ? labels.slice(0, 4) : ["Devices & sensors", "Edge nodes", "Regional gateway", "Central core"];
  const ex = [150, 340, 540, 730];
  return (
    <Frame>
      {/* core */}
      <Node x={W / 2 - 90} y={44} w={180} h={54} r={12} hot />
      <Label x={W / 2} y={70}>{L[3]}</Label>
      {/* regional gateway */}
      <Node x={W / 2 - 70} y={168} w={140} h={44} r={10} />
      <Label x={W / 2} y={194}>{L[2]}</Label>
      <Edge d={`M ${W / 2} 98 V 168`} />
      <Flow d={`M ${W / 2} 102 V 164`} dur={1.5} />
      <Flow d={`M ${W / 2 - 6} 164 V 102`} dur={2.3} delay={0.5} color={CL.orangeSoft} />
      {/* edge nodes */}
      {ex.map((x, i) => (
        <g key={x + i}>
          <Node x={x - 58} y={266} w={116} h={44} r={9} />
          <Label x={x} y={292}>{L[1]}</Label>
          <Edge d={`M ${x} 266 C ${x} 226, ${W / 2 + (x - W / 2) * 0.2} 214, ${W / 2} 212`} color={CL.soft} />
          <Flow d={`M ${x} 264 C ${x} 226, ${W / 2 + (x - W / 2) * 0.2} 214, ${W / 2} 214`} dur={1.9} delay={i * 0.32} />
          <Label x={x + 66} y={258} size={9.5} dim anchor="start">{`${4 + i * 3}ms`}</Label>
        </g>
      ))}
      {/* devices row */}
      {ex.map((x, i) => (
        <g key={"d" + i}>
          {[0, 1, 2].map((j) => (
            <circle key={j} cx={x - 22 + j * 22} cy={356} r={7} fill={CL.fill2} stroke={CL.stroke} className="td-breathe" style={{ animationDelay: `${i * 0.4 + j * 0.2}s` }} />
          ))}
          <Edge d={`M ${x} 344 V 310`} color={CL.soft} />
        </g>
      ))}
      <Label x={W / 2} y={384} dim size={10.5}>{`${L[0]} — filtering and local decisioning at the edge; only signals that need global state travel up`}</Label>
    </Frame>
  );
}

/* ── 9. decision-fabric — knowledge flows into governed decisions ───────── */

function DecisionFabric({ labels }: { labels: string[] }) {
  const L = labels.length >= 4 ? labels.slice(0, 4) : ["Knowledge sources", "Grounded core", "Decision plane", "Governed action"];
  return (
    <Frame>
      {/* sources */}
      {["Documents & policies", "Curated data estate", "Live event streams"].map((s, i) => {
        const y = 96 + i * 74;
        return (
          <g key={s}>
            <Node x={44} y={y} w={208} h={46} r={10} />
            <Label x={148} y={y + 27}>{s}</Label>
            <Edge d={`M 252 ${y + 23} C 330 ${y + 23}, 340 210, 396 210`} color={CL.soft} />
            <Flow d={`M 252 ${y + 23} C 330 ${y + 23}, 340 210, 396 210`} dur={2} delay={i * 0.5} />
          </g>
        );
      })}
      {/* core */}
      <circle cx={440} cy={210} r={54} fill="rgba(43, 86, 114,0.94)" stroke={CL.orange} strokeWidth={1.5} />
      <circle className="td-spin" cx={440} cy={210} r={66} fill="none" stroke={CL.soft} strokeDasharray="3 7" />
      <Label x={440} y={206}>{L[1]}</Label>
      <Label x={440} y={224} dim size={9.5}>retrieval · eval · guard</Label>
      {/* decision plane */}
      <Node x={552} y={182} w={150} h={56} r={11} hot />
      <Label x={627} y={214}>{L[2]}</Label>
      <Edge d="M 494 210 H 552" />
      <Flow d="M 496 210 H 550" dur={1.4} />
      {/* action */}
      <Node x={748} y={182} w={104} h={56} r={11} />
      <Label x={800} y={206} size={11}>{L[3]}</Label>
      <Label x={800} y={222} dim size={9}>signed & logged</Label>
      <Edge d="M 702 210 H 748" />
      <Flow d="M 704 210 H 746" dur={1.2} delay={0.3} />
      {/* guard rail */}
      <rect x={552} y={296} width={300} height={44} rx={10} fill={CL.fill} stroke={CL.stroke} strokeDasharray="3 5" />
      <Label x={702} y={322} dim size={10.5}>policy guardrails · PII fences · approval routing</Label>
      <Edge d="M 702 238 V 296" dashed color={CL.soft} />
    </Frame>
  );
}

/* ── 10. delivery-cadence — gated program timeline ──────────────────────── */

function DeliveryCadence({ labels }: { labels: string[] }) {
  const L = labels.length >= 4 ? labels.slice(0, 4) : ["Diagnose · W1–2", "Pilot · W3–8", "Industrialize · W9–12", "Scale · Q2+"];
  const bw = 186;
  const gap = 22;
  const x0 = (W - (4 * bw + 3 * gap)) / 2;
  const y = 128;
  return (
    <Frame>
      {/* baseline rail */}
      <Edge d={`M ${x0 - 16} ${y - 26} H ${x0 + 4 * bw + 3 * gap + 16}`} color={CL.soft} />
      {L.map((s, i) => {
        const x = x0 + i * (bw + gap);
        return (
          <g key={s + i}>
            <Node x={x} y={y} w={bw} h={96} r={12} hot={i === 1} />
            <Label x={x + 16} y={y + 28} anchor="start">{`0${i + 1}`}</Label>
            <foreignObject x={x + 10} y={y + 38} width={bw - 20} height={50}>
              <div className="td-lbl td-lbl-c td-lbl-2">{s}</div>
            </foreignObject>
            {/* progress fill */}
            <rect className="td-prog" x={x} y={y + 96 - 6} width={bw} height={6} rx={3} fill={CL.orange} opacity={0.85} style={{ animationDelay: `${i * 0.9}s` }} />
            {i < 3 && (
              <g>
                <rect x={x + bw + gap / 2 - 8} y={y + 40} width={16} height={16} rx={3} transform={`rotate(45 ${x + bw + gap / 2} ${y + 48})`} fill="rgba(43, 86, 114,0.95)" stroke={CL.orange} strokeWidth={1.4} />
                <Label x={x + bw + gap / 2} y={y + 22} size={9.5} dim>GATE</Label>
              </g>
            )}
          </g>
        );
      })}
      {/* evidence strip */}
      <rect x={x0 - 16} y={296} width={4 * bw + 3 * gap + 32} height={46} rx={10} fill={CL.fill} stroke={CL.stroke} />
      <Label x={W / 2} y={324} dim size={11}>signed baseline → weekly evidence to your control owner → measured delta at every gate</Label>
      <Pulse cx={x0 + 10} cy={318} delay={0.5} />
    </Frame>
  );
}

/* ── registry ───────────────────────────────────────────────────────────── */

const REGISTRY: Record<DiagramKind, (p: { labels: string[] }) => React.ReactNode> = {
  "layered-stack": LayeredStack,
  pipeline: Pipeline,
  "orchestration-loop": OrchestrationLoop,
  "zero-trust-mesh": ZeroTrustMesh,
  "twin-loop": TwinLoop,
  "optimization-funnel": OptimizationFunnel,
  "ledger-chain": LedgerChain,
  "edge-topology": EdgeTopology,
  "decision-fabric": DecisionFabric,
  "delivery-cadence": DeliveryCadence,
};

export function TechDiagram({
  kind,
  labels,
  note,
  title,
}: {
  kind: DiagramKind;
  labels?: string[];
  note?: string;
  title?: string;
}) {
  const Cmp = REGISTRY[kind] ?? Pipeline;
  return (
    <Reveal className="td-wrap">
      <figure className="td-figure overflow-hidden rounded-2xl border border-line shadow-1">
        <div className="flex items-center justify-between border-b border-line bg-navy-950 px-4 py-2.5">
          <figcaption className="flex items-center gap-2 text-[12.5px] font-semibold text-white">
            <span className="td-live inline-flex h-1.5 w-1.5 rounded-full bg-brand" aria-hidden="true" />
            {title ?? "Reference architecture"}
          </figcaption>
          <span className="rounded-full border border-white/15 px-2.5 py-0.5 text-[9.5px] font-semibold uppercase tracking-[0.18em] text-white/55">
            Achala IT Solutions · live schematic
          </span>
        </div>
        <div className="td-canvas bg-navy-900">
          <Cmp labels={labels ?? []} />
        </div>
        {note && (
          <p className="border-t border-line bg-mist px-4 py-2.5 text-[11.5px] leading-relaxed text-slate-body/75">{note}</p>
        )}
      </figure>
    </Reveal>
  );
}
