{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        inherit (builtins) attrValues;

        pkgs = (import nixpkgs) { inherit system; };

        python-packages = (ps: with ps; [
          discordpy
          python-dotenv
        ]);
      in
      with pkgs;
      {
        devShells.default = mkShell {
          packages = [
            (python311.withPackages python-packages)
          ];

          # Runtime libc fix for neovim LSPs
          shellHook = ''
            export LD_LIBRARY_PATH=${stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
          '';
        };
      }
    );
}
