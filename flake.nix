{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
    pyproject-nix.url = "github:nix-community/pyproject.nix";
    pyproject-nix.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs =
    inputs@{
      nixpkgs,
      flake-parts,
      pyproject-nix,
      ...
    }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      perSystem =
        { pkgs, system, ... }:
        let
          python = pkgs.python312;
          getAttrsValue = name: value: value;
          dev-packages = import ./nix/dev.nix {
            pkgs = pkgs;
            python = python;
            pyproject = pyproject-nix;
          };
        in
        {
          devShells =
            let
              dev-packages = import ./nix/dev.nix {
                pkgs = pkgs;
                python = python;
                pyproject = pyproject-nix;
              };
              gui-lib-path = pkgs.lib.makeLibraryPath [
                pkgs.stdenv.cc.cc.lib
                pkgs.libGL
                pkgs.mtdev
                pkgs.mesa
              ];
            in
            {
              default = pkgs.mkShell {
                name = "pdf-img-converter-gui-dev-env";
                buildInputs = (pkgs.lib.attrsets.mapAttrsToList getAttrsValue dev-packages);
                packages = (pkgs.lib.attrsets.mapAttrsToList getAttrsValue dev-packages);
                shellHook = ''
                  export LD_LIBRARY_PATH=${gui-lib-path}:$LD_LIBRARY_PATH
                  just devenv
                  source .venv/bin/activate
                '';
              };

              ci =
                let
                  ci-packages = import ./nix/ci.nix {
                    pkgs = pkgs;
                    python = python;
                    pyproject = pyproject-nix;
                  };
                  tox-project = pyproject-nix.lib.project.loadPyproject {
                    projectRoot = pkgs.fetchFromGitHub {
                      owner = "tox-dev";
                      repo = "tox-gh";
                      rev = "ea2191adcf8757d76dc4cee4039980859f39b01e";
                      sha256 = "sha256-uRNsTtc7Fr95fF1XvW/oz/qBQORpvCt/Lforpd6VZtk=";
                    };
                  };
                  tox-gh-attrs = tox-project.renderers.buildPythonPackage { inherit python; };
                  tox-gh = python.pkgs.buildPythonPackage (tox-gh-attrs // { version = "1.3.2"; });
                in
                pkgs.mkShell {
                  name = "pdf-img-converter-gui-ci-env";
                  packages = (pkgs.lib.attrsets.mapAttrsToList getAttrsValue ci-packages) ++ [ tox-gh ];
                  shellHook = ''
                    export LD_LIBRARY_PATH=${gui-lib-path}:$LD_LIBRARY_PATH
                  '';
                };
            };
        };
    };
}
