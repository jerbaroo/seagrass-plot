let
  pkgs = import <nixpkgs> { };
in
pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.basemap
      python-pkgs.basemap-data-hires
      python-pkgs.lxml
      python-pkgs.matplotlib
      python-pkgs.pandas
      python-pkgs.scipy
    ]))
  ];
}
