from __future__ import annotations

import argparse
from pathlib import Path


def load_frame_times(path: Path) -> list[float]:
    values: list[float] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        values.append(float(line))
    return values


def percentile(sorted_values: list[float], pct: float) -> float:
    if not sorted_values:
        return 0.0
    idx = int((pct / 100.0) * (len(sorted_values) - 1))
    return sorted_values[idx]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()

    frame_times = load_frame_times(args.input)
    if not frame_times:
        print("No frame times found.")
        return

    fps_values = [1000.0 / ms for ms in frame_times if ms > 0]
    if not fps_values:
        print("No valid frame times (>0 ms) found.")
        return

    fps_sorted = sorted(fps_values)
    avg = sum(fps_values) / len(fps_values)
    p1_low = percentile(fps_sorted, 1)
    p5_low = percentile(fps_sorted, 5)

    print(f"Samples: {len(fps_values)}")
    print(f"Average FPS: {avg:.2f}")
    print(f"Min FPS: {fps_sorted[0]:.2f}")
    print(f"Max FPS: {fps_sorted[-1]:.2f}")
    print(f"1% Low FPS: {p1_low:.2f}")
    print(f"5% Low FPS: {p5_low:.2f}")


if __name__ == "__main__":
    main()
