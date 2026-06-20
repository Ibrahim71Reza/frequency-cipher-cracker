from .scoring import english_score


def rail_pattern(length: int, rails: int) -> list:
    if rails <= 1:
        return [0] * length

    pattern = []
    rail = 0
    direction = 1

    for _ in range(length):
        pattern.append(rail)

        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1

        rail += direction

    return pattern


def encrypt_rail_fence(text: str, rails: int) -> str:
    if rails <= 1:
        return text

    rows = [""] * rails

    for ch, rail in zip(text, rail_pattern(len(text), rails)):
        rows[rail] += ch

    return "".join(rows)


def decrypt_rail_fence(text: str, rails: int) -> str:
    if rails <= 1:
        return text

    pattern = rail_pattern(len(text), rails)
    rail_counts = [pattern.count(rail) for rail in range(rails)]

    rail_text = []
    start = 0

    for count in rail_counts:
        rail_text.append(list(text[start:start + count]))
        start += count

    rail_indexes = [0] * rails
    result = []

    for rail in pattern:
        result.append(rail_text[rail][rail_indexes[rail]])
        rail_indexes[rail] += 1

    return "".join(result)


def crack_rail_fence(text: str, max_rails: int = 10, top: int = 5) -> list:
    results = []

    for rails in range(2, max_rails + 1):
        plaintext = decrypt_rail_fence(text, rails)
        score = english_score(plaintext)

        results.append({
            "rails": rails,
            "score": round(score, 2),
            "plaintext": plaintext,
        })

    return sorted(results, key=lambda item: item["score"])[:top]
