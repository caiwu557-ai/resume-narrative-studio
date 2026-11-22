# Contributing / 参与贡献

Thanks for improving Resume Narrative Studio. Please open an issue before major changes, and include a clear explanation of the user problem your proposal solves.

## Development / 开发

- Python 3 is required for the core HTML generator and static tests.
- Run `python tests/test_skill_package.py` and `python tests/test_photo_policy_v13.py` before proposing a change.
- Browser/PDF tests are optional and require Playwright, Chromium and PyMuPDF. See `README.md`.
- Do not replace truthful claims with invented metrics or alter the human approval and privacy checkpoints.
- When changing layout rules, test ATS mode, no-photo mode, formal CN photo mode, long names and multi-page examples.
- Add a regression test for each bug, especially visual/page-break regressions.

## Privacy and examples / 隐私及测试素材

Use fictional or consented, fully anonymized example data. Do **not** commit real resumes, identity information, patient or student data, medical records, copyrighted images, licensed font binaries, credentials, private API keys or `.env` files.

Please do not submit secret-bearing screenshots or raw user documents as issue attachments. For security problems, follow `SECURITY.md` rather than opening a public issue with exploit details.

## License / 许可

By contributing, you agree your contribution can be distributed under this repository's MIT License. Document the origin and license of third-party assets you introduce.
