"use client";

import { useEffect, useState } from "react";
import { useParams, useSearchParams } from "next/navigation";
import { Loader } from "lucide-react";

import { Editor } from "@/features/editor/components/editor";
import { getComposition, Composition } from "@/lib/ccp-client";

const DEFAULT_COACH = "CCP";

export default function EditorPage() {
  const params = useParams<{ compositionId: string }>();
  const searchParams = useSearchParams();
  const coachAcronym = searchParams.get("coach") ?? DEFAULT_COACH;
  const [composition, setComposition] = useState<Composition | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!params.compositionId) return;
    setIsLoading(true);
    getComposition(params.compositionId, coachAcronym)
      .then((c) => setComposition(c))
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load composition"))
      .finally(() => setIsLoading(false));
  }, [params.compositionId]);

  if (isLoading) {
    return (
      <div className="h-full flex items-center justify-center">
        <Loader className="size-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-full flex items-center justify-center">
        <p className="text-destructive">{error}</p>
      </div>
    );
  }

  return (
    <Editor
      compositionId={params.compositionId}
      initialData={
        composition
          ? {
              width: composition.dimensions?.width_px ?? 1080,
              height: composition.dimensions?.height_px ?? 1350,
            }
          : undefined
      }
    />
  );
}
