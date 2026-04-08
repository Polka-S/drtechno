"use client";

import { useCallback } from "react";

import { BrandBase } from "@/types/brand";
import Carousel from "@/components/Carousel";
import SkeletonBrandCard from "@/components/SkeletonBrand";
import BrandCard from "@/components/BrandCard";


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