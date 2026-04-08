import Image from "next/image";
import Link from "next/link";

import Button from "@/components/Button";
import { ProductBase } from "@/types/product";


const ProductCardCompact = ({ product } : { product: ProductBase }) => {
  const formatPrice = (price: number | null) => {
    if (!price) return null;
    return new Intl.NumberFormat("ru-RU", {
      style: "currency",
      currency: "RUB",
      minimumFractionDigits: 0,
    }).format(price);
  }

  const currentPrice = product.newPrice ?? product.price;
  const oldPrice = product.newPrice ? product.price : null;
  const discount = oldPrice && currentPrice
    ? Math.round(((oldPrice - currentPrice) / oldPrice) * 100)
    : null;
  
  return (
    <Link
      href={`${product.slug ? `/${product.slug}` : "#"}`}
      className="group block bg-white rounded-xl m-px shadow-sm hover:shadow-2xl transition-shadow duration-300 overflow-hidden"
    >
      <div className="relative aspect-square w-full bg-gray-100 overflow-hidden">
        {product.imagePath ? (
          <Image
            src={product.imagePath}
            alt={product.name}
            fill
            className="object-contain group-hover:scale-103 transition-transform duration-300"
          />
        ) : (
          <Image
            src="/no-photo.png"
            alt={product.name}
            fill
            className="object-contain group-hover:scale-103 transition-transform duration-300"
          />
        )}
      </div>
      <div className="name p-4">
        <h3 className="text-lg font-medium text-gray-900 line-clamp-2 mb-2">
          {product.name}
        </h3>

        <div className="content flex flex-col gap-2">
          <div className="price flex flex-wrap items-baseline justify-between gap-1 sm:flex-nowrap">
            {currentPrice && (
              <span className="text-xl font-bold text-gray-900">
                {formatPrice(currentPrice)}
              </span>
            )}
            {oldPrice && (
              <span className="text-sm text-gray-500 line-through">
                {formatPrice(oldPrice)}
              </span>
            )}
            {discount && (
              <span className="ml-auto bg-red-700 text-white text-xs font-semibold px-2 py-1 rounded-full">
                -{discount}%
              </span>
            )}
          </div>
          <div className="buy">
            <Button disabled={!product.isInStock}>Купить</Button>
          </div>
        </div>
      </div>
    </Link>
  );
};

export default ProductCardCompact;