import re
import json
def normalize_price(price):
    price = price.strip()
    price = price.replace("\n", "")
    price = price.replace(" ", "")
    price = price.replace(",", ".")
    return float(price)
def extract_prices(txt):
    pattern = r"x\s*(\d[\d\s]*,\d{2})"
    prices = re.findall(pattern, txt)
    return [normalize_price(p) for p in prices]
def extract_products(txt):
    pattern = r"\d+\.\n(.+?)\n\d+,\d{3}\s*x"
    products = re.findall(pattern, txt)
    return [p.strip() for p in products]
def extract_total(txt):
    match = re.search(r"ИТОГО:\s*\n([\d\s]+,\d{2})", txt)
    if match:
        return normalize_price(match.group(1))
    return None
def extract_datetime(txt):
    match = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})", txt)
    if match:
        return {
            "date": match.group(1),
            "time": match.group(2)
        }
    return None
def extract_payment_method(txt):
    match = re.search(r"(Банковская карта|Наличные)", txt)
    if match:
        return match.group(1)
    return "Unknown"
def parse_receipt(txt):
    prices = extract_prices(txt)
    products = extract_products(txt)
    total = extract_total(txt)
    datetime_info = extract_datetime(txt)
    payment = extract_payment_method(txt)
    return {
        "products": products,
        "prices": prices,
        "total": total,
        "payment_method": payment,
        "datetime": datetime_info
    }
def main():
    with open("raw.txt", "r", encoding="utf-8") as f:
        txt = f.read()
    data = parse_receipt(txt)
    print(json.dumps(data, indent=4, ensure_ascii=False))
if __name__ == "__main__":
    main()