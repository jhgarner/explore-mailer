let
  pkgs = import <nixpkgs> {};
in
pkgs.mkShell {
  buildInputs = [
    (pkgs.python3.withPackages (ps: with ps; [google_api_python_client google-auth-httplib2 google-auth-oauthlib]))
  ];
}
