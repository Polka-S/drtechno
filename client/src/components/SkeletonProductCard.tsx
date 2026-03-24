const SkeletonProductCard = () => {
  return (
    <div className="block bg-white rounded-xl shadow-md overflow-hidden animate-pulse">
      <div className="relative aspect-square w-full bg-gray-200">
        <div className="absolute inset-0 bg-gray-300"></div>
      </div>
      <div className="p-4 space-y-2">
        <div className="h-5 bg-gray-300 rounded w-3/4"></div>
        <div className="h-4 bg-gray-300 rounded w-1/2"></div>
        <div className="flex items-baseline gap-2 mt-2">
          <div className="h-6 bg-gray-300 rounded w-1/3"></div>
          <div className="h-4 bg-gray-300 rounded w-1/4"></div>
        </div>
      </div>
    </div>
  );
};

export default SkeletonProductCard;