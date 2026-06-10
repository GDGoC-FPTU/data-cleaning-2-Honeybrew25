import json

INPUT_FILE = "toxic_sample.json"
OUTPUT_FILE = "sanitized_sample.json"
PRICE_THRESHOLD = 5000  # ngưỡng outlier


def mask_email(email):
    """vana@gmail.com -> v***@gmail.com"""
    if not email or "@" not in email:
        return email
    local, domain = email.split("@", 1)
    if not local:
        return email
    return local[0] + "***@" + domain


def challenge_1_mask_pii(records):
    """Bỏ hẳn field `name` và che `email`."""
    cleaned = []
    for r in records:
        r = dict(r)           # copy để không sửa bản gốc
        r.pop("name", None)   # 1. Remove name
        if "email" in r:
            r["email"] = mask_email(r["email"])  # 2. Mask email
        cleaned.append(r)
    return cleaned


def challenge_2_dedup_and_outliers(records):
    """Khử trùng theo id, loại outlier (giá > ngưỡng) và giá âm."""
    seen_ids = set()
    cleaned = []
    for r in records:
        rid = r.get("id")

        # 1. Deduplicate: mỗi id chỉ xuất hiện 1 lần
        if rid in seen_ids:
            continue
        seen_ids.add(rid)

        price = r.get("price", 0)

        # 3. Sanity check: bỏ giá âm
        if price < 0:
            continue

        # 2. Outlier check: bỏ giá vượt ngưỡng
        if price > PRICE_THRESHOLD:
            continue

        cleaned.append(r)
    return cleaned


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"Đầu vào: {len(data)} bản ghi")

    # Challenge 1
    data = challenge_1_mask_pii(data)
    print(f"Sau Challenge 1 (PII Masking): {len(data)} bản ghi")

    # Challenge 2
    data = challenge_2_dedup_and_outliers(data)
    print(f"Sau Challenge 2 (Dedup & Outliers): {len(data)} bản ghi")

    # Final
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Đã ghi {OUTPUT_FILE} ({len(data)} bản ghi sạch)")


if __name__ == "__main__":
    main()
