{
  mkShell,
  uv,
  python3,
}:
mkShell {
  env = {
    UV_PYTHON = "${python3}/bin/python3";
  };
  nativeBuildInputs = [
    uv
    python3
  ];
}
