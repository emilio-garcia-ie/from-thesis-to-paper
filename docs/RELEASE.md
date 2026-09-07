# Release procedure

FTTP releases are versioned GitHub Release assets for macOS and Linux. The
release ZIP contains a wheel, source distribution, checksums, `install.sh`, and
the Python installer. It is not published to PyPI or npm.

Before proposing a release, run the full test suite, build the bundle with
`python3 scripts/build_release_bundle.py <output-dir>`, and verify the bundle
in a clean temporary prefix. Hosted CI must pass for the candidate commit.

Publishing a tag or GitHub Release requires explicit maintainer approval. The
installer retains earlier managed versions, does not edit shell profiles, and
never searches for or removes paper workspaces. To reactivate a retained
version, run `python3 scripts/release_installer.py --activate <version>` with
the same `--prefix` and `--bin-dir` used during installation. To remove the
active managed version, run it with `--uninstall`.
