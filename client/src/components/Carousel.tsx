"use client";
import { useCallback, useEffect, useState } from "react";
import { CircleChevronLeft, CircleChevronRight } from "lucide-react";
import { motion, useMotionValue, useTransform, animate } from "framer-motion";

import { ProductBase } from '@/types/product';
import ProductCardCompact from "./ProductCardCompact";
import SkeletonProductCard from "./SkeletonProductCard";


const Carousel = () => {
  const [products, setProducts] = useState<ProductBase[]>([]);
  const [error, setError] = useState<Error | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [startIndex, setStartIndex] = useState<number>(0);
  const [visibleCount, setVisibleCount] = useState<number>(3);

  const updateVisibleCount = useCallback(() => {
    const width = window.innerWidth;
    if (width >= 1280) {
      setVisibleCount(5);
    } else if (width >= 1024) {
      setVisibleCount(4);
    } else if (width >= 820) {
      setVisibleCount(3);
    } else if (width >= 600) {
      setVisibleCount(2);
    } else {
      setVisibleCount(1);
    }
  }, [])

  useEffect(() => {
    updateVisibleCount();
    window.addEventListener("resize", updateVisibleCount);
    return () => window.removeEventListener("resize", updateVisibleCount);
  }, [updateVisibleCount]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // await new Promise(resolve => setTimeout(resolve, 2000))
        const response = await fetch("/api/products/top?limit=30")
        if (!response.ok) {
          throw new Error(`HTTP error: Status ${response.status}`);
        }

        const result: ProductBase[] = await response.json();
        setProducts(result);
        setError(null);
      } catch (err){
        err instanceof Error ? setError(err) : setError(new Error('Unknown error'));
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    if (products.length === 0) return;
    const maxStartIndex = Math.max(0, products.length - visibleCount);
    if (startIndex > maxStartIndex) {
      setStartIndex(maxStartIndex);
    }
  }, [visibleCount, products])

  const goToPrev = () => {
    if (startIndex === 0) {
      setStartIndex(products.length - 1)
    } else {
      setStartIndex(prevStartindex => prevStartindex - 1)
    }
  }

  const goToNext = () => {
    if (startIndex === products.length - 1) {
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
        <div className="products grid grid-flow-col gap-3 overflow-hidden flex-1 auto-cols-fr">
          {Array.from({ length: visibleCount }).map((_, idx) => (
            <SkeletonProductCard key={idx} />
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

  if (products.length === 0) {
    return <div className="text-gray-500">Товары не найдены</div>;
  }

  const visibleProducts = products.slice(startIndex, startIndex + visibleCount);

  const isPrevDisabled = startIndex === 0;
  const isNextDisabled = startIndex + visibleCount >= products.length;
  

  return (
    <div className="carousel flex flex-row justify-between items-center gap-4">
      <button
        onClick={goToPrev}
        disabled={isPrevDisabled}
        className="cursor-pointer disabled:opacity-50 disabled:cursor-default"
      >
        <CircleChevronLeft />
      </button>
      <div className="products grid grid-flow-col gap-3 overflow-hidden flex-1 auto-cols-fr">
        {visibleProducts.map((product) => (
          <ProductCardCompact key={product.id} product={product} />
        ))}
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

export default Carousel;