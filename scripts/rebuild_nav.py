"""Rebuild nav.json: professional mega structure, real URLs only (no 404s)."""
import json

old = json.load(open('/home/z/my-project/site/src/content/nav.json'))['nav']
old_primary = {it['label']: it for it in old['primary']}

# keep services tower children as-is (they were correct)
svc_children = {}
for col in old_primary['Services']['mega']:
    svc_children[col['label']] = col.get('children', [])

def col(label, url, children=None):
    return {"label": label, "url": url, **({"children": children} if children is not None else {})}

INS = "/insights/insight-%02d/"

nav = {
  "nav": {
    "primary": [
      {"label": "Services", "url": "/services/", "mega": [
        col(l, u, svc_children.get(l, [])) for l, u in [
          ("Applied AI & Generative AI", "/services/applied-ai-generative-ai/"),
          ("Agentic AI & Hyperautomation", "/services/agentic-ai-hyperautomation/"),
          ("Data, Analytics & Lakehouse", "/services/data-analytics-lakehouse/"),
          ("Cybersecurity & Zero-Trust", "/services/cybersecurity-zero-trust/"),
          ("Cloud, Edge & Platform Engineering", "/services/cloud-edge-platform-engineering/"),
          ("Quantum & Advanced Compute", "/services/quantum-advanced-compute/"),
          ("Blockchain & Digital Trust", "/services/blockchain-digital-trust/"),
          ("IoT, Digital Twin & Robotics", "/services/iot-digital-twin-robotics/"),
        ]
      ]},
      {"label": "Industries", "url": "/industries/", "mega": [
        col("Financial Services & Insurance", "/industries/banking-financial-services/", [
          {"label": "Banking & Financial Services", "url": "/industries/banking-financial-services/"},
          {"label": "Insurance & Risk", "url": "/industries/insurance/"},
        ]),
        col("Health, Public Sector & Education", "/industries/healthcare-life-sciences/", [
          {"label": "Healthcare & Life Sciences", "url": "/industries/healthcare-life-sciences/"},
          {"label": "Public Sector & Government", "url": "/industries/public-sector/"},
          {"label": "Education & Research", "url": "/industries/education-research/"},
        ]),
        col("Industry, Retail & Commerce", "/industries/manufacturing/", [
          {"label": "Manufacturing & Industrial", "url": "/industries/manufacturing/"},
          {"label": "Retail & Consumer Goods", "url": "/industries/retail-consumer-goods/"},
          {"label": "Telecom, Media & Entertainment", "url": "/industries/telecom-media/"},
          {"label": "Logistics & Supply Chain", "url": "/industries/logistics-supply-chain/"},
        ]),
        col("Energy, Infrastructure & Technology", "/industries/energy-utilities/", [
          {"label": "Energy & Utilities", "url": "/industries/energy-utilities/"},
          {"label": "Technology & SaaS", "url": "/industries/technology-saas/"},
          {"label": "Agriculture & Food Systems", "url": "/industries/agriculture-food/"},
        ]),
      ]},
      {"label": "Solutions", "url": "/solutions/", "mega": [
        col("Growth & Revenue", "/solutions/dynamic-pricing/", [
          {"label": "Dynamic Pricing & Revenue Intelligence", "url": "/solutions/dynamic-pricing/"},
          {"label": "Digital Commerce & Experience", "url": "/solutions/digital-commerce/"},
          {"label": "Customer 360 & Hyper-Personalization", "url": "/solutions/customer-360/"},
          {"label": "Marketing Intelligence & CX", "url": "/solutions/marketing-intelligence/"},
          {"label": "New Digital Ventures", "url": "/solutions/digital-ventures/"},
        ]),
        col("Risk & Resilience", "/solutions/fraud-decisioning/", [
          {"label": "Fraud & Financial Crime Decisioning", "url": "/solutions/fraud-decisioning/"},
          {"label": "Cyber Resilience & Threat Command", "url": "/solutions/cyber-resilience-program/"},
          {"label": "Enterprise Risk & Scenario Intelligence", "url": "/solutions/enterprise-risk-analytics/"},
          {"label": "ESG Reporting & Sustainable Ops", "url": "/solutions/esg-operations/"},
        ]),
        col("Operational Excellence", "/solutions/process-automation-scale/", [
          {"label": "Intelligent Process Automation at Scale", "url": "/solutions/process-automation-scale/"},
          {"label": "Autonomous Supply Chain Control Tower", "url": "/solutions/autonomous-supply-chain/"},
          {"label": "Predictive Maintenance & Assets", "url": "/solutions/predictive-asset-program/"},
          {"label": "Quality, Yield & Energy Intelligence", "url": "/solutions/quality-yield-energy/"},
          {"label": "AIOps & Autonomous IT Operations", "url": "/solutions/aiops-autonomous-it/"},
        ]),
        col("Workforce & Experience", "/solutions/enterprise-copilots/", [
          {"label": "Enterprise Copilots & Digital Workplace", "url": "/solutions/enterprise-copilots/"},
          {"label": "Contact Center & Conversational AI", "url": "/solutions/contact-center-transformation/"},
          {"label": "Citizen & Patient Experience", "url": "/solutions/citizen-patient-experience/"},
          {"label": "Frontline Mobile & Field Enablement", "url": "/solutions/frontline-enablement/"},
          {"label": "Knowledge & Collaboration Fabric", "url": "/solutions/knowledge-collaboration-fabric/"},
        ]),
      ]},
      {"label": "Platforms", "url": "/platforms/", "mega": [
        col("Achala Nexus — Decision Intelligence", "/platforms/nexus/", [
          {"label": "Overview", "url": "/platforms/nexus/"},
          {"label": "Architecture & Trust", "url": "/platforms/nexus/architecture/"},
          {"label": "Use cases", "url": "/platforms/nexus/use-cases/"},
        ]),
        col("Achala Forge — Data & Lakehouse", "/platforms/forge/", [
          {"label": "Overview", "url": "/platforms/forge/"},
          {"label": "Architecture & Trust", "url": "/platforms/forge/architecture/"},
          {"label": "Use cases", "url": "/platforms/forge/use-cases/"},
        ]),
        col("Achala Swarm — Agent Orchestration", "/platforms/swarm/", [
          {"label": "Overview", "url": "/platforms/swarm/"},
          {"label": "Architecture & Trust", "url": "/platforms/swarm/architecture/"},
          {"label": "Use cases", "url": "/platforms/swarm/use-cases/"},
        ]),
        col("Achala Sentinel — Security Fabric", "/platforms/sentinel/", [
          {"label": "Overview", "url": "/platforms/sentinel/"},
          {"label": "Architecture & Trust", "url": "/platforms/sentinel/architecture/"},
          {"label": "Use cases", "url": "/platforms/sentinel/use-cases/"},
        ]),
        col("Achala Twinverse — Digital Twin Ops", "/platforms/twinverse/", [
          {"label": "Overview", "url": "/platforms/twinverse/"},
          {"label": "Architecture & Trust", "url": "/platforms/twinverse/architecture/"},
          {"label": "Use cases", "url": "/platforms/twinverse/use-cases/"},
        ]),
        col("Achala Quanta — Advanced Compute", "/platforms/quanta/", [
          {"label": "Overview", "url": "/platforms/quanta/"},
          {"label": "Architecture & Trust", "url": "/platforms/quanta/architecture/"},
          {"label": "Use cases", "url": "/platforms/quanta/use-cases/"},
        ]),
        col("Achala Ledger — Digital Trust", "/platforms/ledger/", [
          {"label": "Overview", "url": "/platforms/ledger/"},
          {"label": "Architecture & Trust", "url": "/platforms/ledger/architecture/"},
          {"label": "Use cases", "url": "/platforms/ledger/use-cases/"},
        ]),
        col("Achala Compass — AI Governance", "/platforms/compass/", [
          {"label": "Overview", "url": "/platforms/compass/"},
          {"label": "Architecture & Trust", "url": "/platforms/compass/architecture/"},
          {"label": "Use cases", "url": "/platforms/compass/use-cases/"},
        ]),
      ]},
      {"label": "Case Studies", "url": "/case-studies/"},
      {"label": "Insights", "url": "/insights/", "mega": [
        col("AI & Data viewpoints", "/insights/applied-ai-generative-ai/", [
          {"label": "Applied AI & GenAI", "url": "/insights/applied-ai-generative-ai/"},
          {"label": "Data & Lakehouse", "url": "/insights/data-analytics-lakehouse/"},
          {"label": "The retrieval layer is the moat", "url": INS % 1},
          {"label": "GenAI unit economics", "url": INS % 2},
        ]),
        col("Automation & operations viewpoints", "/insights/agentic-ai-hyperautomation/", [
          {"label": "Agentic AI & Hyperautomation", "url": "/insights/agentic-ai-hyperautomation/"},
          {"label": "Decision hubs beat model sprawl", "url": INS % 5},
          {"label": "Process mining: cheapest AI you will buy", "url": INS % 6},
        ]),
        col("Security, cloud & trust viewpoints", "/insights/cybersecurity-zero-trust/", [
          {"label": "Cyber & Zero-Trust", "url": "/insights/cybersecurity-zero-trust/"},
          {"label": "Cloud, Edge & Platform", "url": "/insights/cloud-edge-platform-engineering/"},
          {"label": "Blockchain & Digital Trust", "url": "/insights/blockchain-digital-trust/"},
        ]),
        col("Emerging compute viewpoints", "/insights/quantum-advanced-compute/", [
          {"label": "Quantum & Advanced Compute", "url": "/insights/quantum-advanced-compute/"},
          {"label": "IoT, Digital Twin & Robotics", "url": "/insights/iot-digital-twin-robotics/"},
          {"label": "All insights", "url": "/insights/"},
        ]),
      ]},
      {"label": "About Us", "url": "/about-us/", "mega": [
        col("Company", "/about-us/", [
          {"label": "About Achala IT Solutions", "url": "/about-us/"},
          {"label": "Why Achala IT Solutions", "url": "/why-achala-soft/"},
          {"label": "Values & Culture", "url": "/values-culture/"},
          {"label": "Leadership", "url": "/leadership/"},
          {"label": "Global Offices", "url": "/global-offices/"},
        ]),
        col("Our Approach", "/our-approach/the-achala-method/", [
          {"label": "The Achala Method", "url": "/our-approach/the-achala-method/"},
          {"label": "Outcome-Linked Engagements", "url": "/our-approach/outcome-linked-engagements/"},
          {"label": "Responsible AI Framework", "url": "/our-approach/responsible-ai-framework/"},
          {"label": "Global Delivery Model", "url": "/our-approach/global-delivery-model/"},
          {"label": "Patented Intelligence", "url": "/patented-intelligence/"},
        ]),
        col("Join & Contact", "/careers/", [
          {"label": "Careers", "url": "/careers/"},
          {"label": "Newsroom", "url": "/newsroom/"},
          {"label": "Partner Ecosystem", "url": "/partner-ecosystem/"},
          {"label": "Contact", "url": "/contact/"},
          {"label": "System Status", "url": "/status/"},
        ]),
      ]},
    ],
    "cta": old.get('cta') or {"label": "Book a Briefing", "url": "/book-a-briefing/"},
  }
}

# verify every URL exists in the page index
import glob, os
urls = set()
for f in glob.glob('/home/z/my-project/site/src/content/pages/*.json'):
    d = json.load(open(f))
    urls.add(d['url'])
missing = []
def chk(u):
    if u not in urls:
        missing.append(u)
chk(nav['nav']['cta']['url'])
for it in nav['nav']['primary']:
    chk(it['url'])
    for c in it.get('mega', []):
        chk(c['url'])
        for ch in c.get('children', []):
            chk(ch['url'])
print('MISSING URLS:', missing if missing else 'none — all resolve')
json.dump(nav, open('/home/z/my-project/site/src/content/nav.json', 'w'), indent=1, ensure_ascii=False)
print('nav.json rebuilt')
