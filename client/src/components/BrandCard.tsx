import Link from "next/link";

import { BrandBase } from "@/types/brand"


const BrandCard = ({ brand } : {brand: BrandBase}) => {
  return (
    <Link
      href={`brand-card ${brand.slug ? `/${brand.slug}` : "#"}`}
      className="group block bg-gray-100 rounded-xl shadow-sm p-2 m-2 hover:shadow-md transition-shadow duration-300 overflow-hidden"
    >
      <div className="name">{brand.name}</div>
    </Link>
  )
};

export default BrandCard;

