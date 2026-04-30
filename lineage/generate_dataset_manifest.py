import os
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone


DATA_FILES = [
    {
        "dataset_name": "recomart_events",
        "source_type": "csv",
        "local_path": "data/source/recomart/events.csv",
        "s3_raw_path": "s3://recomartdatalake/raw/recomart/events/",
        "target_table": "RAW.RAW_RECOMART_EVENTS",
    },
    {
        "dataset_name": "recomart_item_properties_part1",
        "source_type": "csv",
        "local_path": "data/source/recomart/item_properties_part1.csv",
        "s3_raw_path": "s3://recomartdatalake/raw/recomart/item_properties/",
        "target_table": "RAW.RAW_RECOMART_ITEM_PROPERTIES",
    },
    {
        "dataset_name": "recomart_item_properties_part2",
        "source_type": "csv",
        "local_path": "data/source/recomart/item_properties_part2.csv",
        "s3_raw_path": "s3://recomartdatalake/raw/recomart/item_properties/",
        "target_table": "RAW.RAW_RECOMART_ITEM_PROPERTIES",
    },
    {
        "dataset_name": "recomart_category_tree",
        "source_type": "csv",
        "local_path": "data/source/recomart/category_tree.csv",
        "s3_raw_path": "s3://recomartdatalake/raw/recomart/category_tree/",
        "target_table": "RAW.RAW_RECOMART_CATEGORY_TREE",
    },
]


def calculate_file_hash(file_path: str) -> str:
    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


def count_rows(file_path: str) -> int:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        return max(sum(1 for _ in file) - 1, 0)


def generate_manifest() -> dict:
    manifest = {
        "project_name": "recomart_recommendation_pipeline",
        "manifest_created_ts": datetime.now(timezone.utc).isoformat(),
        "versioning_tool": "DVC",
        "dvc_remote": "s3://recomartdatalake/dvc-store",
        "datasets": [],
    }

    for dataset in DATA_FILES:
        path = Path(dataset["local_path"])

        if not path.exists():
            manifest["datasets"].append(
                {
                    **dataset,
                    "status": "MISSING",
                    "file_size_bytes": None,
                    "row_count": None,
                    "sha256_hash": None,
                }
            )
            continue

        manifest["datasets"].append(
            {
                **dataset,
                "status": "AVAILABLE",
                "file_size_bytes": os.path.getsize(path),
                "row_count": count_rows(str(path)),
                "sha256_hash": calculate_file_hash(str(path)),
            }
        )

    return manifest


def main() -> None:
    os.makedirs("data/metadata", exist_ok=True)

    manifest = generate_manifest()

    output_path = "data/metadata/dataset_version_manifest.json"

    with open(output_path, "w") as file:
        json.dump(manifest, file, indent=2)

    print(f"Dataset version manifest created: {output_path}")


if __name__ == "__main__":
    main()