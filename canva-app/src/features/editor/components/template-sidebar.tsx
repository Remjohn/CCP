"use client";

import { AlertTriangle, Loader } from "lucide-react";
import { useEffect, useState } from "react";

import {
  ActiveTool,
  Editor,
} from "@/features/editor/types";
import { ToolSidebarClose } from "@/features/editor/components/tool-sidebar-close";
import { ToolSidebarHeader } from "@/features/editor/components/tool-sidebar-header";

import { listTemplates, Template } from "@/lib/ccp-client";

import { cn } from "@/lib/utils";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useConfirm } from "@/hooks/use-confirm";

interface TemplateSidebarProps {
  editor: Editor | undefined;
  activeTool: ActiveTool;
  onChangeActiveTool: (tool: ActiveTool) => void;
}

export const TemplateSidebar = ({
  editor,
  activeTool,
  onChangeActiveTool,
}: TemplateSidebarProps) => {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);

  const [ConfirmDialog, confirm] = useConfirm(
    "Are you sure?",
    "You are about to replace the current project with this template.",
  );

  useEffect(() => {
    if (activeTool !== "templates") return;
    setIsLoading(true);
    setIsError(false);
    listTemplates()
      .then((res) => setTemplates(res.templates))
      .catch(() => setIsError(true))
      .finally(() => setIsLoading(false));
  }, [activeTool]);

  const onClose = () => {
    onChangeActiveTool("select");
  };

  const onClick = async (template: Template) => {
    const ok = await confirm();
    if (ok && template.json) {
      editor?.loadJson(template.json as string);
    }
  };

  return (
    <aside
      className={cn(
        "bg-white relative border-r z-[40] w-[360px] h-full flex flex-col",
        activeTool === "templates" ? "visible" : "hidden",
      )}
    >
      <ConfirmDialog />
      <ToolSidebarHeader
        title="Templates"
        description="Choose from registered CCP templates"
      />
      {isLoading && (
        <div className="flex items-center justify-center flex-1">
          <Loader className="size-4 text-muted-foreground animate-spin" />
        </div>
      )}
      {isError && (
        <div className="flex flex-col gap-y-4 items-center justify-center flex-1">
          <AlertTriangle className="size-4 text-muted-foreground" />
          <p className="text-muted-foreground text-xs">Failed to fetch templates</p>
        </div>
      )}
      <ScrollArea>
        <div className="p-4">
          <div className="grid grid-cols-2 gap-4">
            {templates.map((template) => (
              <button
                onClick={() => onClick(template)}
                key={template.template_id}
                className="relative w-full group hover:opacity-75 transition bg-muted rounded-sm overflow-hidden border p-4"
              >
                <div className="text-xs font-medium truncate">
                  {template.template_id}
                </div>
              </button>
            ))}
          </div>
        </div>
      </ScrollArea>
      <ToolSidebarClose onClick={onClose} />
    </aside>
  );
};
