time python scanner.py \
  /c/projects/my_product \
  --fingerprint-db ./fingerprints.sqlite \
  --fingerprint-policy fallback \
  --sbom out/project-known.json \
  --unknown out/project-unknown.json \
  --stats out/project-stats.json \
  --fingerprint-rejections out/project-fingerprint-rejections.json
