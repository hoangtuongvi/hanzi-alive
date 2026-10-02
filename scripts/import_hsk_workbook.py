"""Merge the supplied HSK 1-4 workbook into the checked-in lesson corpus.

The workbook is treated as a vocabulary source, not edited. Existing lesson
order and authored records stay intact; normalized workbook-only words append
in HSK level and row order. Run with the downloaded .xlsx path.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
TABS = ("HSK1", "HSK2", "HSK3", "HSK4")
SUPPLEMENT_MEANINGS = {
    "踢足球": "to play soccer",
    "电子邮箱": "email address; email inbox",
    "百分之": "percent; percentage",
    "弹钢琴": "to play the piano",
}


def read_json(path: str):
    return json.loads((ROOT / path).read_text())


def normalize_word(raw: str) -> str:
    word = re.split(r"[（(]", raw.strip(), maxsplit=1)[0].strip()
    if not word or not all("\u3400" <= char <= "\u9fff" for char in word):
        raise ValueError(f"Unsupported workbook word: {raw!r}")
    return word


def choose_meaning(record: dict) -> str:
    meanings = [meaning for form in record["forms"] for meaning in form.get("meanings", [])]
    for meaning in meanings:
        lower = meaning.lower()
        if not lower.startswith(("variant of", "old variant", "used in", "unofficial variant")) and "surname" not in lower:
            return meaning.split(";")[0].strip()
    return meanings[0].split(";")[0].strip()


def workbook_rows(path: Path) -> list[dict]:
    workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    rows = []
    seen = set()
    for level, tab in enumerate(TABS, 1):
        for values in workbook[tab].iter_rows(values_only=True):
            if not isinstance(values[0], (int, float)) or not isinstance(values[1], str):
                continue
            raw_word = values[1].strip()
            word = normalize_word(raw_word)
            if word in seen:
                continue
            seen.add(word)
            rows.append({
                "level": level,
                "row": int(values[0]),
                "word": word,
                "rawWord": raw_word,
                "pinyin": str(values[2] or "").strip(),
                "meaningVi": str(values[3] or "").strip(),
            })
    return rows


def existing_character_cues() -> dict[str, str]:
    cues = {}
    for path in sorted((ROOT / "data/curation/mnemonics").glob("characters-*.txt")):
        for line in path.read_text().splitlines():
            if line.strip():
                character, image, _, _ = line.split("|", 3)
                cues[character] = image
    for line in (ROOT / "data/curation/mnemonics/extra-cues.txt").read_text().splitlines():
        if line.strip():
            glyph, image = line.split("|", 1)
            cues[glyph] = image
    return cues


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("|", "/")).strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("workbook", type=Path)
    args = parser.parse_args()

    rows = workbook_rows(args.workbook)
    (ROOT / "data/source/hsk-workbook-1-4.json").write_text(
        json.dumps({
            "source": "FULL TỪ VỰNG HSK1- HSK6.xlsx",
            "spreadsheetId": "1fEfxea3e4_p3OChTmDtkKI-hQpu9KdQW",
            "sheets": list(TABS),
            "normalization": "Text before a parenthetical grammar or alias note is the lesson key.",
            "rows": rows,
        }, ensure_ascii=False, indent=2) + "\n"
    )

    selection = read_json("data/selection.json")[:1000]
    selected = {item["simplified"] for item in selection}
    canonical = {item["simplified"]: item for item in read_json("data/source/complete-hsk-vocabulary-complete.json")}
    additions = [row for row in rows if row["word"] not in selected]
    for row in additions:
        word = row["word"]
        if word in canonical:
            record = json.loads(json.dumps(canonical[word], ensure_ascii=False))
        else:
            record = {
                "simplified": word,
                "level": [f"workbook-{row['level']}"],
                "pos": [],
                "forms": [{
                    "traditional": word,
                    "transcriptions": {"pinyin": row["pinyin"]},
                    "meanings": [SUPPLEMENT_MEANINGS[word]],
                }],
                "supplement": "HSK workbook",
            }
        record["workbook"] = row
        selection.append(record)
        selected.add(word)
    (ROOT / "data/selection.json").write_text(json.dumps(selection, ensure_ascii=False, indent=2) + "\n")

    source_characters = {
        item["character"]: item
        for item in map(json.loads, (ROOT / "data/source/makemeahanzi-dictionary.txt").read_text().splitlines())
    }
    old_characters = set(read_json("public/data/characters.json"))
    new_characters = sorted(set("".join(row["word"] for row in additions)) - old_characters)
    character_lines = []
    cues = existing_character_cues()
    for character in new_characters:
        source = source_characters[character]
        definition = clean((source.get("definition") or character).split(";")[0].split(",")[0])
        image = cues.get(character, definition.lower() or character)
        cues[character] = image
        character_lines.append(
            f"{character}|{image}|{character}|Trace {character} as one whole outline and picture {image}."
        )
    (ROOT / "data/curation/mnemonics/characters-11.txt").write_text("\n".join(character_lines) + "\n")

    story_lines = []
    word_lines = []
    for row in additions:
        word = row["word"]
        record = next(item for item in selection if item["simplified"] == word)
        meaning = clean(SUPPLEMENT_MEANINGS.get(word, choose_meaning(record)))
        images = [cues[character] for character in word]
        if len(word) == 1:
            story = f"Trace {word} as one whole outline and picture {images[0]}."
        else:
            sequence = ", then ".join(f"{images[index]} for {character}" for index, character in enumerate(word))
            story = f"Picture {sequence}; together they cue {meaning} ({word})."
            word_lines.append(f"{word}|{story}")
        story_lines.append(f"{word}|{meaning}|{story}")
    for batch, start in enumerate(range(0, len(story_lines), 100), 11):
        (ROOT / f"data/curation/stories-{batch:02d}.txt").write_text("\n".join(story_lines[start:start + 100]) + "\n")
    for batch, start in enumerate(range(0, len(word_lines), 100), 11):
        (ROOT / f"data/curation/mnemonics/words-{batch:02d}.txt").write_text("\n".join(word_lines[start:start + 100]) + "\n")

    print(json.dumps({
        "workbookUniqueWords": len(rows),
        "alreadyPresent": len(rows) - len(additions),
        "addedWords": len(additions),
        "totalWords": len(selection),
        "newCharacters": len(new_characters),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
