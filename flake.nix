{
  description = "Python uv devshell";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShell.${system} = pkgs.mkShell {
        packages = with pkgs; [
          uv
          ffmpeg
        ];

        LD_LIBRARY_PATH= pkgs.lib.makeLibraryPath [
          "/run/opengl-driver"
        ];
      };
    };
}
