import { ModulePage } from "@/components/module-page";

export default async function CatchAllModulePage({
  params,
}: {
  params: Promise<{ module: string[] }>;
}) {
  const { module } = await params;
  return <ModulePage slug={module} />;
}

