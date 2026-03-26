"use client";
import { useCallback } from "react";

import { ProductBase } from '@/types/product';
import ProductCardCompact from "./ProductCardCompact";
import SkeletonProductCard from "./SkeletonProductCard";
import Carousel from "./Carousel";


const TopProductsCarousel = () => {
  const fetchProducts = useCallback(async () => {
    const res = await fetch("/api/products/top?limit=30", {
      method: "GET",
    });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    
    return res.json();
  }, []);

  return (
    <Carousel<ProductBase>
      fetchData={fetchProducts}
      renderItem={(product) => <ProductCardCompact key={product.id} product={product} />}
      renderSkeleton={(key) => <SkeletonProductCard key={key} />}
    />
  )
}

export default TopProductsCarousel;