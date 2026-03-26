"use client";
import React, { useCallback, useEffect, useState } from "react";
import { CircleChevronLeft, CircleChevronRight } from "lucide-react";


interface CarouselProps<T> {
  fetchData: () => Promise<T[]>;
  renderItem: (item: T, index: number) => React.ReactNode;
  renderSkeleton: (key: number) => React.ReactNode;
  maxVisibleCount?: number;
}

export default function Carousel<T>({
  fetchData,
  renderItem,
  renderSkeleton: RenderSkeleton,
  maxVisibleCount = 5,
}: CarouselProps<T>) {
  const [items, setItems] = useState<T[]>([]);
  const [error, setError] = useState<Error | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [startIndex, setStartIndex] = useState<number>(0);
  const [visibleCount, setVisibleCount] = useState<number>(3);

  const updateVisibleCount = useCallback(() => {
    const width = window.innerWidth;
    if (width >= 1280) setVisibleCount(maxVisibleCount);
    else if (width >= 1024) setVisibleCount(maxVisibleCount - 1);
    else if (width >= 820) setVisibleCount(maxVisibleCount - 2);
    else if (width >= 600) setVisibleCount(maxVisibleCount - 3);
    else setVisibleCount(maxVisibleCount - 4);
  }, [])

  useEffect(() => {
    updateVisibleCount();
    window.addEventListener("resize", updateVisibleCount);
    return () => window.removeEventListener("resize", updateVisibleCount);
  }, [updateVisibleCount]);

  useEffect(() => {
    const load = async () => {
      try {
        setIsLoading(true);
        const data = await fetchData();
        setItems(data);
        setError(null);
      } catch (err){
        err instanceof Error ? setError(err) : setError(new Error('Unknown error'));
      } finally {
        setIsLoading(false);
      }
    };

    load();
  }, [fetchData]);

  useEffect(() => {
    if (items.length === 0) return;
    const maxStartIndex = Math.max(0, items.length - visibleCount);
    if (startIndex > maxStartIndex) {
      setStartIndex(maxStartIndex);
    }
  }, [visibleCount, items.length, startIndex]);

  const goToPrev = () => {
    if (startIndex === 0) {
      setStartIndex(items.length - 1)
    } else {
      setStartIndex(prevStartindex => prevStartindex - 1)
    }
  }

  const goToNext = () => {
    if (startIndex === items.length - 1) {
      setStartIndex(0)
    } else {
      setStartIndex(prevStartindex => prevStartindex + 1)
    }
  }

  if (isLoading) {
    return (
      <div className="carousel flex flex-row justify-between items-center gap-4">
        <button className="cursor-pointer disabled:opacity-50" disabled>
          <CircleChevronLeft />
        </button>
        <div className="items grid grid-flow-col gap-2 overflow-hidden flex-1 auto-cols-fr">
          {Array.from({ length: visibleCount }).map((_, idx) => (
            RenderSkeleton(idx)
          ))}
        </div>
        <button className="cursor-pointer disabled:opacity-50" disabled>
          <CircleChevronRight />
        </button>
      </div>
    )
  }

  if (error) {
    return <div className="text-red-500">Ошибка: {error.message}</div>;
  }

  if (items.length === 0) {
    return <div className="text-gray-500">Товары не найдены</div>;
  }

  const visibleItems = items.slice(startIndex, startIndex + visibleCount);

  const isPrevDisabled = startIndex === 0;
  const isNextDisabled = startIndex + visibleCount >= items.length;
  

  return (
    <div className="carousel flex flex-row justify-between items-center gap-4">
      <button
        onClick={goToPrev}
        disabled={isPrevDisabled}
        className="cursor-pointer disabled:opacity-50 disabled:cursor-default"
      >
        <CircleChevronLeft />
      </button>
      <div className="items grid grid-flow-col gap-2 overflow-hidden flex-1 auto-cols-fr">
        {visibleItems.map((item, idx) => renderItem(item, idx))}
      </div>
      <button
        onClick={goToNext}
        disabled={isNextDisabled}
        className="cursor-pointer -default disabled:opacity-50 disabled:cursor-default"
      >
        <CircleChevronRight />
      </button>
    </div>
  );
};