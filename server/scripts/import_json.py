import json
import re
import os
from typing import Dict, Optional

from sqlalchemy.orm import Session
from slugify import slugify

from app.core.db import SessionLocal
from app.models import (
    Category,
    Brand,
    Product,
    Attribute,
    AttributeValue,
    ProductVariant,
    product_accessories
)


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

def get_or_create_attribute(db: Session, name: str) -> Attribute:
    """Находит или создаёт атрибут по имени."""
    slug = slugify(name)
    attr = db.query(Attribute).filter_by(slug=slug).first()
    if not attr:
        attr = Attribute(name=name, slug=slug)
        db.add(attr)
        db.flush()
    return attr

def get_or_create_attribute_value(db: Session, attribute: Attribute, value: str) -> AttributeValue:
    """Находит или создаёт значение атрибута."""

    attr_val = db.query(AttributeValue).filter_by(
        attribute_id=attribute.id, value=value
    ).first()
    if not attr_val:
        attr_val = AttributeValue(attribute_id=attribute.id, value=value)
        db.add(attr_val)
        db.flush()
    return attr_val

def link_product_attribute(product: Product, attr_value: AttributeValue):
    """Добавляет связь продукта со значением атрибута, если её ещё нет."""

    if attr_value not in product.attributes:
        product.attributes.append(attr_value)


def import_products(json_path: str):
    """Основная функция импорта."""
    
    db: Session = SessionLocal()
    with open(json_path, 'r', encoding='utf-8') as f:
        items = json.load(f)

    variants_by_source_id = {}

    try:
        for item in items:
            # Проверяем, существует ли уже вариант с таким article
            existing_variant = db.query(ProductVariant).filter_by(article=item['article']).first()
            if existing_variant:
                variants_by_source_id[item['id']] = existing_variant
                continue

            # Категория и бренд (оставляем как есть)
            category = get_or_create_category(db, item['category'])
            brand_name = item['name'].split()[0]
            brand = get_or_create_brand(db, brand_name)

            # Ищем продукт по имени (если нет – создаём)
            product = db.query(Product).filter_by(name=item['name']).first()
            if not product:
                product_slug = slugify(item['name']) + '-' + item['id']  # можно slug только по имени
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

            if item.get('features'):
                for attr_name, attr_value in item['features'].items():
                    if not attr_value:  # пропускаем пустые значения
                        continue
                    attr = get_or_create_attribute(db, attr_name)
                    
                    # Если значение — список (в ваших данных такого нет, но на всякий случай)
                    if isinstance(attr_value, list):
                        for v in attr_value:
                            attr_val = get_or_create_attribute_value(db, attr, str(v))
                            link_product_attribute(product, attr_val)
                    else:
                        attr_val = get_or_create_attribute_value(db, attr, str(attr_value))
                        link_product_attribute(product, attr_val)
            # Создаём вариант, привязанный к product
            variant = ProductVariant(
                product_id=product.id,
                color=item.get('features', {}).get('Цвет') or item.get('features', {}).get('Цвет корпуса'),
                normalized_color=item.get('features', {}).get('Нормализованный цвет'),
                price=extract_price(item.get('price')),
                new_price=extract_price(item.get('new_price')),
                article=item['article'],
                is_in_stock=item.get('is_in_stock', True),
                link=item.get('link'),
                source_id=item['id'],
            )
            db.add(variant)
            db.flush()
            variants_by_source_id[item['id']] = variant

        # Второй проход – связи аксессуаров (остаётся без изменений)
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

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error during import: {e}")
        raise
    finally:
        db.close()

# def import_products(json_path: str):
#     """Основная функция импорта."""
#     db: Session = SessionLocal()

#     with open(json_path, 'r', encoding='utf-8') as f:
#         items = json.load(f)

#     variants_by_source_id: Dict[str, ProductVariant] = {}

#     try:
#         for item in items:
#             category = get_or_create_category(db, item['category'])

#             brand_name = item['name'].split()[0]
#             brand = get_or_create_brand(db, brand_name)

#             product_slug = slugify(item['name']) + '-' + item['id']
#             product = Product(
#                 name=item['name'],
#                 slug=product_slug,
#                 description=item.get('description', []),
#                 features=item.get('features', {}),
#                 category_id=category.id,
#                 brand_id=brand.id,
#             )
#             db.add(product)
#             db.flush()

#             color = item.get('features', {}).get('Цвет') or item.get('features', {}).get('Цвет корпуса')
#             normalized = item.get('features', {}).get('Нормализованный цвет')

#             price = extract_price(item.get('price'))
#             new_price = extract_price(item.get('new_price')) if item.get('new_price') else None

#             variant = ProductVariant(
#                 product_id=product.id,
#                 color=color,
#                 normalized_color=normalized or color,
#                 price=price,
#                 new_price=new_price,
#                 article=item['article'],
#                 is_in_stock=item.get('is_in_stock', True),
#                 link=item.get('link'),
#                 source_id=item['id'],
#             )
#             db.add(variant)
#             db.flush()

#             variants_by_source_id[item['id']] = variant

#         for item in items:
#             if not item.get('accessories'):
#                 continue

#             current_variant = variants_by_source_id.get(item['id'])
#             if not current_variant:
#                 continue

#             for acc_link in item['accessories']:
#                 acc_source_id = extract_id_from_link(acc_link)
#                 if not acc_source_id:
#                     continue
#                 acc_variant = variants_by_source_id.get(acc_source_id)
#                 if acc_variant and acc_variant not in current_variant.accessories:
#                     current_variant.accessories.append(acc_variant)
#     except Exception as e:
#         db.rollback()
#         print(f"Error during import: {e} with item: {item}")
#         raise
#     db.commit()

#     db.close()


if __name__ == '__main__':
    JSON_FILE = 'db.json'

    import_products(JSON_FILE)