"use client";

import { useState } from "react";
import Link from "next/link";
import { AlertTriangle, Loader, Search } from "lucide-react";

import { ActiveTool, Editor } from "@/features/editor/types";
import { ToolSidebarClose } from "@/features/editor/components/tool-sidebar-close";
import { ToolSidebarHeader } from "@/features/editor/components/tool-sidebar-header";

import { unsplash } from "@/lib/unsplash";

import { cn } from "@/lib/utils";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

interface UnsplashImage {
  id: string;
  urls: { regular: string; small: string; thumb: string };
  alt_description: string | null;
  links: { html: string };
  user: { name: string };
}

interface ImageSidebarProps {
  editor: Editor | undefined;
  activeTool: ActiveTool;
  onChangeActiveTool: (tool: ActiveTool) => void;
}

export const ImageSidebar = ({ editor, activeTool, onChangeActiveTool }: ImageSidebarProps) => {
  const [query, setQuery] = useState("");
  const [images, setImages] = useState<UnsplashImage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const onSearch = async () => {
    if (!query.trim()) return;
    setIsLoading(true);
    setIsError(false);
    setHasSearched(true);
    try {
      const result = await unsplash.search.getPhotos({
        query: query.trim(),
        perPage: 20,
      });
      if (result.response) {
        setImages(result.response.results as unknown as UnsplashImage[]);
      }
    } catch {
      setIsError(true);
    } finally {
      setIsLoading(false);
    }
  };

  const onClose = () => {
    onChangeActiveTool("select");
  };

  return (
    <aside
      className={cn(
        "bg-white relative border-r z-[40] w-[360px] h-full flex flex-col",
        activeTool === "images" ? "visible" : "hidden",
      )}
    >
      <ToolSidebarHeader title="Images" description="Search Unsplash for images" />
      <div className="p-4 border-b">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            onSearch();
          }}
          className="flex gap-x-2"
        >
          <Input
            placeholder="Search images..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <Button type="submit" size="icon" variant="secondary">
            <Search className="size-4" />
          </Button>
        </form>
      </div>
      {isLoading && (
        <div className="flex items-center justify-center flex-1">
          <Loader className="size-4 text-muted-foreground animate-spin" />
        </div>
      )}
      {isError && (
        <div className="flex flex-col gap-y-4 items-center justify-center flex-1">
          <AlertTriangle className="size-4 text-muted-foreground" />
          <p className="text-muted-foreground text-xs">Failed to fetch images</p>
        </div>
      )}
      {!isLoading && !isError && hasSearched && images.length === 0 && (
        <div className="flex items-center justify-center flex-1">
          <p className="text-muted-foreground text-xs">No images found</p>
        </div>
      )}
      <ScrollArea>
        <div className="p-4">
          <div className="grid grid-cols-2 gap-4">
            {images.map((image) => (
              <button
                onClick={() => editor?.addImage(image.urls.regular)}
                key={image.id}
                className="relative w-full h-[100px] group hover:opacity-75 transition bg-muted rounded-sm overflow-hidden border"
              >
                <img
                  src={image.urls.small || image.urls.thumb}
                  alt={image.alt_description || "Image"}
                  className="object-cover w-full h-full"
                  loading="lazy"
                />
                <Link
                  target="_blank"
                  href={image.links.html}
                  className="opacity-0 group-hover:opacity-100 absolute left-0 bottom-0 w-full text-[10px] truncate text-white hover:underline p-1 bg-black/50 text-left"
                >
                  {image.user.name}
                </Link>
              </button>
            ))}
          </div>
        </div>
      </ScrollArea>
      <ToolSidebarClose onClick={onClose} />
    </aside>
  );
};
