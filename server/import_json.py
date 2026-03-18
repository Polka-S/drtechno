import json
import re
import os
from typing import Dict, Optional

from sqlalchemy.orm import Session
from slugify import slugify

from app.core.db import SessionLocal
from app.models import Category, Brand, Product, ProductVariant, product_accessories


def extract_price(price_str: str) -> Optional[float]:
    """Извлекает число из строки вида '67 990р.' или '65990р.'"""
    if not price_str:
        return None
    cleaned = re.sub(r'[^\d,.]', '', price_str.replace(' ', ''))
    cleaned = cleaned.replace(',', '.')
    try:
        return float(cleaned)
    except ValueError:
        return None


def extract_id_from_link(link: str) -> Optional[str]:
    """Извлекает числовой ID из ссылки вида 'https://...?Id=35645'"""
    match = re.search(r'[?&]Id=(\d+)', link, re.IGNORECASE)
    return match.group(1) if match else None


def get_or_create_category(db: Session, name: str) -> Category:
    """Возвращает существующую категорию или создаёт новую."""
    slug = slugify(name)
    category = db.query(Category).filter_by(slug=slug).first()
    if not category:
        category = Category(name=name, slug=slug)
        db.add(category)
        db.flush()
    return category


def get_or_create_brand(db: Session, name: str) -> Brand:
    """Возвращает существующий бренд или создаёт новый."""
    slug = slugify(name)
    brand = db.query(Brand).filter_by(slug=slug).first()
    if not brand:
        brand = Brand(name=name, slug=slug)
        db.add(brand)
        db.flush()
    return brand


def import_products(json_path: str):
    """Основная функция импорта."""
    db: Session = SessionLocal()

    with open(json_path, 'r', encoding='utf-8') as f:
        items = json.load(f)

    variants_by_source_id: Dict[str, ProductVariant] = {}

    try:
        for item in items:
            category = get_or_create_category(db, item['category'])

            brand_name = item['name'].split()[0]
            brand = get_or_create_brand(db, brand_name)

            product_slug = slugify(item['name']) + '-' + item['id']
            product = Product(
                name=item['name'],
                slug=product_slug,
                description=item.get('description', []),
                features=item.get('features', {}),
                category_id=category.id,
                brand_id=brand.id,
            )
            db.add(product)
            db.flush()

            color = item.get('features', {}).get('Цвет') or item.get('features', {}).get('Цвет корпуса')
            normalized = item.get('features', {}).get('Нормализованный цвет')

            price = extract_price(item.get('price'))
            new_price = extract_price(item.get('new_price')) if item.get('new_price') else None

            variant = ProductVariant(
                product_id=product.id,
                color=color,
                normalized_color=normalized or color,
                price=price,
                new_price=new_price,
                article=item['article'],
                is_in_stock=item.get('is_in_stock', True),
                link=item.get('link'),
                source_id=item['id'],
            )
            db.add(variant)
            db.flush()

            variants_by_source_id[item['id']] = variant

        for item in items:
            if not item.get('accessories'):
                continue

            current_variant = variants_by_source_id.get(item['id'])
            if not current_variant:
                continue

            for acc_link in item['accessories']:
                acc_source_id = extract_id_from_link(acc_link)
                if not acc_source_id:
                    continue
                acc_variant = variants_by_source_id.get(acc_source_id)
                if acc_variant and acc_variant not in current_variant.accessories:
                    current_variant.accessories.append(acc_variant)
    except Exception as e:
        db.rollback()
        print(f"Error during import: {e} with item: {item}")
        raise
    db.commit()

    db.close()


if __name__ == '__main__':
    JSON_FILE = 'db.json'

    import_products(JSON_FILE)