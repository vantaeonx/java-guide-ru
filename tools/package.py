#!/usr/bin/env python3
"""Архив для просмотра/релиза без Git, runtime, сборочных файлов и личных решений."""
import hashlib
import zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
EXCLUDE = {'.git', '.idea', '.venv', 'build', 'target', '__pycache__', 'tmp', 'dist'}

def build_archive():
    target = ROOT / 'dist/java-guide-ru.zip'
    target.parent.mkdir(exist_ok=True)
    files = sorted(p for p in ROOT.rglob('*') if p.is_file()
                   and not EXCLUDE.intersection(p.relative_to(ROOT).parts))
    for p in files:
        if p.is_symlink():
            raise ValueError('В архиве не допускаются симлинки: ' + str(p))
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
        for p in files:
            name = Path('java-guide-ru') / p.relative_to(ROOT)
            info = zipfile.ZipInfo(name.as_posix(), date_time=(2026, 10, 16, 12, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100755 if p.suffix == '.sh' else 0o100644) << 16
            archive.writestr(info, p.read_bytes())
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == len(files)
        assert all(not n.startswith('/') and '..' not in Path(n).parts for n in archive.namelist())
        assert sum(n.endswith('.java') for n in archive.namelist()) == 206
    checksum = hashlib.sha256(target.read_bytes()).hexdigest()
    (ROOT / 'dist/SHA256SUMS.txt').write_text(checksum + '  java-guide-ru.zip\n')
    print(target)
    print('Файлов:', len(files), 'SHA256:', checksum)

if __name__ == '__main__':
    build_archive()
