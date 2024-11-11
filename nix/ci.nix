{
  pkgs,
  python,
  pyproject,
}:
let
  tox-pdm-project = pyproject.lib.project.loadPyproject {
    projectRoot = pkgs.fetchzip {
      url = "https://github.com/pdm-project/tox-pdm/archive/refs/tags/0.7.2.zip";
      hash = "sha256-JqIeJpAKTv2ruMx/fB16u7j+JJGQz7dwOEiNc/FGZLo=";
    };
  };
  tox-pdm-attrs = tox-pdm-project.renderers.buildPythonPackage { inherit python; };
  tox-pdm = python.pkgs.buildPythonPackage (tox-pdm-attrs // { version = "0.7.2"; });
in
{
  # To build nixfmt
  inherit (pkgs) cabal-install ghc;

  # CI tools
  inherit (pkgs)
    ruff
    pre-commit
    commitizen
    pdm
    ;
  inherit (python.pkgs) tox;
  tox-pdm = tox-pdm;

  # PDF tool
  inherit (pkgs)
    poppler_utils
    ;

  # GUI dependencies
  inherit (pkgs)
    SDL2
    SDL2_image
    SDL2_ttf
    SDL2_mixer
    mtdev
    mesa
    libGL
    ;
  inherit (pkgs.stdenv.cc.cc) lib;
  inherit (pkgs.gst_all_1)
    gstreamer
    gst-plugins-base
    gst-plugins-good
    gst-plugins-bad
    ;
}
