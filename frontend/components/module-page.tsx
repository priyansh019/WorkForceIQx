import { Card } from "@/components/ui/card";

const moduleCopy: Record<string, { title: string; phase: string; scope: string }> = {
  employees: {
    title: "Employee Intelligence",
    phase: "Phase 2",
    scope: "employee CRUD, profiles, attendance, engagement, training, and evidence-backed observations",
  },
  recruitment: {
    title: "AI Recruitment Intelligence",
    phase: "Phase 3",
    scope: "jobs, candidates, resume parsing, candidate-job alignment, and interview preparation",
  },
  onboarding: {
    title: "Adaptive Onboarding",
    phase: "Phase 7",
    scope: "role-aware onboarding plans, task ownership, deadlines, and completion tracking",
  },
  policies: {
    title: "HR Policy Reasoning",
    phase: "Phase 4",
    scope: "document upload, chunking, embeddings, semantic retrieval, and cited policy answers",
  },
  performance: {
    title: "AI Performance Intelligence",
    phase: "Phase 8",
    scope: "source-backed summaries that separate facts from interpretation",
  },
  skills: {
    title: "Workforce Skill Graph",
    phase: "Phase 9",
    scope: "React Flow skill graph, role gaps, training paths, and department filters",
  },
  insights: {
    title: "AI Workforce Insights",
    phase: "Phase 6",
    scope: "cross-source insight generation, confidence, recommendations, and AI evidence drawer",
  },
  recommendations: {
    title: "Recommendations",
    phase: "Phase 6",
    scope: "human-reviewable recommendation queue with evidence and status workflow",
  },
  documents: {
    title: "Documents",
    phase: "Phase 4",
    scope: "policy, resume, and HR document ingestion with upload validation",
  },
  settings: {
    title: "Settings",
    phase: "Phase 12",
    scope: "environment, role, and deployment configuration surfaces",
  },
};

export function ModulePage({ slug }: { slug: string[] }) {
  const moduleKey = slug[0] ?? "dashboard";
  const module = moduleCopy[moduleKey] ?? {
    title: "WorkForceIQ Workspace",
    phase: "Planned phase",
    scope: "this route is reserved in the application architecture",
  };

  return (
    <div className="mx-auto max-w-5xl">
      <Card>
        <div className="text-sm font-semibold text-primary">{module.phase}</div>
        <h1 className="mt-2 text-2xl font-semibold">{module.title}</h1>
        <p className="mt-3 max-w-3xl text-sm leading-6 text-muted-foreground">{module.scope}</p>
        <div className="mt-6 rounded-md border border-border bg-background p-4 text-sm">
          Phase 1 has created the protected route, navigation entry, backend model foundations,
          and authentication boundary this module will use.
        </div>
      </Card>
    </div>
  );
}

