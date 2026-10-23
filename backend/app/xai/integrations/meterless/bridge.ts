import { readFileSync } from "node:fs";
import { WorldModel } from "./vendor/src/index.ts";

type JobRecord = {
  job_id: string;
  job_title: string;
  company: string;
  required_skills: string[];
  collected_at: string;
  source_type: string;
  source_url?: string | null;
};

async function main() {
  const inputPath = process.argv[2];

  if (!inputPath) {
    throw new Error("Usage: careerbridge-bridge.ts <jobs.json>");
  }

  const jobs = JSON.parse(
    readFileSync(inputPath, "utf8")
  ) as JobRecord[];

  if (!Array.isArray(jobs)) {
    throw new Error("Input must be an array of jobs");
  }

  const world = new WorldModel({
    namespace: "careerbridge-xai",
    storage: "memory",
  });

  const observations = jobs.map((job) => {
    const at = new Date(job.collected_at).toISOString();

    return {
      externalId: `zetaris:${job.job_id}`,
      type: "job",
      title: job.job_title,
      text: JSON.stringify({
        company: job.company,
        required_skills: job.required_skills,
        source_type: job.source_type,
        source_url: job.source_url ?? null,
      }),
      at,
      source: {
        kind: "pipeline" as const,
        by: "careerbridge-zetaris-evidence-agent",
        at,
        ...(job.source_url ? { url: job.source_url } : {}),
      },
      entities: job.required_skills.map((skill) => ({
        type: "skill",
        name: skill,
      })),
    };
  });

  const first = await world.ingest(observations);
  const second = await world.ingest(observations);

  const state = world.stateShape() as {
    entities: Array<{
      id: string;
      type: string;
      name?: string;
      source: {
        kind: string;
        by?: string;
        at: string;
      };
    }>;
    relationships: Array<{
      from: string;
      to: string;
      type: string;
    }>;
  };

  const evidenceGraph = {
    jobs: state.entities
      .filter((entity) => entity.type === "job")
      .map((job) => ({
        id: job.id,
        title: job.name,
        provenance: job.source,
        skills: state.relationships
          .filter((rel) => rel.from === job.id && rel.type === "mentions")
          .map((rel) => state.entities.find((entity) => entity.id === rel.to))
          .filter((entity) => entity?.type === "skill")
          .map((entity) => entity!.name),
      })),
    relationship_count: state.relationships.length,
  };

  console.log(JSON.stringify({
    engine: "Meterless World Model",
    jobs_received: jobs.length,
    evidence_graph: evidenceGraph,
    first_ingest: {
      processed: first.processed,
      skipped_unchanged: first.skippedUnchanged,
    },
    second_ingest: {
      processed: second.processed,
      skipped_unchanged: second.skippedUnchanged,
      changed: second.changed,
    },
  }, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
