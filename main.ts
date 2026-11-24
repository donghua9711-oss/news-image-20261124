// The World in One Day — Tuesday 24 November 2026.
// Entry for make.fun bounty news-image-20261124.
//
// The picture itself is committed beside this file as entry.png: a single
// 1024x1024 front page composed from the day's verified stories (see
// SOURCES.md for the story list and compose.py for how the page is drawn).
// This program's whole job at grade time is to deliver that picture to the
// output folder, after checking it still obeys the contest's caps.

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const MAX_BYTES = 1_048_576; // 1 MiB
const MAX_SIDE = 1024; // pixels, either dimension

function fail(message: string): never {
  console.error(`entry: ${message}`);
  process.exit(1);
}

function pngSize(bytes: Buffer): { width: number; height: number } {
  // A PNG opens with an 8-byte signature; the IHDR chunk follows and its
  // first eight data bytes are the width and the height, big-endian.
  const signature = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
  if (bytes.length < 24) fail('entry.png is too small to be a PNG');
  for (let i = 0; i < signature.length; i++) {
    if (bytes[i] !== signature[i]) fail('entry.png does not start with the PNG signature');
  }
  if (bytes.toString('ascii', 12, 16) !== 'IHDR') fail('entry.png has no IHDR chunk');
  return { width: bytes.readUInt32BE(16), height: bytes.readUInt32BE(20) };
}

function main(): void {
  const here = dirname(fileURLToPath(import.meta.url));
  const picturePath = join(here, 'entry.png');
  const picture = readFileSync(picturePath);

  if (picture.length > MAX_BYTES) {
    fail(`entry.png is ${picture.length} bytes, over the ${MAX_BYTES} byte cap`);
  }
  const { width, height } = pngSize(picture);
  if (width > MAX_SIDE || height > MAX_SIDE) {
    fail(`entry.png is ${width}x${height}, over the ${MAX_SIDE} pixel cap`);
  }

  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
  mkdirSync(outDir, { recursive: true });
  const target = join(outDir, 'entry.png');
  copyFileSync(picturePath, target);
  // Read the delivered file back and compare it byte for byte with the
  // committed picture, so a truncated copy can never pass silently.
  const delivered = readFileSync(target);
  if (!delivered.equals(picture)) fail('the delivered copy differs from entry.png');
  console.log(`entry: wrote ${target} (${width}x${height}, ${picture.length} bytes, verified)`);
}

main();
