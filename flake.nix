{
  description = "Python uv devshell";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};

      nativeDeps = with pkgs; [
        
      ];
    in
    {
      devShell.${system} = pkgs.mkShell {
        packages = with pkgs; [
          uv
        ];

        LD_LIBRARY_PATH= "${pkgs.lib.makeLibraryPath nativeDeps}";
      };
    };
}
