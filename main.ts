// news-image-20261126: a one-day world-news image for Thursday 26 November 2026.
// Node 22, standard library only. The image is pre-rendered by
// generate_image.py (pure Python stdlib) and shipped as entry.png beside
// this file; the program copies it to the grader's output directory, which
// it creates when missing, so both grading runs write identical bytes.
// The copy is byte-for-byte: no re-encoding and no timestamps in the
// output, so the two runs are deterministic by construction.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
