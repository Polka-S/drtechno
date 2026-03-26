"use client";

import { useCallback } from "react";

import Carousel from "./Carousel";
import { BrandBase } from "@/types/brand";
import SkeletonBrandCard from "./SkeletonBrand";
import BrandCard from "./BrandCard";


const BrandsCarousel = () => {
  const fetchBrands = useCallback(async () => {
    const res = await fetch("/api/brands", {
      method: "GET",
    })
    if (!res.ok) throw new Error(`HTTP error: ${res.status}`);
    
    return res.json()
  }, [])

  return (
    <Carousel<BrandBase>
      fetchData={fetchBrands}
      renderItem={(brand) => <BrandCard key={brand.id} brand={brand} />}
      renderSkeleton={(key) => <SkeletonBrandCard key={key}/>}
      maxVisibleCount={6}
    />
  )
}

export default BrandsCarousel;