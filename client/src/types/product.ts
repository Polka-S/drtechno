export interface ProductBase {
  id: number;
  name: string;
  slug: string;
  price: number | null;
  newPrice: number | null;
  isInStock: boolean;
  imagePath: string;
}