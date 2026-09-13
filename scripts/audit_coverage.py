"""Recompute corpus coverage from checked-in content, without network or model calls.

Run `python3 scripts/audit_coverage.py` to regenerate the JSON and Markdown report.
Run with `--check` to verify that all three checked-in artifacts still match the content.
Coverage means an asset or draft exists; it does not establish teaching quality.
"""
from __future__ import annotations

import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import re
import sys

from mnemonics import load_mnemonics

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "data/coverage-report.json"
MARKDOWN_PATH = ROOT / "docs/word-coverage.md"
QUEUE_PATH = ROOT / "data/scene-production-queue.json"


def read(relative: str):
    return json.loads((ROOT / relative).read_text())


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def counts(values) -> dict:
    return dict(sorted(Counter(values).items(), key=lambda item: str(item[0])))


def build_report() -> dict:
    lessons = read("public/data/lessons.json")
    characters = read("public/data/characters.json")
    manifest = read("public/data/manifest.json")
    selection = read("data/selection.json")
    cues = read("public/data/element-cues.json")
    blender = read("public/models/blender/manifest.json")
    source_characters = {
        row["character"]: row
        for row in map(json.loads, (ROOT / "data/source/makemeahanzi-dictionary.txt").read_text().splitlines())
    }
    source_geometry = {}
    for line in (ROOT / "data/source/makemeahanzi-graphics.txt").open():
        row = json.loads(line)
        if row["character"] in characters:
            source_geometry[row["character"]] = row

    errors = []
    warnings = []

    def verify(condition: bool, message: str):
        if not condition:
            errors.append(message)

    required_characters = set("".join(lesson["word"] for lesson in lessons))
    verify(len(lessons) == 1000, "The selected corpus must contain exactly 1,000 lessons.")
    verify(len({lesson["word"] for lesson in lessons}) == len(lessons), "Duplicate word lessons.")
    verify(len({lesson["id"] for lesson in lessons}) == len(lessons), "Duplicate lesson IDs.")
    verify([lesson["word"] for lesson in lessons] == [item["simplified"] for item in selection], "Selection and compiled word order differ.")
    verify(required_characters == set(characters), "Character records do not exactly cover the selected words.")

    geometry = {}
    source_preserved = []
    invalid_geometry = []
    partial = []
    complete = []
    unsplit = []
    nested = []
    for char, meta in characters.items():
        path = ROOT / "public" / meta["geometryUrl"].lstrip("/")
        if not path.is_file():
            invalid_geometry.append(char)
            continue
        data = json.loads(path.read_text())
        geometry[char] = data
        stroke_count = len(data.get("strokes", []))
        valid = (
            data.get("character") == char
            and stroke_count > 0
            and all(isinstance(stroke, str) and stroke.startswith("M") for stroke in data["strokes"])
            and all(len(data.get(key, [])) == stroke_count for key in ("medians", "groups", "matches"))
            and all(group == -1 or 0 <= group < len(meta["components"]) for group in data["groups"])
        )
        if not valid:
            invalid_geometry.append(char)
        source = source_geometry.get(char, {})
        dictionary = source_characters.get(char, {})
        if data.get("strokes") == source.get("strokes") and data.get("medians") == source.get("medians") and data.get("matches") == dictionary.get("matches"):
            source_preserved.append(char)
        if not meta["components"]:
            unsplit.append(char)
        elif -1 in data["groups"]:
            partial.append(char)
        else:
            complete.append(char)
        mnemonic = meta["mnemonic"]
        if mnemonic["kind"] == "parts" and [part["glyph"] for part in mnemonic["elements"]] != meta["components"]:
            nested.append(char)
        expected_usages = sorted(lesson["id"] for lesson in lessons if char in lesson["word"])
        verify(sorted(meta["usages"]) == expected_usages, f"Incorrect reuse links for {char}.")
    verify(not invalid_geometry, f"Missing or invalid geometry: {''.join(invalid_geometry)}")
    verify(len(source_preserved) == len(characters), "Some compiled stroke paths, medians or source matches differ from the source snapshot.")

    # Reuse the compiler's recursive source-tree validation. A valid mnemonic cut
    # can expand a named component, so its order need not match top-level groups.
    compiled_characters = copy.deepcopy(characters)
    word_mnemonics, compiled_cues, mnemonic_hash = load_mnemonics(compiled_characters)
    verify(cues == compiled_cues, "Compiled image cue inventory is stale.")
    verify(all(meta["mnemonic"] == compiled_characters[char]["mnemonic"] for char, meta in characters.items()), "Compiled character mnemonics are stale.")
    verify(mnemonic_hash == manifest["mnemonicSha256"], "Manifest mnemonic checksum is stale.")
    for lesson in lessons:
        word = lesson["word"]
        expected_elements = characters[word]["mnemonic"]["elements"] if len(word) == 1 else [{"glyph": char, "image": cues[char]} for char in word]
        expected_story = word_mnemonics.get(word) or characters[word]["mnemonic"]["story"]
        verify(lesson["memoryElements"] == expected_elements, f"Inconsistent element images in {word}.")
        verify(lesson["story"] == expected_story, f"Compiled story is stale for {word}.")
        verify(bool(lesson.get("pinyin") and lesson.get("meaning") and lesson.get("dictionaryMeanings") and lesson.get("source")), f"Incomplete dictionary fields for {word}.")

    blender_assets = []
    for name, asset in sorted(blender["assets"].items()):
        glb = ROOT / "public" / asset["url"].lstrip("/")
        native = ROOT / asset["blendFile"]
        valid = glb.is_file() and native.is_file() and digest(glb) == asset["sha256"]
        verify(valid, f"Missing or changed Blender asset: {name}.")
        blender_assets.append({"word": asset["word"], "scene": name, "glb": asset["url"], "native": asset["blendFile"], "verified": valid})

    # This inventory records authored scene definitions, not every word that can
    # use a generic rendering fallback. Model rendering is tested separately.
    authored_scenes = read("src/explorer/scene-catalog.json")
    verify(len({item["word"] for item in authored_scenes}) == len(authored_scenes), "Duplicate scene-catalog word entries.")
    corpus_words = {lesson["word"] for lesson in lessons}
    catalog_words = {scene["word"] for scene in authored_scenes}
    excluded_words = read("data/curation/illustration-exclusions.json")
    verify(not catalog_words.intersection(excluded_words), "The scene catalog contains a word explicitly excluded from illustration.")
    blender_words = {asset["word"] for asset in blender_assets}
    verify(len(blender_words) == len(blender_assets), "Duplicate word entries in the Blender asset manifest.")
    verify(catalog_words <= corpus_words, "The scene catalog contains words outside the selected corpus.")
    verify(blender_words <= corpus_words, "The Blender manifest contains words outside the selected corpus.")
    verify(blender_words <= catalog_words, "The Blender manifest contains words not admitted by the scene catalog.")
    for scene in authored_scenes:
        source_lesson = next((lesson for lesson in lessons if lesson["word"] == scene["word"]), None)
        if source_lesson:
            verify(set(scene.get("mnemonicImages", {})) <= {part["glyph"] for part in source_lesson["memoryElements"]}, f"Mnemonic label overrides name unknown parts in {scene['word']}.")
            verify(all(isinstance(image, str) and image.strip() for image in scene.get("mnemonicImages", {}).values()), f"Empty mnemonic label override in {scene['word']}.")
        if scene["format"] == "blender":
            verify(any(asset["word"] == scene["word"] and asset["glb"] == scene["asset"] for asset in blender_assets), f"Catalog Blender asset is not in the model manifest: {scene['word']}.")
    historical_files = sorted(
        str(path.relative_to(ROOT))
        for path in (ROOT / "public/reference/assets").glob("*.svg")
        if re.search(r"-(oracle|bronze|seal)\.svg$", path.name)
    )
    history_words = [scene["word"] for scene in authored_scenes if scene.get("history")]

    lesson_drafts = sum(lesson.get("status") == "draft" for lesson in lessons)
    reviewed = manifest.get("independentlyReviewed", 0)
    if reviewed:
        warnings.append("The manifest reports independent review; reviewer evidence is not checked by this structural audit.")
    partial_set = set(partial)
    partially_mapped_words = [lesson["word"] for lesson in lessons if partial_set.intersection(lesson["characters"])]
    outline_characters = [char for char, meta in characters.items() if meta["mnemonic"]["kind"] == "outline"]
    provenance_paths = [
        "public/data/lessons.json", "public/data/characters.json", "public/data/element-cues.json",
        "public/data/manifest.json", "public/models/blender/manifest.json",
        "src/explorer/scene-catalog.json",
        "data/curation/illustration-exclusions.json",
    ]
    return {
        "schemaVersion": 1,
        "scope": "Checked-in selected corpus and authored assets; counts do not establish editorial quality or runtime availability.",
        "contentRevision": manifest["version"],
        "selection": manifest["selection"],
        "words": {
            "target": 1000, "lessons": len(lessons), "uniqueWords": len({lesson["word"] for lesson in lessons}),
            "dictionaryFieldsComplete": sum(bool(item.get("pinyin") and item.get("meaning") and item.get("dictionaryMeanings") and item.get("source")) for item in lessons),
            "characterOccurrences": sum(len(lesson["characters"]) for lesson in lessons),
            "characterLengthDistribution": counts(len(lesson["word"]) for lesson in lessons),
            "spokenSyllableDistribution": counts(lesson["syllables"] for lesson in lessons),
            "hsk20LevelDistribution": counts(str(lesson["level"]) if lesson["level"] is not None else "supplement" for lesson in lessons),
            "stressCases": sum(lesson["stressTest"] for lesson in lessons),
        },
        "characters": {
            "required": len(required_characters), "records": len(characters),
            "validGeometry": len(characters) - len(invalid_geometry), "sourceGeometryPreserved": len(source_preserved),
            "strokePaths": sum(len(data["strokes"]) for data in geometry.values()),
            "completeTopLevelStrokeMapping": len(complete), "partialTopLevelStrokeMapping": len(partial),
            "withoutTopLevelComponents": len(unsplit),
            "unassignedStrokesInSplitCharacters": sum(data["groups"].count(-1) for char, data in geometry.items() if characters[char]["components"]),
            "wordsContainingPartialStrokeMapping": len(partially_mapped_words),
            "nestedMnemonicCuts": len(nested),
            "singleCharacterLessonsWithNestedCuts": sum(lesson["word"] in nested for lesson in lessons),
        },
        "memoryContent": {
            "wordStories": sum(bool(lesson.get("story")) for lesson in lessons),
            "uniqueWordStories": len({lesson["story"] for lesson in lessons}),
            "lessonKinds": counts(lesson["mnemonicKind"] for lesson in lessons),
            "characterStories": sum(bool(meta["mnemonic"].get("story")) for meta in characters.values()),
            "uniqueCharacterStories": len({meta["mnemonic"]["story"] for meta in characters.values()}),
            "characterKinds": counts(meta["mnemonic"]["kind"] for meta in characters.values()),
            "sharedElementImageCues": len(cues),
            "selectedSenseOverrides": sum(1 for line in (ROOT / "data/curation/mnemonics/single-senses.txt").read_text().splitlines() if line.strip()),
        },
        "editorial": {
            "lessonStatuses": counts(lesson["status"] for lesson in lessons),
            "draftWordStories": lesson_drafts,
            "independentlyReviewedWordsRecorded": reviewed,
            "independentReviewEvidence": "No independent reviewer records in the compiled corpus; element-review files are source/gloss worklists, not review verdicts.",
            "learningEffectiveness": "Not measured by this audit; draft story presence is not evidence of memorability or cultural accuracy.",
        },
        "visualAssets": {
            "blenderWords": len(blender_assets), "blenderAssets": blender_assets,
            "authoredSceneDefinitions": len(authored_scenes), "authoredScenes": authored_scenes,
            "historicalCharactersRouted": len(history_words), "historicalWords": history_words,
            "historicalSvgAssets": historical_files,
            "note": "The Blender scenes are a subset of the authored scenes. Neither count describes generic glyph rendering or guarantees 1,000 distinct illustrated scenes.",
        },
        "sources": {
            "revisions": manifest["sourceRevisions"],
            "charactersWithSourceAttribution": sum(bool(meta.get("source")) for meta in characters.values()),
            "importedEtymologyTypes": counts((meta.get("etymology") or {}).get("type", "missing") for meta in characters.values()),
            "note": "Imported etymology labels are source analyses. They are separate from original memory stories, reviewed historical claims and bundled historical glyphs.",
        },
        "workQueues": {
            "partialStrokeMappingCharacters": partial,
            "wordsContainingPartialStrokeMapping": partially_mapped_words,
            "wholeOutlineMnemonicCharacters": outline_characters,
            "nestedMnemonicCutCharacters": nested,
            "missingOrInvalidGeometryCharacters": invalid_geometry,
        },
        "verification": {"passed": not errors, "errors": errors, "warnings": warnings, "inputSha256": {path: digest(ROOT / path) for path in provenance_paths}},
    }


def markdown(report: dict) -> str:
    w, c, m = (report[key] for key in ("words", "characters", "memoryContent"))
    e, v, s = (report[key] for key in ("editorial", "visualAssets", "sources"))
    queues = report["workQueues"]
    history = "、".join(v["historicalWords"]) or "none detected"
    blender_words = "、".join(asset["word"] for asset in v["blenderAssets"])
    scene_words = "、".join(scene["word"] for scene in v["authoredScenes"])
    total = lambda value: f"{value:,}"
    return f"""# Word coverage

Generated by `python3 scripts/audit_coverage.py`. Run `python3 scripts/audit_coverage.py --check` to detect stale reports. The detailed machine-readable report is [data/coverage-report.json](../data/coverage-report.json). The [scene production queue](../data/scene-production-queue.json) contains every lesson ID, its draft story and elements, known scene assets and a priority based on shared image reuse. Reuse counts include both the word's direct memory elements and its characters' nested elements, with each image counted once per word.

The collection already contains **{total(w['uniqueWords'])} words and {total(c['records'])} distinct characters**. Every word has a dictionary reading, a selected meaning and a draft memory story. Every required character has sourced writing geometry. The remaining work is editorial review and richer visual coverage, rather than filling an empty word list.

## Coverage by layer

| Layer | Present | Meaning of the count |
| --- | ---: | --- |
| Unique word lessons | {total(w['uniqueWords'])} / {total(w['target'])} | Selected corpus, not a universal top-1,000 list |
| Dictionary reading, selected meaning and source | {total(w['dictionaryFieldsComplete'])} / {total(w['lessons'])} | One selected dictionary form per word |
| Word memory stories | {total(m['wordStories'])} / {total(w['lessons'])} | Original draft stories; all {total(m['uniqueWordStories'])} sentences are distinct |
| Character memory stories | {total(m['characterStories'])} / {total(c['records'])} | {total(m['characterKinds']['parts'])} use sourced ordered parts; {total(m['characterKinds']['outline'])} use a whole-outline cue |
| Character stroke geometry | {total(c['validGeometry'])} / {total(c['required'])} | {total(c['strokePaths'])} paths; paths, medians and source matches match the preserved snapshot |
| Complete top-level stroke grouping | {total(c['completeTopLevelStrokeMapping'])} / {total(c['records'] - c['withoutTopLevelComponents'])} split characters | {total(c['partialTopLevelStrokeMapping'])} have some unassigned strokes; {c['withoutTopLevelComponents']} other characters have no top-level split |
| Shared visual image cues | {total(m['sharedElementImageCues'])} | Reusable labels for characters and component shapes |
| Independently reviewed word stories recorded | {total(e['independentlyReviewedWordsRecorded'])} / {total(w['lessons'])} | All {total(e['draftWordStories'])} lessons remain marked draft |
| Blender model scenes | {v['blenderWords']} / {total(w['lessons'])} | {blender_words}; native files and GLB checksums verified |
| Authored scene definitions | {v['authoredSceneDefinitions']} / {total(w['lessons'])} | {scene_words}; includes the Blender words |
| Characters with routed historical forms | {v['historicalCharactersRouted']} / {total(c['records'])} | {history}; {len(v['historicalSvgAssets'])} bundled oracle, bronze and seal SVGs |

The visual counts are not additive. Three-dimensional writing, reusable scene rendering, authored illustrations and native Blender models are different levels of coverage. This report inventories checked-in content; runtime routing and browser behavior require separate tests.

## What has already progressed

- The `elements-2` revision has {total(m['characterStories'])} character mnemonics and {total(m['lessonKinds']['word'])} compound-word stories. The {total(w['characterLengthDistribution'][1])} one-character word lessons use character mnemonics, with {m['selectedSenseOverrides']} selected-sense overrides.
- Word lengths are {total(w['characterLengthDistribution'][1])} single characters, {total(w['characterLengthDistribution'][2])} two characters, {total(w['characterLengthDistribution'][3])} three characters and {total(w['characterLengthDistribution'][4])} four characters. These are writing lengths; spoken-syllable bins differ for an 儿 suffix.
- Character reuse is linked across {total(w['characterOccurrences'])} occurrences. All existing words can therefore share the same sourced character data and image cues.
- Ordered mnemonic parts are checked against recursive source decomposition trees. {c['nestedMnemonicCuts']} character stories expand beyond the top-level split; {c['singleCharacterLessonsWithNestedCuts']} are standalone word lessons. Rendering must follow those nested source paths rather than assigning mnemonic positions to top-level stroke groups.

## Remaining work

1. **Review the drafts.** The collection records {total(e['independentlyReviewedWordsRecorded'])} independently reviewed words. Files in `data/curation/element-review/` contain source/gloss worklists, not reviewer verdicts. Automated checks establish consistency and coverage, not memorability, linguistic accuracy or learner outcomes.
2. **Resolve uncertain splits without inventing strokes.** {c['partialTopLevelStrokeMapping']} characters have partial source mappings, affecting {c['wordsContainingPartialStrokeMapping']} word lessons. Those split characters contain {c['unassignedStrokesInSplitCharacters']} unassigned strokes. Preserve them intact and neutral unless stronger source evidence supports a mapping. Whole-outline mnemonic cues are a separate category and can overlap partial mappings.
3. **Expand authored visual scenes.** Only {v['blenderWords']} words currently have Blender exports and {v['authoredSceneDefinitions']} have bespoke scene definitions. Generic rendering can broaden access but should not be counted as 1,000 bespoke Blender artworks.
4. **Expand sourced history separately.** Imported etymology metadata exists for {c['records'] - s['importedEtymologyTypes'].get('missing', 0)} characters. That does not make their invented memory stories historical explanations, and it does not provide bundled ancient glyphs beyond {history}.

### Characters with partial stroke mappings

{'、'.join(queues['partialStrokeMappingCharacters'])}

### Characters using whole-outline mnemonic cues

{'、'.join(queues['wholeOutlineMnemonicCharacters'])}

The JSON report also lists the affected words and nested mnemonic cuts for prioritization.

## Reproducibility and sources

{report['selection']}

The audit reads compiled data, compares stroke paths and medians with `data/source/`, re-runs authored mnemonic/source-tree alignment, checks character reuse links and verifies Blender checksums. It makes no network or model calls. See [SOURCES.md](../SOURCES.md) for attribution and licenses. Input hashes and pinned source revisions are recorded in the JSON report.

Structural audit: **{'PASS' if report['verification']['passed'] else 'FAIL'}**. This is independent of application tests, browser checks and editorial review.
"""


def build_production_queue(report: dict) -> dict:
    lessons = read("public/data/lessons.json")
    characters = read("public/data/characters.json")
    cues = read("public/data/element-cues.json")
    catalog = {scene["word"]: scene for scene in report["visualAssets"]["authoredScenes"]}
    excluded = read("data/curation/illustration-exclusions.json")
    direct = Counter(element["glyph"] for lesson in lessons for element in lesson["memoryElements"])
    nested = Counter(element["glyph"] for lesson in lessons for char in lesson["characters"] for element in characters[char]["mnemonic"]["elements"])
    image_word_usage = Counter()
    glyph_word_usage = Counter()
    for lesson in lessons:
        elements = [*lesson["memoryElements"], *[
            element for char in lesson["characters"] for element in characters[char]["mnemonic"]["elements"]
        ]]
        glyph_word_usage.update({element["glyph"] for element in elements})
        image_word_usage.update({element["image"] for element in elements})

    # A small explicit design seed list distinguishes familiar reusable objects
    # from abstract concepts. Unclassified cues remain open design work; the
    # heuristic is never used as a linguistic or historical classification.
    categories = {
        "natural object": {"tree", "woods", "forest", "grass", "water", "sun", "moon", "earth", "river", "river channel", "mountain", "stone", "field", "fire", "fire dots", "bamboo", "flower", "rain", "snow", "cloud", "fruit", "rice"},
        "person, body or animal": {"person", "woman", "child", "mouth", "heart", "hand", "hand again", "thumb", "eye", "foot", "head", "two horns", "king", "horse", "bird", "fish", "dog", "cat", "sheep", "cow", "insect", "tiger", "rabbit", "snake"},
        "object or constructed shape": {"road", "roof", "lid", "knife", "spoon", "speech bubble", "vehicle", "machine", "door", "window", "table", "nail", "pole", "drop", "slash", "hook", "bent hook", "square", "crossed ribbons", "open frame", "open container", "private cocoon"},
        "number or written symbol": {"one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "hundred", "thousand", "zero"},
        "action, quality or abstract idea": {"good", "clear", "sunny", "green", "emotion", "please", "permission", "strength", "rest", "grow", "not", "so", "idea", "walking", "walk", "high", "up", "down", "divide", "long", "big", "heavy", "want", "repeat", "convenient", "suitable", "reason", "think"},
    }
    def category(image: str) -> str:
        return next((name for name, images in categories.items() if image in images), "needs concept design")

    inventory = [{
        "glyph": glyph, "image": image,
        "sourceRole": "selected character" if glyph in characters else "component-only cue",
        "planningCategory": category(image),
        "directLessonElementOccurrences": direct[glyph],
        "characterElementOccurrencesAcrossWords": nested[glyph],
        "wordsReusingGlyph": glyph_word_usage[glyph],
        "wordsReusingImage": image_word_usage[image],
    } for glyph, image in cues.items()]
    inventory.sort(key=lambda item: (-item["wordsReusingImage"], -item["characterElementOccurrencesAcrossWords"], item["glyph"]))

    rows = []
    for lesson in lessons:
        breakdowns = [{"character": char, "kind": characters[char]["mnemonic"]["kind"], "elements": characters[char]["mnemonic"]["elements"], "story": characters[char]["mnemonic"]["story"]} for char in lesson["characters"]]
        images = {element["image"] for element in lesson["memoryElements"]} | {
            element["image"] for breakdown in breakdowns for element in breakdown["elements"]
        }
        existing = catalog.get(lesson["word"])
        mnemonic_images = (existing or {}).get("mnemonicImages", {})
        rows.append({
            "lessonId": lesson["id"], "word": lesson["word"], "pinyin": lesson["pinyin"], "meaning": lesson["meaning"],
            "story": (existing or {}).get("story", lesson["story"]),
            "memoryElements": [{**element, "image": mnemonic_images.get(element["glyph"], element["image"])} for element in lesson["memoryElements"]],
            "characterBreakdowns": breakdowns,
            "storyReviewStatus": lesson["status"],
            "illustrationStatus": "excluded" if lesson["word"] in excluded else "ready-existing" if existing else "needs-illustration",
            **({"exclusionReason": excluded[lesson["word"]]} if lesson["word"] in excluded else {}),
            "knownAssets": [existing] if existing else [],
            "sharedCueReuseScore": sum(image_word_usage[image] for image in images),
            "missingIllustrationRequirements": [] if existing or lesson["word"] in excluded else ["Word-specific visual composition connecting all selected memory elements", "Authored scene geometry and label anchors", "Visual review of story, readability and transitions"],
        })
    rows.sort(key=lambda row: ({"needs-illustration": 0, "ready-existing": 1, "excluded": 2}[row["illustrationStatus"]], -row["sharedCueReuseScore"], row["lessonId"]))
    for priority, row in enumerate(rows, 1):
        row["priority"] = priority
    return {
        "schemaVersion": 1,
        "scope": "Production planning only. Draft story/element records are not authored scene compositions or reviewed lessons.",
        "statusDefinitions": {
            "ready-existing": "An authored illustration exists in the scene catalog. This does not certify editorial review or Blender format.",
            "needs-illustration": "The word has source data and draft memory content but no authored scene in the catalog.",
            "excluded": "Explicitly removed from illustration; do not restore in future batches without a new user request.",
        },
        "priorityMethod": "Missing scenes first, then sum of distinct-word reuse counts for each unique image in the union of the word's direct memory elements and its characters' nested elements. An image is counted once per word even when repeated or present at both levels; aliases with the same image name share its count. Ties use stable lesson ID. Review priority can override this asset reuse heuristic.",
        "cueReuseScope": "wordsReusingGlyph and wordsReusingImage count the per-word union of direct memory elements and nested character elements. Direct and nested occurrence fields remain separate and may contain repeats.",
        "cueCategoryMethod": "Explicit design seed list for common images; every other image is marked needs concept design. These are unreviewed planning categories, not linguistic analysis.",
        "summary": {
            "lessons": len(rows), "readyExisting": sum(row["illustrationStatus"] == "ready-existing" for row in rows),
            "needsIllustration": sum(row["illustrationStatus"] == "needs-illustration" for row in rows),
            "excluded": sum(row["illustrationStatus"] == "excluded" for row in rows),
            "characterCues": sum(glyph in characters for glyph in cues), "componentOnlyCues": sum(glyph not in characters for glyph in cues),
            "cuePlanningCategories": counts(item["planningCategory"] for item in inventory),
        },
        "cueInventory": inventory,
        "lessons": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated reports differ from checked-in reports.")
    args = parser.parse_args()
    report = build_report()
    artifacts = {
        JSON_PATH: json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        MARKDOWN_PATH: markdown(report),
        QUEUE_PATH: json.dumps(build_production_queue(report), ensure_ascii=False, indent=2) + "\n",
    }
    stale = []
    for path, content in artifacts.items():
        if args.check:
            if not path.is_file() or path.read_text() != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    for error in report["verification"]["errors"]:
        print(f"ERROR: {error}", file=sys.stderr)
    if stale:
        print("Stale coverage reports: " + ", ".join(stale), file=sys.stderr)
        print("Run python3 scripts/audit_coverage.py to regenerate.", file=sys.stderr)
    if not report["verification"]["passed"] or stale:
        return 1
    print(f"PASS: {report['words']['uniqueWords']:,} words; {report['characters']['validGeometry']} sourced character geometries; {report['editorial']['draftWordStories']:,} draft stories; {report['visualAssets']['blenderWords']} Blender scenes. Reports {'current' if args.check else 'written'}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
