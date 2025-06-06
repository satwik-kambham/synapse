{
  description = "Synapse";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs {
        inherit system;
        config = {
          allowUnfree = true;
          cudaSupport = true;
        };
      };
    in
    {
      devShell.${system} = pkgs.mkShell {
        packages = with pkgs; [
          ffmpeg
          espeak
          uv
        ];
      };
    };
}
