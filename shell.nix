{
  mkShell,
  uv,
  python3,
}:
mkShell {
  env = {
    UV_PYTHON = "${python3}/bin/python3";
  };
  shellHook = ''
    source .venv/bin/activate
  '';
  nativeBuildInputs = [
    uv
    python3
  ];
}
